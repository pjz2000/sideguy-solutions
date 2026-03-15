#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

source docs/brain/config/brain-rules.env 2>/dev/null || true
MAX="${MAX_UPGRADE_RECOMMENDATIONS:-75}"

INPUT="docs/brain/queues/internal-link-gravity.csv"
OUTPUT="docs/brain/queues/upgrade-recommendations.csv"

if [ ! -f "$INPUT" ]; then
  echo "No internal-link-gravity.csv found. Run internal-link-gravity.sh first."
  exit 0
fi

echo "page,reason" > "$OUTPUT"
awk -F, 'NR>1 && $2>0 { print $1",high_link_gravity" }' "$INPUT" | head -n "$MAX" >> "$OUTPUT"

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Upgrade recommendations: $COUNT pages queued (max=$MAX)"
