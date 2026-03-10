#!/bin/bash

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

echo "SideGuy Content Gravity Engine"
echo "-------------------------------"

echo ""
echo "Detecting newest HTML pages..."

find "$ROOT" -maxdepth 1 -name "*.html" -printf "%T@ %f\n" \
| sort -nr \
| head -20 \
| awk '{print $2}'

echo ""
echo "Recommended actions:"
echo ""

echo "Link these pages to:"
echo "- sideguy-command-center.html"
echo "- payments-knowledge-hub.html"
echo "- ai-automation-knowledge-hub.html"
echo "- software-development-knowledge-hub.html"
echo "- future-infrastructure-knowledge-hub.html"

echo ""
echo "Also add backlinks from the hubs."
