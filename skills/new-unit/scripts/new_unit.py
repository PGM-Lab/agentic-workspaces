#!/usr/bin/env python3
"""Create a unit of work from the workspace templates.

Seeds the README/STATUS/LOG contract so every unit starts the same shape.
Edit KINDS below to match your workspace's top-level folders.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

# kind -> (top-level folder, README template in resources/templates/)
# EDIT THIS to match your workspace. See SKILL.md.
KINDS = {
    "project": ("projects", "project_README.md"),
    "area": ("areas", "area_README.md"),
}

# Kinds that are a single note rather than a folder with the full contract.
NOTE_KINDS = {
    "person": ("people", "person_README.md"),
}

# kind -> subfolders to create instead of the default notes/
SUBFOLDERS: dict[str, tuple[str, ...]] = {}

# kind -> extra contract files, as (filename, template name)
EXTRA_FILES: dict[str, tuple[tuple[str, str], ...]] = {}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-unit"


def fill(text: str, name: str, summary: str) -> str:
    return (
        text.replace("{Unit name}", name)
        .replace("{YYYY-MM-DD}", date.today().isoformat())
        .replace("{Summary}", summary or "TODO: describe this unit.")
    )


def read_template(templates: Path, name: str) -> str:
    path = templates / name
    if not path.exists():
        sys.exit(f"Missing template: {path}")
    return path.read_text()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name", help="human-readable name of the unit")
    p.add_argument("--type", default="project", choices=[*KINDS, *NOTE_KINDS])
    p.add_argument("--summary", default="", help="one-line summary")
    p.add_argument("--root", default=".", help="workspace root (default: cwd)")
    p.add_argument(
        "--templates",
        default="resources/templates",
        help="templates directory, relative to root",
    )
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Workspace root does not exist: {root}")
    templates = root / args.templates
    if not templates.is_dir():
        sys.exit(f"Templates directory does not exist: {templates}")

    slug = slugify(args.name)

    # Single-file kinds: one note, no contract.
    if args.type in NOTE_KINDS:
        folder, tpl = NOTE_KINDS[args.type]
        dest = root / folder / f"{slug}.md"
        if dest.exists():
            sys.exit(f"Already exists: {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(fill(read_template(templates, tpl), args.name, args.summary))
        print(dest)
        return 0

    folder, readme_tpl = KINDS[args.type]
    base = root / folder / slug
    if base.exists():
        sys.exit(f"Already exists: {base}")

    for sub in SUBFOLDERS.get(args.type, ("notes",)):
        (base / sub).mkdir(parents=True)

    contract = [
        ("README.md", readme_tpl),
        ("STATUS.md", "STATUS.md"),
        ("LOG.md", "LOG.md"),
        *EXTRA_FILES.get(args.type, ()),
    ]
    for filename, tpl in contract:
        (base / filename).write_text(
            fill(read_template(templates, tpl), args.name, args.summary)
        )

    # Unit-level AGENTS.md is optional; seed it only if a template exists,
    # and delete it if the unit turns out to have no rules of its own.
    agents_tpl = templates / "unit_AGENTS.md"
    if agents_tpl.exists():
        (base / "AGENTS.md").write_text(
            fill(agents_tpl.read_text(), args.name, args.summary)
        )

    print(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
