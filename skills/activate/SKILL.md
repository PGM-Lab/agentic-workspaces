---
name: activate
description: Write the README/STATUS/LOG contract for one folder that already holds work, drafting from the material that is there. Use when the user points at an existing folder and says "activate this", "activa esta carpeta", "give this the contract", "document this project", "esta carpeta ya existe, méteme los ficheros", or when adopting the method over folders that were moved into a workspace but never documented.
---

# Activate an existing folder

`new-unit` creates an empty folder from a template. This does the other half:
a folder that already holds years of material, and needs the contract written
around it.

It is the repetitive part of adoption, and the part where an agent is most
likely to do harm, because a confidently wrong `STATUS.md` is worse than no
`STATUS.md`. Both you and the user will believe it.

## Hard rules

These are not style preferences. Breaking any of them damages the workspace.

1. **Additive only.** Create `README.md`, `STATUS.md` and `LOG.md`. Never
   move, rename, delete or reorganise anything. If the folder is in the wrong
   place or should be split, say so and stop; that is a separate decision the
   user takes, on storage that usually has no undo.
2. **One folder per invocation.** If asked to activate several, do the first,
   show it, and ask whether to continue. Batch activation produces batch
   filler, which is the failure mode the whole method warns about.
3. **Never invent the next action.** It is not in the folder. Ask.
4. **Never reconstruct history.** See the log section below.
5. **Leave placeholders, never omit.** Anything you could not determine stays
   as a visible `{...}` naming what is missing. An omitted line looks
   finished and passes every check.
6. **Do not bulk-read confidential material.** The inspection script gives
   you shape, dates and pointers without opening files. Open a specific
   document only when you need it and the user is fine with it.

## Workflow

### 1. Check it should be a unit at all

Before writing anything, confirm with the user that this folder is a unit and
not something that should never get the contract: an archive of finished
work, a container holding other units, a working subfolder, a reference
collection, or an inbox. See
[`../../docs/adopting-existing-work.md`](../../docs/adopting-existing-work.md)
for the full list and the reasoning.

The test that settles most cases: if you cannot end up with a real next
action, it is not a unit.

If the work looks finished, propose archiving instead of activating, and let
the user move it.

### 2. Inspect

```sh
python3 <path-to-skill>/scripts/inspect_folder.py <folder> --root <workspace>
```

Read-only. It reports what the contract already has, the kind inferred from
the parent folder, how much material there is and of what type, the date
range and how long it has been quiet, the top-level entries, and any pointers
to a canonical source elsewhere (a git remote, LaTeX sources, links in
top-level notes).

Read its closing lines. They name what the folder cannot tell you.

### 3. Draft the README

This is the part worth delegating: it is mostly recoverable from the
material. Write what the work is, who is involved if the material says so,
and **where the canonical source lives** if the pointers suggest it is
elsewhere. That last one does real work: it stops anyone, including you,
treating a stale copy here as authoritative.

Use the workspace's own template for the kind
(`resources/templates/`) so the fields match its other units.

Mark what you inferred rather than read. "Appears to be a proposal to the
2026 call, from the filenames" is honest; stating it flatly is not.

### 4. Draft the state, ask for the next action

Write the state line of `STATUS.md` from the evidence: what stage the work
seems to be at, when it was last touched, any deadline you can see in the
material.

Then **stop and ask the user for the next action.** Do not guess it, do not
derive it from the goal, and do not write "continue with the paper", which
is a restatement, not an action.

If the user does not know, that is information. Either write it down as
`{Next step: undecided as of <date>}`, or say plainly that the unit may be
dormant and ask whether it belongs in the archive. A dormant unit honestly
marked is fine; a dormant unit with an invented next step is a lie the board
will repeat every week.

### 5. Write the honest log

Past decisions and their reasoning are not in the folder. They are in
people's heads and in mail archives. Do not reconstruct them, and do not let
them be inferred from filenames.

The log for a folder activated from existing material has exactly one entry:

```markdown
## 2026-07-29
Activated from existing material. Everything before this date is in the files
themselves and is not reconstructed here.
```

That is not a placeholder to be improved later. It is the truthful statement
that the record starts now, and it is worth more than an invented history. If
the user volunteers a decision worth keeping, add it as a second entry in
their words, dated when it happened.

### 6. Verify and stop

Run the audit and show the result:

```sh
python3 <canonical-skills>/audit-workspace/scripts/audit.py --root <workspace>
```

The unit should have moved out of "not started". Report what is still
unfilled, then stop. Do not continue to the next folder unless asked.

## What good looks like

A `README.md` that says what the thing is and points at the real source. A
`STATUS.md` whose next action a human wrote. A `LOG.md` with one honest
entry. Nothing moved, nothing renamed, nothing invented.

Half a workspace activated properly is worth more than all of it activated
with plausible fiction.
