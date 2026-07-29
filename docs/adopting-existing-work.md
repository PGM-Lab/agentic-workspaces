# Adopting the method over work that already exists

[`getting-started.md`](getting-started.md) assumes an empty folder. Almost
nobody has one. You have years of material: folders inside folders, a
downloads directory that became permanent, three copies of the same proposal,
work from 2019 that may or may not be finished.

This document is about that case. It is the harder one, and it is the one the
method was actually built in.

## The one distinction that matters

**Moved is not the same as activated.**

- *Moved*: the material is physically in the right workspace, in a folder
  with a sensible name.
- *Activated*: that folder has a `README.md`, a `STATUS.md` and a `LOG.md`
  that say something true.

Moving is fast, mechanical, and can be done in an afternoon for a whole
career's worth of folders. Activating is slow, requires judgement, and cannot
be batched, because writing a real `STATUS.md` means deciding what the work
actually is and what state it is actually in.

Conflating the two is the mistake that ruins adoptions. People move
everything, then generate templates for everything, and end up with two
hundred folders containing `{one line: where this is right now}`. That is
worse than where they started, because now the emptiness is disguised as
structure.

Expect a long stretch where most units are moved and few are activated. That
is the normal state, not a failure. What matters is that you can tell which
is which.

## How this runs

Same as the rest of the kit: you ask, a skill answers, and you check the
result. The steps below say what to ask for, which skill responds, and what
should exist afterwards.

One rule throughout: **the agent never moves your files.** Moving is your
decision, taken folder by folder. The agent surveys, proposes and drafts.

## Step 1: survey before you touch anything

Say:

> Audit this workspace and tell me what is not activated.

That is `audit-workspace`. To run it yourself:

```bash
python3 ~/.agents/skills/audit-workspace/scripts/audit.py --root <workspace>
```

It sorts folders into three groups: units that already have a `STATUS.md`,
folders with a `README.md` but nothing else, and folders that hold material
with no contract file at all. In an existing tree the third group is nearly
everything.

Treat the output as a first draft of an inventory, not as a verdict. Telling a
unit from a container from a folder of loose notes cannot be done from
filenames, and the script gets some of both wrong. Its value is that it gives
you a list to argue with instead of a blank page.

**Postcondition:** a list you have read, not a list you have acted on.

## Step 2: decide what is not a unit

This is the highest-value hour in the whole adoption, and it is subtraction
rather than addition. Most of what the survey lists should never get a
contract.

Rule out, deliberately:

- **The archive.** Finished and dead work does not get retro-fitted. It has
  to stay searchable, not become curated. If something is reactivated later,
  it earns a contract then.
- **Container folders.** The folder that holds your projects is not itself a
  project. It gets one line in the workspace `AGENTS.md`, not a contract.
- **Working subfolders.** `meetings/`, `notes/`, `figures/`, `drafts/`. They
  belong to a unit; they are not units.
- **Reference collections and boilerplate.** Shared examples, templates, past
  proposals kept for reuse. They have no state and no next action, so two of
  the three files would be empty by construction.
- **Generated material.** Anything a pipeline produces and a human does not
  edit.
- **Support directories.** Admin, salary, an inbox that has not been emptied
  in a year.

A useful test: if you cannot write a `STATUS.md` for it with a real next
action, it is not a unit. Notes and reference material fail that test, which
is the point.

Work through the survey with the agent, saying which of its lines are not
units and why. That conversation is the valuable part, and it is yours: an
agent cannot tell a dead project from a quiet one.

**Postcondition:** every line of the survey is classified, including the ones
you ruled out. Ruled out on purpose is a decision; unexamined is not.

## Step 3: classify the rest, including "I do not know"

For what survives, you need four states, not two:

- **Complete**: has the three files.
- **Partial**: has some of them.
- **Pending**: is a real unit, has nothing yet.
- **To classify**: you genuinely cannot tell whether this is live work or
  history until you look properly.

