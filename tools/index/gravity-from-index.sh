#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX="$ROOT/docs/index/page-metadata.tsv"

echo "Top gravity pages:"

tail -n +2 "$INDEX" | awk -F'\t' '
{
score = $2 + ($3*50)
print score " " $1
}
' | sort -rn | head -20

