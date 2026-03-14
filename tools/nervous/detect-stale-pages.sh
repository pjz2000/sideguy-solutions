#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

# shellcheck source=docs/nervous/config/freshness-rules.env
source docs/nervous/config/freshness-rules.env

INPUT="docs/nervous/page-scan.csv"
OUTPUT="docs/nervous/queues/stale-pages.csv"

[ -f "$INPUT" ] || { echo "No page-scan.csv. Run scan-pages.sh first."; exit 1; }

echo "file,age_days" > "$OUTPUT"

tail -n +2 "$INPUT" | while IFS=, read -r file mod age; do
  [[ "$age" =~ ^[0-9]+$ ]] || continue
  if [ "$age" -gt "$STALE_DAYS" ]; then
    echo "$file,$age" >> "$OUTPUT"
  fi
done

STALE=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Stale pages detected — $STALE pages older than ${STALE_DAYS} days"
