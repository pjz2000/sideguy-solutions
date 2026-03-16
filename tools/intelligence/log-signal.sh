#!/bin/bash

TOPIC="$1"
ACTION="$2"
PAGE="$3"

if [ -z "$TOPIC" ] || [ -z "$ACTION" ] || [ -z "$PAGE" ]; then
  echo "Usage: ./tools/intelligence/log-signal.sh \"topic\" \"action\" \"page.html\""
  exit
fi

DATE=$(date +"%Y-%m-%d")
LOG="docs/signals/signal-log.md"

[ ! -f "$LOG" ] && cat <<EOF2 > "$LOG"
# SidePalantir Signal Log

Date | Signal | Action | Page
--- | --- | --- | ---
EOF2

echo "$DATE | $TOPIC | $ACTION | $PAGE" >> "$LOG"

echo "Logged:"
echo "$DATE | $TOPIC | $ACTION | $PAGE"
