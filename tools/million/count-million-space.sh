#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

for f in docs/million-page/manifests/*.csv; do
  [ -f "$f" ] || continue
  COUNT=$(( $(wc -l < "$f") - 1 ))
  echo "$(basename "$f"): $COUNT rows"
done

TOTAL=$(awk 'FNR>1 {n++} END {print n+0}' docs/million-page/manifests/*.csv 2>/dev/null)
echo ""
echo "TOTAL PAGE SPACE: $TOTAL"
