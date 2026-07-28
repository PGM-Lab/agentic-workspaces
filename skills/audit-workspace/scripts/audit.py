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


def candidate_dirs(root: Path):
    """Every directory the contract could apply to, root included."""
    yield root
    for path in sorted(root.rglob("*")):
        if not path.is_dir():
            continue
        if set(path.relative_to(root).parts) & SKIP:
            continue
        yield path


def find_units(root: Path, max_depth: int) -> tuple[list[Path], list[Path]]:
    """Split directories into confirmed units and unactivated candidates.

    A `STATUS.md` is what makes a directory a unit. It is the file the whole
    system revolves around, and the one the overview board reads.

    A directory with a `README.md` but no `STATUS.md` is ambiguous from the
    files alone. It is either a unit that was migrated but never activated, or
    else a container (`papers/`, the workspace root) or a working subfolder
    inside a unit, both of which may reasonably carry a README explaining
    themselves. Two heuristics separate them, and neither is exact, which is
    why these are reported as candidates rather than findings:

    - A directory with units below it is a container.
    - Units live near the top of a workspace. Anything deeper than
      `max_depth` is treated as working material inside a unit.
    """
    dirs = list(candidate_dirs(root))
    units = [d for d in dirs if (d / "STATUS.md").exists()]

    def depth(d: Path) -> int:
        return 0 if d == root else len(d.relative_to(root).parts)

    unit_set = set(units)
    candidates = [
        d
        for d in dirs
        if d not in unit_set
        and (d / "README.md").exists()
        and depth(d) <= max_depth
        and not any(u != d and d in u.parents for u in units)
    ]
    return units, candidates


def audit_unit(unit: Path, root: Path, stale_days: int) -> dict:
    rel = str(unit.relative_to(root)) if unit != root else "(workspace root)"
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
    p.add_argument(
        "--max-depth",
        type=int,
        default=3,
        help="deepest level a unit can live at, below the workspace root",
    )
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    units, candidates = find_units(root, args.max_depth)
    results = [audit_unit(u, root, args.stale_days) for u in units]
    candidate_names = [str(c.relative_to(root)) for c in candidates]

    if args.as_json:
        print(
            json.dumps(
                {"root": str(root), "units": results, "candidates": candidate_names},
                indent=2,
            )
        )
        return 0

    flagged = [r for r in results if not r["complete"] or r["stale_days"]]
    complete = sum(1 for r in results if r["complete"])

    if not units and not candidates:
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
        print("No structural problems found in activated units.")

    if candidate_names:
        print("\nPossibly unactivated (README but no STATUS.md). Check whether")
        print("each is a unit that needs activating or just a container folder:")
        for name in candidate_names:
            print(f"  {name}")

    total = len(units) + len(candidates)
    print(f"\nCoverage: {complete}/{total} with the full contract.")
    if candidates:
        print(f"{len(candidates)} not activated yet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
