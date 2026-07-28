#!/usr/bin/env bash
# List every relevant STATUS.md across the configured workspace roots,
# as "<days-since-modified>\t<path>", most recently touched first.
#
# Roots come from the arguments, or from roots.txt next to this script
# (one absolute path per line, blank lines and # comments ignored).
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
roots_file="$here/../roots.txt"

roots=()
if [ "$#" -gt 0 ]; then
  roots=("$@")
elif [ -f "$roots_file" ]; then
  while IFS= read -r line; do
    line="${line%%#*}"
    line="$(printf '%s' "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
    [ -n "$line" ] && roots+=("$line")
  done < "$roots_file"
fi

if [ "${#roots[@]}" -eq 0 ]; then
  echo "No workspace roots configured." >&2
  echo "Pass them as arguments, or create $roots_file with one path per line." >&2
  exit 2
fi

# Seconds since epoch, portable between macOS (BSD stat) and Linux (GNU
# stat). GNU first: BSD's -f flag means --file-system to GNU stat, which
# would print filesystem info instead of failing, so it cannot go first.
mtime() {
  stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null
}

now="$(date +%s)"

for root in "${roots[@]}"; do
  if [ ! -d "$root" ]; then
    echo "Missing root, skipped: $root" >&2
    continue
  fi
  # Keep this prune list in sync with SKIP in audit-workspace/scripts/audit.py.
  find "$root" \
    \( -type d \( \
         -name archive -o -name archives -o -name inbox -o \
         -name templates -o -name resources -o -name reference -o \
         -name admin -o -name .git -o -name .claude -o \
         -name node_modules -o -name __pycache__ \
       \) -prune \) -o \
    -type f -name STATUS.md -print 2>/dev/null
done | while IFS= read -r path; do
  m="$(mtime "$path")"
  [ -z "$m" ] && continue
  printf '%s\t%s\n' "$(( (now - m) / 86400 ))" "$path"
done | sort -n
