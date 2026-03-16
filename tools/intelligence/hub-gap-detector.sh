#!/bin/bash

OUTPUT="reports/hub-gaps.txt"
> "$OUTPUT"

echo "Scanning for likely hub coverage gaps..."

for file in *.html; do
  [ ! -f "$file" ] && continue

  title=$(grep -i -m1 "<title>" "$file" | sed 's/<[^>]*>//g')
  faq=$(grep -io "FAQ" "$file" | wc -l | tr -d ' ')
  links=$(grep -o "<a " "$file" | wc -l | tr -d ' ')
  words=$(wc -w < "$file" | tr -d ' ')

  gap_score=0
  [ "$faq" -eq 0 ] && gap_score=$((gap_score + 3))
  [ "$links" -lt 8 ] && gap_score=$((gap_score + 3))
  [ "$words" -lt 700 ] && gap_score=$((gap_score + 4))

  echo "$gap_score | $file | title:$title | words:$words | links:$links | faq:$faq" >> "$OUTPUT"

done

sort -nr "$OUTPUT" > reports/hub-gaps-ranked.txt

echo ""
echo "Created:"
echo "reports/hub-gaps-ranked.txt"
