#!/usr/bin/env bash

VERTICALS=7
HUBS=150
PAGES_PER_HUB=80

TOTAL=$((VERTICALS * HUBS * PAGES_PER_HUB))

echo ""
echo "SideGuy Million Simulator"
echo "Verticals: $VERTICALS"
echo "Hubs per vertical: $HUBS"
echo "Pages per hub: $PAGES_PER_HUB"
echo ""
echo "Projected pages: $TOTAL"
echo ""
