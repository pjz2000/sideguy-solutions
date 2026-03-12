#!/usr/bin/env bash

echo "SideGuy Fast Mode"
echo ""

git config --global core.preloadindex true
git config --global gc.auto 0

echo "Cleaning stale dev processes..."
pkill -f "python3 tools" 2>/dev/null || true
pkill -f "node.*next" 2>/dev/null || true

echo ""
echo "System snapshot:"
top -b -n1 | head -15

echo ""
echo "Fast mode ready."
