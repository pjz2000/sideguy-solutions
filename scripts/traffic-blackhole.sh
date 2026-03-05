#!/usr/bin/env bash
# SIDEGUY TRAFFIC BLACK HOLE ENGINE
# Routes internal traffic toward strongest authority pages
#
# Env knobs:
#   BH_TOP_N=20      number of top nodes to wire in
#   BH_DRY_RUN=1     preview only, no files written

set -euo pipefail
cd "$(dirname "$0")/.."

BH_TOP_N="${BH_TOP_N:-20}"
BH_DRY_RUN="${BH_DRY_RUN:-0}"
export BH_TOP_N BH_DRY_RUN

echo "================================"
echo " SIDEGUY TRAFFIC BLACK HOLE"
echo " TOP_N=$BH_TOP_N  DRY_RUN=$BH_DRY_RUN"
echo "================================"
echo ""

python3 scripts/traffic-blackhole.py

echo ""
echo "Black hole deployed"
