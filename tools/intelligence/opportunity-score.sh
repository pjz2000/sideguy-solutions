#!/bin/bash

OUTPUT="reports/page-priority-report.txt"
> "$OUTPUT"

echo "Scoring live HTML pages..."

for file in *.html; do
  [ ! -f "$file" ] && continue

  links=$(grep -o "<a " "$file" | wc -l | tr -d ' ')
  faq=$(grep -io "FAQ" "$file" | wc -l | tr -d ' ')
  words=$(wc -w < "$file" | tr -d ' ')
  payments=$(grep -i "payment\|USDC\|settlement\|merchant\|stablecoin" "$file" | wc -l | tr -d ' ')
  ai=$(grep -i "AI\|automation\|agent" "$file" | wc -l | tr -d ' ')
  local=$(grep -i "San Diego\|local\|operator\|business owner" "$file" | wc -l | tr -d ' ')

  score=$((links + faq*5 + words/200 + payments*2 + ai*2 + local*2))

  echo "$score | $file | links:$links faq:$faq words:$words payments:$payments ai:$ai local:$local" >> "$OUTPUT"

done

sort -nr "$OUTPUT" > reports/page-priority-ranked.txt

echo ""
echo "Created:"
echo "reports/page-priority-ranked.txt"
