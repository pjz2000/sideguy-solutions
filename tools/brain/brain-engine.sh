#!/usr/bin/env bash
set -e

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo "============================================="
echo " SideGuy Brain Engine — Phase 6"
echo "============================================="

echo ""
echo "[1/7] Calculating topic momentum..."
bash tools/brain/topic-momentum.sh

echo ""
echo "[2/7] Detecting cluster dominance..."
bash tools/brain/cluster-dominance.sh

echo ""
echo "[3/7] Scoring internal link gravity..."
bash tools/brain/internal-link-gravity.sh

echo ""
echo "[4/7] Building expansion recommendations..."
bash tools/brain/build-recommendations.sh

echo ""
echo "[5/7] Building upgrade recommendations..."
bash tools/brain/upgrade-recommendations.sh

echo ""
echo "[6/7] Feeding discovery queue..."
bash tools/brain/feed-discovery.sh

echo ""
echo "[7/7] Generating brain report..."
bash tools/brain/build-report.sh

echo ""
echo "============================================="
echo " Brain Engine complete."
echo " Queues: docs/brain/queues/"
echo " Reports: docs/brain/reports/"
echo "============================================="
