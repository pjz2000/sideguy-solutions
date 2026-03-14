#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/nervous/queues/cluster-expansion.csv"
[ -f "$INPUT" ] || { echo "No cluster-expansion.csv found."; exit 0; }

mkdir -p docs/alive/inbox

SENT=0
tail -n +2 "$INPUT" | while IFS=, read -r theme reason; do
  [ -z "$theme" ] && continue
  echo "$theme expansion opportunities" >> docs/alive/inbox/cluster-expansion.txt
  SENT=$((SENT+1))
done

echo "Expansion signals sent to Alive Engine inbox"
