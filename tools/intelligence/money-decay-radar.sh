#!/usr/bin/env bash

echo "=============================="
echo "SideGuy Money Decay Radar"
echo "=============================="

FILE="docs/money-theory/clusters/money-decay-pages.txt"

if [ ! -f "$FILE" ]; then
  echo "Money decay topics missing."
  exit
fi

echo ""
echo "Money / Better Rails Topics:"
echo ""
cat "$FILE"
echo ""
echo "Next step: build calm explanatory pages."
