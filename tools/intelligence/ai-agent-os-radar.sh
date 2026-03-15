#!/usr/bin/env bash

echo "SideGuy AI Agent OS Radar"

FILE="docs/ai-agent-os/clusters/ai-agent-os-pages.txt"

if [ ! -f "$FILE" ]; then
 echo "Missing topic file"
 exit
fi

cat "$FILE"
