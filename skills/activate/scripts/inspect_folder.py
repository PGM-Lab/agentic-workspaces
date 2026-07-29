#!/usr/bin/env python3
"""Summarise a folder that already holds work, so its contract can be drafted.

Read-only. It never writes, and it never prints the contents of a file: it
reports shape, dates and pointers. That is deliberate. The folders being
activated often hold confidential material, and the drafting agent needs to
know what the folder *is*, not what is inside every file.

What it cannot tell you is the one thing that matters most: what the next
action is. That is not in the folder.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

CONTRACT = ("README.md", "STATUS.md", "LOG.md")
SKIP_DIRS = {".git", ".claude", "node_modules", "__pycache__", ".DS_Store"}
URL = re.compile(r"https?://[^\s<>()\"'\]]+")
GIT_URL = re.compile(r"^\s*url\s*=\s*(.+?)\s*$", re.M)
TEXT_SUFFIXES = {".md", ".txt"}
MAX_TEXT_BYTES = 100_000

# Suffixes that usually mean the real artefact lives somewhere else.
CANONICAL_HINTS = {
    ".tex": "LaTeX sources: the manuscript may be canonical in Overleaf or a repo",
    ".ipynb": "notebooks: the code may be canonical in a repository",
    ".py": "code: it probably belongs in a repository, not here",
    ".R": "code: it probably belongs in a repository, not here",
}


def walk(root: Path):
    for p in root.rglob("*"):
        if set(p.relative_to(root).parts) & SKIP_DIRS:
            continue
        if p.name.startswith("."):
            continue
        yield p


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} GB"


def infer_kind(folder: Path, workspace: Path) -> str:
    """Guess the kind from the parent folder, using the workspace's kinds."""
    kinds_file = workspace / "resources" / "kinds.json"
    if not kinds_file.is_file():
        return ""
    try:
        kinds = json.loads(kinds_file.read_text())
    except (OSError, ValueError):
        return ""
    parent = folder.parent.name
    for kind, spec in kinds.items():
        if isinstance(spec, dict) and spec.get("folder") == parent:
            return kind
    return ""


def find_pointers(folder: Path, files: list) -> list:
    pointers = []

    gitconfig = folder / ".git" / "config"
    if gitconfig.is_file():
        try:
            urls = GIT_URL.findall(gitconfig.read_text(errors="replace"))
        except OSError:
            urls = []
        pointers.append(
            "git repository" + (f", remote: {urls[0]}" if urls else ", no remote")
        )

    suffixes = {f.suffix for f in files}
    for suffix, note in CANONICAL_HINTS.items():
        if suffix in suffixes:
            pointers.append(note)

    urls: list = []
    for f in files:
        if f.suffix.lower() not in TEXT_SUFFIXES or f.parent != folder:
            continue
        try:
            if f.stat().st_size > MAX_TEXT_BYTES:
                continue
            urls.extend(URL.findall(f.read_text(errors="replace")))
        except OSError:
            continue
    seen = []
    for u in urls:
        u = u.rstrip(".,;)")
        if u not in seen:
            seen.append(u)
    if seen:
        pointers.append("links found in top-level notes: " + ", ".join(seen[:5]))
    return pointers


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", help="the folder to inspect")
    p.add_argument("--root", default="", help="workspace root (default: parent of folder)")
    p.add_argument("--entries", type=int, default=20, help="top-level entries to list")
    args = p.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.is_dir():
        sys.exit(f"Not a directory: {folder}")
    workspace = Path(args.root).expanduser().resolve() if args.root else folder.parent

    entries = list(walk(folder))
    files = [p for p in entries if p.is_file()]
    if not files:
        print(f"{folder}: no material inside. Nothing to activate.")
        return 0

    present = [n for n in CONTRACT if (folder / n).is_file()]
    missing = [n for n in CONTRACT if n not in present]
    mtimes = [f.stat().st_mtime for f in files]
    now = time.time()
    depth = max(len(f.relative_to(folder).parts) for f in files)
    kind = infer_kind(folder, workspace)

    try:
        rel = folder.relative_to(workspace)
    except ValueError:
        rel = folder

    print(f"Folder: {rel}")
    print(
        "Contract: "
        + (", ".join(f"{n} present" for n in present) if present else "nothing yet")
        + (f"; missing {', '.join(missing)}" if missing else "")
    )
    if kind:
        print(f"Kind: probably '{kind}', from the parent folder and resources/kinds.json")

    total = sum(f.stat().st_size for f in files)
    print(f"\nMaterial: {len(files)} files, {human(total)}, {depth} levels deep")
    types = Counter(f.suffix.lower() or "(none)" for f in files)
    print("Types: " + ", ".join(f"{s} {n}" for s, n in types.most_common(8)))

    quiet = int((now - max(mtimes)) // 86400)
    print(
        f"Activity: oldest {time.strftime('%Y-%m-%d', time.localtime(min(mtimes)))}, "
        f"newest {time.strftime('%Y-%m-%d', time.localtime(max(mtimes)))} "
        f"(untouched for {quiet} days)"
    )
    recent = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)[:5]
    print(
        "Recent: "
        + ", ".join(
            f"{f.relative_to(folder)} ({time.strftime('%Y-%m-%d', time.localtime(f.stat().st_mtime))})"
            for f in recent
        )
    )

    top = sorted(
        p.name + ("/" if p.is_dir() else "")
        for p in folder.iterdir()
        if not p.name.startswith(".")
    )
    shown = top[: args.entries]
    print(f"\nTop level ({len(top)} entries): " + ", ".join(shown))
    if len(top) > len(shown):
        print(f"  ... and {len(top) - len(shown)} more")

    pointers = find_pointers(folder, files)
    if pointers:
        print("\nPointers:")
        for hint in pointers:
            print(f"  - {hint}")

    print("\nNot in this folder, and not inferable from it:")
    print("  - the next action")
    print("  - why past decisions were taken")
    print("  - whether this work is alive or merely quiet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
