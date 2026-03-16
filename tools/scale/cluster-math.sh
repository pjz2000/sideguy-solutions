#!/usr/bin/env bash

VERTICALS="${1:-10}"
HUBS_PER_VERTICAL="${2:-10}"
PROBLEMS_PER_HUB="${3:-50}"
COMPARISONS_PER_HUB="${4:-10}"
LOCALS_PER_HUB="${5:-20}"

TOTAL_HUBS=$((VERTICALS * HUBS_PER_VERTICAL))
TOTAL_PROBLEMS=$((TOTAL_HUBS * PROBLEMS_PER_HUB))
TOTAL_COMPARISONS=$((TOTAL_HUBS * COMPARISONS_PER_HUB))
TOTAL_LOCALS=$((TOTAL_HUBS * LOCALS_PER_HUB))

TOTAL=$((TOTAL_HUBS + TOTAL_PROBLEMS + TOTAL_COMPARISONS + TOTAL_LOCALS))

echo ""
echo "SideGuy Cluster Math"
echo "---------------------"
echo "Verticals: $VERTICALS"
echo "Hubs/Vertical: $HUBS_PER_VERTICAL"
echo "Problems/Hub: $PROBLEMS_PER_HUB"
echo "Comparisons/Hub: $COMPARISONS_PER_HUB"
echo "Local/Hub: $LOCALS_PER_HUB"
echo ""
echo "Total Hubs: $TOTAL_HUBS"
echo "Problem Pages: $TOTAL_PROBLEMS"
echo "Comparison Pages: $TOTAL_COMPARISONS"
echo "Local Pages: $TOTAL_LOCALS"
echo ""
echo "TOTAL PAGES: $TOTAL"
echo ""

if [ "$TOTAL" -ge 1000000 ]; then
echo "Million-page capable configuration reached."
else
echo "Below million scale."
fi
