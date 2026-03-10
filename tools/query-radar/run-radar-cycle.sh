#!/usr/bin/env bash

echo "--------------------------------"
echo "Running SideGuy Radar Cycle"
echo "--------------------------------"

bash tools/index/run-index-system.sh
bash tools/query-radar/run-query-radar.sh
bash tools/query-radar/feed-expansion.sh

echo "Radar cycle complete."

