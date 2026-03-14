#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

QUEUE="data/matrix-queue/all-slugs.txt"
LIMIT="${1:-50}"

if [ ! -f "$QUEUE" ]; then
  echo "ERROR: Slug queue not found. Run hyper-matrix-engine.sh first."
  exit 1
fi

COUNT=0

echo ""
echo "Building $LIMIT pages from $QUEUE..."
echo ""

while IFS= read -r SLUG; do
  [[ -z "$SLUG" ]] && continue

  if [ "$COUNT" -ge "$LIMIT" ]; then
    break
  fi

  python3 tools/page-builder/build_from_slug.py "$SLUG"
  COUNT=$((COUNT+1))

done < "$QUEUE"

echo ""
echo "Built pages: $COUNT"
echo ""
