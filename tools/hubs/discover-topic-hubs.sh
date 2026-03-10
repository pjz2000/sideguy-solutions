#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/hubs/topic-hub-candidates.txt"

echo "Scanning for hub candidates..."

> "$OUTPUT"

grep -h -o -E "[a-zA-Z0-9-]+-(automation|payments|software|ai|infrastructure)" *.html \
| sort \
| uniq -c \
| sort -rn \
> "$OUTPUT"

echo "Hub candidates written to:"
echo "$OUTPUT"
