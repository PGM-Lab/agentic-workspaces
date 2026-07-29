# Coastal Systems Research — workspace instructions

This workspace holds research work: papers in progress, funded projects,
consortium responsibilities and collaborator notes. Teaching lives in a
separate workspace and its contents must never be copied here. Fieldwork data
is not here either; it lives on the institutional store, and unit READMEs
point at it.

The files in this workspace are the source of truth. Agents, editors and
scripts are views or hands over these files, never a second copy.

Before working in a subfolder, read the `AGENTS.md`, `README.md` and
`STATUS.md` closest to the work. Local instructions complement these rules and
win where they are more specific.

## Structure

- `projects/` — one folder per piece of work with an end: a paper, a report, a
  deliverable. Arrives when the work starts for real, leaves for `archive/`
  when it is published or abandoned.
- `areas/` — standing responsibilities with no end date: consortium roles,
  editorial work, committees.
- `people/` — one note per collaborator. Safe to share: no personal
  identifiers, no confidential content.
- `resources/` — templates, LaTeX classes, reusable material.
- `inbox/` — unclassified incoming material. Should trend to empty.
- `archive/` — finished or dead work of any kind. Searchable, not curated.

A new recurring kind of work earns its own top-level folder the day it happens
for real. Do not pre-create empty ones.

## The file contract

Every unit under `projects/` and `areas/` uses the same three files:

- `README.md` — what it is: purpose, people, and where the canonical source
  lives if it is not here. Changes rarely.
- `STATUS.md` — the present: state, the single next action, dated pending
  items, blockers. OVERWRITTEN. This is what the overview board reads.
- `LOG.md` — the past: dated decisions and their reasoning. APPEND-ONLY. If a
  decision reverses an earlier one, say so in the entry.
- `AGENTS.md` — only when the unit has rules of its own.

`people/` is the exception: one note per person, no contract, because there is
no state to track.

The contract does not apply to `archive/`, `inbox/`, `resources/`, or working
subfolders inside a unit.

## Rules

- Prefer editing existing files over creating new ones. Prefer plain Markdown.
- After substantial work on a unit, overwrite its `STATUS.md` and append to
  its `LOG.md` (skill `session-log`).
- When creating a unit, use the `new-unit` skill so it starts from the right
  template.
- Do not maintain a task list by hand. The board is generated from
  `STATUS.md` files.
- Use ISO dates (`YYYY-MM-DD`) everywhere.
- Mark unknowns as `TODO`. Never invent dates, names, figures or commitments.
- Manuscripts and code live in Overleaf and in Git repositories, not here.
  When a `README.md` points elsewhere, nothing in this folder is canonical.
- This tree is on cloud storage, so there is no version control and no undo.
  Copy before moving, archive instead of deleting, and confirm before any bulk
  operation.
- Never submit a compute job on the shared cluster without explicit
  confirmation.

## Confidentiality

- Manuscripts under review are confidential and never leave this tree. Do not
  quote from them in summaries or boards.
- Unpublished data from consortium partners is covered by the consortium
  agreement. It may not be sent to any external service, including an AI
  provider, without checking the agreement first.
- Collaborator notes in `people/` must stay safe to share: no personal
  identifiers, no health data, no salary or contract terms, no private
  addresses.
- Reviews written for journals are confidential to the journal. Keep them in
  the relevant unit and never in a board or summary.

## Board

The overview board runs outside this workspace, so what it needs to know about
it has to be written here.

- Group entries by kind (projects, areas, people) rather than as one flat
  list. Sorted only by date, the standing areas bury the deadlines.
- On a board that leaves this tree, name a project and its state, never a
  manuscript title under review and never a line quoted from a review.
- A `people/` note may appear by the collaborator's name, with state and dates
  only.

## Skills

The structural skills this workspace relies on (`new-unit`, `session-log`)
are installed globally, in the agent's own skills directory, from the kit
this workspace was created with.

A workspace that carries skills of its own keeps them as real folders under
`.claude/skills/` and lists each one here with its path and a one-line
trigger. Claude Code discovers those on its own; other agents do not, so the
list is what lets any agent be told to read and follow the named `SKILL.md`.
This workspace has none yet.

## Done means

The output is in the right place, the source of truth is identified, the
confidentiality rules above have been respected, and the unit's `STATUS.md`
and `LOG.md` reflect what happened. Say briefly what changed and what still
needs a decision.
