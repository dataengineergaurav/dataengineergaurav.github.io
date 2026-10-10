#!/usr/bin/env python3
"""LLM Wiki (second brain) ingest, synthesis and backup pipeline.

Reads new Hermes agent sessions, personal notes and Hermes memories, summarizes them
with an LLM into an Obsidian-style markdown vault, and backs the vault up to its own
private remote. Incremental and idempotent. The vault is private and is not published.
"""

import argparse
import fcntl
import hashlib
import json
import logging
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME", "/root/.hermes"))
STATE_DB = HERMES_HOME / "state.db"
MEMORY_DIR = HERMES_HOME / "memories"
ENV_FILE = HERMES_HOME / ".env"

WIKI_ROOT = Path(os.environ.get("WIKI_ROOT", "/root/second-brain"))
SUBJECTS_DIR = WIKI_ROOT / "subjects"
DAILY_DIR = WIKI_ROOT / "daily"
INBOX_DIR = WIKI_ROOT / "inbox"
INDEX_PATH = WIKI_ROOT / "index.md"
STATE_PATH = WIKI_ROOT / ".wiki" / "state.json"
LOG_PATH = WIKI_ROOT / ".wiki" / "ingest.log"
LOCK_PATH = WIKI_ROOT / ".wiki" / "ingest.lock"

BLOG_REPO = Path(os.environ.get("WIKI_BLOG_REPO", "/root/dataengineergaurav.github.io"))

WIKI_BACKEND = os.environ.get("WIKI_BACKEND", "command-code")
WIKI_MODEL = os.environ.get("WIKI_MODEL", "gpt-5.6-sol")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
CHAT_URL = OPENAI_BASE_URL + "/chat/completions"
CMD_BIN = os.environ.get("WIKI_CMD_BIN", "cmd")
CMD_MODEL = os.environ.get("WIKI_CMD_MODEL", "")
CMD_TIMEOUT = int(os.environ.get("WIKI_CMD_TIMEOUT", "600"))
MAX_PAYLOAD_CHARS = int(os.environ.get("WIKI_MAX_PAYLOAD_CHARS", "120000"))

DEFAULT_LIMIT = int(os.environ.get("WIKI_INGEST_LIMIT", "25"))
MAX_MESSAGES_PER_SESSION = 60
MAX_CHARS_PER_MESSAGE = 1500
MAX_CHARS_PER_SESSION = 12000

LOGGER = logging.getLogger("wiki_ingest")

SYSTEM_PROMPT = (
    "You maintain a personal 'second brain' wiki. You receive a batch of recent agent "
    "sessions and personal notes. Extract durable, useful knowledge into (a) evergreen "
    "subject pages and (b) a dated daily log. Be concrete and specific; preserve names, "
    "decisions, numbers, and open questions. Never invent facts. Prefer merging into "
    "existing subjects over creating near-duplicates. Answer with JSON only."
)

JSON_SCHEMA_HINT = {
    "daily_logs": [
        {
            "date": "YYYY-MM-DD",
            "summary": "one-paragraph summary of the day's activity",
            "highlights": ["notable outcome or finding"],
            "decisions": ["decision made and why"],
            "open_threads": ["unfinished task or question"],
            "subjects": ["existing-or-new subject slug touched today"],
        }
    ],
    "subjects": [
        {
            "slug": "kebab-case-topic",
            "title": "Human title",
            "tags": ["tag"],
            "summary": "one sentence describing the topic page",
            "body": "markdown body, use [[slug]] links to related subjects",
            "related": ["other-slug"],
            "visibility": "private",
        }
    ],
}

