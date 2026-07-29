---
name: new-unit
description: Create a new unit of work in a workspace from the standard templates (a project, a standing area, or a person note) so it starts with the README/STATUS/LOG contract already in place. Use whenever the user starts something that has no folder yet: "empiezo un proyecto", "I'm starting X", "we won the contract", "I'm taking on Y", "add a note about Z", or when discussing work that turns out to have nowhere to live.
---

# New Unit

Seed a new unit so everything in the workspace has the same shape. The value
is not saving keystrokes, it is that units created this way never end up
missing a `LOG.md`.

## The kinds of unit a workspace has

Kinds are **per workspace**, not per machine, so they live in the workspace
itself at `resources/kinds.json`. Never edit the script to change them: the
skill is installed once and shared by every workspace, so editing it would
break the workspaces you set up earlier.

To see what a workspace has:

```sh
python3 <path-to-skill>/scripts/new_unit.py --list-kinds --root <workspace>
```

Without a `kinds.json`, three generic kinds are used (`project`, `area`,
`person`), which is what lets the skill work in a fresh workspace. A real
workspace names its own. The format, one entry per kind:

```json
{
  "paper":  { "folder": "papers",  "readme": "paper_README.md" },
  "grant":  { "folder": "grants",  "readme": "grant_README.md" },
  "student": {
    "folder": "students",
    "readme": "student_README.md",
    "subfolders": ["admin", "meetings"],
    "extra": { "TIMELINE.md": "student_TIMELINE.md" }
  },
  "person": { "folder": "people", "readme": "person_README.md", "note": true }
}
```

`folder` and `readme` are required. `note: true` marks a kind that is a single
file rather than a folder with the contract. `subfolders` defaults to
`["notes"]`. `extra` adds contract files beyond the three, for kinds that need
them. Add a matching README variant to the workspace templates for each kind
you add.

A kind whose work nests inside another unit puts `{parent}` in its folder, and
each unit says which parent it belongs to:

```json
{
  "semester": { "folder": "semesters", "readme": "semester_README.md" },
  "course":   { "folder": "semesters/{parent}", "readme": "course_README.md" }
}
```

```sh
python3 <path-to-skill>/scripts/new_unit.py "Machine Intelligence" \
  --type course --parent 2026-Autumn --root .
```

The parent has to exist already. The script will not create it, because a
mistyped parent would appear as a new empty folder rather than an error.

A kind named with an identifier rather than a title takes `"literal": true`,
and its name becomes the folder name untouched. Use it where slugifying would
damage a name that is already canonical, like `2026-Autumn` or a course code.

Templates come from the workspace's `resources/templates/` when it exists.
When it does not, the script falls back to the copy bundled with this skill
(`templates/` next to it). To customize, copy the bundle to
`<workspace>/resources/templates/` and edit there; the workspace copy then
takes precedence.

## Workflow

1. **Decide the kind.** If it is ambiguous, ask one short question rather than
   guessing. The distinction that matters most: something with a completion
   state is a project, something without one is an area.

2. **Run the helper** from the workspace root:

```sh
python3 <path-to-skill>/scripts/new_unit.py "Name of the thing" --type project --root .
```

   If the kind does not exist, the script says which ones this workspace has.

   It creates the folder, seeds `README.md`, `STATUS.md` and `LOG.md` from the
   templates, and substitutes the name and today's date.

3. **Fill in the placeholders** with real content from the conversation. Do
   not leave `{curly braces}` behind: a template satisfied without being
   filled in is worse than an absent file, because it looks answered. When no
   `--summary` is given, the script leaves `{Summary}` in place on purpose,
   so the audit keeps flagging the unit until someone writes the real thing.

4. **Delete lines that do not apply** rather than leaving them empty. An empty
   field reads as missing information; a deleted one reads as not applicable.

5. **Keep the unit-level `AGENTS.md` only if the unit has rules of its own.**
   Otherwise delete it. Repeating workspace rules creates two copies that will
   disagree.

6. **Report the created path** and anything still needing input from the user.

## Lifecycle

Units move. Handle the transitions explicitly rather than leaving two copies:

- A unit that gets promoted (an application that is funded, a prospect that
  becomes a client) becomes a new unit of the new kind. The old folder moves
  to `archive/` and the new README links back to it.
- Finished or dead work of any kind moves to `archive/`. It stays searchable
  and is not curated retroactively.
- On storage without version control, copy first, verify, then remove. There
  is no undo.
