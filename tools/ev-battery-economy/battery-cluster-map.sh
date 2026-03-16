#!/usr/bin/env bash

PROBLEMS="manifests/ev-battery-economy/problem-pages.txt"
SYSTEMS="manifests/ev-battery-economy/system-pages.txt"
FUTURE="manifests/ev-battery-economy/future-pages.txt"

OUT="logs/ev-battery-cluster-map.txt"

echo "SideGuy EV Battery Economy Cluster Map" > "$OUT"
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
