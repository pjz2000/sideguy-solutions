#!/usr/bin/env bash

echo "SideGuy 2035 Tech Radar"

FILE="docs/future-2035/clusters/future-clusters-2035.txt"

if [ ! -f "$FILE" ]; then
 echo "Missing cluster file"
 exit
fi

cat "$FILE"