That fourth state is the one people skip, and skipping it is expensive. Old
folders are ambiguous by nature: work that stopped without ceremony looks
identical to work that is merely quiet. Deciding "live or historical" is a
different question from "activated or not", and it has to come first, because
activating dead work is pure waste and archiving live work is worse.

Write the classification down in one place, as its own document. The audit
computes what it can see; the inventory records what you decided. When they
disagree, the inventory wins, and the difference tells you what changed since
you last looked.

Keep the census in exactly one file. Every other document should link to it
rather than repeat its numbers. Totals that appear in three places will
disagree within a month; that is not a hypothesis.

## Step 4: activate in the right order

Never in bulk. Roughly cheapest-first, then by what you are actually touching:

1. **Units that are nearly there.** Something with a good `README.md` that
   only needs a `STATUS.md` and a `LOG.md` is twenty minutes and gives you a
   working example to model the rest on.
2. **Whatever you are working on this week.** Activating a unit you are about
   to open anyway costs almost nothing, because the context is already in your
   head. This is the sustainable path: adoption as a side effect of work.
3. **Standing areas.** They are few, they are stable, and they are what an
   agent most often needs context about.
4. **The long tail of pending units**, in small batches, when you have a
   reason to touch them.
5. **The "to classify" pile**, last, and as a decision session rather than a
   documentation session.

Anything you never touch can stay unactivated indefinitely. A folder nobody
opens does not need a status.

## What you can and cannot recover

When activating an existing folder, the three files are not equally
recoverable from the material. This asymmetry decides how much you can
delegate to an agent.

**`README.md` is mostly recoverable.** What the work is, who is involved,
where the canonical source lives: an agent reading the folder can draft this
well, and you correct it. This is the part worth delegating.

**`STATUS.md` is half recoverable.** Deadlines can be read out of the files,
and "last touched" out of the timestamps. But the *next action* almost never
exists in the folder. It lives in your head, or in an email thread, or in a
conversation from three weeks ago. An agent that invents one produces a
confident, plausible, wrong status, and a wrong status is worse than a missing
one, because both you and the agent will believe it.

So: let an agent draft the state, and write the next action yourself. If you
cannot state one, that is information. Say so explicitly, or consider whether
the unit is actually dormant.

In practice, for each unit: ask the agent to read the folder and draft the
`README.md` and the state line of `STATUS.md`, then write the next action
yourself and correct what it got wrong. There is no skill for this yet, so
say what you want explicitly. Never let it invent the next action, and never
let it batch several units at once.

**`LOG.md` is not recoverable at all.** Past decisions and their reasoning are
not in the folder. They are in people's heads and in mail archives. Do not
reconstruct them, and above all do not let them be inferred. For a unit
activated from existing material, the honest log has one entry:

```markdown
## 2026-07-28
Activated from existing material. Everything before this date is in the files
themselves and is not reconstructed here.
```

That is not a placeholder. It is the truthful statement that the record starts
now, and it is worth more than an invented history.

## Safety while you do this

Adoption is the phase where the most files move, and usually the storage has
no version control.

- Copy before moving, and delete only after verifying the copy.
- Archive instead of deleting.
- Activation should only ever *add* files. If a session proposes moving,
  renaming or reorganising as part of activating, that is a separate decision
  taken separately.
- Do not let an agent perform a bulk operation without showing you the plan
  first.
- When a workspace holds confidential material, remember that a survey walks
  the whole tree. Reports should name folders, not enumerate what is inside
  them.

## When you are done, you will not be done

A realistic outcome after the first serious pass is that roughly half the
units have a contract, the archive is untouched by design, and a pile of old
folders is still marked "to classify". That is a healthy state. The system is
useful from the first activated unit; it does not require completeness to pay
off.

What would make it useless is pretending otherwise. Make sure your inventory
states the real numbers, and that anything generating a global view says
plainly which parts of the tree contributed nothing. Silence should never read
as "nothing pending".
