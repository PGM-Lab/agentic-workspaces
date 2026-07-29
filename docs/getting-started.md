# Getting started

Setting up the first workspace takes about an hour, and most of that hour is
you deciding what your units are. The mechanical part is done by an agent
using the kit's own skills, which is the point: a method for working with
agents should be installable by one.

Read [`the-method.md`](the-method.md) first. It is short, and both you and
the agent need it: one that has not read it will append to `STATUS.md` and
rewrite `LOG.md`, and the contract stops meaning anything. Then read
[`../examples/`](../examples/), because one filled-in workspace makes the
templates obvious in a way the templates themselves do not.

If you already have folders full of work, which is the normal case, read
[`adopting-existing-work.md`](adopting-existing-work.md) alongside this. The
setup below is the same; the hard part becomes deciding what your existing
folders are and in what order to activate them.

## Where things live

The clone of this repository is **not** where you work. It is the source of
the skills and the documentation. Your work lives in your own directories.

Keep the clone on local disk, for instance under `~/Documents`. Never inside
a synced folder such as Google Drive, Dropbox or OneDrive: the installation
uses symlinks and sync services do not carry them.

## 1. Install

Clone the repository, open your agent inside the clone, and say:

> Install these skills.

The agent finds `setup-workspace` (the clone ships the skills where both
Claude Code and Codex look) and runs it. If you would rather do it yourself:

```bash
python3 skills/setup-workspace/scripts/setup_workspace.py --install
```

One canonical copy goes to `~/.agents/skills/`, which Codex reads natively,
and is symlinked into `~/.claude/skills/`. One copy, both agents, and
`git pull` in the clone updates everything.

The install is additive. If you already have a skill with one of these names,
it is left alone and reported; nothing is overwritten.

Add `--copy` to install real directories instead of symlinks. Do that on
Windows, where symlinks need administrator rights; if you intend to delete the
clone; or if `~/.agents/skills` is itself a repository you share, since
symlinks into your own machine are broken pointers for everybody else. Copies
do not follow a `git pull`, so they are updated with `--update` instead.

**Postconditions:** `~/.agents/skills/` contains the kit's skills, and your
agent lists them. Ask it "what skills do you have?" to check.

*Using Claude Code and nothing else?* There is a plugin route instead, which
handles versioning for you:

```bash
/plugin marketplace add PGM-Lab/agentic-workspaces
```

It is Claude-only, and it puts the skills somewhere else, so the postcondition
above does not apply; ask the agent what skills it has. If you use Codex too,
prefer the canonical copy or you will maintain two divergent installations.

*Using an agent that is neither Claude Code nor Codex?* The skills are plain
`SKILL.md` folders following the open standard, so they work anywhere. Put
them where your agent looks, and list them in your workspace `AGENTS.md`
under `## Skills` with their paths, which any agent can be told to follow.

## 2. Create a workspace

Open your agent in the directory where the work should live and say:

> Create a workspace here for my teaching.

`setup-workspace` asks three questions and nothing more: what the workspace
is for, where it lives, and whether your work comes in **kinds** with
different lifecycles (papers, grants, reviews) or moves in **cycles** that
end together (semesters, terms). Then it creates the skeleton and drafts the
`AGENTS.md` for you to correct.

Correct it properly. `AGENTS.md` is the only file that genuinely needs
thought, and it is where an agent learns what it must never do. Be concrete:
"never submit a cluster job without asking me first" is a rule; "follow best
practices" is noise. Anything the agent could not fill stays as a visible
`{placeholder}` rather than being quietly dropped.

Ask it to add a short **Why this shape** section to the workspace `README.md`
while the reasons are fresh: why these folders, what is confidential, where
the canonical sources live. Three lines. It is the part nobody can
reconstruct a year later.

**Postconditions:**

- `AGENTS.md`, `CLAUDE.md` and `README.md` exist at the workspace root.
- `CLAUDE.md` contains only the `@AGENTS.md` import.
- `AGENTS.md` has no empty sections and no leftover placeholders you did not
  put there on purpose.
- `resources/kinds.json` names *your* kinds, not the generic ones.
- The audit runs clean:
  `python3 ~/.agents/skills/audit-workspace/scripts/audit.py --root .`

The kinds live in the workspace, at `resources/kinds.json`, never in the
installed skill. That is deliberate: the skill is shared by every workspace,
so editing it to suit one would break the others.

## 3. Create one unit and use it

Say:

> I'm starting a paper on compound storm surge.

`new-unit` seeds the folder with `README.md`, `STATUS.md` and `LOG.md` from
the right template. Fill in the three files with real content, once,
properly. Not placeholder text. This first unit is the model every later one
follows, and it is how you find out whether your `README.md` template asks
for the right things.

Then work in that folder for a week. At the end of each session say "close
the session" or invoke `session-log`, which overwrites `STATUS.md` and
appends a dated entry to `LOG.md`.

**Postcondition:** a unit whose `STATUS.md` tells the truth when you open it
cold a week later.

## 4. Check whether it is working

After a week, one question: does `STATUS.md` still tell the truth?

If yes, add a second workspace. `setup-workspace` will offer "same as
`<existing>` except X" rather than asking everything again.

If no, the cause is almost always that sessions are not being closed. Fix
that before adding anything. Put the rule explicitly in `AGENTS.md` so the
agent proposes it unprompted, or make a habit of ending with "close the
session". A second workspace built on a habit that has not formed just
doubles the number of files that lie to you.

## The rest of the day to day

- **What is pending?** `workspace-overview` generates the board from your
  `STATUS.md` files. Never keep a second list by hand.
- **Is anything half-finished?** `audit-workspace` checks units against the
  contract and surveys what is not activated yet.
- **Updating the kit:** `git pull` in the clone. With symlinks there is
  nothing else to do. With `--copy`, re-run the installer as
  `--install --copy --update`: it replaces the copies it made itself and still
  leaves alone any skill of that name that you wrote.

## Common mistakes

**Working inside the clone.** It is the source of the kit, not a workspace.

**Converting everything in one weekend.** The most reliable way to end up
with forty folders of empty templates. The template is not the value; the
filled-in content is, and that part cannot be batched.

**Applying the full contract to tiny units.** Something that lives two weeks
and has one fact worth recording deserves one file.

**Putting status in the README.** It will go stale, and unlike `STATUS.md`
nobody will think to check it.

**Keeping a separate to-do list.** It becomes a second source of truth and
starts to diverge. Generate the view instead.

**Accepting the drafted `AGENTS.md` without reading it.** It is the one file
the agent cannot get right on its own, because most of what belongs in it is
in your head.
