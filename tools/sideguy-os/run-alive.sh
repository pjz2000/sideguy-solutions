#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "Running SideGuy Alive Engine"
echo ""

if [ -f tools/alive/alive-engine.sh ]; then
  bash tools/alive/alive-engine.sh
else
  echo "Alive Engine not yet installed at tools/alive/alive-engine.sh"
fi

echo ""
echo "Alive Engine finished"
