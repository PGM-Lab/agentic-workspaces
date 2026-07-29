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

# Folders the contract does not apply to. Keep in sync with the prune list
# in workspace-overview/scripts/scan.sh.
SKIP = {
    "archive",
    "archives",
    "inbox",
    "resources",
    "templates",
    "reference",
    "admin",
    # people/ holds notes, one file per person, not units with a contract.
    "people",
    ".git",
    ".claude",
    "node_modules",
    "__pycache__",
}

PLACEHOLDER = re.compile(r"\{[^{}]{0,300}\}")
TODO = re.compile(r"\bTODO\b")
HEADING = re.compile(r"^(#{2,})\s+(.*?)\s*$")


def audit_workspace_agents(root: Path) -> dict:
    """Check the workspace's own AGENTS.md, which no other check looks at.

    It is the file the setup guide calls the only one that genuinely needs
    thought, and the only place the confidentiality rules exist.

    Only language-independent checks are made: whether the file is there,
    whether a section was left with no body, and whether placeholders survive.
    Whether a *needed* section is absent altogether cannot be detected, since
    workspaces are written in the author's own language. That is why the
    setup skill must leave an explicit placeholder rather than omitting a
    section it could not fill.
    """
    path = root / "AGENTS.md"
    empty_result = {"present": False, "placeholders": 0, "empty_sections": []}
    if not path.exists():
        return empty_result
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return empty_result

    # Split on level-2+ headings and find the ones with no body.
    sections: list = []
    current = None
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            current = (m.group(2), [])
            sections.append(current)
        elif current is not None:
            current[1].append(line)

    empty = [
        title
        for title, body in sections
        if not any(l.strip() and not l.strip().startswith("<!--") for l in body)
    ]

    return {
        "present": True,
        "placeholders": len(PLACEHOLDER.findall(text)),
        "empty_sections": empty,
    }


def candidate_dirs(root: Path):
    """Every directory the contract could apply to, root included."""
    yield root
    for path in sorted(root.rglob("*")):
        if not path.is_dir():
            continue
        if set(path.relative_to(root).parts) & SKIP:
            continue
        yield path


def has_loose_files(path: Path) -> bool:
    """True if the directory holds work of its own, not just subfolders.

    The signal that separates a container (`papers/`, which holds units) from
    a unit that was moved into place but never documented (`papers/old-thing`,
    which holds the actual material). Dotfiles do not count.
    """
    try:
        return any(
            p.is_file() and not p.name.startswith(".") for p in path.iterdir()
        )
    except OSError:
        return False


def find_units(root: Path, max_depth: int) -> tuple[list[Path], list[Path], list[Path]]:
    """Sort directories into units, candidates and not-started work.

    A `STATUS.md` is what makes a directory a unit. It is the file the whole
    system revolves around, and the one the overview board reads.

    Everything else is ambiguous from the files alone, so the other two groups
    are reported as questions rather than findings:

    - **candidates**: a `README.md` but no `STATUS.md`. Either a unit that was
      documented and never activated, or a container, or a working subfolder
      that explains itself.
    - **not started**: no contract file at all, but real material inside.
      Either work that was moved into place and never documented, or a folder
      that was never meant to be a unit.

    Three heuristics separate them, none of them exact: a directory with units
    below it is a container; units live near the top of a workspace, so
    anything deeper than `max_depth` is treated as working material; and a
    directory holding loose files of its own is doing work rather than holding
    other units.
    """
    dirs = list(candidate_dirs(root))
    units = [d for d in dirs if (d / "STATUS.md").exists()]

    def depth(d: Path) -> int:
        return 0 if d == root else len(d.relative_to(root).parts)

    def inside_a_unit(d: Path) -> bool:
        # The root is exempt as ancestor: a workspace that is itself a unit
        # can still contain units and undocumented work below it.
        return any(u != root and u in d.parents for u in units)

    unit_set = set(units)
    candidates = [
        d
        for d in dirs
        if d not in unit_set
        and (d / "README.md").exists()
        and depth(d) <= max_depth
        and not any(u != d and d in u.parents for u in units)
        and not inside_a_unit(d)
    ]

    documented = unit_set | set(candidates)

    def has_documented_sibling(d: Path) -> bool:
        """True if something beside this folder is already an activated unit.

        The strongest signal available that a folder sits at unit level: if
        `funding/x` has the contract, then `funding/y` is a unit too, whether
        or not it keeps its material in subfolders.
        """
        return any(o.parent == d.parent and o != d for o in documented)

    # Walk top down (rglob is sorted, so parents come before children) and
    # claim the shallowest undocumented folder that holds work. Everything
    # below a claimed folder is its own material, not a separate unit. This
    # is also what stops the report descending into someone's files and
    # enumerating them, which matters when the material is confidential.
    not_started: list[Path] = []
    claimed: set[Path] = set()
    for d in dirs:
        if d == root:  # the root is the workspace, never a not-started unit.
            continue
        if not 1 <= depth(d) <= max_depth:
            continue
        if d in documented or inside_a_unit(d):
            continue
        if any((d / name).exists() for name in CONTRACT):
            continue
        # A folder holding documented units is a container, not lost work.
        if any(o != d and d in o.parents for o in documented):
            continue
        # Below something already reported, at either level.
        if any(c in d.parents for c in claimed):
            continue
        if any(o in d.parents for o in documented):
            continue
        if not (has_loose_files(d) or has_documented_sibling(d)):
            continue
        not_started.append(d)
        claimed.add(d)
    return units, candidates, not_started


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
        help="deepest level below the root scanned for unactivated "
        "candidates; confirmed units (with a STATUS.md) are found at any "
        "depth",
    )
    p.add_argument("--json", action="store_true", dest="as_json")
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    units, candidates, not_started = find_units(root, args.max_depth)
    results = [audit_unit(u, root, args.stale_days) for u in units]
    candidate_names = [str(c.relative_to(root)) for c in candidates]
    not_started_names = [str(d.relative_to(root)) for d in not_started]
    agents = audit_workspace_agents(root)

    if args.as_json:
        print(
            json.dumps(
                {
                    "root": str(root),
                    "units": results,
                    "candidates": candidate_names,
                    "not_started": not_started_names,
                    "workspace_agents_md": agents,
                },
                indent=2,
            )
        )
        return 0

    # The workspace AGENTS.md goes first: it governs everything below it.
    if not agents["present"]:
        print("AGENTS.md: missing at the workspace root. Agents working here")
        print("have no rules, no structure and no confidentiality boundaries.\n")
    else:
        problems = []
        if agents["empty_sections"]:
            problems.append("empty sections: " + ", ".join(agents["empty_sections"]))
        if agents["placeholders"]:
            problems.append(f"{agents['placeholders']} unfilled placeholder(s)")
        if problems:
            print("AGENTS.md (workspace root): " + "; ".join(problems))
            print("This is the file that tells an agent what it may not do.\n")

    flagged = [r for r in results if not r["complete"] or r["stale_days"]]
    complete = sum(1 for r in results if r["complete"])

    if not units and not candidates and not not_started:
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

    if not_started_names:
        print("\nNot started (material but no contract file at all). Check")
        print("whether each is a unit to activate, archive, or leave alone:")
        for name in not_started_names:
            print(f"  {name}")

    total = len(units) + len(candidates) + len(not_started)
    print(f"\nCoverage: {complete}/{total} with the full contract.")
    pending = len(candidates) + len(not_started)
    if pending:
        print(
            f"{pending} not activated yet "
            f"({len(candidates)} documented, {len(not_started)} not started)."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
