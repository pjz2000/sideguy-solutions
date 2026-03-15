#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

source docs/brain/config/brain-rules.env 2>/dev/null || true
MAX="${MAX_BUILD_RECOMMENDATIONS:-100}"

INPUT="docs/brain/queues/cluster-dominance.csv"
OUTPUT="docs/brain/queues/build-recommendations.csv"

if [ ! -f "$INPUT" ]; then
  echo "No cluster-dominance.csv found. Run cluster-dominance.sh first."
  exit 0
fi

echo "theme,action" > "$OUTPUT"
awk -F, 'NR>1 { print $1",expand_cluster" }' "$INPUT" | head -n "$MAX" >> "$OUTPUT"

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Build recommendations: $COUNT themes queued (max=$MAX)"
