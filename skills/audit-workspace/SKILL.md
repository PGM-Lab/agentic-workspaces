---
name: audit-workspace
description: Check a workspace for consistency against the file contract: units missing a README, STATUS or LOG, unfilled template placeholders, STATUS files that have gone stale, and units whose files contradict each other. Use when the user asks to "audit the workspace", "check consistency", "auditar", "revisar el workspace", "what's half-finished", "which projects are not activated", or before handing a workspace to someone else.
---

# Audit Workspace

Check that units actually honour the contract, and report. This finds the two
failure modes the structure is prone to: units that were moved but never given
a context layer, and units whose templates were satisfied without being filled
in.

**Read-only by default.** Report findings and let the user decide. Fix things
only when explicitly asked, and one unit at a time.

## Workflow

1. Run `scripts/audit.py` against the workspace root:

```sh
python3 <path-to-skill>/scripts/audit.py --root <workspace>
```

   It reports missing contract files, leftover `{placeholders}` and `TODO`
   markers, and `STATUS.md` files older than the staleness threshold. Pass
   `--json` when another tool will consume the output. `--max-depth` widens
   how deep the search for unactivated candidates goes; confirmed units,
   which have a `STATUS.md`, are found at any depth.

   It also lists folders with a `README.md` but no `STATUS.md`, as
   "possibly unactivated". That list needs judgement: from the files alone a
   half-activated unit is indistinguishable from a container folder or a
   working subfolder that happens to document itself.

2. Read the flagged files. The script finds candidates; deciding whether
   something is a real problem needs judgement, and the script has none.

3. Check the things a script cannot:

   - **Does the `README.md` say anything real**, or is it the template with
     the braces filled by restating the folder name?
   - **Does `STATUS.md` match reality** as far as you can tell from the log and
     recent files? A confidently wrong status is worse than a missing one.
   - **Is the next step a next step**, or a restatement of the goal? "Finish
     the paper" is not an action.
   - **Do the files contradict each other?** A `LOG.md` whose latest entry
     describes work that `STATUS.md` does not reflect means a session was not
     closed.
   - **Is the unit still a unit?** Long-dead work belongs in `archive/`, and
     something that has grown two independent workstreams is two units.

4. Report grouped by severity, not by folder:

   - **Wrong**: files that state something untrue. Highest priority, since
     they mislead both you and the agent.
   - **Missing**: units with no context layer at all. These are visible as
     absent, which is honest, so they matter less than wrong ones.
   - **Stale**: not touched in a long time. May be fine. Flag, do not nag.
   - **Cosmetic**: leftover placeholders in otherwise filled-in files.

5. End with a coverage line: how many units have the full contract, out of how
   many exist. During adoption this number is the useful one, and it should be
   stated rather than implied.

## Notes

- The contract does not apply to `archive/`, `inbox/`, `resources/`, working
  subfolders inside a unit, or generated reference material. Do not report
  those as missing.
- Some kinds deliberately use a lighter contract, typically short-lived units
  with a single file. Check the workspace `AGENTS.md` before reporting a
  deviation: it may be documented and intentional.
- Do not open confidential material in bulk to audit it. Structure can be
  checked from filenames and headers.
- **The coverage number is not the adoption number.** The script only sees
  folders that already have at least one contract file. Work that was moved
  into place but never given any documentation at all is invisible to it, and
  during adoption that is usually the largest group. If the workspace keeps a
  separate inventory of what exists versus what is activated, that inventory
  is the honest denominator, and the audit only checks the folders that have
  started.
