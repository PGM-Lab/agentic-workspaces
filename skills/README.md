# Skills

Five skills that operate the structure. Everything else you build on top will
be domain work.

| Skill | What it does | When |
|---|---|---|
| `setup-workspace` | Installs the kit and creates a workspace | Once per machine, once per workspace |
| `new-unit` | Creates a unit from the right template | Whenever work has no folder yet |
| `session-log` | Overwrites STATUS, appends to LOG | End of every working session |
| `workspace-overview` | Generates the pending board from STATUS files | Weekly, or on demand |
| `audit-workspace` | Checks the contract and surveys what is not activated | Occasionally, and while adopting |

## Installing

Open your agent inside a clone of this repository and say "install these
skills". It finds `setup-workspace` because the clone ships the skills where
both Claude Code and Codex look, and runs it.

To do it by hand:

```bash
python3 skills/setup-workspace/scripts/setup_workspace.py --install
```

One canonical copy goes to `~/.agents/skills/`, which Codex reads natively,
and is symlinked into `~/.claude/skills/`. One copy, both agents, and
`git pull` in the clone updates everything.

The install is additive: a skill of the same name that is already installed
is left alone and reported, never overwritten. Add `--copy` on Windows, where
symlinks need administrator rights, or if you plan to delete the clone.

Claude Code users can instead install through the plugin marketplace, which
handles versioning for them:

```bash
/plugin marketplace add PGM-Lab/agentic-workspaces
```

That route is Claude-only. If you use Codex as well, prefer the canonical
copy above so you do not end up maintaining two divergent installations.

**The clone must live on local disk**, not in Google Drive or another synced
folder: sync services do not carry symlinks.

## Global versus workspace-local

These five are cross-workspace and belong in the agent's skills directory. A
skill that only makes sense inside one workspace goes in that workspace at
`.claude/skills/<name>/`, as a real folder.

Claude Code discovers workspace-local skills automatically. Other agents do
not. The bridge is a `## Skills` section in the workspace `AGENTS.md` listing
each skill with its path and its trigger, phrased so any agent can be told to
read and follow the file.

## What is configured where

Nothing here should be edited to suit one workspace. The two things that vary
live in the workspace itself:

- `resources/kinds.json` — the kinds of unit this workspace has. Editing the
  installed `new-unit` instead would break every other workspace.
- `resources/templates/` — the workspace's own templates, if it wants any.
  Without them, `new-unit` uses the copy bundled with the skill.

The one exception is `workspace-overview`, which needs to know which
workspaces exist: `setup-workspace` appends each new one to its `roots.txt`,
and never rewrites the file.
