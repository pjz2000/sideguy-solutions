#!/bin/bash

echo "SideGuy Authority Map"
echo "---------------------"

echo ""
echo "Total root-level HTML pages:"
find . -maxdepth 1 -name "*.html" | wc -l

echo ""
echo "Pages missing FAQ schema:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'FAQPage' \
| wc -l

echo ""
echo "Pages missing command center links:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'sideguy-command-center.html' \
| wc -l

echo ""
echo "Pages missing hub links:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L 'knowledge-hub' \
| wc -l

echo ""
echo "Potential thin pages (no <p> tag):"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -L '<p>' \
| wc -l

echo ""
echo "Top keyword clusters:"
find . -maxdepth 1 -name "*.html" -print0 \
| xargs -0 grep -ohE '\b(payment|automation|software|ai|agent|stablecoin|infrastructure)\b' \
| tr '[:upper:]' '[:lower:]' \
| sort \
| uniq -c \
| sort -rn \
| head -15

echo ""
echo "Authority map complete."
