#!/usr/bin/env bash

VERTICALS="${1:-10}"
HUBS="${2:-200}"
PAGES_PER_HUB="${3:-80}"

TOTAL=$((VERTICALS * HUBS * PAGES_PER_HUB))

echo ""
echo "SideGuy Foundation Growth Math"
echo "--------------------------------"

echo "Verticals: $VERTICALS"
echo "Hubs per vertical: $HUBS"
echo "Pages per hub: $PAGES_PER_HUB"

echo ""
echo "Projected pages: $TOTAL"
echo ""
