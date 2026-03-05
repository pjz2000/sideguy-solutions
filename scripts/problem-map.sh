#!/usr/bin/env bash
# SIDEGUY INTERNET PROBLEM MAP (Wikipedia Mode)
# Builds a human-navigable map of the site using real internal link gravity
#
# Output:
#   map/index.html          — master index (site-wide top nodes)
#   map/<bucket>.html       — per-bucket ranked pages
#   data/problem-map.json   — machine-readable export

set -euo pipefail
cd "$(dirname "$0")/.."

echo "============================================"
echo " SIDEGUY INTERNET PROBLEM MAP (Wikipedia Mode)"
echo "============================================"
echo ""

python3 scripts/problem-map.py

echo ""
echo "DONE: /map/index.html"
