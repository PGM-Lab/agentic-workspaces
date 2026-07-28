# agentic-workspaces — agent instructions

This repository holds the generic method: documentation, templates and skills
for organizing work as agent-readable plain text. It is a source to be copied,
not a workspace itself.

## What lives where

- `docs/` — the method and its rationale (`the-method.md`), the setup guide
  (`getting-started.md`), and how to adopt it over folders that already exist
  (`adopting-existing-work.md`).
- `templates/` — the file contract, ready to copy. `workspace/` for the root
  of a new workspace, `unit/` for a unit of work, `variants/` for
  kind-specific README shapes.
- `skills/` — the four structural skills, in the portable `SKILL.md` format.
- `examples/` — one small fictional workspace, filled in, for reading.

## Rules

- **Everything here is generic.** No real names, institutions, grant numbers,
  URLs of private repositories or paths from anyone's machine. The examples
  are fictional and must stay fictional.
- **Templates use `{curly braces}` for placeholders.** Keep that convention;
  the `new-unit` script substitutes on it.
- **Skills must not hardcode paths.** They take the workspace root as an
  argument or infer it. A skill that only works on one person's laptop does
  not belong here.
- **Documentation is in English**, including examples and template comments.
  One deliberate exception: skill descriptions and trigger examples mix in
  Spanish phrases, because triggers must match what the intended adopters
  actually type, and they work in both languages.
- **Prose style: plain and short.** No em dashes in running text, no
  three-item lists used for rhythm, no marketing register. The reader is a
  colleague deciding whether to adopt this, not an audience.
- Changes to the contract itself (the three files and their update rules) are
  not routine. They need a reason written down, since every adopter's
  workspace depends on it.

## Before committing

- Run `tests/smoke.sh`. It walks docs/getting-started.md end to end against a
  scratch workspace and fails if the three template copies (`templates/`, the
  `new-unit` bundle, the example workspace) drift.
- Check that no absolute path from a real machine leaked into a doc or skill.
- Check that `docs/the-method.md` and `README.md` still agree. They describe
  the same thing at different lengths and drift easily.
