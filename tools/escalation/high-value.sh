#!/usr/bin/env bash
# Filters inbox for high-intent leads (cost, price, quote, repair, install, urgent)

INPUT="logs/responder/inbox.txt"
OUTPUT="logs/responder/high-value.txt"

if [ ! -f "$INPUT" ]; then
  echo "No inbox at $INPUT — nothing to process"
  exit 0
fi

> "$OUTPUT"
grep -iE "cost|price|quote|repair|install|urgent|replace|asap|emergency" "$INPUT" >> "$OUTPUT"

count=$(wc -l < "$OUTPUT")
echo "High value leads detected: ${count}"
