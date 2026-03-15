#!/bin/bash

echo "=============================="
echo "SideGuy Money Decay Radar"
echo "=============================="

FILE="docs/money-theory/clusters/money-decay-pages.txt"

if [ ! -f "$FILE" ]; then
  echo "Money decay page list missing."
  exit
fi

echo ""
echo "Money Decay / Better Rails Topics:"
echo ""

cat "$FILE"

echo ""
echo "Next move:"
echo "Turn these into calm explanatory pages."
