#!/usr/bin/env python3
"""Deterministic GitHub activity collector for the weekly progress blog.

Reads GitHub REST API activity for a reporting window and emits a normalized
JSON "activity pack" consumed by the progress-analyzer / technical-blog-writer
skills. No LLM here: this is the reproducible substrate the agent reasons over.

Usage:
    collect.py collect [--since ISO] [--until ISO] [--window-days N]
                       [--out PATH] [--dry-run] [--from-raw PATH]
    collect.py doctor
"""
import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = REPO_ROOT / ".progress-generator"
ACTIVITY_DIR = RUNTIME_DIR / "activity"
PROJECTS_FILE = REPO_ROOT / ".commandcode" / "skills" / "github-project-context" / "projects.yaml"
HERMES_ENV = Path("/root/.hermes/.env")
API_ROOT = "https://api.github.com"
USER_AGENT = "GauravWeeklyProgress/1.0"
GITHUB_USER = os.environ.get("GITHUB_USER", "dataengineergaurav")
WINDOW_DAYS = int(os.environ.get("PROGRESS_WINDOW_DAYS", "7"))
MAX_PAYLOAD_CHARS = int(os.environ.get("PROGRESS_MAX_PAYLOAD_CHARS", "200000"))
MAX_COMMIT_DETAILS = int(os.environ.get("PROGRESS_MAX_COMMIT_DETAILS", "40"))
MAX_REPOS = int(os.environ.get("PROGRESS_MAX_REPOS", "40"))

LOCKFILES = {
    "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "gemfile.lock", "poetry.lock", "pipfile.lock", "uv.lock", "cargo.lock",
    "go.sum", "composer.lock", "packages.lock.json",
}
MERGE_RE = re.compile(r"^merge (branch|pull request|remote-tracking|tag)\b", re.I)
CHURN_RE = re.compile(
    r"(dependabot|renovate|^bump\b|\bbump\b|chore\(deps\)|^format\b|prettier|"
    r"\blint\b|isort|black\b|whitespace|^style:|^chore: version)",
    re.I,
)


def _load_env_value(key):
    if os.environ.get(key):
        return os.environ[key]
    if HERMES_ENV.exists():
        for line in HERMES_ENV.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{key}="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def github_token():
    token = _load_env_value("GITHUB_TOKEN")
    if not token:
        raise SystemExit(
            "GITHUB_TOKEN is not set (environment or /root/.hermes/.env). "
            "A token with 'repo' + 'read:user' scopes is required."
        )
    return token


def _request(url, token, accept="application/vnd.github+json"):
    request = Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": accept,
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8")), dict(response.headers)
    except HTTPError as error:
        if error.code in (403, 429) and error.headers.get("X-RateLimit-Remaining") == "0":
            raise SystemExit(f"GitHub rate limit exhausted for {url}") from error
        if error.code == 401:
            raise SystemExit("GitHub token rejected (401): check GITHUB_TOKEN scopes") from error
        raise SystemExit(f"GitHub request failed ({error.code}): {url}") from error
    except URLError as error:
        raise SystemExit(f"GitHub request failed: {url}: {error.reason}") from error


# --------------------------------------------------------------------------- #
# YAML subset parser (no PyYAML dependency) for the project catalog
# --------------------------------------------------------------------------- #

