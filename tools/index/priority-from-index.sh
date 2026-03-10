#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX="$ROOT/docs/index/page-metadata.tsv"
OUTPUT="$ROOT/docs/index/priority-report.txt"

echo "Building fast priority report..."

tail -n +2 "$INDEX" | awk -F'\t' '
{
score = $2 + ($3*50) + ($4*200)
print score " | " $1 " | words:" $2 " links:" $3 " h2:" $4
}
' | sort -rn > "$OUTPUT"

echo "Priority report written to:"
echo "$OUTPUT"

