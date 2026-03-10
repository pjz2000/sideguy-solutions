#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/gravity/gravity-report.txt"

echo "Building SideGuy Gravity Report..."

> "$OUTPUT"

find "$ROOT" -maxdepth 1 -name "*.html" | while read -r f
do

links=$(grep -o "<a " "$f" | wc -l)
words=$(wc -w < "$f")

score=$((links + words/150))

printf "%s | %s links | %s words\n" "$score" "$(basename "$f")" "$links" >> "$OUTPUT"

done

sort -rn "$OUTPUT" -o "$OUTPUT"

echo "Gravity report created:"
echo "$OUTPUT"