_SECRET_FALLBACK = re.compile(
    r"(?i)\b(sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"AIza[0-9A-Za-z_-]{30,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|"
    r"[A-Za-z0-9_-]{0,6}:[A-Za-z0-9_-]{25,})\b"
)


def _configure_logging():
    if LOGGER.handlers:
        return
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(LOG_PATH, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.INFO)


def _redactor():
    try:
        sp = str(HERMES_HOME / "venv" / "lib" / "python3.12" / "site-packages")
        if sp not in sys.path:
            sys.path.insert(0, sp)
        from agent.redact import redact_sensitive_text

        return lambda text: redact_sensitive_text(text, force=True)
    except Exception:
        return lambda text: _SECRET_FALLBACK.sub("[REDACTED]", text)


REDACT = _redactor()


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _today():
    return datetime.now(timezone.utc).date().isoformat()


def _slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")
    return (slug or "untitled")[:64]


def _load_state():
    if not STATE_PATH.exists():
        return {"version": 1, "processed_sessions": [], "processed_notes": {},
                "last_run": None}
    data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    data.setdefault("processed_sessions", [])
    data.setdefault("processed_notes", {})
    return data


def _save_state(state):
    _atomic_write(STATE_PATH, json.dumps(state, indent=2))


def _atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def _parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")
    meta = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("["):
            try:
                meta[key] = json.loads(val)
                continue
            except Exception:
                pass
        if val in ("null", ""):
            meta[key] = None
        elif val == "true":
            meta[key] = True
        elif val == "false":
            meta[key] = False
        else:
            meta[key] = val.strip('"')
    return meta, body


def _render_front_matter(meta):
    order = ["title", "layout", "tags", "visibility", "created", "updated", "sources", "summary"]
    keys = [k for k in order if k in meta] + [k for k in meta if k not in order]
    lines = ["---"]
    for key in keys:
        val = meta[key]
        if isinstance(val, list):
            lines.append(f"{key}: {json.dumps(val, ensure_ascii=False)}")
        elif isinstance(val, bool):
            lines.append(f"{key}: {str(val).lower()}")
        elif val is None:
            lines.append(f"{key}: null")
        else:
            lines.append(f"{key}: {json.dumps(str(val), ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _write_page(path, meta, body):
    _atomic_write(path, _render_front_matter(meta) + "\n" + body.rstrip() + "\n")


def _read_page(path):
    if not path.exists():
        return {}, ""
    return _parse_front_matter(path.read_text(encoding="utf-8"))


def _openai_key():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("OPENAI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def _candidate_sessions(processed):
    con = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "SELECT id, source, title, started_at, ended_at, message_count "
            "FROM sessions WHERE message_count >= 2 ORDER BY started_at"
        ).fetchall()
    finally:
        con.close()
    processed = set(processed)
    return [r for r in rows if r[0] not in processed]


def _session_transcript(con, session_id):
    rows = con.execute(
        "SELECT role, content FROM messages "
        "WHERE session_id = ? AND role IN ('user','assistant') AND content IS NOT NULL "
        "ORDER BY id LIMIT ?",
        (session_id, MAX_MESSAGES_PER_SESSION),
    ).fetchall()
    chunks, total = [], 0
    for role, content in rows:
        text = str(content).strip()
        if not text:
            continue
        text = text[:MAX_CHARS_PER_MESSAGE]
        block = f"{role.upper()}: {text}"
        if total + len(block) > MAX_CHARS_PER_SESSION:
            break
        chunks.append(block)
        total += len(block)
    return "\n\n".join(chunks)


def _collect_notes(state):
    notes = []
    if INBOX_DIR.exists():
        for path in sorted(INBOX_DIR.glob("*.md")):
            text = path.read_text(encoding="utf-8", errors="replace")
            digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
            if state["processed_notes"].get(path.name) == digest:
                continue
            notes.append({"name": path.name, "text": text[:MAX_CHARS_PER_SESSION], "hash": digest})
    # Hermes memories (MEMORY.md / USER.md) are injected into every session's system
    # prompt, so they never appear in the stored transcripts — ingest them directly.
    if MEMORY_DIR.exists():
        for name in ("MEMORY.md", "USER.md"):
            path = MEMORY_DIR / name
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            if not text:
                continue
            digest = hashlib.sha1(text.encode("utf-8")).hexdigest()
            key = f"memory:{name}"
            if state["processed_notes"].get(key) == digest:
                continue
            notes.append({"name": key, "text": text[:MAX_CHARS_PER_SESSION], "hash": digest})
    return notes


def _existing_subject_catalog():
    catalog = []
    if not SUBJECTS_DIR.exists():
        return catalog
    for path in sorted(SUBJECTS_DIR.glob("*.md")):
        meta, _ = _read_page(path)
        catalog.append({"slug": path.stem, "title": meta.get("title", path.stem)})
    return catalog


def _build_payload(sessions, transcripts, notes, catalog):
    payload = {
        "today": _today(),
        "existing_subjects": catalog,
        "sessions": [
            {
                "id": s[0],
                "source": s[1],
                "title": s[2],
                "started_at": s[3],
                "transcript": transcripts.get(s[0], ""),
            }
            for s in sessions
        ],
        "notes": [{"name": n["name"], "text": n["text"]} for n in notes],
        "output_schema": JSON_SCHEMA_HINT,
    }
    while len(json.dumps(payload, ensure_ascii=False)) > MAX_PAYLOAD_CHARS and len(payload["sessions"]) > 1:
        payload["sessions"].pop()
    while len(json.dumps(payload, ensure_ascii=False)) > MAX_PAYLOAD_CHARS and payload["notes"]:
        payload["notes"].pop()
    return payload


def _call_llm_openai(payload):
    key = _openai_key()
    if not key:
        raise RuntimeError("OPENAI_API_KEY not found (set in environment or ~/.hermes/.env)")
    body = {
        "model": WIKI_MODEL,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    }
    for attempt in (0, 1):
        req_body = dict(body)
        if attempt == 0:
            req_body["response_format"] = {"type": "json_object"}
        data = json.dumps(req_body).encode("utf-8")
        req = urllib.request.Request(
            CHAT_URL, data=data, method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                parsed = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as err:
            if attempt == 0 and err.code in (400, 404, 422):
                LOGGER.info("model rejected response_format; retrying without it")
                continue
            raise
    content = parsed["choices"][0]["message"]["content"]
    content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.MULTILINE).strip()
    return json.loads(content)


def _extract_final_text(stdout):
    final = None
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("type") == "result" and obj.get("finalText"):
            final = obj["finalText"]
    return final


def _call_llm_command_code(payload):
    prompt = (
        SYSTEM_PROMPT
        + "\n\nReturn ONLY the JSON object described by output_schema. Do not use tools. "
        + "Do not add prose or code fences.\n\nINPUT:\n"
        + json.dumps(payload, ensure_ascii=False)
    )
    argv = [
        CMD_BIN, "-p", prompt, "--output-format", "json", "--no-session",
        "--skip-onboarding", "--no-skills", "--no-auto-update", "--max-turns", "4",
    ]
    if CMD_MODEL:
        argv += ["-m", CMD_MODEL]
    with tempfile.TemporaryDirectory(prefix="wiki-ingest-") as workdir:
        proc = subprocess.run(argv, cwd=workdir, capture_output=True, text=True, timeout=CMD_TIMEOUT)
    final = _extract_final_text(proc.stdout)
    if final is None:
        detail = (proc.stderr or proc.stdout or "").strip()[-300:]
        raise RuntimeError(f"command-code backend produced no result (exit {proc.returncode}): {detail}")
    final = re.sub(r"^```(?:json)?|```$", "", final.strip(), flags=re.MULTILINE).strip()
    return json.loads(final)


def _call_llm(payload):
    if WIKI_BACKEND == "openai":
        return _call_llm_openai(payload)
    return _call_llm_command_code(payload)


def _as_list(value):
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def _strip_leading_h1(text):
    lines = text.splitlines()
    start = 0
    while start < len(lines) and not lines[start].strip():
        start += 1
    if start < len(lines) and lines[start].startswith("# "):
        lines = lines[:start] + lines[start + 1:]
    while lines and not lines[0].strip():
        lines = lines[1:]
    return "\n".join(lines).strip()


def _demote_headings(text):
    out = []
    for line in text.splitlines():
        out.append("#" + line if re.match(r"^#{1,5}\s", line) else line)
    return "\n".join(out)


def _merge_subject(entry, source_ids):
    slug = _slugify(entry.get("slug") or entry.get("title"))
    path = SUBJECTS_DIR / f"{slug}.md"
    meta, body = _read_page(path)
    today = _today()
    tags = sorted(set(_as_list(meta.get("tags")) + _as_list(entry.get("tags"))))
    sources = sorted(set(_as_list(meta.get("sources")) + list(source_ids)))
    section = _strip_leading_h1(REDACT(str(entry.get("body", "")).strip()))
    title = str(entry.get("title") or meta.get("title") or slug.replace("-", " ").title())
    if not meta:
        body = f"# {title}\n\n{section}\n"
    elif section:
        body = body.rstrip() + f"\n\n## {today} — update\n\n{_demote_headings(section)}\n"
    meta.update({
        "title": title,
        "tags": tags,
        "visibility": str(meta.get("visibility") or "private"),
        "created": meta.get("created") or today,
        "updated": today,
        "sources": sources,
        "summary": REDACT(str(entry.get("summary") or meta.get("summary") or "")),
    })
    _write_page(path, meta, body)
    return slug


def _merge_daily(entry, source_ids):
    date = str(entry.get("date") or _today())
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        date = _today()
    path = DAILY_DIR / f"{date}.md"
    meta, body = _read_page(path)
    parts = [REDACT(str(entry.get("summary", "")).strip())]
    for label, key in (("Highlights", "highlights"), ("Decisions", "decisions"),
                       ("Open threads", "open_threads")):
        items = _as_list(entry.get(key))
        if items:
            parts.append(f"**{label}**\n" + "\n".join(f"- {REDACT(i)}" for i in items))
    section = _strip_leading_h1("\n\n".join(p for p in parts if p))
    if not meta:
        body = f"# Daily log — {date}\n\n{section}\n"
    elif section:
        body = body.rstrip() + f"\n\n## Ingest {_now_iso()[:19]}Z\n\n{_demote_headings(section)}\n"
    sources = sorted(set(_as_list(meta.get("sources")) + list(source_ids)))
    meta.update({
        "title": f"Daily log — {date}",
        "tags": sorted(set(_as_list(meta.get("tags")) + ["daily"])),
        "visibility": meta.get("visibility") or "private",
        "created": meta.get("created") or date,
        "updated": _today(),
        "sources": sources,
    })
    _write_page(path, meta, body)


def _rebuild_index():
    entries = []
    if SUBJECTS_DIR.exists():
        for path in sorted(SUBJECTS_DIR.glob("*.md")):
            meta, _ = _read_page(path)
            entries.append({
                "slug": path.stem,
                "title": meta.get("title", path.stem),
                "summary": meta.get("summary", ""),
                "tags": _as_list(meta.get("tags")),
                "updated": meta.get("updated", ""),
                "visibility": meta.get("visibility", "private"),
            })
    entries.sort(key=lambda e: (e["updated"] or ""), reverse=True)
    lines = ["---", 'title: "Second Brain — Index"', f"updated: {json.dumps(_today())}", "---", "",
             "# Second Brain", "",
             "Generated catalog of subject pages. Rebuilt by `wiki_ingest.py`.", ""]
    if not entries:
        lines.append("_No subjects yet._")
    for e in entries:
        tags = f" · `{'` `'.join(e['tags'])}`" if e["tags"] else ""
        vis = "" if e["visibility"] == "public" else " *(private)*"
        lines.append(f"- **[[{e['slug']}|{e['title']}]]**{vis} — {e['summary']}{tags}")
    _atomic_write(INDEX_PATH, "\n".join(lines).rstrip() + "\n")
    return len(entries)


def _run_git(*args, cwd):
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)


def backup(push=False, dry_run=False):
    """Commit (and optionally push) the vault — the source of truth — to its private remote.

    The vault is a separate git repository from the blog. It is private: pages never
    leave this machine unless backed up here.
    """
    if not (WIKI_ROOT / ".git").exists():
        return "backup: vault is not a git repository"
    dirty = bool(_run_git("status", "--porcelain", cwd=WIKI_ROOT).stdout.strip())
    if dry_run:
        return f"backup (dry-run): {'would commit' if dirty else 'no changes'}"
    committed = False
    if dirty:
        _run_git("add", "-A", cwd=WIKI_ROOT)
        _run_git("commit", "-m", "wiki: back up ingested subjects and daily logs", cwd=WIKI_ROOT)
        committed = True
    if not push:
        return f"backup: {'committed' if committed else 'no changes'}"
    if not _run_git("remote", cwd=WIKI_ROOT).stdout.split():
        return f"backup: {'committed' if committed else 'no changes'}; vault has no remote to push to"
    result = _run_git("push", cwd=WIKI_ROOT)
    if result.returncode != 0:
        raise RuntimeError(f"vault push failed: {result.stderr.strip()}")
    return f"backup: {'committed' if committed else 'no changes'}, pushed"


def ingest(limit=None, dry_run=False):
    if limit is None:
        limit = DEFAULT_LIMIT
    state = _load_state()
    candidates = _candidate_sessions(state["processed_sessions"])
    if limit and limit > 0:
        candidates = sorted(candidates, key=lambda r: r[3] or "", reverse=True)[:limit]
    notes = _collect_notes(state)
    if not candidates and not notes:
        state["last_run"] = _now_iso()
        _save_state(state)
        return "ingest: no new sessions or notes"
    con = sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)
    try:
        transcripts = {s[0]: _session_transcript(con, s[0]) for s in candidates}
    finally:
        con.close()
    payload = _build_payload(candidates, transcripts, notes, _existing_subject_catalog())
    LOGGER.info("ingest batch: %d session(s), %d note(s)", len(candidates), len(notes))
    if dry_run:
        return f"ingest (dry-run): would process {len(candidates)} session(s), {len(notes)} note(s)"
    result = _call_llm(payload)
    source_ids = [s[0] for s in candidates]
    subjects = result.get("subjects") or []
    daily_logs = result.get("daily_logs") or []
    written = []
    for entry in subjects:
        if isinstance(entry, dict):
            written.append(_merge_subject(entry, source_ids))
    for entry in daily_logs:
        if isinstance(entry, dict):
            _merge_daily(entry, source_ids)
    _rebuild_index()
    state["processed_sessions"] = sorted(set(state["processed_sessions"]) | set(source_ids))
    for note in notes:
        state["processed_notes"][note["name"]] = note["hash"]
    state["last_run"] = _now_iso()
    _save_state(state)
    return (f"ingest: {len(source_ids)} session(s), {len(notes)} note(s); "
            f"{len(written)} subject(s), {len(daily_logs)} daily log(s)")


