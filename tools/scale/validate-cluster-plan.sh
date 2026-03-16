#!/usr/bin/env bash

PLAN="$1"
REPORT="logs/cluster-validation.txt"

mkdir -p logs
: > "$REPORT"

if [ ! -f "$PLAN" ]; then
echo "Plan not found"
exit 0
fi

tail -n +2 "$PLAN" | while IFS=',' read type slug title parent vertical locality intent notes
do

status="PASS"

if [ -z "$slug" ] || [ -z "$parent" ]; then
status="CHECK"
fi

echo "$status | $type | $slug | hub:$parent | intent:$intent" >> "$REPORT"

done

echo "Validation written:"
echo "$REPORT"
