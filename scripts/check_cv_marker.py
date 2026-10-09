#!/usr/bin/env python3
"""CI check: the committed CV pdf must match its version marker.

Guards against a PDF that was swapped or regenerated without its marker, which
would let the published CV drift from the recorded render.

Usage:
    check_cv_marker.py [--root PATH]
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "automation" / "weekly-progress"))

import cv_sync  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Verify the committed CV pdf against its marker.")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args(argv)

    findings = cv_sync.marker_violations(Path(args.root))
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
