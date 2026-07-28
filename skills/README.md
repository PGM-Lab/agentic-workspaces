# Skills

Four skills that operate the structure. Everything else you build on top will
be domain work.

| Skill | What it does | Edit before use |
|---|---|---|
| `new-unit` | Creates a unit from the right template | Yes, the kinds list |
| `session-log` | Closes a session: overwrite STATUS, append LOG | Usually not |
| `workspace-overview` | Generates the pending board from STATUS files | Yes, the roots |
| `audit-workspace` | Checks units against the contract | Usually not |

## Installing

Copy the folders into your agent's skills directory:

```bash
cp -r skills/* ~/.claude/skills/
```

Codex uses `~/.codex/skills/`. Both read the same `SKILL.md` format, so the
same folder works in either.

If you use more than one agent, keep one canonical copy on local disk and
symlink it into each agent's directory, rather than maintaining two versions.
Symlinks do not survive cloud sync, so the canonical copy must not live in a
synced folder.

## Global versus workspace-local

A skill that applies across all your work goes in the agent's skills
directory, as above. A skill that only makes sense inside one workspace goes
in that workspace, at `.claude/skills/<name>/`, as a real folder.

Claude Code discovers workspace-local skills automatically. Other agents do
not. The bridge is a `## Skills` section in the workspace `AGENTS.md` listing
each skill with its path and its trigger, phrased so that any agent can be
told to read and follow the file. Every agent reads `AGENTS.md`.

## Before you use these

`new-unit` ships with generic kinds (`project`, `area`, `person`) and
`workspace-overview` ships with no roots configured. Both say so at the top of
their `SKILL.md`. Edit them to match your setup; they are meant to be adapted,
not used as-is.
