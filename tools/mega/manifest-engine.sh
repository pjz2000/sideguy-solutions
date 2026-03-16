#!/usr/bin/env bash

VERTICALS="manifests/mega/mega-verticals.txt"
HUBS="manifests/hubs/hub-inventory.txt"

OUT="manifests/mega/million-engine.csv"

echo "type,slug,title,vertical,parent" > "$OUT"

while read vertical
do

[ -z "$vertical" ] && continue

while read hub
do

[ -z "$hub" ] && continue

echo "hub,$hub,$hub,$vertical,root" >> "$OUT"
echo "problem,what-is-$hub,what is $hub,$vertical,$hub" >> "$OUT"
echo "problem,how-does-$hub-work,how does $hub work,$vertical,$hub" >> "$OUT"
echo "comparison,$hub-vs-traditional,$hub vs traditional,$vertical,$hub" >> "$OUT"

done < "$HUBS"

done < "$VERTICALS"

echo "Mega manifest generated."
