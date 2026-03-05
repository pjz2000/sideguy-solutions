#!/usr/bin/env bash
# SIDEGUY FUTURE AUTO BUILDER
# Builds pages from Future Radar topics (future/top-topics.txt)

set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== SIDEGUY FUTURE AUTO BUILDER ==="
echo ""

python3 scripts/future-auto-builder.py

echo ""
echo "Future pages generated → future-build/"
