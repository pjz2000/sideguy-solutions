#!/usr/bin/env bash

INPUT="data/gsc/queries-latest.csv"
OUTPUT="manifests/intent/intent-priority.csv"

if [ ! -f "$INPUT" ]; then
  echo "Missing $INPUT"
  exit 0
fi

echo "query,score,type" > "$OUTPUT"

while IFS=, read -r query clicks impressions ctr position; do

  # skip header
  if [[ "$query" == "query" ]]; then
    continue
  fi

  q=$(echo "$query" | tr '[:upper:]' '[:lower:]')

  score=0
  type="info"

  ########################################
  # MONEY SIGNALS
  ########################################

  if [[ "$q" == *"cost"* ]] || [[ "$q" == *"pricing"* ]] || [[ "$q" == *"price"* ]]; then
    score=$((score+10))
    type="money"
  fi

  if [[ "$q" == *"best"* ]] || [[ "$q" == *"vs"* ]] || [[ "$q" == *"compare"* ]]; then
    score=$((score+8))
    type="money"
  fi

  if [[ "$q" == *"near me"* ]] || [[ "$q" == *"san diego"* ]]; then
    score=$((score+9))
    type="local-money"
  fi

  if [[ "$q" == *"automation"* ]] || [[ "$q" == *"payment"* ]] || [[ "$q" == *"software"* ]]; then
    score=$((score+6))
  fi

  ########################################
  # TRAFFIC SIGNALS
  ########################################

  imp=$(printf "%.0f" "$impressions")
  clk=$(printf "%.0f" "$clicks")

  score=$((score + imp + (clk*3)))

  ########################################
  # OUTPUT
  ########################################

  echo "$query,$score,$type" >> "$OUTPUT"

done < "$INPUT"

# SORT
sort -t, -k2 -nr "$OUTPUT" -o "$OUTPUT"

echo "Saved intent priority → $OUTPUT"
