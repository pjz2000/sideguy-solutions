#!/usr/bin/env bash

VERTICALS=7
HUBS_PER_VERTICAL=150
PAGES_PER_HUB=80

TOTAL=$((VERTICALS * HUBS_PER_VERTICAL * PAGES_PER_HUB))

echo ""
echo "SideGuy Million Page Simulator"
echo "--------------------------------"

echo "Verticals: $VERTICALS"
echo "Hubs per vertical: $HUBS_PER_VERTICAL"
echo "Pages per hub: $PAGES_PER_HUB"
echo ""

echo "Projected pages: $TOTAL"
echo ""

if [ "$TOTAL" -ge 1000000 ]; then
echo "Million page scale achievable."
else
echo "Increase hubs or pages per hub."
fi
