#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "SideGuy Nervous System starting..."
echo ""

bash tools/nervous/scan-pages.sh
bash tools/nervous/detect-stale-pages.sh
bash tools/nervous/refresh-stale-pages.sh
bash tools/nervous/detect-clusters.sh
bash tools/nervous/build-expansion-queue.sh
bash tools/nervous/trigger-cluster-expansion.sh
bash tools/nervous/build-report.sh

echo ""
echo "SideGuy Nervous System cycle complete."
echo ""
