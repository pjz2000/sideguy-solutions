#!/usr/bin/env bash

echo "--------------------------------------"
echo "Running SideGuy Expansion System"
echo "--------------------------------------"

bash tools/expansion/build-expansion-manifest.sh
bash tools/expansion/build-expansion-batch.sh 500

echo "Expansion run complete."
