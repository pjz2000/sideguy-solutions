#!/usr/bin/env bash

INPUT="manifests/intent/intent-priority.csv"
OUTPUT="manifests/intent/build-now.txt"

if [ ! -f "$INPUT" ]; then
  echo "Missing $INPUT"
  exit 0
fi

echo "" > "$OUTPUT"

head -20 "$INPUT" | tail -n +2 | while IFS=, read -r query score type; do

  if [[ "$type" == "money" ]] || [[ "$type" == "local-money" ]]; then
    echo "$query" >> "$OUTPUT"
  fi

done

echo "Top money queries → $OUTPUT"
