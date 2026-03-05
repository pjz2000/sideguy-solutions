#!/usr/bin/env bash
# SIDEGUY FUTURE RADAR (SEO Time Travel)
# Pulls fresh operator pain signals, scores + clusters, outputs build list

set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== SIDEGUY FUTURE RADAR ==="
echo ""

python3 scripts/future-radar.py

echo ""
echo "Open: future/radar.html"
echo "Topics: future/top-topics.txt"
