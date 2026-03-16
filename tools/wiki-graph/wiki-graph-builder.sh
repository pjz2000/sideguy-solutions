#!/bin/bash

REL_FILE="manifests/wiki-graph/relationships.csv"
OUT="logs/wiki-graph-map.txt"

echo "SideGuy Wiki Graph Map" > "$OUT"
echo "" >> "$OUT"

tail -n +2 "$REL_FILE" | while IFS=',' read source target relation
do
echo "$source → $target ($relation)" >> "$OUT"
done

echo "Graph map generated"
