#!/usr/bin/env bash
# SideGuy Trend Radar — daily refresh
# Usage: bash tools/trend-radar/run_trend_radar.sh
set -e
cd "$(dirname "$0")/../.."
python3 tools/trend-radar/trend_radar.py
echo "Trend radar refreshed. Review: docs/trend-radar/radar-report.md"