def status():
    state = _load_state()
    candidates = _candidate_sessions(state["processed_sessions"])
    notes = _collect_notes(state)
    subjects = len(list(SUBJECTS_DIR.glob("*.md"))) if SUBJECTS_DIR.exists() else 0
    daily = len(list(DAILY_DIR.glob("*.md"))) if DAILY_DIR.exists() else 0
    return (
        f"wiki: {WIKI_ROOT}\n"
        f"last_run: {state.get('last_run')}\n"
        f"processed_sessions: {len(state['processed_sessions'])}\n"
        f"pending_sessions: {len(candidates)}\n"
        f"pending_notes: {len(notes)}\n"
        f"subjects: {subjects}\ndaily_logs: {daily}\n"
        f"backend: {WIKI_BACKEND}\n"
        f"model: {CMD_MODEL or WIKI_MODEL}"
    )


def doctor():
    problems = []
    if not WIKI_ROOT.exists():
        problems.append(f"vault missing: {WIKI_ROOT}")
    for d in (SUBJECTS_DIR, DAILY_DIR, INBOX_DIR, STATE_PATH.parent):
        if not d.exists():
            problems.append(f"missing directory: {d}")
    if not STATE_PATH.exists():
        problems.append(f"missing state: {STATE_PATH}")
    else:
        try:
            _load_state()
        except Exception as error:
            problems.append(f"state unreadable: {error}")
    if not STATE_DB.exists():
        problems.append(f"session store missing: {STATE_DB}")
    else:
        try:
            sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True).execute(
                "SELECT count(*) FROM sessions").fetchone()
        except Exception as error:
            problems.append(f"session store unreadable: {error}")
    if WIKI_BACKEND == "openai":
        if not _openai_key():
            problems.append("OPENAI_API_KEY not found (env or ~/.hermes/.env)")
    elif not shutil.which(CMD_BIN):
        problems.append(f"synthesis backend '{CMD_BIN}' not found on PATH")
    if not BLOG_REPO.exists():
        problems.append(f"blog repo missing: {BLOG_REPO}")
    if problems:
        raise RuntimeError("doctor found issues:\n- " + "\n- ".join(problems))
    return "doctor: ok"


def main(argv=None):
    parser = argparse.ArgumentParser(description="LLM Wiki (second brain) ingest and backup")
    commands = parser.add_subparsers(dest="command", required=True)
    ingest_parser = commands.add_parser("ingest")
    ingest_parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ingest_parser.add_argument("--dry-run", action="store_true")
    backup_parser = commands.add_parser("backup")
    backup_parser.add_argument("--push", action="store_true")
    backup_parser.add_argument("--dry-run", action="store_true")
    commands.add_parser("status")
    commands.add_parser("doctor")
    args = parser.parse_args(argv)
    _configure_logging()
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    lock_file = open(LOCK_PATH, "w")
    try:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("wiki_ingest: another run is in progress")
        return 0
    try:
        if args.command == "ingest":
            result = ingest(args.limit, args.dry_run)
        elif args.command == "backup":
            result = backup(args.push, args.dry_run)
        elif args.command == "status":
            result = status()
        else:
            result = doctor()
        LOGGER.info("%s", result.replace("\n", " | "))
        print(result)
        return 0
    except Exception as error:
        LOGGER.error("%s failed: %s", args.command, error)
        print(f"error: {error}")
        return 1
    finally:
        fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()


if __name__ == "__main__":
    raise SystemExit(main())
