#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

OUTPUT="docs/analysis/page-priority-report.txt"
mkdir -p docs/analysis
> "$OUTPUT"

echo "Running SideGuy Priority Engine..."

for f in *.html
do
  [ -f "$f" ] || continue

  links=$(grep -o "<a " "$f" | wc -l)
  faq=$(grep -i "faq" "$f" | wc -l)
  hubs=$(grep -i "knowledge-hub" "$f" | wc -l)
  words=$(wc -w < "$f")

  score=$((links + faq*5 + hubs*4 + words/200))

  echo "$score | $f | links:$links faq:$faq hubs:$hubs words:$words" >> "$OUTPUT"
done

sort -rn "$OUTPUT" -o "$OUTPUT"

echo "Priority report created:"
echo "$OUTPUT"
