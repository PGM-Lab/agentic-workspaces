#!/usr/bin/env python3
"""Create a unit of work from the workspace templates.

Seeds the README/STATUS/LOG contract so every unit starts the same shape.

The kinds of unit a workspace has are per workspace, not per machine, so they
live in <root>/resources/kinds.json. Without that file the generic kinds below
are used, which is what makes the skill work in a fresh workspace.

Templates come from <root>/resources/templates/ when it exists, otherwise from
the copy bundled with this skill.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

SKILL_TEMPLATES = Path(__file__).resolve().parents[1] / "templates"
KINDS_FILE = "resources/kinds.json"

# Used when the workspace has no kinds.json of its own. A real workspace
# names its own kinds: papers, grants and reviews for research; semesters and
# courses for teaching; clients and engagements for a consultancy.
DEFAULT_KINDS = {
    "project": {"folder": "projects", "readme": "project_README.md"},
    "area": {"folder": "areas", "readme": "area_README.md"},
    "person": {"folder": "people", "readme": "person_README.md", "note": True},
}


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


def load_kinds(root: Path) -> dict:
    """Read the workspace's kinds, falling back to the generic ones."""
    path = root / KINDS_FILE
    if not path.is_file():
        return DEFAULT_KINDS
    try:
        kinds = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        sys.exit(f"Cannot read {path}: {exc}")
    if not isinstance(kinds, dict) or not kinds:
        sys.exit(f"{path} must be a non-empty object mapping kind -> settings")
    for kind, spec in kinds.items():
        if not isinstance(spec, dict) or "folder" not in spec or "readme" not in spec:
            sys.exit(f"{path}: kind '{kind}' needs at least 'folder' and 'readme'")
    return kinds


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
    p.add_argument(
        "name", nargs="?", help="human-readable name of the unit"
    )
    p.add_argument(
        "--type",
        default="project",
        help="kind of unit; the workspace's kinds come from "
        f"{KINDS_FILE} (default: %(default)s)",
    )
    p.add_argument("--summary", default="", help="one-line summary")
    p.add_argument(
        "--parent",
        default="",
        help="for a kind whose folder contains {parent}, the unit this one "
        "goes inside: a semester, a programme, a client",
    )
    p.add_argument("--root", default=".", help="workspace root (default: cwd)")
    p.add_argument(
        "--templates",
        default=default_templates,
        help="templates directory, relative to root (default: %(default)s, "
        "falling back to the skill's bundled templates)",
    )
    p.add_argument(
        "--list-kinds", action="store_true", help="print this workspace's kinds and exit"
    )
    args = p.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        sys.exit(f"Workspace root does not exist: {root}")
    kinds = load_kinds(root)

    if args.list_kinds:
        source = KINDS_FILE if (root / KINDS_FILE).is_file() else "built-in defaults"
        print(f"kinds from {source}:")
        for kind, spec in sorted(kinds.items()):
            shape = "single note" if spec.get("note") else "README/STATUS/LOG"
            print(f"  {kind:<12} -> {spec['folder']}/  ({shape})")
        return 0

    if not args.name:
        p.error("the following arguments are required: name")
    if args.type not in kinds:
        sys.exit(
            f"Unknown kind '{args.type}'. This workspace has: "
            f"{', '.join(sorted(kinds))}.\n"
            f"Add a kind by editing {root / KINDS_FILE}."
        )
    spec = kinds[args.type]
    templates = resolve_templates(root, args.templates, default_templates)

    # Some work nests: a course inside a semester, a project inside a
    # programme. The kind says so by putting {parent} in its folder, since
    # which parent is a per-unit answer and the folder is a per-kind one.
    folder = spec["folder"]
    if "{parent}" in folder:
        if not args.parent:
            sys.exit(
                f"Kind '{args.type}' goes inside another unit: its folder is "
                f"'{folder}'. Say which one with --parent."
            )
        folder = folder.replace("{parent}", args.parent)
        if not (root / folder).is_dir():
            sys.exit(
                f"No such parent: {root / folder}\n"
                "Create it first, or check the spelling. Creating it here "
                "would hide a typo as a new empty folder."
            )
    elif args.parent:
        sys.exit(
            f"Kind '{args.type}' does not nest: its folder is '{folder}', "
            "with no {parent} in it, so --parent has nowhere to go."
        )

    def read_template(name: str) -> str:
        path = templates / name
        if not path.exists():
            sys.exit(f"Missing template: {path}")
        return path.read_text()

    # Some kinds are named with an identifier rather than a title: a semester
    # (2026-Autumn), a cohort, a course code. Slugifying those damages a name
    # that was already canonical, so the kind can ask to keep it verbatim.
    if spec.get("literal"):
        slug = args.name.strip()
        if not slug or slug.startswith(".") or "/" in slug or "\\" in slug:
            sys.exit(
                f"Kind '{args.type}' uses the name as the folder name, so "
                f"'{args.name}' will not do: no slashes, and not starting "
                "with a dot."
            )
    else:
        slug = slugify(args.name)

    # Single-file kinds: one note, no contract.
    if spec.get("note"):
        content = fill(read_template(spec["readme"]), args.name, args.summary)
        dest = root / folder / f"{slug}.md"
        if dest.exists():
            sys.exit(f"Already exists: {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)
        print(dest)
        return 0

    base = root / folder / slug
    if base.exists():
        sys.exit(f"Already exists: {base}")

    contract = [
        ("README.md", spec["readme"]),
        ("STATUS.md", "STATUS.md"),
        ("LOG.md", "LOG.md"),
        *sorted(spec.get("extra", {}).items()),
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

    for sub in spec.get("subfolders", ["notes"]):
        (base / sub).mkdir(parents=True)
    for filename, content in rendered:
        (base / filename).write_text(content)

    print(base)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
