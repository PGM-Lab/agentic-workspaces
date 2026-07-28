---
name: session-log
description: Close a working session by overwriting the touched unit's STATUS.md and appending a dated entry to its LOG.md. Use ALWAYS after substantial work on any unit in a workspace, and when the user says "close the session", "cierra la sesión", "write this down", "apunta esto", "update the status", "we decided X" or "hemos decidido X" — even if they do not explicitly ask for documentation.
---

# Session Log

Keep `STATUS.md` and `LOG.md` true after real work happens. This is the
write-back half of the loop: without it, a workspace decays into stale files
that an agent will still believe.

## Workflow

1. Identify which units were touched in this session. If work spanned several,
   handle each one.

2. For each unit:

   **`STATUS.md`** — overwrite it so it reflects the present. Current state in
   one line, the single concrete next step, pending items with their dates,
   what is blocked and on whom. Keep it under one screen. Update the
   "Last updated" date.

   **`LOG.md`** — append ONE dated entry at the top: two to four lines saying
   what was done, what was decided and why. Never rewrite an existing entry.

3. If a decision reverses an earlier one, say so explicitly in the entry
   ("supersedes the 2026-05-10 decision on X"). The point of an append-only
   log is that the reversal is visible, not hidden.

4. If the workspace keeps an aggregate `STATUS.md` at a level above the unit
   (a semester, a programme), update that row too so the two do not disagree.

## Rules

- `STATUS.md` is the present and is overwritten. `LOG.md` is the past and is
  append-only. Do not let either drift into the other's job.
- No filler. Concrete nouns, dates, names, identifiers. If nothing substantial
  happened, skip the log entry rather than writing something to have written
  something.
- Never invent a date, a commitment or an outcome. Mark unknowns as `TODO`.
- Respect the workspace's confidentiality rules when writing. A `STATUS.md`
  that will be read by an overview board should not carry personal data.
