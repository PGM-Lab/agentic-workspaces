#!/usr/bin/env bash
# Walk the getting-started flow end to end against a scratch workspace, and
# check the three template copies stay in sync. Run from anywhere:
#
#   bash tests/smoke.sh
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
fail() { echo "SMOKE FAIL: $*" >&2; exit 1; }

# 1. Template copies in sync: templates/ vs the new-unit bundle vs the example.
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

# 2. Getting started, steps 2 and 5: fresh workspace, bundled-template fallback.
ws="$tmp/my-workspace"
mkdir -p "$ws"
cp "$repo"/templates/workspace/*.md "$ws"/
python3 "$repo/skills/new-unit/scripts/new_unit.py" "Coastal notes" \
  --type project --root "$ws" >/dev/null \
  || fail "new-unit could not seed a unit in a fresh workspace"
[ -f "$ws/projects/coastal-notes/LOG.md" ] || fail "contract not fully seeded"

# 3. A fresh, unfilled unit must not count as complete.
python3 "$repo/skills/audit-workspace/scripts/audit.py" --root "$ws" \
  | grep -q "Coverage: 0/" || fail "unfilled unit counted as complete"

# 4. Workspace-local templates take precedence once they exist.
mkdir -p "$ws/resources/templates"
cp "$repo"/skills/new-unit/templates/*.md "$ws/resources/templates/"
python3 "$repo/skills/new-unit/scripts/new_unit.py" "Second unit" \
  --type area --summary "Standing duty." --root "$ws" >/dev/null \
  || fail "new-unit failed with workspace templates present"

# 5. The board scan sees both STATUS files.
n="$(bash "$repo/skills/workspace-overview/scripts/scan.sh" "$ws" | wc -l | tr -d ' ')"
[ "$n" = "2" ] || fail "scan found $n STATUS files, expected 2"

# 6. The example workspace still audits clean.
python3 "$repo/skills/audit-workspace/scripts/audit.py" \
  --root "$repo/examples/example-workspace" \
  | grep -q "Coverage: 2/2" || fail "example workspace regressed"

echo "smoke OK"
