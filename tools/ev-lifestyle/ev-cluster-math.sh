#!/usr/bin/env bash

PROBLEMS="${1:-40}"
SYSTEMS="${2:-15}"
DECISIONS="${3:-15}"

TOTAL=$((PROBLEMS + SYSTEMS + DECISIONS))

echo ""
echo "SideGuy EV Lifestyle Cluster Math"
echo "----------------------------------"

echo "Problem pages: $PROBLEMS"
echo "System pages: $SYSTEMS"
echo "Decision pages: $DECISIONS"

echo ""
echo "Total cluster pages: $TOTAL"
echo ""
