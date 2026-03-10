#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

INPUT="$ROOT/docs/radar/query-opportunities.txt"
OUTPUT="$ROOT/docs/problem-expansion/generated-topics.txt"

echo "Feeding radar ideas into expansion engine..."

cat "$INPUT" >> "$OUTPUT"

echo "Ideas appended."

