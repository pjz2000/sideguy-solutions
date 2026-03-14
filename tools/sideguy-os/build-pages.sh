#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

read -rp "How many pages to build? " NUM

if ! [[ "$NUM" =~ ^[0-9]+$ ]]; then
  echo "Invalid number: $NUM"
  exit 1
fi

bash tools/page-builder/build_batch.sh "$NUM"

echo ""
echo "Pages built: $NUM"
