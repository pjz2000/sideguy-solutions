#!/bin/bash

echo "================================="
echo "SideGuy Future Radar Scan"
echo "================================="

RADAR="docs/future-radar/radar-topics.txt"

if [ ! -f "$RADAR" ]; then
  echo "Radar topic file missing"
  exit
fi

echo ""
echo "Tracked Future Topics:"
echo ""

cat $RADAR

echo ""
echo "Next step:"
echo "Create explanation pages for new radar topics."
