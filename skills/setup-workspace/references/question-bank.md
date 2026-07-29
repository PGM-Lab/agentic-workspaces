# Question bank for setting up a workspace

Loaded by `setup-workspace` when drafting a workspace `AGENTS.md`. It exists
so the conversation stays short and concrete, and so nothing gets invented.

Recognition beats recall. People cannot answer "what is confidential in your
work?" cold, but they can point at the categories that apply to them. Offer
menus; do not run an interview.

## The three opening questions

Ask these and nothing else before creating anything.

1. **What is this workspace for?** Looking for one area of responsibility.
   If the answer covers several roles with different rules, say so and
   suggest starting with one.
2. **Where should it live?** A path. Not inside the clone of this kit.
3. **Kinds or cycles?** "Does your work come in different kinds with
   different lifecycles, or does it move in seasons that all end together?"
   Kinds picks `by-kind`, seasons picks `by-cycle`. If they hesitate, ask
   what they would call the folder holding last year's work.

## The confidentiality menu

Offer as a list to pick from, multiple choice, with "none of these" as a real
option. For each one they pick, write the concrete rule, not the category
name.

- **Work under review or embargo.** Manuscripts, submissions, anything
  unpublished that a third party controls.
- **Data about identifiable people.** Students, patients, participants,
  employees. Includes grades, assessments, complaints and supervision notes.
- **Material governed by an agreement.** Consortium data, NDAs, licensed
  datasets, client material. The rule usually is: check the agreement before
  anything leaves.
- **Personal identifiers and financial detail.** National IDs, addresses,
  bank or card numbers, invoices, salary.
- **Internal-only institutional material.** Not secret, but not for
  publication either.
- **Credentials.** Keys, tokens, passwords. These should not be in the
  workspace at all; say so if they pick it.
- **None of these.** A legitimate answer. Write "Nothing here is
  confidential" explicitly rather than leaving the section empty, so a later
  reader knows it was considered.

Then ask the one question that turns a category into a rule: **"what must
never happen to it?"** Typical answers: it never leaves this folder, it never
goes to an external service, it never appears in a summary or a board, it is
never quoted verbatim.

## Rules worth asking about, briefly

Only ask these if the workspace plausibly has them. Skip the rest.

- **Where does the real thing live?** If manuscripts are in Overleaf or code
  is in git, the workspace holds the private layer and nothing in it is
  canonical. This is the rule that prevents an agent editing a stale copy.
- **What needs confirmation before it runs?** Submitting a job, sending mail,
  posting anything, touching a shared system.
- **What must never be touched?** Original submissions, scanned forms,
  generated directories, anything a pipeline owns.
- **Storage without version control?** If it is on cloud sync, the rule is
  copy before moving and archive instead of deleting, and no bulk operations
  without showing the plan.

## Invariants: do not ask, just write

These are the same in every workspace. Asking about them wastes the user's
patience and invites inconsistent answers across workspaces.

- ISO dates, `YYYY-MM-DD`.
- `STATUS.md` is overwritten; `LOG.md` is append-only.
- After substantial work, update `STATUS.md` and append to `LOG.md`.
- Unknowns are marked `TODO`, never invented.
- The pending board is generated, never maintained by hand.

## What to do with what you could not fill

Leave it as a visible placeholder naming what is missing, for example
`{TODO: confidentiality not decided yet}`. Never drop the section.

An omitted section looks finished and passes every check. A placeholder is
caught by `audit-workspace` and by anyone reading the file. When in doubt,
leave the placeholder and tell the user what is still open.
