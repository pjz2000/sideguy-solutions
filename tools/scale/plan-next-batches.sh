#!/bin/bash

# =========================================
# SIDEGUY — NEXT BATCH PLANNER
# Reads manifests and calculates batch size.
# =========================================

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
MANIFESTS="$ROOT/docs/manifests/scale-batches"

TOPICS=$(grep -cv '^#\|^$' "$MANIFESTS/batch-001-core-topics.txt" 2>/dev/null || echo 0)
CITIES=$(grep -cv '^#\|^$' "$MANIFESTS/batch-001-cities.txt" 2>/dev/null || echo 0)
INDUSTRIES=$(grep -cv '^#\|^$' "$MANIFESTS/batch-001-industries.txt" 2>/dev/null || echo 0)

CORE_PAGES=$((TOPICS * 5))
INDUSTRY_PAGES=$((TOPICS * INDUSTRIES * 3))
LOCAL_PAGES=$((TOPICS * CITIES * 3))
TOTAL=$((CORE_PAGES + INDUSTRY_PAGES + LOCAL_PAGES))

echo "SideGuy Next Batch Planner"
echo "--------------------------"
echo ""
echo "Manifests loaded:"
echo "  Topics:     $TOPICS"
echo "  Cities:     $CITIES"
echo "  Industries: $INDUSTRIES"
echo ""
echo "Estimated pages:"
echo "  Core pages      ($TOPICS topics × 5):                  $CORE_PAGES"
echo "  Industry pages  ($TOPICS topics × $INDUSTRIES industries × 3):  $INDUSTRY_PAGES"
echo "  Local pages     ($TOPICS topics × $CITIES cities × 3):          $LOCAL_PAGES"
echo "  -----------------------------------------------"
echo "  TOTAL BATCH:                                     $TOTAL"
echo ""

CURRENT=$(find "$ROOT" -maxdepth 1 -name "*.html" | wc -l)
echo "Current root page count: $CURRENT"
echo "After batch:             $((CURRENT + TOTAL))"
echo ""
echo "Run: bash tools/scale/generate-100k-batch.sh"
