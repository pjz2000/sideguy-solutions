#!/usr/bin/env bash

LOCATIONS="${1:-1000}"
CHARGERS="${2:-10}"

TOTAL=$((LOCATIONS * CHARGERS))

echo ""
echo "EV Infrastructure Expansion Math"
echo "--------------------------------"

echo "Locations: $LOCATIONS"
echo "Chargers per location: $CHARGERS"

echo ""
echo "Total charging spots: $TOTAL"
echo ""
