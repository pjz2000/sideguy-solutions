#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

OUTPUT="docs/brain/queues/topic-momentum.csv"

# Use wave-selection as fallback if alive scored topics not yet present
INPUT_ALIVE="docs/alive/manifests/alive-topic-ideas-scored.csv"
INPUT_WAVE="docs/million-page/selected/wave-selection.csv"

echo "theme,count" > "$OUTPUT"

if [ -f "$INPUT_ALIVE" ]; then
  awk -F, 'NR>1 { gsub(/"/,"",$2); if($2!="") count[$2]++ }
    END { for(t in count) print t","count[t] }' \
    "$INPUT_ALIVE" | sort -t, -k2,2nr >> "$OUTPUT"
elif [ -f "$INPUT_WAVE" ]; then
  awk -F, 'NR>1 { gsub(/"/,"",$4); if($4!="") count[$4]++ }
    END { for(t in count) print t","count[t] }' \
    "$INPUT_WAVE" | sort -t, -k2,2nr >> "$OUTPUT"
else
  echo "No topic input found."
  exit 0
fi

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Topic momentum calculated — $COUNT themes"
