#!/usr/bin/env bash

# =========================================
# STAGE 2: SIGNAL CATEGORIZER
# Maps each signal to a parent topic bucket
# using keyword matching.
# Output: docs/signals/categorized-signals.tsv
# Format: bucket TAB signal
# =========================================

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INPUT="$ROOT/docs/signals/ingested-signals.txt"
OUTPUT="$ROOT/docs/signals/categorized-signals.tsv"

if [ ! -f "$INPUT" ]; then
  echo "Missing: $INPUT — run ingest-signals.sh first"
  exit 1
fi

: > "$OUTPUT"
printf "bucket\tsignal\n" >> "$OUTPUT"

categorize() {
  local signal="$1"
  local s
  s=$(echo "$signal" | tr '[:upper:]' '[:lower:]')

  if echo "$s" | grep -qE 'stablecoin|solana|crypto|instant.settlement|machine.to.machine|m2m|robot.*pay|autonomous.*pay'; then
    echo "future-payments"
  elif echo "$s" | grep -qE 'payment|invoice|fee|stripe|square|settle|merchant|credit.card|processing|get.paid|accept.*pay'; then
    echo "payment-processing"
  elif echo "$s" | grep -qE 'ai|automat|agent|workflow|robot|schedul|dispatch|office.manager|replace.*staff'; then
    echo "ai-automation"
  elif echo "$s" | grep -qE 'software|saas|app|web.app|build.*app|custom.software|coding|develop|platform'; then
    echo "software-development"
  elif echo "$s" | grep -qE 'infrastructure|energy.trad|ev.charg|next.econom|future.of|machine.commerce'; then
    echo "future-infrastructure"
  elif echo "$s" | grep -qE 'san.diego|carlsbad|encinitas|escondido|oceanside|vista|san.marcos'; then
    echo "san-diego-local"
  else
    echo "general-business"
  fi
}

while IFS= read -r signal; do
  [ -z "$signal" ] && continue
  bucket=$(categorize "$signal")
  printf "%s\t%s\n" "$bucket" "$signal" >> "$OUTPUT"
done < "$INPUT"

echo ""
echo "Stage 2: Categorized signals → $OUTPUT"
echo ""
echo "Bucket counts:"
awk -F'\t' 'NR>1 {print $1}' "$OUTPUT" | sort | uniq -c | sort -rn
