#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "Running Hyper Matrix Generator"
echo ""

bash tools/intelligence/hyper-matrix-engine.sh

echo ""
echo "Million Engine finished"
