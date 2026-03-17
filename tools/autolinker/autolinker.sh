#!/usr/bin/env bash
# tools/autolinker/autolinker.sh
# Link graph: scan pages → inject internal links → update crawl graph

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

LINK_LOG="logs/autolinker-$(date +%Y%m%d).log"
mkdir -p logs

echo "-- AutoLinker: building link graph --"

# Run internal link engine
if [ -f tools/internal-links/run_link_engine.sh ]; then
  bash tools/internal-links/run_link_engine.sh >> "$LINK_LOG" 2>&1 || true
  echo "  Internal link engine complete"
fi

# Run crawl amplifier
if [ -f tools/crawl-amplifier/link_boost.py ]; then
  python3 tools/crawl-amplifier/link_boost.py >> "$LINK_LOG" 2>&1 || true
  echo "  Crawl amplifier complete"
fi

# Run link booster
if [ -f tools/booster/link-booster.sh ]; then
  bash tools/booster/link-booster.sh >> "$LINK_LOG" 2>&1 || true
  echo "  Link booster complete"
fi

# Build hub mesh
if [ -f tools/linking-mesh/run-mesh.sh ]; then
  bash tools/linking-mesh/run-mesh.sh >> "$LINK_LOG" 2>&1 || true
  echo "  Cluster mesh complete"
fi

# Snapshot edge count from map if available
EDGE_COUNT=0
if [ -f docs/map/data/edges.csv ]; then
  EDGE_COUNT=$(wc -l < docs/map/data/edges.csv | tr -d ' ')
fi

echo "-- AutoLinker complete: $EDGE_COUNT edges in graph --"
