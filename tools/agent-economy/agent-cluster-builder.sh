#!/bin/bash

PROBLEMS="manifests/agent-economy/problem-pages.txt"
SYSTEMS="manifests/agent-economy/system-pages.txt"
DECISIONS="manifests/agent-economy/decision-pages.txt"
FUTURE="manifests/agent-economy/future-pages.txt"

echo ""
echo "SideGuy Autonomous Agent Economy Cluster"
echo "----------------------------------------"

echo ""
echo "Problem pages:"
cat "$PROBLEMS"

echo ""
echo "System pages:"
cat "$SYSTEMS"

echo ""
echo "Decision pages:"
cat "$DECISIONS"

echo ""
echo "Future pages:"
cat "$FUTURE"
