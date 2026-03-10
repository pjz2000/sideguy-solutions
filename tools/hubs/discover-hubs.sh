#!/bin/bash

echo "SideGuy Hub Discovery"
echo "---------------------"

echo ""
echo "Scanning HTML pages..."

grep -rohE '\b(payment|payments|automation|ai|software|stablecoin|robot|agent|infrastructure)\b' \
--include="*.html" . \
| tr '[:upper:]' '[:lower:]' \
| sort \
| uniq -c \
| sort -rn \
| head -20

echo ""
echo "Potential hub candidates above."
