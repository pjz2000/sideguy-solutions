#!/usr/bin/env bash

echo ""
echo "=========================================="
echo "SIDEGUY FULL LOOP (INTENT MODE)"
echo "=========================================="
echo ""

cd /workspaces/sideguy-solutions || exit 0

echo "STEP 1: GSC PULL"
python3 tools/intelligence/gsc-query-pull.py

echo ""
echo "STEP 2: EXPAND"
bash tools/intelligence/query-auto-expander.sh

echo ""
echo "STEP 3: INTENT BOOST"
bash tools/intelligence/intent-boost.sh

echo ""
echo "STEP 4: BUILD TARGETS"
bash tools/intelligence/intent-action.sh

echo ""
echo "DONE"
echo "Check:"
echo "manifests/intent/build-now.txt"
echo ""
