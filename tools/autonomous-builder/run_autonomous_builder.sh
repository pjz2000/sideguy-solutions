#!/usr/bin/env bash
PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo ""
echo "================================="
echo "SideGuy Autonomous Page Builder"
echo "================================="
echo ""
echo "1 Build master manifest"
echo "2 Split into 500-page queues"
echo "3 Build one batch"
echo "4 Run setup + build first batch"
echo ""
read -p "Select option: " OPT

if [ "$OPT" = "1" ]; then
  python3 tools/autonomous-builder/build_manifest.py
elif [ "$OPT" = "2" ]; then
  python3 tools/autonomous-builder/split_manifest.py
elif [ "$OPT" = "3" ]; then
  read -p "Batch file path: " BATCH
  bash tools/autonomous-builder/run_builder.sh "$BATCH"
elif [ "$OPT" = "4" ]; then
  python3 tools/autonomous-builder/build_manifest.py
  python3 tools/autonomous-builder/split_manifest.py
  bash tools/autonomous-builder/run_builder.sh "docs/autonomous-builder/queues/batch-0001.tsv"
else
  echo "Invalid option."
fi
