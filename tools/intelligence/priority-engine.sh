#!/usr/bin/env bash

# SideGuy Priority Engine
# Purpose:
# Identify high-opportunity pages that deserve upgrades.

ROOT_DIR="."

echo "Scanning HTML pages..."
echo ""
echo "PAGE | SCORE | LINKS | HUB | FAQ | LENGTH"

find "$ROOT_DIR" -maxdepth 1 -name "*.html" -print0 \
| xargs -0 -P4 awk '
  FNR==1 {
    links=0; hub=0; faq=0; length=0; file=FILENAME
  }
  {
    length++
    links += gsub(/<a /,"<a ")
    if (tolower($0) ~ /knowledge-hub/) hub++
    if (tolower($0) ~ /faq|faqpage/) faq++
  }
  ENDFILE {
    score = links + hub*5 + faq*3 + int(length/200)
    print file " | " score " | " links " | " hub " | " faq " | " length
  }
' \
| sort -t'|' -k2 -nr

echo ""
echo "Priority Engine Complete."
echo "Top pages listed first."
