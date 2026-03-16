#!/usr/bin/env bash

PROBLEMS="manifests/machine-energy/problem-pages.txt"
SYSTEMS="manifests/machine-energy/system-pages.txt"
FUTURE="manifests/machine-energy/future-pages.txt"

OUT="logs/machine-energy-cluster-map.txt"

echo "SideGuy Machine Energy Cluster Map" > "$OUT"
echo "" >> "$OUT"

while read p
do
[ -z "$p" ] && continue

while read s
do
[ -z "$s" ] && continue

while read f
do
[ -z "$f" ] && continue

echo "$p -> $s -> $f" >> "$OUT"

done < "$FUTURE"

done < "$SYSTEMS"

done < "$PROBLEMS"

echo "Cluster map generated."
echo "See: $OUT"
