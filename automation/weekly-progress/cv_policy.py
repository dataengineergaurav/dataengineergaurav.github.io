#!/usr/bin/env python3
"""Policy gate for the rendered CV PDFs.

The CV is published on the site, so its text must obey the same client-scoped
denylist the site applies to PDFs: employers-of-record are allowed, clients are
not. A PDF that yields no text cannot be verified, so it fails closed rather than
passing silently.

Usage:
    cv_policy.py --pdf PATH [--pdf PATH ...]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from public_policy import cv_forbidden_names  # noqa: E402

DENYLIST = cv_forbidden_names()


def text_violations(text: str) -> list[str]:
    """Denylisted terms present in `text`, case-insensitively."""
    low = text.casefold()
    return [term for term in DENYLIST if term in low]


def pdf_text_violations(text: str) -> list[str]:
    """Violations for extracted PDF text; empty extraction is itself a finding."""
    if not text.strip():
        return ["unreadable pdf"]
    return text_violations(text)


def extract_text(path: Path) -> str:
    import pypdf

    reader = pypdf.PdfReader(str(path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def pdf_violations(path: Path) -> list[str]:
    try:
        text = extract_text(path)
    except Exception:
        text = ""
    return pdf_text_violations(text)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan rendered CV PDFs against the client-scoped denylist."
    )
    parser.add_argument("--pdf", action="append", required=True, help="repeat per PDF")
    args = parser.parse_args(argv)

    findings = [f"{path}: {term}" for path in args.pdf for term in pdf_violations(Path(path))]
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
