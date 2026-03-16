#!/bin/bash

PROBLEMS="${1:-50}"
SYSTEMS="${2:-20}"
DECISIONS="${3:-20}"

TOTAL=$((PROBLEMS + SYSTEMS + DECISIONS))

echo ""
echo "SideGuy Tesla Cluster Math"
echo "---------------------------"

echo "Problem pages: $PROBLEMS"
echo "System pages: $SYSTEMS"
echo "Decision pages: $DECISIONS"

echo ""
echo "Total cluster pages: $TOTAL"
echo ""
