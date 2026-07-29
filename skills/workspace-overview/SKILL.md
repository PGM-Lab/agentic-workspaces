---
name: workspace-overview
description: Generate a single overview board of everything pending across all workspaces by scanning their STATUS.md files: upcoming deadlines, blocked items, active work, stale entries. Works from any session regardless of the current directory. Use when the user asks "what's pending", "qué tengo pendiente", "overview", "dashboard", "tablero", "what deadlines are coming", "estado de todo", "what's on this week", or on a scheduled weekly run.
---

# Workspace Overview

Compute the board from the source of truth, which is the `STATUS.md` of every
unit. Never maintain a separate list: the board is a derived view, regenerated
on every run. A hand-maintained global list becomes a second source of truth
and starts to diverge within a fortnight.

**Read-only.** Never write into a workspace from this skill. The board goes to
the chat; write it to a file only if the user asks.

## Before first use

Configure the roots to scan. Create
`~/.config/agentic-workspaces/roots.txt` with one absolute workspace path per
line, or pass the paths as arguments, or point `AGENTIC_WORKSPACES_ROOTS` at a
file elsewhere. `setup-workspace` writes that file for you as it seeds each
workspace. Without any of them, the script has nothing to scan and says so.

The file is machine configuration: absolute paths that are nobody else's. It
lives outside this skill's directory on purpose, since the installer owns that
directory and replaces it on update. A `roots.txt` left next to the script
from an older install is still read, but move it.

## Workflow

1. Run `scripts/scan.sh --roots` and read the `AGENTS.md` at the top of each
   root it prints, or `CLAUDE.md` where that is what holds the rules. This is
   the one skill that runs outside the workspaces it reports on, so nothing
   loads those files for you. They are where a workspace states two things this
   skill cannot know: which of its units do not carry their own `STATUS.md`,
   and what it allows onto a board that leaves its tree. Honour what you read.
   The rules below are the floor, not the ceiling.

2. Run `scripts/scan.sh`. It prints every relevant `STATUS.md` as
   `<days-since-modified>` and `<path>`, newest first, already excluding
   archives, inboxes, templates and generated material. If the script cannot
   run, fall back to finding `STATUS.md` files under each root with the same
   exclusions.

3. Read each file and extract: the state line, the next step, pending items
   with deadlines, blocked items, and the last-updated date. Use the scan's
   file age as a fallback when the header date is missing.

4. Apply the aggregation exceptions from step 1. Short lived units sometimes
   carry a single file instead of the contract, aggregated at the workspace
   root: read the aggregate and do not walk the subfolders. If a root says
   nothing, treat one `STATUS.md` per unit as the rule.

5. Produce the board in this order:

   - **Deadlines in the next 30 days**, sorted by date, each with its unit and
     workspace.
   - **Blocked or waiting**: what, on whom, since when.
   - **Active work**: one line each (state plus next step), grouped by
     workspace.
   - **Stale**: units whose `STATUS.md` has not changed in over 30 days. Flag
     them, do not nag.
   - **Coverage**: one closing line naming any workspace that contributed no
     `STATUS.md` at all, so that silence is visible rather than mistaken for
     "nothing pending". This matters most during adoption, when many units are
     migrated but not yet activated.

6. Keep it tight. This is a scan, not a report.

## Confidentiality

The board aggregates across workspaces, which means it crosses the boundaries
those workspaces exist to enforce. Apply the strictest rule that applies to
each source, and apply whatever its own `AGENTS.md` adds on top of these.

- Refer to confidential units by project, course or initiative, never by
  person's name.
- Where a unit is a person, carry only state, next step and dates. Never
  contract, health, visa, grade or other personal data.
- Quote nothing verbatim from a confidential tree. One-line summaries only.
- For workspaces that front a private archive (mail, documents), read only the
  aggregate `STATUS.md`. Never search the underlying store while building the
  board, and never include senders, subjects, identifiers or filenames.
- Never include amounts, account numbers, invoice details or accounting codes.
