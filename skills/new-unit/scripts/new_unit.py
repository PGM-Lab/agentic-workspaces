#!/usr/bin/env python3
"""Create a unit of work from the workspace templates.

Seeds the README/STATUS/LOG contract so every unit starts the same shape.
Edit KINDS below to match your workspace's top-level folders.

Templates are looked up in <root>/resources/templates/ first. If the
workspace has none, the copy bundled with this skill (../templates/) is used,
so the skill works out of the box; copy that bundle into the workspace the
day you want to customize it.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

SKILL_TEMPLATES = Path(__file__).resolve().parents[1] / "templates"

# kind -> (top-level folder, README template in the templates directory)
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
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-unit"


def fill(text: str, name: str, summary: str) -> str:
    text = text.replace("{Unit name}", name).replace(
        "{YYYY-MM-DD}", date.today().isoformat()
    )
    # With no summary given, {Summary} stays in place on purpose: the audit
    # then reports the unit as unfilled instead of counting it complete.
    if summary:
        text = text.replace("{Summary}", summary)
    return text


def resolve_templates(root: Path, requested: str, default: str) -> Path:
    path = root / requested
    if path.is_dir():
        return path
    if requested != default:
        sys.exit(f"Templates directory does not exist: {path}")
    if SKILL_TEMPLATES.is_dir():
        print(f"note: {path} not found, using the skill's bundled templates")
        return SKILL_TEMPLATES
    sys.exit(f"No templates: neither {path} nor {SKILL_TEMPLATES} exists")


def main() -> int:
    default_templates = "resources/templates"
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name", help="human-readable name of the unit")
    p.add_argument("--type", default="project", choices=[*KINDS, *NOTE_KINDS])
    p.add_argument("--summary", default="", help="one-line summary")
    p.add_argument("--root", default=".", help="workspace root (default: cwd)")
    p.add_argument(
        "--templates",
        default=default_templates,
        help="templates directory, relative to root (default: %(default)s, "
        "falling back to the skill's bundled templates)",
    )
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Workspace root does not exist: {root}")
    templates = resolve_templates(root, args.templates, default_templates)

    def read_template(name: str) -> str:
        path = templates / name
        if not path.exists():
            sys.exit(f"Missing template: {path}")
        return path.read_text()

    slug = slugify(args.name)

    # Single-file kinds: one note, no contract.
    if args.type in NOTE_KINDS:
        folder, tpl = NOTE_KINDS[args.type]
        content = fill(read_template(tpl), args.name, args.summary)
        dest = root / folder / f"{slug}.md"
        if dest.exists():
            sys.exit(f"Already exists: {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
        print(dest)
        return 0

    folder, readme_tpl = KINDS[args.type]
    base = root / folder / slug
    if base.exists():
        sys.exit(f"Already exists: {base}")

    contract = [
        ("README.md", readme_tpl),
        ("STATUS.md", "STATUS.md"),
        ("LOG.md", "LOG.md"),
        *EXTRA_FILES.get(args.type, ()),
    ]
    # Unit-level AGENTS.md is optional; seed it only if a template exists,
    # and delete it if the unit turns out to have no rules of its own.
    if (templates / "unit_AGENTS.md").exists():
        contract.append(("AGENTS.md", "unit_AGENTS.md"))

    # Render every template before writing anything: a missing template must
    # not leave a half-created unit behind, least of all on storage with no
    # version control.
    rendered = [
        (filename, fill(read_template(tpl), args.name, args.summary))
        for filename, tpl in contract
    ]

    for sub in SUBFOLDERS.get(args.type, ("notes",)):
        (base / sub).mkdir(parents=True)
    for filename, content in rendered:
        (base / filename).write_text(content)

    print(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
