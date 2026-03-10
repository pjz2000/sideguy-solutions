#!/usr/bin/env bash

echo "-----------------------------------"
echo "Running SideGuy Hub Engine"
echo "-----------------------------------"

bash tools/hubs/discover-topic-hubs.sh
bash tools/hubs/build-hubs.sh 20

echo "Hub engine complete."
