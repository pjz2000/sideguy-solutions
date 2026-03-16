#!/bin/bash

WATCHLIST="tools/intelligence/vertical-watchlist.txt"
OUTPUT="reports/topic-opportunities-ranked.txt"

echo "Scanning topic opportunities..."

> "$OUTPUT"

while IFS= read -r topic
do
  [ -z "$topic" ] && continue

  score=0

  echo "$topic" | grep -qi "AI" && score=$((score+5))
  echo "$topic" | grep -qi "payments\|stablecoin\|settlement" && score=$((score+6))
  echo "$topic" | grep -qi "robotics\|machine" && score=$((score+4))
  echo "$topic" | grep -qi "energy\|EV" && score=$((score+3))
  echo "$topic" | grep -qi "business\|operator\|service" && score=$((score+4))

  echo "$score | $topic" >> "$OUTPUT"

done < "$WATCHLIST"

sort -nr "$OUTPUT" > "$OUTPUT.tmp"
mv "$OUTPUT.tmp" "$OUTPUT"

echo ""
echo "Topic opportunities:"
echo "$OUTPUT"
