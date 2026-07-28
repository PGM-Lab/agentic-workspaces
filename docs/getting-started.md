# Getting started

Setting up the first workspace takes about an hour. Most of that hour is
deciding what your units are, not copying files.

Before you start, read [`../examples/`](../examples/). Seeing one filled-in
workspace makes the rest of this obvious.

## 1. Pick one area

One. Not your whole working life.

Choose something you are actively working on, with a handful of live projects.
Resist starting with the biggest or messiest area: you want a first workspace
that proves the method to you, and the messy one will teach you the wrong
lesson about whether it works.

Decide where it goes. Cloud storage is fine and is what most people will use,
with the constraints in [`the-method.md`](the-method.md#practical-constraints).
Code repositories stay outside it.

## 2. Create the workspace root

Copy `templates/workspace/` into your new folder. You get three files:

- `AGENTS.md` — fill this in. It is the only file that genuinely needs
  thought.
- `CLAUDE.md` — leave it alone. One import line.
- `README.md` — a human-facing map of the workspace.

Filling in `AGENTS.md` means answering four questions. What is this workspace
for. What are the top-level folders and what goes in each. What are the rules
an agent must follow. What is confidential and must not leave.

Be concrete and be short. "Never submit a cluster job without asking me first"
is a useful rule. "Follow best practices" is not a rule.

## 3. Decide your top-level folders

This is the design decision that matters, and there are two common shapes.

**By kind of work**, when different kinds have different lifecycles. A
research workspace might use `papers/`, `grants/`, `funding/`, `reviews/`,
each with its own natural beginning and end.

**By cycle**, when the work is seasonal and everything moves together. A
teaching workspace might use `semesters/2026-autumn/<course>/`, because the
whole semester is archived at once.

Whichever you choose, add these:

- `areas/` for standing responsibilities with no end date.
- `resources/` for templates and reusable material.
- `archive/` for finished work. Searchable, not curated. Nothing here needs
  the contract applied retroactively.
- `inbox/` only if you actually have unclassified material arriving. It should
  trend toward empty; if it becomes permanent storage, drop it.

Do not pre-create empty folders for work you might do one day. A new kind of
work earns a folder the day it happens for real.

## 4. Install the skills

Copy the contents of `skills/` into your agent's skills directory:

```bash
cp -r skills/* ~/.claude/skills/
```

For Codex the directory is `~/.codex/skills/`. If you use both agents, keep
one canonical copy somewhere and symlink it into each, so you are not
maintaining two versions. Note that symlinks do not survive cloud sync, so the
canonical copy belongs on local disk.

Then open `skills/new-unit/SKILL.md` and edit the kinds list to match the
folders you chose in step 3. It ships with generic ones (`project`, `area`,
`person`) and it is meant to be edited.

Finally, list your skills in the workspace `AGENTS.md`, under `## Skills`,
each with its path and a one-line trigger. Claude Code discovers skills on its
own; other agents do not, and this section is what lets you say "read and
follow that file" to any agent.

## 5. Create one unit and use it

Ask your agent to create a unit for something real you are working on, or run
the script directly:

```bash
python3 ~/.claude/skills/new-unit/scripts/new_unit.py "Name of the thing" --type project --root .
```

Then fill in the three files by hand, once, properly. Not with placeholder
text. This first unit is the example every later one gets modelled on, and it
is also how you find out whether your `README.md` template is asking for the
right things.

Work in that folder for a week. At the end of each session, tell the agent to
close the session, or invoke `session-log` by name.

## 6. Check whether it is working

After a week, one question: when you open that folder cold, does `STATUS.md`
tell you the truth?

If yes, add a second workspace.

If no, the problem is almost always that sessions are not being closed. Before
adding anything, fix that. Options that work: put the rule explicitly in
`AGENTS.md` so the agent proposes it unprompted, or make a habit of ending
with "cierra la sesión" or "close the session". A second workspace built on a
habit that has not formed just doubles the number of files that lie to you.

## Common mistakes

**Converting everything in one weekend.** The most reliable way to end up with
forty folders of empty templates. The template is not the value; the filled-in
content is, and that part cannot be batched.

**Applying the full contract to tiny units.** Something that lives two weeks
and has one fact worth recording deserves one file. Keep the contract for
units with enough state to justify it.

**Putting status in the README.** It will go stale, and unlike `STATUS.md`
nobody will think to check it. If it changes, it belongs in `STATUS.md`.

**Keeping a separate to-do list.** Once a global list exists as its own
document it becomes a second source of truth and starts to diverge. Generate
the view instead.

**Writing rules nobody follows.** An `AGENTS.md` full of aspirational process
trains you to ignore it. Write down the rules that are real, including the
unglamorous ones.
