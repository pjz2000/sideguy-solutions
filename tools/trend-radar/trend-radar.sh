#!/bin/bash

cd /workspaces/sideguy-solutions

python3 tools/trend-radar/trend_radar.py

echo
echo "========================================"
echo "DAILY UPGRADE BRIEF"
echo "========================================"
echo

sed -n '1,220p' docs/intelligence/daily-upgrade-brief.md

echo
echo "========================================"
echo "Files written:"
echo " - docs/intelligence/daily-upgrade-brief.md"
echo " - docs/intelligence/daily-upgrade-brief.json"
echo " - data/signals/latest-signals.json"
echo "========================================"
