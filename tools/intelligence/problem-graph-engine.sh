#!/usr/bin/env bash

echo "=============================="
echo "SideGuy Problem Graph Engine"
echo "=============================="

PROBLEMS="docs/problem-graph/problems/problem-list.txt"

if [ ! -f "$PROBLEMS" ]; then
  echo "Problem list missing."
  exit
fi

echo ""
echo "Tracked Problems:"
echo ""
cat "$PROBLEMS"
echo ""
echo "Use these to create explanation pages and skill mappings."
