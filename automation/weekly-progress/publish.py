#!/usr/bin/env python3
"""Deterministic publisher for the weekly progress blog.

Takes the single post file the agent produced (``_posts/<date>-weekly-progress.md``),
and on an isolated branch commits exactly that file, pushes it, and opens a pull
request. It never pushes to the base branch. All git/PR actions live here so the
LLM stages cannot touch git.

Usage:
    publish.py --date YYYY-MM-DD [--body-file PATH] [--base master] [--remote origin]
               [--dry-run | --no-push]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import date as date_cls
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
HERMES_ENV = Path("/root/.hermes/.env")
GIT = "/usr/bin/git"
USER_AGENT = "GauravWeeklyProgress/1.0"

# The site pull request may also carry the CV refreshed by the CV stage.
CV_PDF = "Gaurav_Gurjar_CV_AI-Data-Engineer.pdf"
CV_VERSION = "Gaurav_Gurjar_CV_AI-Data-Engineer.version.json"


def git(*args, check=True, raw=False, cwd=REPO_ROOT):
    result = subprocess.run(
        [GIT, *args], cwd=cwd, text=not raw, capture_output=True, check=False, timeout=120,
    )
    if check and result.returncode != 0:
        detail = (result.stderr if not raw else (result.stderr or b"").decode("utf-8", "replace"))
        raise SystemExit(f"git {' '.join(args)} failed: {str(detail).strip()}")
    return result.stdout if raw else result.stdout.strip()


def _load_env_value(key):
    if os.environ.get(key):
        return os.environ[key]
    if HERMES_ENV.exists():
        for line in HERMES_ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def sha256_bytes(payload):
    return hashlib.sha256(payload).hexdigest()


def parse_remote(url):
    cleaned = url.strip()
    if cleaned.startswith("git@"):
        path = cleaned.split(":", 1)[1]
    else:
        path = cleaned.split("github.com/", 1)[-1]
    path = path[:-4] if path.endswith(".git") else path
    owner, _, repo = path.partition("/")
    if not owner or not repo:
        raise SystemExit(f"cannot parse GitHub owner/repo from remote: {url}")
    return owner, repo


def post_path_for(date):
    return REPO_ROOT / "_posts" / f"{date}-weekly-progress.md"


def _changed_paths(repo_root=REPO_ROOT):
    """Every path the worktree reports as changed, tracked or untracked.

    Reads raw output on purpose: git() strips stdout, which eats the first
    porcelain line's leading status column and truncates its path by one
    character.
    """
    raw = git("status", "--porcelain", "--untracked-files=all", cwd=repo_root, raw=True)
    text = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
    return [line[3:].strip() for line in text.splitlines() if line.strip()]


def only_change_guard(relatives, repo_root=REPO_ROOT, required=None):
    """The worktree may hold only `relatives`, and every path in `required`."""
    allowed = sorted(set(relatives))
    needed = sorted(set(required) if required is not None else set(relatives))
    seen = sorted(_changed_paths(repo_root))
    unexpected = [path for path in seen if path not in allowed]
    missing = [path for path in needed if path not in seen]
    if unexpected or missing:
        raise SystemExit(
            "publish guard failed: "
            f"unexpected={unexpected or 'none'}, missing={missing or 'none'}, "
            f"worktree={seen or ['(clean)']}"
        )


def _api(token, method, url, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
        **({"Content-Type": "application/json"} if data else {}),
    })
    try:
        with urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read().decode("utf-8") or "{}")
    except HTTPError as error:
        body = error.read().decode("utf-8", "replace")
        return error.code, {"raw": body}


def existing_pr(token, owner, repo, branch):
    query = urlencode({"head": f"{owner}:{branch}", "state": "all"})
    status, payload = _api(token, "GET", f"https://api.github.com/repos/{owner}/{repo}/pulls?{query}")
    if status == 200 and payload:
        return payload[0]
    return None


def publish(date, base="master", remote="origin", body_file=None, push=True):
    relative = f"_posts/{date}-weekly-progress.md"
    path = post_path_for(date)
    if not path.is_file():
        raise SystemExit(f"post not found: {path}")

    git("fetch", remote, base)
    base_head = git("rev-parse", f"{remote}/{base}")
    current = git("branch", "--show-current")
    if current != base:
        raise SystemExit(f"must publish from '{base}' (currently on '{current}')")
    if git("rev-parse", "HEAD") != base_head:
        raise SystemExit(f"HEAD is not synchronized with {remote}/{base}; sync before publishing")

    changed_cv = set(_changed_paths()) & {CV_PDF, CV_VERSION}
    if changed_cv and changed_cv != {CV_PDF, CV_VERSION}:
        raise SystemExit(
            "publish guard failed: the CV pdf and its version marker must change together"
        )
    only_change_guard([relative, CV_PDF, CV_VERSION], required=[relative])

    branch = f"weekly-progress/{date}"

    if not push:
        print(f"(no-push) would branch {branch}, commit {relative}, push {remote}, open PR (base {base})")
        return 0

    remote_url = git("remote", "get-url", remote)
    owner, repo = parse_remote(remote_url)
    token = _load_env_value("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required to open a pull request")
    found = existing_pr(token, owner, repo, branch)
    if found:
        print(f"PR already exists: {found['html_url']}")
        return 0

    reviewed_hash = sha256_bytes(path.read_bytes())
    git("checkout", "-B", branch, base_head)
    try:
        git("add", "--", relative)
        if git("diff", "--cached", "--name-only").splitlines() != [relative]:
            raise SystemExit("cached paths do not match the reviewed post")
        staged = git("show", f":{relative}", raw=True)
        if sha256_bytes(staged) != reviewed_hash:
            raise SystemExit("staged post hash does not match the reviewed file")
        git("commit", "-m", f"progress: weekly progress {date}")
        if git("rev-parse", "HEAD^") != base_head:
            raise SystemExit("commit is not a single step from the base head")
        git("push", remote, f"HEAD:refs/heads/{branch}")
    except SystemExit:
        git("checkout", base, check=False)
        git("branch", "-D", branch, check=False)
        raise

    body = Path(body_file).read_text(encoding="utf-8") if body_file and Path(body_file).is_file() else (
        f"Weekly progress for {date}."
    )
    status, payload = _api(token, "POST", f"https://api.github.com/repos/{owner}/{repo}/pulls", {
        "title": f"Weekly progress — {date}",
        "head": branch,
        "base": base,
        "body": body,
    })
    if status not in (200, 201):
        raise SystemExit(f"failed to open PR ({status}): {payload.get('raw', payload)}")
    git("checkout", base, check=False)
    print(f"opened PR: {payload['html_url']}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Publish the weekly progress post as a pull request.")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--base", default="master")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--body-file")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args(argv)
    try:
        date_cls.fromisoformat(args.date)
    except ValueError:
        raise SystemExit(f"--date must be YYYY-MM-DD, got {args.date!r}")
    return publish(
        args.date, base=args.base, remote=args.remote,
        body_file=args.body_file, push=not (args.dry_run or args.no_push),
    )


if __name__ == "__main__":
    sys.exit(main())
