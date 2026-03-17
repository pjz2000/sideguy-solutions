#!/usr/bin/env bash
# tools/autobuilder/autobuilder.sh
# Supply creation: consume manifests → build new pages

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

MANIFEST_DIR="manifests/factory"
BUILD_LOG="logs/autobuilder-$(date +%Y%m%d).log"
mkdir -p logs

echo "-- AutoBuilder: scanning manifests --"

BUILT=0
SKIPPED=0

# Process any pending manifests in the factory queue
for manifest in "$MANIFEST_DIR"/*.csv; do
  [ -f "$manifest" ] || continue
  name=$(basename "$manifest")

  # Skip already-processed manifests (marked with .done)
  [ -f "$manifest.done" ] && { SKIPPED=$((SKIPPED + 1)); continue; }

  echo "  Processing: $name"

  # Delegate to autonomous builder if available
  if [ -f tools/autonomous-builder/run_builder.sh ]; then
    bash tools/autonomous-builder/run_builder.sh "$manifest" >> "$BUILD_LOG" 2>&1 || true
  fi

  touch "$manifest.done"
  BUILT=$((BUILT + 1))
done

# Also run the auto-builder Python runner if it exists
if [ -f tools/auto-builder/run_builder.py ]; then
  python3 tools/auto-builder/run_builder.py >> "$BUILD_LOG" 2>&1 || true
fi

TOTAL_PAGES=$(find public -name '*.html' | wc -l | tr -d ' ')

echo "-- AutoBuilder complete: $BUILT manifests processed, $TOTAL_PAGES total pages --"
