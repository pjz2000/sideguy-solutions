#!/usr/bin/env bash

# =========================================
# STAGE 1: SIGNAL INGESTION
# Reads raw-signals.txt, strips comments/blanks,
# outputs clean signals to ingested-signals.txt
# =========================================

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INPUT="$ROOT/docs/signals/raw-signals.txt"
OUTPUT="$ROOT/docs/signals/ingested-signals.txt"

if [ ! -f "$INPUT" ]; then
  echo "Missing: $INPUT"
  echo "Add search-style queries (one per line) to that file."
  exit 1
fi

grep -v '^\s*#' "$INPUT" | grep -v '^\s*$' > "$OUTPUT"

count=$(wc -l < "$OUTPUT")
echo "Stage 1: Ingested $count signals → $OUTPUT"
