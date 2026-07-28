#!/usr/bin/env python3
"""Check a workspace against the README/STATUS/LOG contract.

Finds candidates, not verdicts: a unit flagged here still needs a human or an
agent to decide whether it is actually a problem.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

CONTRACT = ("README.md", "STATUS.md", "LOG.md")

# Folders the contract does not apply to.
SKIP = {
    "archive",
    "archives",
    "inbox",
    "resources",
    "templates",
    "reference",
    "admin",
    ".git",
    ".claude",
    "node_modules",
    "__pycache__",
}

PLACEHOLDER = re.compile(r"\{[A-Za-z][^{}\n]{0,60}\}")
TODO = re.compile(r"\bTODO\b")


def is_unit(path: Path) -> bool:
    """A directory is a unit if it holds any of the contract files."""
    return any((path / name).exists() for name in CONTRACT)


def find_units(root: Path) -> list[Path]:
    units = []
    for path in sorted(root.rglob("*")):
        if not path.is_dir():
            continue
        parts = set(path.relative_to(root).parts)
        if parts & SKIP:
            continue
        if is_unit(path):
            units.append(path)
    # A unit inside a unit is a working subfolder, not a unit of its own.
    return [u for u in units if not any(u != o and o in u.parents for o in units)]


def audit_unit(unit: Path, root: Path, stale_days: int) -> dict:
    rel = str(unit.relative_to(root))
    missing = [n for n in CONTRACT if not (unit / n).exists()]
    placeholders: list[str] = []
    todos: list[str] = []
    stale_in = None

    for name in CONTRACT:
        f = unit / name
        if not f.exists():
            continue
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        if PLACEHOLDER.search(text):
            placeholders.append(name)
        if TODO.search(text):
            todos.append(name)

    status = unit / "STATUS.md"
    if status.exists():
        age = int((time.time() - status.stat().st_mtime) // 86400)
        if age > stale_days:
            stale_in = age

    return {
        "unit": rel,
        "missing": missing,
        "placeholders": placeholders,
        "todos": todos,
        "stale_days": stale_in,
        "complete": not missing and not placeholders,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", default=".", help="workspace root (default: cwd)")
    p.add_argument("--stale-days", type=int, default=30)
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    units = find_units(root)
    results = [audit_unit(u, root, args.stale_days) for u in units]

    if args.as_json:
        print(json.dumps({"root": str(root), "units": results}, indent=2))
        return 0

    flagged = [r for r in results if not r["complete"] or r["stale_days"]]
    complete = sum(1 for r in results if r["complete"])

    if not units:
        print(f"No units found under {root}.")
        print("Either the workspace is empty, or nothing has the contract yet.")
        return 0

    for r in flagged:
        bits = []
        if r["missing"]:
            bits.append("missing " + ", ".join(r["missing"]))
        if r["placeholders"]:
            bits.append("placeholders in " + ", ".join(r["placeholders"]))
        if r["todos"]:
            bits.append("TODO in " + ", ".join(r["todos"]))
        if r["stale_days"]:
            bits.append(f"STATUS {r['stale_days']}d old")
        print(f"{r['unit']}: {'; '.join(bits)}")

    if not flagged:
        print("No structural problems found.")
    print(f"\nCoverage: {complete}/{len(units)} units with the full contract.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
