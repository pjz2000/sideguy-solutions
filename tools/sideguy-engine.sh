#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo ""
echo "========================================"
echo "🧠 SIDEGUY ENGINE :: FULL SYSTEM RUN"
echo "========================================"
echo ""

########################################
# 1. SIGNAL INGESTION (REAL DEMAND)
########################################

echo "== Signals :: ingest + process =="
bash tools/signals/signal-engine.sh

echo ""

########################################
# 2. TREND INGESTION (FUTURE DEMAND)
########################################

echo "== Trends :: ingest + process =="
bash tools/trends/trend-engine.sh

echo ""

########################################
# 3. BUILD PAGES (SUPPLY CREATION)
########################################

echo "== AutoBuilder :: create pages =="
bash tools/autobuilder/autobuilder.sh

echo ""

########################################
# 4. LINK GRAPH (AUTHORITY FLOW)
########################################

echo "== AutoLinker :: connect pages =="
bash tools/autolinker/autolinker.sh

echo ""

########################################
# 5. AUTHORITY BOOST (WINNERS)
########################################

echo "== Authority :: amplify winners =="
bash tools/authority/authority-engine.sh

echo ""

########################################
# 6. SNAPSHOT METRICS
########################################

TOTAL_PAGES=$(find public -name '*.html' | wc -l | tr -d ' ')

echo "========================================"
echo "📊 SIDEGUY STATUS"
echo "========================================"
echo "Total Pages: $TOTAL_PAGES"
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

echo "🔥 Engine cycle complete."
echo ""
