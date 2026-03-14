#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

source docs/nervous/config/freshness-rules.env

INPUT="docs/nervous/queues/cluster-winners.csv"
OUTPUT="docs/nervous/queues/cluster-expansion.csv"

[ -f "$INPUT" ] || { echo "No cluster-winners.csv. Run detect-clusters.sh first."; exit 1; }

echo "theme,expansion_reason" > "$OUTPUT"

tail -n +2 "$INPUT" | while IFS=, read -r theme count; do
  [[ "$count" =~ ^[0-9]+$ ]] || continue
  if [ "$count" -gt "$CLUSTER_WINNER_THRESHOLD" ]; then
    echo "$theme,cluster_growth_signal" >> "$OUTPUT"
  fi
done

WINNERS=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Expansion queue built — $WINNERS themes queued"
