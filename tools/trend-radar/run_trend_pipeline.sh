#!/usr/bin/env bash
PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo ""
echo "=============================="
echo "SideGuy Trend Pipeline"
echo "=============================="
echo ""

echo "1. Capture trend signals"
bash tools/trend-radar/run_trend_radar.sh

echo ""
echo "2. Feed Alive discovery engine"
bash tools/trend-radar/feed_alive_engine.sh

echo ""
echo "3. Run Alive engine"
bash tools/alive/alive-engine.sh

echo ""
echo "Trend pipeline complete."
echo ""
