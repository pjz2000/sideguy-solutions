#!/usr/bin/env bash

ROOT="${1:-.}"
STAMP=$(date "+%Y-%m-%d %H:%M:%S")

REPORT="logs/publish-gate/publish-gate-report.txt"

mkdir -p logs/publish-gate

echo "SideGuy Publish Gate Report" > "$REPORT"
echo "Generated: $STAMP" >> "$REPORT"
echo >> "$REPORT"


echo "Scanning HTML pages..." >> "$REPORT"
echo >> "$REPORT"


find "$ROOT" -maxdepth 1 -type f -name "*.html" | while read -r page
do

name=$(basename "$page")

title=$(grep -Eo '<title>.*</title>' "$page" | sed 's/<[^>]*>//g')

h1=$(grep -Eo '<h1[^>]*>.*</h1>' "$page" | sed 's/<[^>]*>//g' | head -1)

canonical=$(grep -Eic 'rel="canonical"' "$page")

links=$(grep -Eoi 'href="[^"]+\.html"' "$page" | wc -l | tr -d ' ')

words=$(tr '\n' ' ' < "$page" | sed 's/<[^>]*>/ /g' | tr -s ' ' '\n' | wc -l | tr -d ' ')

faq=$(grep -Eic 'FAQPage|faq' "$page" | tr -d ' ')

echo "$name" >> "$REPORT"

echo "   title: $title" >> "$REPORT"
echo "   h1: $h1" >> "$REPORT"
echo "   word count: $words" >> "$REPORT"
echo "   internal links: $links" >> "$REPORT"
echo "   faq blocks: $faq" >> "$REPORT"
echo "   canonical tag: $canonical" >> "$REPORT"


status="PASS"


if [ -z "$title" ]; then
echo "   ⚠ missing title tag" >> "$REPORT"
status="FAIL"
fi


if [ -z "$h1" ]; then
echo "   ⚠ missing H1" >> "$REPORT"
status="FAIL"
fi


if [ "$words" -lt 600 ]; then
echo "   ⚠ content depth too low (<600 words)" >> "$REPORT"
status="FAIL"
fi


if [ "$links" -lt 3 ]; then
echo "   ⚠ not enough internal links" >> "$REPORT"
status="FAIL"
fi


if [ "$canonical" -eq 0 ]; then
echo "   ⚠ missing canonical tag" >> "$REPORT"
status="FAIL"
fi


if [ "$faq" -eq 0 ]; then
echo "   ⚠ no FAQ schema detected" >> "$REPORT"
fi


echo "   STATUS: $status" >> "$REPORT"

echo >> "$REPORT"

done


echo "Publish Gate Complete." >> "$REPORT"

echo
echo "Publish gate report generated:"
echo "$REPORT"
