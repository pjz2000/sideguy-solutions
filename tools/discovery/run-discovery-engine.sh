#!/usr/bin/env bash

echo "-----------------------------------"
echo "Running SideGuy Discovery Engine"
echo "-----------------------------------"

bash tools/index/run-index-system.sh
bash tools/discovery/build-recent-pages.sh
bash tools/discovery/build-all-pages-index.sh

echo "Discovery pages built."

