#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/analysis/authority-map.txt"

mkdir -p "$ROOT/docs/analysis"
> "$OUTPUT"

echo "Building authority map..."

for f in "$ROOT"/*.html
do
  [ -f "$f" ] || continue

  links=$(grep -o "<a " "$f" | wc -l)
  words=$(wc -w < "$f")

  echo "$links links | $words words | $(basename $f)" >> "$OUTPUT"
done

sort -rn "$OUTPUT" -o "$OUTPUT"

echo "Authority map saved:"
echo "$OUTPUT"
