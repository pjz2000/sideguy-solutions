#!/usr/bin/env bash

# =========================================
# SIGNAL PIPELINE ORCHESTRATOR
# search-style signals
#   → categorized topic buckets
#   → new page ideas
#   → trend radar + problem engine + lattice
# =========================================

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$ROOT"

echo "========================================"
echo "SideGuy Signal Pipeline"
echo "========================================"
echo ""

echo "[ Stage 1 ] Ingesting signals..."
bash tools/signals/ingest-signals.sh
echo ""

echo "[ Stage 2 ] Categorizing into topic buckets..."
bash tools/signals/categorize-signals.sh
echo ""

echo "[ Stage 3 ] Generating page ideas..."
bash tools/signals/generate-page-ideas.sh
echo ""

echo "[ Stage 4 ] Feeding downstream tools..."
bash tools/signals/feed-downstream.sh
echo ""

echo "========================================"
echo "Signal Pipeline Complete"
echo ""
echo "Outputs:"
echo "  docs/signals/ingested-signals.txt"
echo "  docs/signals/categorized-signals.tsv"
echo "  docs/signals/page-ideas.txt"
echo ""
echo "Downstream updated:"
echo "  docs/trend-radar/trend-signals.txt"
echo "  docs/problem-engine/problem-page-ideas.txt"
echo "  docs/manifests/lattice/child-topics.txt"
echo ""
echo "Next: review docs/signals/page-ideas.txt"
echo "Then: bash tools/production/production-builder.sh 500"
echo "========================================"
