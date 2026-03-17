#!/usr/bin/env bash
# tools/signals/signal-engine.sh
# Signal ingestion pipeline: ingest → categorize → score → output queue

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

SIGNAL_DIR="docs/signals"
PROCESSED="$SIGNAL_DIR/processed"
mkdir -p "$PROCESSED"

echo "-- Signals: ingesting --"

# Stage 1: ingest raw signals
bash tools/signals/ingest-signals.sh

# Stage 2: categorize
if [ -f tools/signals/categorize-signals.sh ]; then
  bash tools/signals/categorize-signals.sh
fi

# Stage 3: generate page ideas from signals
if [ -f tools/signals/generate-page-ideas.sh ]; then
  bash tools/signals/generate-page-ideas.sh
fi

# Stage 4: feed downstream queues
if [ -f tools/signals/feed-downstream.sh ]; then
  bash tools/signals/feed-downstream.sh
fi

# Snapshot
SIGNAL_COUNT=0
if [ -f "$SIGNAL_DIR/ingested-signals.txt" ]; then
  SIGNAL_COUNT=$(wc -l < "$SIGNAL_DIR/ingested-signals.txt" | tr -d ' ')
fi

echo "-- Signals complete: $SIGNAL_COUNT signals processed --"
