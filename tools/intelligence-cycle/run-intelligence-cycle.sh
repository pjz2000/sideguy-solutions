#!/usr/bin/env bash

echo "--------------------------------------"
echo "SideGuy Intelligence Cycle"
echo "--------------------------------------"

echo "Step 1: run trend radar"
bash tools/trend-radar/trend-radar.sh

echo "Step 2: rebuild page index"
bash tools/index/run-index-system.sh

echo "Step 3: rebuild discovery pages"
bash tools/discovery/run-discovery-engine.sh

echo "Step 4: run gravity engine"
bash tools/gravity/run-gravity.sh

echo "Step 5: update sitemap"
node update-sitemap.js

echo "Step 6: commit intelligence updates"
git add -A
git commit -m "SideGuy intelligence cycle update"

echo "Cycle complete."
