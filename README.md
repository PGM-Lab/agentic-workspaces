# Agentic Workspaces

A way to organize your working life in plain text so that an AI agent can open
a session in any folder, understand where it is and get to work.

There is no app to adopt and no database to migrate into. Markdown files in
folders, plus two small conventions that agents already understand:
`AGENTS.md` for instructions and `SKILL.md` for repeatable procedures. It works with Claude Code, Codex, Cursor
and anything else that reads those standards.

This repository holds the method, the templates and the skills that operate
it. It is meant to be copied and adapted, not installed.

## The shape of it

Your work is split into **workspaces**, one per role or area of
responsibility. Inside a workspace, every **unit** of work (a project, a
course, a client, a person you supervise) is a folder with three files:

| File | Question it answers | Update rule |
|---|---|---|
| `README.md` | What is this and who is involved? | Rarely. Stable facts only. |
| `STATUS.md` | Where is it right now, and what is the next action? | Overwritten. |
| `LOG.md` | What was decided, when, and why? | Append-only. |

That is the whole contract. An agent reads those three files and knows as much
as you do about the unit.

Two more files make it work for agents:

- `AGENTS.md` at the workspace root holds the instructions: how the workspace
  is organized, what the rules are, what must never leave the folder.
- `CLAUDE.md` next to it does nothing but import that file (`@AGENTS.md`),
  because Claude Code does not read `AGENTS.md` directly. Every other agent
  reads the canonical file.

Repeatable procedures live as skills, so "create a new project" or "close the
session properly" is one instruction instead of a paragraph you retype.

## Why bother

Agents remember nothing between sessions. Left alone they re-derive your
context every time, badly. The fix is not a bigger prompt, it is writing the
context down where the agent can find it, in the folder the work already lives
in.

The side effect may matter even more: the same files that make an agent
useful make the work legible to you six months later, and to a colleague who
takes over.

The reasoning behind each design choice, with references to the standards and
practices it borrows from, is in [`docs/the-method.md`](docs/the-method.md).

## Getting started

Clone this repository somewhere on local disk, open your agent inside the
clone, and say:

> Install these skills and set me up a workspace.

That runs the `setup-workspace` skill: it installs the skills into your
agent, asks three questions, and drafts the workspace for you to correct.

Read in this order: [`docs/the-method.md`](docs/the-method.md) for why the
contract is shaped the way it is, ten minutes, and an agent that has not read
it will misuse the contract; [`examples/`](examples/) for one filled-in
workspace; then [`docs/getting-started.md`](docs/getting-started.md) to set up
and check it worked. If you already have folders full of work, which is the
normal case, [`docs/adopting-existing-work.md`](docs/adopting-existing-work.md)
covers what setup does not: what should never become a unit, in what order to
activate the rest, and what cannot be recovered from what is already there.

Adopting this in one weekend across everything you do is the most common way
to end up with forty folders full of unfilled templates. Start with one area
of your work and let it prove itself.

**Where things live.** The clone is not where you work: it is the source of
the skills and the documentation. Keep it on local disk, never inside a synced
folder like Google Drive or Dropbox, because the install symlinks into the
clone and sync services do not carry symlinks.
[`docs/getting-started.md`](docs/getting-started.md#1-install) covers the
`--copy` install for when that is not possible.

## What is in here

```
docs/          The method and the rationale, a setup guide, and how to
               adopt it over work that already exists
templates/     Every file in the contract, ready to copy
skills/        The six skills that operate the structure
examples/      A small worked workspace, filled in, to read before you start
tests/         A smoke test that walks the setup guide end to end
```

## Status and feedback

This is a working system, not a finished product. It is in daily use across
eight workspaces and it is still changing. Known weak points are listed at the
end of [`docs/the-method.md`](docs/the-method.md), and the honest one is that
the contract only holds if you close sessions properly.

If you try it and something does not fit your work, that is useful to hear.
Open an issue. [`CONTRIBUTING.md`](CONTRIBUTING.md) says what kind of feedback
helps most.

## License

MIT. See [`LICENSE`](LICENSE).
