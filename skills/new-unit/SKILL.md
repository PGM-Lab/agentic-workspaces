---
name: new-unit
description: Create a new unit of work in a workspace from the standard templates (a project, a standing area, or a person note) so it starts with the README/STATUS/LOG contract already in place. Use whenever the user starts something that has no folder yet: "empiezo un proyecto", "I'm starting X", "we won the contract", "I'm taking on Y", "add a note about Z", or when discussing work that turns out to have nowhere to live.
---

# New Unit

Seed a new unit so everything in the workspace has the same shape. The value
is not saving keystrokes, it is that units created this way never end up
missing a `LOG.md`.

## Before first use

**Edit the `KINDS` table in `scripts/new_unit.py`** to match your workspace's
top-level folders. It ships with three generic kinds:

| Kind | Goes to | README template |
|---|---|---|
| `project` | `projects/` | `project_README.md` |
| `area` | `areas/` | `area_README.md` |
| `person` | `people/` | `person_README.md` (single file, no contract) |

A research workspace would replace these with `paper`, `grant`, `application`,
`review`, `student`. A consultancy might use `client`, `engagement`,
`proposal`. Add a matching README variant to the templates for each kind you
add.

Templates come from the workspace's `resources/templates/` when it exists.
When it does not, the script falls back to the copy bundled with this skill
(`templates/` next to it), so the skill works in a fresh workspace with no
setup. To customize, copy the bundle to `<workspace>/resources/templates/`
and edit there; the workspace copy then takes precedence.

## Workflow

1. **Decide the kind.** If it is ambiguous, ask one short question rather than
   guessing. The distinction that matters most: something with a completion
   state is a project, something without one is an area.

2. **Run the helper** from the workspace root:

```sh
python3 <path-to-skill>/scripts/new_unit.py "Name of the thing" --type project --root .
```

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
