#!/usr/bin/env bash

PROBLEMS="manifests/pyramid/problem-layer.txt"
SYSTEMS="manifests/pyramid/system-layer.txt"
RESOLUTIONS="manifests/pyramid/resolution-layer.txt"

OUT="logs/pyramid-map.txt"

> "$OUT"

while read p
do
[ -z "$p" ] && continue

while read s
do
[ -z "$s" ] && continue

while read r
do
[ -z "$r" ] && continue

echo "$p -> $s -> $r" >> "$OUT"

done < "$RESOLUTIONS"

done < "$SYSTEMS"

done < "$PROBLEMS"

echo "Pyramid clusters generated."
