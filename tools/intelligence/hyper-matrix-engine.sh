#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

TOPICS="docs/million-engine/topics.txt"
MODS="docs/million-engine/modifiers.txt"
LOCS="docs/million-engine/locations.txt"
INDS="docs/million-engine/industries.txt"

OUTPUT="data/matrix-queue/all-slugs.txt"

mkdir -p "$(dirname "$OUTPUT")"

COUNT=0

echo ""
echo "SIDEGUY HYPER MATRIX GENERATOR"
echo ""

> "$OUTPUT"

while IFS= read -r TOPIC; do
  [[ -z "$TOPIC" ]] && continue
  while IFS= read -r MOD; do
    [[ -z "$MOD" ]] && continue
    while IFS= read -r LOC; do
      [[ -z "$LOC" ]] && continue
      while IFS= read -r IND; do
        [[ -z "$IND" ]] && continue

        SLUG="${TOPIC}-${MOD}-${LOC}-${IND}"
        echo "$SLUG" >> "$OUTPUT"
        COUNT=$((COUNT+1))

      done < "$INDS"
    done < "$LOCS"
  done < "$MODS"
done < "$TOPICS"

echo "Generated: $COUNT slugs"
echo "Saved to:  $OUTPUT"
echo ""
