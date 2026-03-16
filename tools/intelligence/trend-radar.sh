#!/bin/bash

WATCHLIST="tools/intelligence/topic-watchlist.txt"
OUTPUT="reports/topic-opportunities.txt"

echo "Generating topic opportunity list..."
> "$OUTPUT"

while IFS= read -r topic; do
  [ -z "$topic" ] && continue

  slug=$(echo "$topic" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')

  score=0

  echo "$topic" | grep -qi "AI" && score=$((score + 4))
  echo "$topic" | grep -qi "payments\|settlement\|USDC\|stablecoin" && score=$((score + 5))
  echo "$topic" | grep -qi "local\|business\|service" && score=$((score + 4))
  echo "$topic" | grep -qi "robotics\|machine-to-machine\|infrastructure\|API" && score=$((score + 3))
  echo "$topic" | grep -qi "compliance\|software" && score=$((score + 2))

  echo "$score | $topic | /$slug.html" >> "$OUTPUT"

done < "$WATCHLIST"

sort -nr "$OUTPUT" > reports/topic-opportunities-ranked.txt

echo ""
echo "Created:"
echo "reports/topic-opportunities-ranked.txt"
