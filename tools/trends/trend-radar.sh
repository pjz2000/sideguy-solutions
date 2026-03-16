#!/bin/bash

SIGNALS="manifests/trends/emerging-tech.txt"
PROBLEMS="manifests/trends/future-problems.txt"

echo ""
echo "SideGuy Trend Radar"
echo "-------------------"

echo ""
echo "Emerging Technology Signals:"
cat "$SIGNALS"

echo ""
echo "Future Problem Searches:"
cat "$PROBLEMS"

echo ""
echo "These signals can become content clusters."
