#!/bin/bash

OUTPUT="reports/hub-strength-ranked.txt"
> "$OUTPUT"

echo "Analyzing hub strength..."

for page in $(find . -name "*.html" -not -path "./.git/*")
do

slug=$(basename "$page")

links=$(grep -o "<a " "$page" | wc -l)
words=$(wc -w < "$page")

score=$((links * 5 + words / 50))

echo "$score | $slug | links:$links | words:$words" >> "$OUTPUT"

done

sort -nr "$OUTPUT" > "$OUTPUT.tmp"
mv "$OUTPUT.tmp" "$OUTPUT"

echo ""
echo "Hub strength report:"
echo "$OUTPUT"
