#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/radar/emerging-signals.txt"

mkdir -p "$ROOT/docs/radar"

echo "Scanning for emerging signals..."

DATE=$(date)

echo "---- Signal Scan $DATE ----" >> "$OUTPUT"

signals=(
"AI agents for small businesses"
"machine-to-machine payments"
"autonomous energy trading"
"stablecoin business payments"
"AI customer support automation"
"software cost automation tools"
"robots paying for EV charging"
"AI operations for contractors"
)

for s in "${signals[@]}"
do
  echo "$s" >> "$OUTPUT"
done

echo "Signals written to $OUTPUT"
