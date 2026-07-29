#!/usr/bin/env bash
# Walk the setup flow end to end against a scratch workspace, and check the
# template copies stay in sync. Run from anywhere:
#
#   bash tests/smoke.sh
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }

# 1. Unit templates in sync: templates/ vs new-unit's bundle vs the example.
for pair in \
  "unit/STATUS.md:STATUS.md" \
  "unit/LOG.md:LOG.md" \
  "unit/AGENTS.md:unit_AGENTS.md" \
  "variants/project_README.md:project_README.md" \
  "variants/area_README.md:area_README.md" \
  "variants/person_README.md:person_README.md"; do
  src="$repo/templates/${pair%%:*}"
  name="${pair##*:}"
  cmp -s "$src" "$repo/skills/new-unit/templates/$name" \
    || fail "new-unit bundle drifted from templates/: $name"
  cmp -s "$src" "$repo/examples/example-workspace/resources/templates/$name" \
    || fail "example workspace drifted from templates/: $name"
done

# 2. Workspace templates in sync: templates/workspace/ vs setup's bundle.
for f in "$repo"/templates/workspace/*.md; do
  cmp -s "$f" "$repo/skills/setup-workspace/templates/workspace/$(basename "$f")" \
    || fail "setup-workspace bundle drifted from templates/workspace/: $(basename "$f")"
done
grep -q '^@AGENTS.md$' "$repo/templates/workspace/CLAUDE.md" \
  || fail "the workspace CLAUDE.md template lost its @AGENTS.md import"

# 3. Every skill is discoverable by both agents from a fresh clone.
for d in "$repo"/skills/*/; do
  name="$(basename "$d")"
  [ -f "$d/SKILL.md" ] || continue
  for agent in .claude .agents; do
    [ -f "$repo/$agent/skills/$name/SKILL.md" ] \
      || fail "$name is not reachable via $agent/skills/ (agents will not find it)"
  done
done

# 4. Setup seeds a workspace, without touching anything outside the scratch dir.
ws="$tmp/my-workspace"
python3 "$repo/skills/setup-workspace/scripts/setup_workspace.py" \
  --workspace "$ws" --name "My Workspace" --layout by-kind --overview-roots none >/dev/null \
  || fail "setup could not seed a workspace"
for f in AGENTS.md CLAUDE.md README.md resources/kinds.json; do
  [ -f "$ws/$f" ] || fail "setup did not create $f"
done
python3 -c "import json,sys; json.load(open('$ws/resources/kinds.json'))" \
  || fail "setup wrote an invalid kinds.json"

# 5. Setup is idempotent: a second run must not overwrite an edited file.
echo "EDITED BY HAND" >> "$ws/AGENTS.md"
python3 "$repo/skills/setup-workspace/scripts/setup_workspace.py" \
  --workspace "$ws" --name "My Workspace" --overview-roots none >/dev/null
grep -q "EDITED BY HAND" "$ws/AGENTS.md" || fail "second setup run clobbered an edited file"

# 6. new-unit works in the seeded workspace, and honours its kinds.json.
python3 "$repo/skills/new-unit/scripts/new_unit.py" "Coastal notes" \
  --type project --root "$ws" >/dev/null || fail "new-unit failed in a seeded workspace"
[ -f "$ws/projects/coastal-notes/LOG.md" ] || fail "contract not fully seeded"
python3 "$repo/skills/new-unit/scripts/new_unit.py" "X" --type nosuchkind \
  --root "$ws" >/dev/null 2>&1 && fail "new-unit accepted a kind not in kinds.json"

# 7. A fresh, unfilled unit must not count as complete.
python3 "$repo/skills/audit-workspace/scripts/audit.py" --root "$ws" \
  | grep -q "Coverage: 0/" || fail "unfilled unit counted as complete"

# 8. The audit sees an empty section in the workspace AGENTS.md.
printf '\n## Confidentiality\n\n## Rules\n\n- something\n' >> "$ws/AGENTS.md"
python3 "$repo/skills/audit-workspace/scripts/audit.py" --root "$ws" \
  | grep -q "empty sections" || fail "audit missed an empty AGENTS.md section"

# 9. A folder with material and no contract is seen as not started, and the
#    inspect script reports on it without writing anything.
mkdir -p "$ws/projects/moved-in/sub"
printf 'see https://example.org/x\n' > "$ws/projects/moved-in/notes.md"
: > "$ws/projects/moved-in/sub/data.csv"
before="$(find "$ws/projects/moved-in" | sort)"
python3 "$repo/skills/audit-workspace/scripts/audit.py" --root "$ws" \
  | grep -q "projects/moved-in" || fail "audit missed a folder with material and no contract"
