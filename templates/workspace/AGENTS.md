# {Workspace name}

{One paragraph: what this workspace covers and what it does not. Name the
adjacent workspaces and where the boundary runs, since that is the question an
agent will get wrong.}

The files in this workspace are the source of truth. External tools (agents,
editors, scripts) are views or hands over these files, never a second copy.

Before working in a subfolder, read the `AGENTS.md`, `README.md` and
`STATUS.md` closest to the work. Local instructions complement these rules and
win where they are more specific.

## Structure

{One line per top-level folder: what goes in it and what its lifecycle is.}

- `{folder}/` — {what belongs here; when an entry arrives and when it leaves}
- `areas/` — standing responsibilities with no end date.
- `resources/` — templates and reusable material.
- `inbox/` — unclassified incoming material. Should trend to empty.
- `archive/` — finished work of any kind. Searchable, not curated.

## The file contract

Every unit under {list the folders where the contract applies} uses the same
three files:

- `README.md` — what it is: purpose, people, and where the canonical source
  lives if it is not here. Changes rarely.
- `STATUS.md` — the present: state, the single next action, dated pending
  items, blockers. OVERWRITTEN. This is what the overview board reads.
- `LOG.md` — the past: dated decisions and their reasoning. APPEND-ONLY. If a
  decision reverses an earlier one, say so in the entry.
- `AGENTS.md` — only when the unit has rules of its own.

The contract does not apply to `archive/`, `inbox/`, `resources/`, or working
subfolders inside a unit.

{Note any kind that extends the contract, e.g. an extra TIMELINE.md.}

## Rules

- Prefer editing existing files over creating new ones. Prefer plain Markdown.
- After substantial work on a unit, overwrite its `STATUS.md` and append to
  its `LOG.md` (skill `session-log`).
- When creating a unit, use the `new-unit` skill so it starts from the right
  template.
- Do not maintain a task list by hand. The board is generated from
  `STATUS.md` files.
- Use ISO dates (`YYYY-MM-DD`) everywhere.
- Mark unknowns as `TODO`. Never invent dates, names or commitments.
- {Storage rule, if this workspace is on cloud storage: no version control
  here, so copy before moving and archive instead of deleting.}
- {Where code lives, if any: repositories outside this tree, pointed at from
  the unit README.}

## Confidentiality

{Be specific. This is the section an agent most needs and most often lacks.}

- {What is confidential in this workspace and what it must never be mixed
  with.}
- {What must never leave for an external service without explicit
  authorization.}
- {What must never appear in summaries, boards or cross-workspace views.}

## Skills

{List every skill an agent needs in this workspace, wherever it is
installed. Skills that belong to this workspace alone live as real folders
under `.claude/skills/`. Claude Code discovers those on its own; other
agents do not, so this list is what lets any agent be told to read and
follow the named `SKILL.md`.}

- **{skill-name}** (`.claude/skills/{skill-name}/SKILL.md`, or "installed
  globally") — {one-line trigger: when this skill applies}

Cross-workspace skills stay in the agent's own skills directory; only
workspace-specific skills belong in the workspace.

## Done means

{What has to be true before a piece of work counts as finished: output in the
right place, source of truth identified, privacy constraints respected,
STATUS and LOG updated.}