def _scalar(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    if value in ("true", "false"):
        return value == "true"
    return value


def _inline_list(value):
    inner = value.strip()[1:-1].strip()
    if not inner:
        return []
    return [_scalar(item) for item in inner.split(",") if item.strip()]


def _inline_map(value):
    inner = value.strip()[1:-1].strip()
    result = {}
    if not inner:
        return result
    depth, current, parts = 0, "", []
    for char in inner:
        if char in "[{":
            depth += 1
        elif char in "]}":
            depth -= 1
        if char == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += char
    parts.append(current)
    for part in parts:
        if ":" not in part:
            continue
        key, _, val = part.partition(":")
        result[key.strip()] = _scalar(val)
    return result


def load_projects(path=PROJECTS_FILE):
    """Parse the restricted projects.yaml shape: slug -> {key: value|list|map}."""
    if not path.exists():
        return {}
    projects, current = {}, None
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, sep, value = line.strip().partition(":")
        if not sep:
            continue
        if indent == 0:
            current = key.strip()
            projects[current] = {} if not value.strip() else {"value": _scalar(value)}
        elif current is not None:
            value = value.strip()
            if value.startswith("[") and value.endswith("]"):
                projects[current][key.strip()] = _inline_list(value)
            elif value.startswith("{") and value.endswith("}"):
                projects[current][key.strip()] = _inline_map(value)
            else:
                projects[current][key.strip()] = _scalar(value)
    return projects


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #

def fetch_repos(token):
    repos, page = [], 1
    while page <= 3:
        url = f"{API_ROOT}/user/repos?" + urlencode({
            "affiliation": "owner,collaborator,organization_member",
            "per_page": 100, "sort": "pushed", "page": page,
        })
        batch, _ = _request(url, token)
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def fetch_commits(token, full_name, user, since, until):
    url = f"{API_ROOT}/repos/{full_name}/commits?" + urlencode({
        "author": user, "since": since, "until": until, "per_page": 100,
    })
    return _request(url, token)[0]


def fetch_commit_detail(token, full_name, sha):
    return _request(f"{API_ROOT}/repos/{full_name}/commits/{sha}", token)[0]


def fetch_search_issues(token, user, since):
    results = []
    for kind in ("pr", "issue"):
        url = f"{API_ROOT}/search/issues?" + urlencode({
            "q": f"author:{user} type:{kind} created:>={since[:10]}",
            "sort": "updated", "order": "desc", "per_page": 100,
        })
        results.extend(_request(url, token)[0].get("items", []))
    return results


def fetch_releases(token, full_name):
    return _request(f"{API_ROOT}/repos/{full_name}/releases?per_page=20", token)[0]


def fetch_events(token, user):
    events, page = [], 1
    while page <= 3:
        url = f"{API_ROOT}/users/{user}/events?" + urlencode({"per_page": 100, "page": page})
        batch, _ = _request(url, token)
        events.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return events


def raw_snapshot(token, user, since, until):
    repos = fetch_repos(token)
    active = [
        repo for repo in repos
        if repo.get("pushed_at") and repo["pushed_at"] >= since
        or (repo.get("created_at") and repo["created_at"] >= since)
    ][:MAX_REPOS]
    commits, details = {}, {}
    for repo in active:
        name = repo["full_name"]
        try:
            listing = fetch_commits(token, name, user, since, until)
        except SystemExit:
            listing = []
        commits[name] = listing
    # fetch details for the newest commits across repos, up to the cap
    pending = []
    for name, items in commits.items():
        for item in items:
            authored = item.get("commit", {}).get("author", {}).get("date", "")
            pending.append((authored, name, item["sha"]))
    pending.sort(key=lambda row: row[0], reverse=True)
    for _, name, sha in pending[:MAX_COMMIT_DETAILS]:
        try:
            details[sha] = fetch_commit_detail(token, name, sha)
        except SystemExit:
            continue
    releases = {}
    for repo in active:
        try:
            releases[repo["full_name"]] = fetch_releases(token, repo["full_name"])
        except SystemExit:
            continue
    return {
        "user": user, "since": since, "until": until,
        "repos": repos, "commits": commits, "commit_details": details,
        "search_issues": fetch_search_issues(token, user, since),
        "releases": releases, "events": fetch_events(token, user),
    }


# --------------------------------------------------------------------------- #
# Normalization (pure)
# --------------------------------------------------------------------------- #

def _files_for(sha, details):
    detail = details.get(sha) or {}
    return [item.get("filename", "") for item in detail.get("files", [])]


def _flags(files, message):
    basenames = [Path(name).name for name in files]
    lower = [name.lower() for name in basenames]
    readme = any(name.startswith("readme") for name in lower)
    docs = any(
        name.startswith("docs/") or (name.lower().endswith(".md") and not name.lower().startswith("readme"))
        for name in files
    )
    tests = any(name.startswith(("test", "tests/")) or "/tests/" in name or "test_" in name for name in files)
    churn = bool(files) and all(name in LOCKFILES for name in lower)
    if not churn and CHURN_RE.search(message) and not readme and not docs and not tests:
        churn = True
    return {"readme": readme, "docs": docs, "test": tests, "churn": churn}


def build_pack(raw, projects, since, until):
    repo_index = {repo["full_name"]: repo for repo in raw.get("repos", [])}
    active_repos, commits = [], []
    for name, listing in raw.get("commits", {}).items():
        repo = repo_index.get(name, {})
        repo_commits = 0
        for item in listing:
            message = (item.get("commit", {}).get("message") or "").splitlines()[0].strip()
            if MERGE_RE.match(message):
                continue
            sha = item.get("sha", "")
            files = _files_for(sha, raw.get("commit_details", {}))
            commits.append({
                "repo": name, "sha": sha,
                "date": item.get("commit", {}).get("author", {}).get("date", ""),
                "message": message, "files": files, "flags": _flags(files, message),
                "url": f"https://github.com/{name}/commit/{sha}",
            })
            repo_commits += 1
        if repo_commits:
            active_repos.append({
                "full_name": name, "private": bool(repo.get("private")),
                "created_at": repo.get("created_at"), "pushed_at": repo.get("pushed_at"),
                "archived": bool(repo.get("archived")),
                "new": bool(repo.get("created_at") and repo["created_at"] >= since),
                "url": repo.get("html_url", f"https://github.com/{name}"),
            })

    pull_requests, issues = [], []
    for item in raw.get("search_issues", []):
        entry = {
            "repo": item.get("repository_url", "").rsplit("/repos/", 1)[-1],
            "number": item.get("number"), "title": item.get("title"),
            "state": item.get("state"), "url": item.get("html_url", ""),
            "created_at": item.get("created_at"), "updated_at": item.get("updated_at"),
        }
        if "pull_request" in item:
            entry["merged"] = bool(item["pull_request"].get("merged_at"))
            entry["merged_at"] = item["pull_request"].get("merged_at")
            pull_requests.append(entry)
        else:
            issues.append(entry)

    releases = []
    for name, entries in raw.get("releases", {}).items():
        for release in entries:
            published = release.get("published_at") or release.get("created_at") or ""
            if published and published >= since:
                releases.append({
                    "repo": name, "tag": release.get("tag_name"),
                    "name": release.get("name"), "created_at": published,
                    "url": release.get("html_url", ""),
                })

    new_projects, deleted_projects, archived_projects = [], [], []
    for event in raw.get("events", []):
        event_type = event.get("type")
        repo_name = (event.get("repo") or {}).get("name")
        if not repo_name:
            continue
        if event_type == "CreateEvent" and (event.get("payload") or {}).get("ref_type") == "repository":
            new_projects.append(repo_name)
        elif event_type == "DeleteEvent" and (event.get("payload") or {}).get("ref_type") == "repository":
            deleted_projects.append(repo_name)
        elif event_type == "PublicEvent":
            new_projects.append(repo_name)
    for repo in raw.get("repos", []):
        if repo.get("archived") and repo.get("updated_at") and repo["updated_at"] >= since:
            archived_projects.append(repo["full_name"])

    real_commits = [commit for commit in commits if not commit["flags"]["churn"]]
    pack = {
        "period": {"since": since, "until": until, "days": WINDOW_DAYS},
        "user": raw.get("user", GITHUB_USER),
        "repos": active_repos,
        "commits": commits,
        "pull_requests": pull_requests,
        "issues": issues,
        "releases": releases,
        "new_projects": sorted(set(new_projects)),
        "deleted_projects": sorted(set(deleted_projects)),
        "archived_projects": sorted(set(archived_projects)),
        "projects_context": {k: v for k, v in projects.items()},
        "stats": {
            "commits": len(real_commits),
            "churn_commits": len(commits) - len(real_commits),
            "files_changed": len({name for commit in commits for name in commit["files"]}),
            "prs_opened": len([pr for pr in pull_requests]),
            "prs_merged": len([pr for pr in pull_requests if pr.get("merged")]),
            "issues_opened": len(issues),
            "releases": len(releases),
        },
    }
    return _truncate(pack)


def _truncate(pack, limit=MAX_PAYLOAD_CHARS):
    if len(json.dumps(pack)) <= limit:
        return pack
    for commit in pack["commits"]:
        commit["files"] = []
    if len(json.dumps(pack)) <= limit:
        return pack
    while pack["commits"] and len(json.dumps(pack)) > limit:
        pack["commits"].pop(0)
    while pack.get("releases") and len(json.dumps(pack)) > limit:
        pack["releases"].pop()
    return pack


def summarize(pack):
    stats = pack["stats"]
    lines = [
        f"period {pack['period']['since']} .. {pack['period']['until']} "
        f"({pack['period']['days']}d)",
        f"repos: {len(pack['repos'])}  commits: {stats['commits']} "
        f"(churn {stats['churn_commits']})  files: {stats['files_changed']}",
        f"PRs: {stats['prs_opened']} ({stats['prs_merged']} merged)  "
        f"issues: {stats['issues_opened']}  releases: {stats['releases']}",
    ]
    if pack["new_projects"]:
        lines.append("new: " + ", ".join(pack["new_projects"]))
    if pack["archived_projects"]:
        lines.append("archived: " + ", ".join(pack["archived_projects"]))
    if not stats["commits"] and not stats["prs_opened"] and not stats["issues_opened"]:
        lines.append("no non-churn activity in window")
    return "\n".join(lines)


def _iso(value):
    return value.replace("+00:00", "Z") if value else value


def default_period(window_days=WINDOW_DAYS, now=None):
    now = now or datetime.now(timezone.utc)
    until = now.replace(microsecond=0)
    since = until - timedelta(days=window_days)
    return _iso(since.isoformat()), _iso(until.isoformat())


def write_pack(pack, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(pack, indent=2) + "\n", encoding="utf-8")
    tmp.replace(out_path)


def doctor():
    findings = []
    token = _load_env_value("GITHUB_TOKEN")
    if not token:
        findings.append("GITHUB_TOKEN missing (environment or /root/.hermes/.env)")
    else:
        try:
            user, headers = _request(f"{API_ROOT}/user", token)
            scopes = headers.get("X-OAuth-Scopes", "")
            login = user.get("login")
            if login and login != GITHUB_USER:
                findings.append(f"token belongs to '{login}', expected '{GITHUB_USER}'")
            if "repo" not in scopes and "public_repo" not in scopes:
                findings.append(f"token scopes lack 'repo' (have: {scopes or 'none'})")
        except SystemExit as error:
            findings.append(str(error))
    projects = load_projects()
    if not projects:
        findings.append(f"project catalog empty or unreadable: {PROJECTS_FILE}")
    if findings:
        for finding in findings:
            print(f"FAIL {finding}")
        return 1
    print("OK token, scopes, and project catalog")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Collect GitHub activity for the weekly progress blog.")
    parser.add_argument("command", nargs="?", default="collect", choices=("collect", "doctor"))
    parser.add_argument("--since")
    parser.add_argument("--until")
    parser.add_argument("--window-days", type=int, default=WINDOW_DAYS)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--from-raw", type=Path, help="build a pack from a saved raw snapshot (offline)")
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return doctor()

    projects = load_projects()
    raw = json.loads(args.from_raw.read_text(encoding="utf-8")) if args.from_raw else None
    if args.since and args.until:
        since, until = args.since, args.until
    elif raw and raw.get("since") and raw.get("until"):
        since, until = raw["since"], raw["until"]
    else:
        since, until = default_period(args.window_days)
    if raw is None:
        raw = raw_snapshot(github_token(), GITHUB_USER, since, until)
    pack = build_pack(raw, projects, since, until)

    out = args.out or ACTIVITY_DIR / f"{date.fromisoformat(until[:10]).isoformat()}.json"
    if args.dry_run:
        print(summarize(pack))
        print(f"(dry run) would write {out}")
        return 0
    write_pack(pack, out)
    print(f"wrote {out}")
    print(summarize(pack))
    return 0


if __name__ == "__main__":
    sys.exit(main())
