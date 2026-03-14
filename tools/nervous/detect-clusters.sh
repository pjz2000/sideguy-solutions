#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

# Cluster detection works from either alive scored topics or the wave-selection
INPUT_ALIVE="docs/alive/manifests/alive-topic-ideas-scored.csv"
INPUT_WAVE="docs/million-page/selected/wave-selection.csv"
OUTPUT="docs/nervous/queues/cluster-winners.csv"

echo "theme,count" > "$OUTPUT"

# Use whichever source exists
if [ -f "$INPUT_ALIVE" ]; then
  awk -F, 'NR>1 {gsub(/"/,"",$2); count[$2]++}
    END { for(t in count) if(t!="") print t","count[t] }' \
    "$INPUT_ALIVE" | sort -t, -k2,2nr >> "$OUTPUT"
elif [ -f "$INPUT_WAVE" ]; then
  # col 4 = theme (0-indexed: $4 in 1-indexed awk)
  awk -F, 'NR>1 {gsub(/"/,"",$4); count[$4]++}
    END { for(t in count) if(t!="") print t","count[t] }' \
    "$INPUT_WAVE" | sort -t, -k2,2nr >> "$OUTPUT"
else
  echo "No input data found for cluster detection."
  exit 0
fi

CLUSTERS=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Cluster detection complete — $CLUSTERS themes found"
