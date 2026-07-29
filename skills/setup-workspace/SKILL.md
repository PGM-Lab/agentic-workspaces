---
name: setup-workspace
description: Install this kit's skills into the user's agent and create a new workspace, interviewing them briefly and drafting its AGENTS.md for them to correct. Use when the user says "set me up", "install these skills", "create a workspace", "móntame un workspace", "instálate", or opens a session in a clone of the kit and asks to get started.
disable-model-invocation: true
---

# Set up a workspace

Two jobs: install the skills once per machine, and create a workspace. The
mechanical parts are a script; your job is the conversation and the drafting.

Read [`../../docs/the-method.md`](../../docs/the-method.md) before you start
if you have not. A workspace set up by someone who has not read it will have a
`STATUS.md` that gets appended to and a `LOG.md` that gets rewritten, and the
whole thing stops being worth having.

## Install

Run once per machine:

```sh
python3 <path-to-skill>/scripts/setup_workspace.py --install
```

It puts one canonical copy in `~/.agents/skills/` (which Codex reads
natively) and symlinks it into `~/.claude/skills/`. It is additive: a skill
of the same name that is already there is left alone and reported, never
replaced. Tell the user what was skipped, if anything, and that nothing was
overwritten.

Pass `--copy` if the user is on Windows, where symlinks need administrator
rights, or if they intend to delete the clone.

For an agent that is neither Claude Code nor Codex, the skills still work:
they are plain `SKILL.md` folders. Tell the user to list them in the
workspace's `AGENTS.md` under `## Skills` with their paths, which is the
bridge any agent can follow.

## Create a workspace

### 1. Ask three questions, not twelve

- **What is this workspace for?** One area of responsibility, not their whole
  working life.
- **Where should it live?** A path. Warn if it is inside the clone: the clone
  is the source of the kit, not a place to work.
- **Does the work come in kinds with different lifecycles, or does it move in
  cycles?** Papers, grants and reviews are kinds; semesters and terms are
  cycles. This picks `--layout by-kind` or `--layout by-cycle`.

Stop there. A twelve-question interview before anything exists is how people
abandon a setup.

### 2. Run the script

```sh
python3 <path-to-skill>/scripts/setup_workspace.py \
    --workspace <path> --name "<name>" --layout by-kind
```

It creates the root files from the templates, writes
`resources/kinds.json`, copies the unit templates into the workspace, and
adds the workspace to the overview board's roots. It never overwrites a file
that already exists, so it is safe to run twice.

### 3. Draft the AGENTS.md, then have them correct it

This is the file that matters, and the only one that genuinely needs thought.
Do not hand over a template with braces and hope. Do not interview them at
length either. Draft it, then show it.

Fill in the structure and the rules from what they told you. For
confidentiality, do not ask the open question "what is confidential here?",
because people cannot answer it cold. Offer the menu in
[`references/question-bank.md`](references/question-bank.md) and let them
recognise their categories, including "none of these".

Then show the complete draft and ask for corrections on specific lines.

**Two hard rules while drafting:**

- **Write only what they told you.** Never invent a plausible-sounding rule.
  "Follow best practices" is worse than nothing: it trains the reader to
  ignore the file.
- **Never omit a section you could not fill.** Leave it with an explicit
  `{placeholder}` saying what is missing. An omitted confidentiality section
  is invisible; a placeholder is caught by `audit-workspace` and by the eye.
  This matters more than it looks: nothing else in the system knows what must
  not leave the tree.

Keep it under 120 lines. If the draft is longer, cut before you show it.

### 4. Record why this shape

Add a short **Why this shape** section to the workspace's `README.md`, three
lines at most: why the folders are organised the way they are, what is
confidential, where the code or the canonical sources live. The what is
already in `AGENTS.md`; this is the why, and it is what nobody can
reconstruct a year later.

Do not create a `LOG.md` at the workspace root. The contract defines one per
unit, not per workspace, and a file nothing reads is a file that goes stale.

### 5. Verify, out loud

Run the audit and show the result:

```sh
python3 <canonical-skills>/audit-workspace/scripts/audit.py --root <workspace>
```

The postconditions the script prints are the specification. Check them rather
than asserting success. In particular: `AGENTS.md` has no empty sections,
`CLAUDE.md` is only the import line, `kinds.json` names their kinds.

### 6. Say what comes next

- If they already have folders full of work, which is usual, point them at
  [`../../docs/adopting-existing-work.md`](../../docs/adopting-existing-work.md).
  Do not start moving or activating anything now: that is a separate decision
  with a separate order of work.
- If they are starting fresh, tell them to create one unit with `new-unit`
  and use it for a week before adding a second workspace.

## On the second and later workspaces

Do not re-run the interview from scratch. Offer "same as `<existing
workspace>` except X", read the existing `AGENTS.md`, and ask only what
differs. Invariants like date format and storage rules should not be
re-decided each time, or the workspaces will drift apart.

Note that `kinds.json` is per workspace: never edit an installed skill to
change a workspace's kinds.
