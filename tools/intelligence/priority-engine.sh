#!/usr/bin/env bash

ROOT="${1:-.}"
STAMP="$(date '+%Y-%m-%d %H:%M:%S')"
OUT_DIR="logs/intelligence"
OUT_FILE="$OUT_DIR/priority-report.txt"
TMP_FILE="$OUT_DIR/.priority-temp.txt"

mkdir -p "$OUT_DIR"
: > "$TMP_FILE"

find "$ROOT" -maxdepth 1 -type f -name "*.html" ! -name "404.html" | sort | while read -r file; do
  rel="$(basename "$file")"

  internal_links=$(grep -Eoi 'href="[^"]+\.html"' "$file" 2>/dev/null | wc -l | tr -d ' ')
  hub_connections=$(grep -Eoi 'href="[^"]*(hub|index|directory|payments|automation|services|solutions)[^"]*\.html"' "$file" 2>/dev/null | wc -l | tr -d ' ')
  faq_presence=$(grep -Eic 'FAQPage|Frequently Asked|faq' "$file" 2>/dev/null | tr -d ' ')
  schema_presence=$(grep -Eic 'application/ld\+json' "$file" 2>/dev/null | tr -d ' ')
  words=$(tr '\n' ' ' < "$file" | sed 's/<[^>]*>/ /g' | tr -s ' ' '\n' | wc -l | tr -d ' ')
  examples=$(grep -Eic 'example|for example|how it works|use case|common scenario' "$file" 2>/dev/null | tr -d ' ')
  cta_presence=$(grep -Eic 'Text PJ|773-544-1231|text us|contact|get help' "$file" 2>/dev/null | tr -d ' ')
  title_presence=$(grep -Eic '<title>' "$file" 2>/dev/null | tr -d ' ')
  h1_presence=$(grep -Eic '<h1' "$file" 2>/dev/null | tr -d ' ')
  intro_strength=$(head -n 120 "$file" | grep -Eic '<p|clarity|human|fast|simple|real help' | tr -d ' ')

  score=0
  score=$((score + internal_links * 2))
  score=$((score + hub_connections * 4))
  score=$((score + faq_presence * 8))
  score=$((score + schema_presence * 6))
  score=$((score + examples * 3))
  score=$((score + cta_presence * 4))
  score=$((score + title_presence * 3))
  score=$((score + h1_presence * 4))
  score=$((score + intro_strength * 2))

  if [ "$words" -ge 1800 ]; then
    score=$((score + 18))
  elif [ "$words" -ge 1200 ]; then
    score=$((score + 12))
  elif [ "$words" -ge 700 ]; then
    score=$((score + 7))
  elif [ "$words" -ge 350 ]; then
    score=$((score + 3))
  fi

  printf "%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" \
    "$score" "$rel" "$internal_links" "$hub_connections" "$words" "$faq_presence" "$schema_presence" "$examples" "$cta_presence" "$intro_strength" \
    >> "$TMP_FILE"
done

{
  echo "SideGuy Priority Intelligence Report"
  echo "Generated: $STAMP"
  echo
  echo "Scoring factors:"
  echo "- internal links"
  echo "- hub connections"
  echo "- content depth"
  echo "- FAQ presence"
  echo "- schema presence"
  echo "- examples/use-cases"
  echo "- CTA presence"
  echo "- intro strength"
  echo
  echo "Top Pages To Upgrade / Protect"
  echo "================================"
  echo
  sort -t'|' -k1,1nr "$TMP_FILE" | nl -w1 -s'. ' | while IFS='|' read -r n score rel internal_links hub_connections words faq_presence schema_presence examples cta_presence intro_strength; do
    echo "$n $rel"
    echo "   Score: $score"
    echo "   Internal links: $internal_links"
    echo "   Hub connections: $hub_connections"
    echo "   Words: $words"
    echo "   FAQ blocks: $faq_presence"
    echo "   Schema blocks: $schema_presence"
    echo "   Examples: $examples"
    echo "   CTA hits: $cta_presence"
    echo "   Intro strength: $intro_strength"
    echo
  done
} > "$OUT_FILE"

rm -f "$TMP_FILE"

echo "Wrote $OUT_FILE"
