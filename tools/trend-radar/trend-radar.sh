#!/bin/bash

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

SIGNALS="$ROOT/docs/trend-radar/trend-signals.txt"

if [ ! -f "$SIGNALS" ]; then
  echo "Trend signals file not found."
  exit 1
fi

echo "SideGuy Trend Radar"
echo "-------------------"

echo ""
echo "Active signals:"
echo ""

cat "$SIGNALS"

echo ""
echo "Suggested page topics:"
echo ""

cat "$SIGNALS" \
| sed 's/$/ explained/' \
| sed 's/^/what is /'

echo ""
echo "Trend radar scan complete."
