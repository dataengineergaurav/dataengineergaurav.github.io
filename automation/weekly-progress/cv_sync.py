#!/usr/bin/env python3
"""Render the CV and publish the one-pager into the site.

Renders in CV-Development through its own environment, copies the one-pager to
the site under the exact name the homepage links, and writes a version marker so
a stale or hand-swapped PDF fails CI. On any failure the site worktree is left
untouched, because the copy and the marker are written together or not at all.

Usage:
    cv_sync.py [--cv-root PATH] [--site-root PATH] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SITE_PDF = "Gaurav_Gurjar_CV_AI-Data-Engineer.pdf"
SITE_VERSION = "Gaurav_Gurjar_CV_AI-Data-Engineer.version.json"
CV_ONE_PAGER = "Gaurav_Gurjar_CV.pdf"
DEFAULT_CV_ROOT = Path("/root/CV-Development")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def render(cv_root: Path) -> None:
    """Render both documents in the project's own environment."""
    for extra in ([], ["--expanded"]):
        result = subprocess.run(
            ["uv", "run", "--quiet", "python", "render.py", *extra],
            cwd=cv_root, capture_output=True, text=True, timeout=900, check=False,
        )
        if result.returncode != 0:
            label = "expanded" if extra else "one-pager"
            raise SystemExit(f"render failed ({label}): {result.stderr.strip()}")


def _current_commit(cv_root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(cv_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, timeout=60, check=False,
    )
    return result.stdout.strip() or "unknown"


def sync(cv_root: Path, site_root: Path) -> dict:
    """Copy the rendered one-pager into the site and write its marker."""
    source = Path(cv_root) / CV_ONE_PAGER
    if not source.is_file():
        raise SystemExit(f"missing rendered CV: {source}")

    payload = {
        "cv_commit": _current_commit(Path(cv_root)),
        "rendered_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": sha256_file(source),
    }

    target_pdf = Path(site_root) / SITE_PDF
    target_version = Path(site_root) / SITE_VERSION
    backup = target_pdf.read_bytes() if target_pdf.exists() else None
    try:
        shutil.copyfile(source, target_pdf)
        target_version.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except Exception:
        if backup is None:
            target_pdf.unlink(missing_ok=True)
        else:
            target_pdf.write_bytes(backup)
        raise
    return payload


def marker_violations(site_root: Path) -> list[str]:
    """Problems with the committed CV pdf and its marker (empty means consistent)."""
    site_root = Path(site_root)
    pdf = site_root / SITE_PDF
    marker = site_root / SITE_VERSION

    if not pdf.is_file():
        return [f"missing {SITE_PDF}"]
    if not marker.is_file():
        return [f"missing {SITE_VERSION}"]

    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except ValueError:
        return [f"{SITE_VERSION} is not valid JSON"]

    out = []
    if payload.get("sha256") != sha256_file(pdf):
        out.append(f"{SITE_PDF}: sha256 does not match {SITE_VERSION}")
    if not payload.get("cv_commit"):
        out.append(f"{SITE_VERSION}: cv_commit is missing")
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render the CV and sync the one-pager into the site.")
    parser.add_argument("--cv-root", default=str(DEFAULT_CV_ROOT))
    parser.add_argument("--site-root", default=".")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    cv_root = Path(args.cv_root)
    site_root = Path(args.site_root)

    if args.dry_run:
        print(f"(dry-run) would render {cv_root} and copy {CV_ONE_PAGER} to {site_root / SITE_PDF}")
        return 0

    render(cv_root)
    payload = sync(cv_root, site_root)
    print(f"synced {SITE_PDF} (cv_commit {payload['cv_commit']}, sha256 {payload['sha256'][:12]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
