#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

INDEX="$ROOT/docs/index/page-metadata.tsv"
OUTPUT="$ROOT/docs/radar/query-opportunities.txt"

echo "Running SideGuy Query Radar..."

tail -n +2 "$INDEX" | awk -F'\t' '{print $1}' | \
sed 's/.html//' | tr '-' '\n' | \
grep -v -E 'for|the|and|with|san|diego' | \
sort | uniq -c | sort -rn | head -50 > /tmp/top-terms.txt

echo "" > "$OUTPUT"

while read count term
do
echo "ai-$term-for-small-business.html" >> "$OUTPUT"
echo "automation-$term-tools.html" >> "$OUTPUT"
echo "future-$term-systems.html" >> "$OUTPUT"
echo "$term-software-platforms.html" >> "$OUTPUT"
done < /tmp/top-terms.txt

echo "Query radar output:"
echo "$OUTPUT"

wc -l "$OUTPUT"

