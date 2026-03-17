#!/usr/bin/env bash
# tools/authority/authority-engine.sh
# Authority boost: amplify winners, build hubs, update sitemap

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

LOG="logs/authority-engine-$(date +%Y%m%d).log"
mkdir -p logs

echo "-- Authority: amplifying winners --"

# Run the full authority pipeline
bash tools/authority/run-authority-engine.sh 2>&1 | tee -a "$LOG"

HUB_COUNT=$(find public/authority -maxdepth 1 -name "*.html" 2>/dev/null | wc -l | tr -d ' ')

echo "-- Authority complete: $HUB_COUNT authority pages --"
