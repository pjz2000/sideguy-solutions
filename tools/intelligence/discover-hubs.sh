#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/analysis/hub-discovery.txt"

mkdir -p "$ROOT/docs/analysis"
> "$OUTPUT"

echo "Scanning for cluster keywords..."

grep -h -o -E "[a-zA-Z0-9-]+-(software|automation|payments|ai|infrastructure)" "$ROOT"/*.html \
| sort | uniq -c | sort -rn > "$OUTPUT"

echo "Hub discovery saved:"
echo "$OUTPUT"
