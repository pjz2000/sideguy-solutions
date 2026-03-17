#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

INPUT="manifests/authority/topic-registry.json"
OUTPUT="docs/authority/authority-sitemap-snippets.txt"
LOG="logs/authority-sitemap.log"

touch "$LOG"
timestamp=$(date +"%Y-%m-%d %H:%M:%S")

{
  echo "https://sideguy.solutions/authority/index.html"
  jq -r '.[] | "https://sideguy.solutions/authority/" + .slug + ".html"' "$INPUT"
} > "$OUTPUT"

echo "[$timestamp] BUILT $OUTPUT" >> "$LOG"
echo "Built sitemap snippets: $OUTPUT"
