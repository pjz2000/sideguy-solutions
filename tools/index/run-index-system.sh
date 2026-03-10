#!/usr/bin/env bash

echo "-----------------------------------"
echo "Running SideGuy Page Index System"
echo "-----------------------------------"

bash tools/index/build-page-index.sh
bash tools/index/priority-from-index.sh
bash tools/index/gravity-from-index.sh

echo "Index system complete."

