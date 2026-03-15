#!/usr/bin/env bash
PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo ""
echo "SideGuy Trend Radar"
echo ""

python3 tools/trend-radar/trend_radar.py

STAMP=$(date +%Y%m%d-%H%M%S)
cp docs/trend-signals/trend-signals.tsv docs/trend-signals/logs/trend-${STAMP}.tsv

echo ""
echo "Trend signals captured"
echo ""
