#!/usr/bin/env python3
"""Install the skills, and create a workspace skeleton.

The mechanical half of setup. It is a script rather than something an agent
does with file tools because almost every write lands outside the directory
an agent is launched in: skills go to the home directory, the workspace goes
wherever the user keeps their work. Running one command with explicit
destinations avoids a session spent approving writes.

Never destructive. It adds; it never overwrites a file someone has edited,
and it leaves an existing skill of the same name alone rather than replacing
it.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILLS_SRC = REPO / "skills"
BUNDLED_WORKSPACE = Path(__file__).resolve().parents[1] / "templates" / "workspace"
BUNDLED_UNIT = REPO / "skills" / "new-unit" / "templates"

# Canonical location: Codex reads it natively, and Claude Code picks it up
# through a symlink. One copy, two agents.
CANONICAL = Path.home() / ".agents" / "skills"
CLAUDE = Path.home() / ".claude" / "skills"

KIND_PRESETS = {
    "by-kind": {
        "project": {"folder": "projects", "readme": "project_README.md"},
        "area": {"folder": "areas", "readme": "area_README.md"},
        "person": {"folder": "people", "readme": "person_README.md", "note": True},
    },
    "by-cycle": {
        "unit": {"folder": "cycles", "readme": "project_README.md"},
        "area": {"folder": "areas", "readme": "area_README.md"},
        "person": {"folder": "people", "readme": "person_README.md", "note": True},
    },
}

SUPPORT_DIRS = ("resources/templates", "inbox", "archive")


def say(msg: str) -> None:
    print(msg)


def link_or_copy(src: Path, dest: Path, copy: bool) -> str:
    """Return a one-word outcome: linked, copied, kept, or conflict."""
    if dest.is_symlink() or dest.exists():
        if dest.is_symlink() and dest.resolve() == src.resolve():
            return "kept"
        return "conflict"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if copy:
        shutil.copytree(src, dest, symlinks=True)
        return "copied"
    # Absolute, so the link survives the skills directory being moved. The
    # links checked into the repo are relative instead, because those have to
    # work in anybody's clone.
    dest.symlink_to(src.resolve())
    return "linked"


def install_skills(copy: bool, canonical: Path, claude: Path) -> int:
    if not SKILLS_SRC.is_dir():
        sys.exit(f"Cannot find the kit's skills at {SKILLS_SRC}")

    found = [
        name
        for name, path in (
            ("Claude Code", claude.parent),
            ("Codex", Path.home() / ".codex"),
        )
        if path.is_dir()
    ]
    say(f"Agents detected: {', '.join(found) if found else 'none (installing anyway)'}")

    conflicts = []
    for src in sorted(p for p in SKILLS_SRC.iterdir() if (p / "SKILL.md").is_file()):
        outcome = link_or_copy(src, canonical / src.name, copy)
        if outcome == "conflict":
            conflicts.append(src.name)
            say(f"  {src.name}: already installed, left untouched")
            continue
        say(f"  {src.name}: {outcome} into {canonical}")
        # Claude Code reads its own directory; point it at the canonical copy.
        bridge = link_or_copy(canonical / src.name, claude / src.name, copy=False)
        if bridge == "conflict":
            say(f"  {src.name}: a different skill of this name exists in {claude}")

    if conflicts:
        say(
            "\nLeft alone because something of the same name was already there: "
            + ", ".join(conflicts)
            + "\nNothing was overwritten. Compare them yourself and merge if you want the kit's version."
        )
    if not copy:
        say(
            f"\nInstalled as symlinks into this clone ({REPO}).\n"
            "Update everything later with: git pull. Do not delete or move the clone."
        )
    return 0


def seed_workspace(root: Path, name: str, preset: str, overview_roots: Path | None) -> int:
    created, kept = [], []

    def write(path: Path, content: str) -> None:
        if path.exists():
            kept.append(path)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        created.append(path)

    if not BUNDLED_WORKSPACE.is_dir():
        sys.exit(f"Cannot find the workspace templates at {BUNDLED_WORKSPACE}")

    for tpl in sorted(BUNDLED_WORKSPACE.glob("*.md")):
        write(root / tpl.name, tpl.read_text().replace("{Workspace name}", name))

    write(
        root / "resources" / "kinds.json",
        json.dumps(KIND_PRESETS[preset], indent=2) + "\n",
    )
    for d in SUPPORT_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    # The unit templates come along so the workspace owns them and can be
    # edited without touching the installed skill.
    if BUNDLED_UNIT.is_dir():
        for tpl in sorted(BUNDLED_UNIT.glob("*.md")):
            write(root / "resources" / "templates" / tpl.name, tpl.read_text())

    for p in created:
        say(f"  created {p.relative_to(root)}")
    for p in kept:
        say(f"  kept    {p.relative_to(root)} (already existed, not touched)")

    if overview_roots is not None:
        line = str(root)
        existing = (
            overview_roots.read_text().splitlines() if overview_roots.exists() else []
        )
        if line in [l.strip() for l in existing]:
            say(f"  kept    {overview_roots} (already lists this workspace)")
        else:
            overview_roots.parent.mkdir(parents=True, exist_ok=True)
            with overview_roots.open("a") as fh:
                fh.write(line + "\n")
            say(f"  added   {root} to {overview_roots}")

    say("\nPostconditions to check:")
    say(f"  - {root}/AGENTS.md exists and its rules are yours, not the template's")
    say(f"  - {root}/CLAUDE.md contains only the @AGENTS.md import")
    say(f"  - {root}/resources/kinds.json names this workspace's kinds")
    say("  - audit-workspace reports no empty sections in AGENTS.md")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--install", action="store_true", help="install the kit's skills")
    p.add_argument("--copy", action="store_true", help="copy skills instead of symlinking")
    p.add_argument("--workspace", help="path of the workspace to create")
    p.add_argument("--name", default="", help="human name of the workspace")
    p.add_argument(
        "--layout",
        choices=sorted(KIND_PRESETS),
        default="by-kind",
        help="starting kinds: by-kind for work with different lifecycles, "
        "by-cycle for seasonal work (default: %(default)s)",
    )
    p.add_argument(
        "--canonical",
        default=str(CANONICAL),
        help="where the one canonical copy of the skills lives (default: %(default)s)",
    )
    p.add_argument(
        "--claude-skills",
        default=str(CLAUDE),
        help="Claude Code's skills directory (default: %(default)s)",
    )
    p.add_argument(
        "--overview-roots",
        default="",
        help="roots.txt to append the new workspace to; 'none' to skip "
        "(default: the installed workspace-overview skill's own roots.txt)",
    )
    args = p.parse_args()

    if not args.install and not args.workspace:
        p.error("nothing to do: pass --install, --workspace, or both")

    canonical = Path(args.canonical).expanduser()
    claude = Path(args.claude_skills).expanduser()

    if args.install:
        say("Installing skills")
        install_skills(args.copy, canonical, claude)

    if args.workspace:
        root = Path(args.workspace).expanduser().resolve()
        say(f"\nSeeding workspace at {root}")
        if args.overview_roots == "none":
            roots = None
        elif args.overview_roots:
            roots = Path(args.overview_roots).expanduser()
        else:
            roots = canonical / "workspace-overview" / "roots.txt"
        seed_workspace(root, args.name or root.name, args.layout, roots)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
