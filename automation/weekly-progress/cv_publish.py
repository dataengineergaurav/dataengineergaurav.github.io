#!/usr/bin/env python3
"""Deterministic publisher for the weekly CV pull request.

Takes the highlights-only edit the agent made to data/experience.yaml plus the
regenerated artifacts, and on an isolated branch commits exactly those files,
pushes, and opens a pull request against CV-Development. It never pushes to the
base branch, and it reuses publish.py's git/PR helpers so both publishers share
one implementation of the safety rules.

Usage:
    cv_publish.py --date YYYY-MM-DD [--body-file PATH] [--base main]
                  [--remote origin] [--repo-root PATH] [--dry-run | --no-push]
"""
from __future__ import annotations

import argparse
import sys
from datetime import date as date_cls
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PIPELINE_DIR))

import publish as site  # noqa: E402  (same directory)

CV_ROOT = Path("/root/CV-Development")
CV_FILES = [
    "data/experience.yaml",
    "resume.html",
    "resume_expanded.html",
    "Gaurav_Gurjar_CV.pdf",
    "Gaurav_Gurjar_CV_extended.pdf",
]
REQUIRED_FILES = ["data/experience.yaml"]


def branch_for(date: str) -> str:
    return f"cv-refresh/{date}"


def assert_only(expected, actual) -> None:
    """Raise unless the worktree holds exactly `expected`."""
    want, seen = sorted(set(expected)), sorted(set(actual))
    if want != seen:
        raise SystemExit(f"cv guard failed: expected {want}, saw {seen}")


def publish(date, base="main", remote="origin", repo_root=CV_ROOT, body_file=None, push=True):
    root = Path(repo_root)

    site.git("fetch", remote, base, cwd=root)
    base_head = site.git("rev-parse", f"{remote}/{base}", cwd=root)
    current = site.git("branch", "--show-current", cwd=root)
    if current != base:
        raise SystemExit(f"must publish from '{base}' (currently on '{current}')")
    if site.git("rev-parse", "HEAD", cwd=root) != base_head:
        raise SystemExit(f"HEAD is not synchronized with {remote}/{base}; sync before publishing")

    assert_only(CV_FILES, site._changed_paths(root))

    branch = branch_for(date)
    if not push:
        print(
            f"(no-push) would branch {branch}, commit {len(CV_FILES)} files "
            f"in {root}, push {remote}, open PR (base {base})"
        )
        return 0

    owner, repo = site.parse_remote(site.git("remote", "get-url", remote, cwd=root))
    token = site._load_env_value("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required to open a pull request")
    found = site.existing_pr(token, owner, repo, branch)
    if found:
        print(f"PR already exists: {found['html_url']}")
        return 0

    reviewed = {rel: site.sha256_bytes((root / rel).read_bytes()) for rel in CV_FILES}
    site.git("checkout", "-B", branch, base_head, cwd=root)
    try:
        site.git("add", "--", *CV_FILES, cwd=root)
        assert_only(CV_FILES, site.git("diff", "--cached", "--name-only", cwd=root).splitlines())
        for rel in CV_FILES:
            staged = site.git("show", f":{rel}", raw=True, cwd=root)
            if site.sha256_bytes(staged) != reviewed[rel]:
                raise SystemExit(f"staged {rel} does not match the reviewed file")
        site.git("commit", "-m", f"cv: weekly highlights {date}", cwd=root)
        if site.git("rev-parse", "HEAD^", cwd=root) != base_head:
            raise SystemExit("commit is not a single step from the base head")
        site.git("push", remote, f"HEAD:refs/heads/{branch}", cwd=root)
    except SystemExit:
        site.git("checkout", base, check=False, cwd=root)
        site.git("branch", "-D", branch, check=False, cwd=root)
        raise

    body = f"Weekly CV highlights for {date}."
    if body_file and Path(body_file).is_file():
        body = Path(body_file).read_text(encoding="utf-8")
    status, payload = site._api(token, "POST", f"https://api.github.com/repos/{owner}/{repo}/pulls", {
        "title": f"CV highlights — {date}",
        "head": branch,
        "base": base,
        "body": body,
    })
    if status not in (200, 201):
        raise SystemExit(f"failed to open PR ({status}): {payload.get('raw', payload)}")
    site.git("checkout", base, check=False, cwd=root)
    print(f"opened PR: {payload['html_url']}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Publish the weekly CV highlights as a pull request.")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--base", default="main")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--repo-root", default=str(CV_ROOT))
    parser.add_argument("--body-file")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    args = parser.parse_args(argv)

    try:
        date_cls.fromisoformat(args.date)
    except ValueError:
        raise SystemExit(f"--date must be YYYY-MM-DD, got {args.date!r}")

    return publish(
        args.date, base=args.base, remote=args.remote, repo_root=Path(args.repo_root),
        body_file=args.body_file, push=not (args.dry_run or args.no_push),
    )


if __name__ == "__main__":
    raise SystemExit(main())
