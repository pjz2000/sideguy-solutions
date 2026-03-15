#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

source docs/brain/config/brain-rules.env 2>/dev/null || true
THRESHOLD="${CLUSTER_DOMINANCE_THRESHOLD:-10}"

INPUT="docs/brain/queues/topic-momentum.csv"
OUTPUT="docs/brain/queues/cluster-dominance.csv"

if [ ! -f "$INPUT" ]; then
  echo "No topic-momentum.csv found. Run topic-momentum.sh first."
  exit 0
fi

echo "theme,count" > "$OUTPUT"
awk -F, -v t="$THRESHOLD" \
  'NR>1 && $2>=t { print }' \
  "$INPUT" >> "$OUTPUT"

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Cluster dominance: $COUNT dominant themes (threshold=${THRESHOLD})"
