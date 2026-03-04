#!/usr/bin/env bash
# SideGuy Problem Multiplier Engine (idempotent, no-hands)
# Usage:  bash scripts/problem-multiplier-engine.sh
# Knobs:  LIMIT=300 TOPICS=40 INDUSTRIES=18 bash scripts/problem-multiplier-engine.sh

set -e

echo "=== SideGuy Problem Multiplier Engine ==="
echo "LIMIT=${LIMIT:-250}  TOPICS=${TOPICS:-35}  INDUSTRIES=${INDUSTRIES:-16}"
echo ""

python3 scripts/problem-multiplier.py

if [ -f scripts/generate-sitemap.py ]; then
  echo ""
  echo "--- Regenerating sitemap ---"
  python3 scripts/generate-sitemap.py
fi

if [ -f scripts/build-problem-hub.py ]; then
  echo ""
  echo "--- Rebuilding problem hub ---"
  python3 scripts/build-problem-hub.py
fi

echo ""
echo "=== Done. ==="
echo "Tip: Increase output with:"
echo "  LIMIT=500 TOPICS=60 INDUSTRIES=20 bash scripts/problem-multiplier-engine.sh"
