#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/million-page/selected/wave-selection.csv"
OUTPUT="docs/million-page/authority/upgrade-candidates.csv"

[ -f "$INPUT" ] || { echo "No wave-selection.csv found. Run Phase 2 first."; exit 1; }

head -n 1 "$INPUT" > "$OUTPUT"

# Score is always the last field; use NF
tail -n +2 "$INPUT" | awk -F, '{
  score=$(NF); gsub(/"/,"",score)
  if (score+0 >= 45) print $0
}' >> "$OUTPUT"

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Authority candidates saved → $OUTPUT ($COUNT pages)"
