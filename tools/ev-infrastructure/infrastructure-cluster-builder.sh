#!/usr/bin/env bash

PROBLEMS="manifests/ev-infrastructure/problem-pages.txt"
SYSTEMS="manifests/ev-infrastructure/system-pages.txt"
FUTURE="manifests/ev-infrastructure/future-pages.txt"

OUT="logs/ev-infrastructure-map.txt"

echo "SideGuy EV Infrastructure Cluster Map" > "$OUT"
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
