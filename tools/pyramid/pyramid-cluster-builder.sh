#!/usr/bin/env bash

PROBLEMS="manifests/pyramid/problem-layer.txt"
SYSTEMS="manifests/pyramid/system-layer.txt"
RESOLUTIONS="manifests/pyramid/resolution-layer.txt"

OUT="logs/pyramid-clusters.txt"
CSV="logs/pyramid-clusters.csv"

echo "problem,system,resolution" > "$CSV"
echo "SideGuy Pyramid Clusters" > "$OUT"

while IFS= read -r problem
do
[ -z "$problem" ] && continue

echo "" >> "$OUT"
echo "Problem: $problem" >> "$OUT"

while IFS= read -r system
do
[ -z "$system" ] && continue

echo "  System: $system" >> "$OUT"

while IFS= read -r resolution
do
[ -z "$resolution" ] && continue

echo "    Resolution: $resolution" >> "$OUT"
echo "$problem,$system,$resolution" >> "$CSV"

done < "$RESOLUTIONS"

done < "$SYSTEMS"

done < "$PROBLEMS"

echo ""
echo "Pyramid clusters built"
echo "Text output: $OUT"
echo "CSV output: $CSV"
