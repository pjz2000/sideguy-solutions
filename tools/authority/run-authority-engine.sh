#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 0

LOG="logs/authority-run.log"
touch "$LOG"

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "" >> "$LOG"
echo "[$timestamp] AUTHORITY RUN START" >> "$LOG"

bash tools/authority/build-authority-hub.sh
bash tools/authority/build-topic-hubs.sh
bash tools/authority/build-link-map.sh
bash tools/authority/build-authority-sitemap-snippets.sh
bash tools/authority/build-coverage-scoreboard.sh

hub_count=$(find public/authority -maxdepth 1 -name "*.html" | wc -l | tr -d ' ')
topic_count=$(jq 'length' manifests/authority/topic-registry.json)

echo "[$timestamp] HUB COUNT $hub_count" >> "$LOG"
echo "[$timestamp] TOPIC COUNT $topic_count" >> "$LOG"
echo "[$timestamp] AUTHORITY RUN END" >> "$LOG"

echo ""
echo "=========================================="
echo "AUTHORITY ENGINE COMPLETE"
echo "Topic zones: $topic_count"
echo "Authority HTML files: $hub_count"
echo "Master hub: public/authority/index.html"
echo "Coverage scoreboard: docs/authority/coverage-scoreboard.md"
echo "Internal link map: docs/authority/internal-link-map.md"
echo "Sitemap snippets: docs/authority/authority-sitemap-snippets.txt"
echo "=========================================="
echo ""
