#!/usr/bin/env python3
"""Highlights-only guard for data/experience.yaml.

The weekly pipeline may append or refine achievement bullets and nothing else.
This compares the committed file with the working tree and rejects any change
outside a `highlights` list, plus any entry that exceeds the highlight cap. Lists
of records are matched by `id`, so reordering is not a change.

Usage:
    cv_guard.py --data PATH [--base-ref HEAD]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

MAX_HIGHLIGHTS_PER_ENGAGEMENT = 5


def _by_id(seq):
    if seq and all(isinstance(item, dict) and "id" in item for item in seq):
        return {item["id"]: item for item in seq}
    return None


def _diff(old, new, path, out):
    if isinstance(old, dict) and isinstance(new, dict):
        for key in sorted(set(old) | set(new), key=str):
            here = f"{path}.{key}" if path else key
            if key == "highlights":
                continue
            if key not in old:
                out.append(f"{here} added")
            elif key not in new:
                out.append(f"{here} removed")
            else:
                _diff(old[key], new[key], here, out)
        return

    if isinstance(old, list) and isinstance(new, list):
        old_by_id, new_by_id = _by_id(old), _by_id(new)
        if old_by_id is not None and new_by_id is not None:
            for key in sorted(set(old_by_id) | set(new_by_id), key=str):
                here = f"{path}[{key}]"
                if key not in old_by_id:
                    out.append(f"{here} added")
                elif key not in new_by_id:
                    out.append(f"{here} removed")
                else:
                    _diff(old_by_id[key], new_by_id[key], here, out)
            return
        if len(old) != len(new):
            out.append(f"{path} length changed")
            return
        for index, (a, b) in enumerate(zip(old, new)):
            _diff(a, b, f"{path}[{index}]", out)
        return

    if old != new:
        out.append(f"{path} changed")


def structural_violations(old: dict, new: dict) -> list[str]:
    """Changes outside a highlights list, as readable paths."""
    out: list[str] = []
    _diff(old or {}, new or {}, "", out)
    return out


def cap_violations(new: dict, cap: int = MAX_HIGHLIGHTS_PER_ENGAGEMENT) -> list[str]:
    """Entries whose highlights exceed the cap."""
    out = []
    for section in ("engagements", "projects"):
        for item in new.get(section) or []:
            count = len(item.get("highlights") or [])
            if count > cap:
                out.append(f"{section}[{item.get('id')}]: {count} highlights (cap {cap})")
    return out


def violations(old: dict, new: dict) -> list[str]:
    """Everything the guard refuses: structural edits plus cap breaches."""
    return structural_violations(old, new) + cap_violations(new)


def _git(args, cwd):
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=60, check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Reject any CV edit that is not a highlight.")
    parser.add_argument("--data", required=True, help="path to experience.yaml")
    parser.add_argument("--base-ref", default="HEAD")
    args = parser.parse_args(argv)

    data_path = Path(args.data).resolve()
    repo_root = Path(_git(["rev-parse", "--show-toplevel"], data_path.parent).strip())
    relative = data_path.relative_to(repo_root).as_posix()

    old = yaml.safe_load(_git(["show", f"{args.base_ref}:{relative}"], repo_root))
    new = yaml.safe_load(data_path.read_text(encoding="utf-8"))

    findings = violations(old or {}, new or {})
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
