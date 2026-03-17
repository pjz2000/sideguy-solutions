#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

INPUT="manifests/authority/topic-registry.json"
OUTPUT="docs/authority/coverage-scoreboard.md"
LOG="logs/coverage-scoreboard.log"

touch "$LOG"
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

{
  echo "# SideGuy Coverage Scoreboard"
  echo ""
  echo "Generated: $timestamp"
  echo ""
  echo "| Topic | Category | Priority | Page Count |"
  echo "|---|---|---|---|"

  jq -r '.[] | "| " + .title + " | " + .category + " | " + .priority + " | " + ((.pages | length) | tostring) + " |"' "$INPUT"
} > "$OUTPUT"

echo "[$timestamp] BUILT $OUTPUT" >> "$LOG"
echo "Built coverage scoreboard: $OUTPUT"
