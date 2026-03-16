#!/bin/bash

HUBS="manifests/intelligence/hubs.txt"
OUTPUT="reports/hub-gaps-ranked.txt"

echo "Scanning clusters for missing pages..."
> "$OUTPUT"

while read hub
do
  [ -z "$hub" ] && continue

  count=$(grep -R "$hub" . --include="*.html" 2>/dev/null | wc -l)

  score=$((20 - count))

  echo "$score | $hub | mentions:$count" >> "$OUTPUT"

done < "$HUBS"

sort -nr "$OUTPUT" > "$OUTPUT.tmp"
mv "$OUTPUT.tmp" "$OUTPUT"

echo ""
echo "Cluster gaps ranked:"
echo "$OUTPUT"
