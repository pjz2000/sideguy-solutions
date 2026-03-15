#!/usr/bin/env bash

echo "SideGuy Intelligence Engine"

SIGNALS="docs/intelligence/signals/tech-signals.txt"

if [ ! -f "$SIGNALS" ]; then
 echo "Signal list missing."
 exit
fi

cat "$SIGNALS"
