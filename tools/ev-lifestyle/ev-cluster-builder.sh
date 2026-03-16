#!/usr/bin/env bash

PROBLEMS="manifests/ev-lifestyle/problem-pages.txt"
SYSTEMS="manifests/ev-lifestyle/system-pages.txt"
DECISIONS="manifests/ev-lifestyle/decision-pages.txt"

OUT="logs/ev-cluster-map.txt"

echo "SideGuy EV Lifestyle Cluster Map" > "$OUT"
echo "" >> "$OUT"

while read p
do
[ -z "$p" ] && continue

while read s
do
[ -z "$s" ] && continue

while read d
do
[ -z "$d" ] && continue

echo "$p -> $s -> $d" >> "$OUT"

done < "$DECISIONS"

done < "$SYSTEMS"

done < "$PROBLEMS"

echo "Cluster map generated."
echo "See: $OUT"
