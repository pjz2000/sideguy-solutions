#!/usr/bin/env bash

echo "===================================="
echo "Running SideGuy Production Cycle"
echo "===================================="

./tools/sideguy-brain.sh

echo ""
echo "Launching production builder..."

tools/production/production-builder.sh 500

echo ""
echo "Committing batch..."

git add .
git commit -m "SideGuy Production Batch"

echo ""
echo "Cycle complete."
