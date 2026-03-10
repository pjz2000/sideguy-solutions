#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/problem-expansion/generated-topics.txt"

mkdir -p "$ROOT/docs/problem-expansion"

INDUSTRIES=(
plumbers electricians dentists contractors restaurants
law-firms solar-companies hvac-companies med-spas auto-shops
)

PROBLEMS=(
ai-automation
payment-processing-fees
software-for-small-business
automation-tools
stablecoin-payments
)

LOCATIONS=(
san-diego california texas florida new-york
)

echo "Generating problem expansion topics..." > "$OUTPUT"

for problem in "${PROBLEMS[@]}"
do
  for industry in "${INDUSTRIES[@]}"
  do
    for location in "${LOCATIONS[@]}"
    do
      echo "$problem-for-$industry-$location.html" >> "$OUTPUT"
    done
  done
done

echo "Expansion complete. Output: $OUTPUT"
