#!/usr/bin/env bash

echo "SideGuy Local Problem Radar"

FILE="docs/local-problems/clusters/local-problem-clusters.txt"

if [ ! -f "$FILE" ]; then
 echo "Local problem list missing."
 exit
fi

cat "$FILE"
