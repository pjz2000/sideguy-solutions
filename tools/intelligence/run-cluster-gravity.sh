#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo ""
echo "Running SideGuy Cluster Gravity Engine..."
echo ""

python3 tools/intelligence/cluster-gravity-engine.py

echo ""
echo "Main outputs:"
echo "- docs/cluster-gravity/reports/cluster-summary.csv"
echo "- docs/cluster-gravity/reports/cluster-pages.csv"
echo "- docs/cluster-gravity/reports/cluster-gravity-report.md"
echo "- docs/cluster-gravity/reports/upgrade-targets.md"
echo ""
