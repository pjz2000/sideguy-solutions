#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/brain/queues/build-recommendations.csv"
INBOX="docs/alive/inbox/brain-discovery.txt"

mkdir -p "$(dirname "$INBOX")"

if [ ! -f "$INPUT" ]; then
  echo "No build-recommendations.csv found. Nothing to feed."
  exit 0
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "# Brain discovery — $TIMESTAMP" >> "$INBOX"
awk -F, 'NR>1 { print $1 }' "$INPUT" >> "$INBOX"

COUNT=$(( $(wc -l < "$INPUT") - 1 ))
echo "Feed discovery: $COUNT themes appended to $INBOX"
