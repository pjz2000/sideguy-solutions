#!/usr/bin/env bash
# tools/trends/trend-engine.sh
# Trend ingestion pipeline: radar → manifest → queue

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

TREND_DIR="docs/trends"
mkdir -p "$TREND_DIR/processed" "$TREND_DIR/queues"

echo "-- Trends: scanning --"

# Stage 1: run trend radar (generates trend-manifest + report)
if [ -f tools/trends/trend-radar.sh ]; then
  bash tools/trends/trend-radar.sh
fi

# Stage 2: cluster generator from trend signals
if [ -f tools/trends/cluster-generator.sh ]; then
  bash tools/trends/cluster-generator.sh
fi

# Stage 3: compute trend math (opportunity scoring)
if [ -f tools/trends/trend-math.sh ]; then
  bash tools/trends/trend-math.sh
fi

# Snapshot
MANIFEST_COUNT=$(find manifests/factory -name "trend-manifest-*.csv" 2>/dev/null | wc -l | tr -d ' ')

echo "-- Trends complete: $MANIFEST_COUNT trend manifests ready --"
