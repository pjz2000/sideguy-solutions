#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "Running ALL SideGuy Engines..."
echo ""

bash tools/auto-loop/run.sh
bash tools/confusion/run.sh
bash tools/local/run.sh
bash tools/prediction/run.sh

echo ""
echo "=================================="
echo "ALL ENGINES COMPLETE"
echo "=================================="
echo ""
