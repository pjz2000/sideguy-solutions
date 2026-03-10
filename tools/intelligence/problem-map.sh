#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/intelligence/problem-map.md"

mkdir -p "$ROOT/docs/intelligence"

echo "# SideGuy Problem Map" > "$OUTPUT"
echo "" >> "$OUTPUT"
echo "Generated: $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

for FILE in "$ROOT"/*.html
do
  name=$(basename "$FILE")

  if echo "$name" | grep -qi "payment"; then
    echo "- Payments: $name" >> "$OUTPUT"
  fi

  if echo "$name" | grep -qi "ai"; then
    echo "- AI Automation: $name" >> "$OUTPUT"
  fi

  if echo "$name" | grep -qi "software"; then
    echo "- Software: $name" >> "$OUTPUT"
  fi

  if echo "$name" | grep -qi "infrastructure"; then
    echo "- Future Infrastructure: $name" >> "$OUTPUT"
  fi

done

echo "" >> "$OUTPUT"
echo "Problem map complete."
