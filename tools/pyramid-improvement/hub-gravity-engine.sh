#!/usr/bin/env bash

HUBS="manifests/pyramid-improvement/hub-list.txt"

echo ""
echo "SideGuy Hub Gravity Scan"
echo "------------------------"

while read hub
do

[ -z "$hub" ] && continue

count=$(grep -R "$hub" . --include="*.html" | wc -l)

echo "Hub: $hub | mentions:$count"

done < "$HUBS"
