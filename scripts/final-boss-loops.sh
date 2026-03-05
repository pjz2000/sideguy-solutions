#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."

echo "=== FINAL BOSS: AUTO-REFRESH AUTHORITY LOOPS ==="
echo "  LOOPS_GLOBAL=${LOOPS_GLOBAL:-20}  LOOPS_BUCKET=${LOOPS_BUCKET:-8}  LOOPS_TIGHT=${LOOPS_TIGHT:-5}"

# If problem map missing, build it first
if [ ! -f data/problem-map.json ]; then
  if [ -f scripts/problem-map.sh ]; then
    echo "[boss] data/problem-map.json missing -> building..."
    bash scripts/problem-map.sh
  else
    echo "[boss] data/problem-map.json not found and scripts/problem-map.sh missing."
    echo "Build problem map first, then rerun."
    exit 0
  fi
fi

LOOPS_GLOBAL="${LOOPS_GLOBAL:-20}" \
LOOPS_BUCKET="${LOOPS_BUCKET:-8}" \
LOOPS_TIGHT="${LOOPS_TIGHT:-5}" \
python3 scripts/final-boss-loops.py

echo ""
echo "Report: reports/final-boss-loops.json"
echo "DONE."
