#!/bin/bash

echo "SideGuy Hub Discovery"
echo "---------------------"

echo ""
echo "Scanning root-level HTML pages..."

find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -ohE '\b(payment|payments|automation|ai|software|stablecoin|robot|agent|infrastructure)\b' \
| tr '[:upper:]' '[:lower:]' \
| sort \
| uniq -c \
| sort -rn \
| head -20

echo ""
echo "Potential hub candidates above."
