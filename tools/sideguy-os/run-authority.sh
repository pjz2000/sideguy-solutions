#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "Running Authority Upgrade Engine"
echo ""

bash tools/million/million-phase-3.sh

echo ""
echo "Authority upgrades complete"
