#!/usr/bin/env bash

echo "===================================="
echo "Running SideGuy Intelligence Stack"
echo "===================================="

tools/intelligence/signal-harvester.sh
tools/problem-expansion/problem-expander.sh
tools/intelligence/priority-engine.sh
tools/intelligence/authority-map.sh
tools/intelligence/discover-hubs.sh
tools/intelligence/problem-map.sh
tools/upgrades/authority-upgrader.sh

echo "===================================="
echo "SideGuy Intelligence Run Complete"
echo "===================================="