out="$(python3 "$repo/skills/activate/scripts/inspect_folder.py" \
  "$ws/projects/moved-in" --root "$ws")"
grep -q "nothing yet" <<<"$out" || fail "inspect did not report the missing contract"
grep -q "the next action" <<<"$out" || fail "inspect dropped its statement of what it cannot know"
[ "$before" = "$(find "$ws/projects/moved-in" | sort)" ] \
  || fail "inspect_folder wrote something; it must be read-only"

# 10. A brand-new workspace with material but nothing activated yet. This
#     needs its own workspace: once anything below has a STATUS.md the root is
#     already excluded as a container, which hides the bug. Every workspace
#     has a root README, so treating it as a candidate made it the ancestor of
#     everything and suppressed every real finding.
fresh="$tmp/fresh"
python3 "$repo/skills/setup-workspace/scripts/setup_workspace.py" \
  --workspace "$fresh" --name Fresh --overview-roots none >/dev/null
mkdir -p "$fresh/projects/moved-in-too"
: > "$fresh/projects/moved-in-too/paper.pdf"
fresh_out="$(python3 "$repo/skills/audit-workspace/scripts/audit.py" --root "$fresh")"
grep -qE '^  \.$' <<<"$fresh_out" \
  && fail "the workspace root was reported as an unactivated unit"
grep -q "projects/moved-in-too" <<<"$fresh_out" \
  || fail "a workspace with nothing activated yet reported none of its material"

# 11. The board scan sees the unit's STATUS file.
n="$(bash "$repo/skills/workspace-overview/scripts/scan.sh" "$ws" | wc -l | tr -d ' ')"
[ "$n" = "1" ] || fail "scan found $n STATUS files, expected 1"

# 12. The example workspace still audits clean.
python3 "$repo/skills/audit-workspace/scripts/audit.py" \
  --root "$repo/examples/example-workspace" \
  | grep -q "Coverage: 2/2" || fail "example workspace regressed"

# 13. The scan can name its roots. The board skill runs outside the workspaces
#     it reports on, so this is how it finds their AGENTS.md to read the
#     exceptions each one declares.
n="$(bash "$repo/skills/workspace-overview/scripts/scan.sh" --roots "$ws" "$fresh" \
  | wc -l | tr -d ' ')"
[ "$n" = "2" ] || fail "scan.sh --roots printed $n roots, expected 2"
bash "$repo/skills/workspace-overview/scripts/scan.sh" --roots "$ws" | grep -qx "$ws" \
  || fail "scan.sh --roots did not print the root it was given"

# 14. Install into a scratch home, then update. A copy install cannot follow a
#     git pull, so --update has to replace the kit's own copies; a skill the
#     user wrote under one of those names must survive both runs.
home="$tmp/home"
mkdir -p "$home/.agents/skills/audit-workspace" "$home/.claude/skills"
printf -- '---\nname: audit-workspace\n---\nWRITTEN BY THE USER\n' \
  > "$home/.agents/skills/audit-workspace/SKILL.md"
setup_home() {
  python3 "$repo/skills/setup-workspace/scripts/setup_workspace.py" \
    --copy --canonical "$home/.agents/skills" --claude-skills "$home/.claude/skills" "$@"
}
setup_home --install >/dev/null || fail "install into a scratch home failed"
[ -f "$home/.agents/skills/new-unit/SKILL.md" ] || fail "install did not copy new-unit"
[ -L "$home/.claude/skills/new-unit" ] || fail "install did not bridge to Claude Code"
grep -q "WRITTEN BY THE USER" "$home/.agents/skills/audit-workspace/SKILL.md" \
  || fail "install clobbered a skill the user wrote"

out="$(setup_home --update)"
grep -q "new-unit: kept" <<<"$out" \
  || fail "--update did not recognize an already up-to-date copy"

echo "STALE" >> "$home/.agents/skills/new-unit/SKILL.md"
out="$(setup_home --update)"
grep -q "new-unit: updated" <<<"$out" || fail "--update did not refresh an outdated copy"
grep -q "STALE" "$home/.agents/skills/new-unit/SKILL.md" \
  && fail "--update left the outdated copy in place"
grep -q "WRITTEN BY THE USER" "$home/.agents/skills/audit-workspace/SKILL.md" \
  || fail "--update replaced a skill the user wrote"
[ -L "$home/.claude/skills/new-unit" ] || fail "--update broke the bridge to Claude Code"

echo "smoke OK"
