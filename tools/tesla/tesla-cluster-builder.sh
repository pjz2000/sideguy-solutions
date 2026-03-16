#!/bin/bash

PROBLEMS="manifests/tesla/tesla-problem-pages.txt"
SYSTEMS="manifests/tesla/tesla-system-pages.txt"
DECISIONS="manifests/tesla/tesla-decision-pages.txt"

echo ""
echo "SideGuy Tesla Cluster Builder"
echo "-----------------------------"

echo ""
echo "Problem pages:"
cat "$PROBLEMS"

echo ""
echo "System pages:"
cat "$SYSTEMS"

echo ""
echo "Decision pages:"
cat "$DECISIONS"
