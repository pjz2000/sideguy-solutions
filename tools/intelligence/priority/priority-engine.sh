#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo "======================================="
echo "SideGuy Priority Engine"
echo "Ranking what matters most"
echo "======================================="

OUTPUT="docs/intelligence/priority/priority-report-$(date +%Y%m%d-%H%M%S).txt"

echo "PAGE | SCORE | REASON" > "$OUTPUT"

find public -name "*.html" | while read file; do

  page=$(basename "$file")

  links=$(grep -o "<a " "$file" | wc -l)
  faq=$(grep -i "faq" "$file" | wc -l)
  words=$(wc -w < "$file")

  score=$((links + faq + words/150))

  reason=""

  if [ "$links" -lt 5 ]; then
    reason="$reason low_links"
  fi

  if [ "$faq" -lt 1 ]; then
    reason="$reason missing_faq"
  fi

  if [ "$words" -lt 400 ]; then
    reason="$reason thin_content"
  fi

  echo "$page | $score | $reason" >> "$OUTPUT"

done

echo ""
echo "Priority report built:"
echo "$OUTPUT"
echo ""
