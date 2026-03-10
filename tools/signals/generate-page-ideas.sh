#!/usr/bin/env bash

# =========================================
# STAGE 3: PAGE IDEA GENERATOR
# For each categorized signal, generates
# specific page slug ideas.
# Output: docs/signals/page-ideas.txt
# =========================================

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INPUT="$ROOT/docs/signals/categorized-signals.tsv"
OUTPUT="$ROOT/docs/signals/page-ideas.txt"

if [ ! -f "$INPUT" ]; then
  echo "Missing: $INPUT — run categorize-signals.sh first"
  exit 1
fi

: > "$OUTPUT"

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9 -]//g' \
    | tr ' ' '-' \
    | sed 's/--*/-/g' \
    | sed 's/^-//; s/-$//'
}

INDUSTRIES=(contractors restaurants "law-firms" "hvac-companies" "medical-practices" "solar-companies")
LOCATIONS=("san-diego" "california" "texas")

tail -n +2 "$INPUT" | while IFS=$'\t' read -r bucket signal; do
  [ -z "$signal" ] && continue

  slug=$(slugify "$signal")

  # Core page types
  echo "what-is-${slug}.html | $bucket | core" >> "$OUTPUT"
  echo "how-to-${slug}.html | $bucket | core" >> "$OUTPUT"
  echo "how-much-does-${slug}-cost.html | $bucket | cost" >> "$OUTPUT"
  echo "${slug}-vs-alternatives.html | $bucket | comparison" >> "$OUTPUT"

  # Industry overlays (top 3)
  for industry in "${INDUSTRIES[@]:0:3}"; do
    echo "${slug}-for-${industry}.html | $bucket | industry" >> "$OUTPUT"
  done

  # Local overlay
  echo "${slug}-san-diego.html | $bucket | local" >> "$OUTPUT"

done

total=$(wc -l < "$OUTPUT")
echo ""
echo "Stage 3: Generated $total page ideas → $OUTPUT"
echo ""
echo "By type:"
awk -F'|' '{print $3}' "$OUTPUT" | tr -d ' ' | sort | uniq -c | sort -rn
echo ""
echo "By bucket:"
awk -F'|' '{print $2}' "$OUTPUT" | tr -d ' ' | sort | uniq -c | sort -rn
