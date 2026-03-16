#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo ""
echo "=================================================="
echo "SideGuy Inventory Brain"
echo "=================================================="
echo ""

python3 tools/inventory-brain/build-inventory.py
python3 tools/inventory-brain/cluster-strength.py
python3 tools/inventory-brain/build-upgrade-queue.py
python3 tools/inventory-brain/build-freshness-queue.py
python3 tools/inventory-brain/build-link-queue.py

echo ""
echo "Reports created:"
echo "docs/inventory-brain/reports/master-inventory.tsv"
echo "docs/inventory-brain/reports/strong-clusters.md"
echo "docs/inventory-brain/reports/weak-clusters.md"
echo "docs/inventory-brain/reports/priority-upgrade-queue.md"
echo "docs/inventory-brain/reports/freshness-queue.md"
echo "docs/inventory-brain/reports/link-improvement-queue.md"
echo ""
