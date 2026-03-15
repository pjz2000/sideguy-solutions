#!/usr/bin/env bash

echo "SideGuy AI Orchestration Radar"

FILE="docs/ai-orchestration/clusters/ai-orchestration-pages.txt"

if [ ! -f "$FILE" ]; then
 echo "Missing topic file"
 exit
fi

cat "$FILE"
