#!/bin/bash

echo "Cluster Scan"

for hub in $(cat manifests/cluster-intelligence/hubs.txt 2>/dev/null)
do
count=$(grep -R "$hub" *.html | wc -l)
echo "$hub → $count pages"
done
