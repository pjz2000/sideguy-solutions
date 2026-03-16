#!/usr/bin/env bash

VERTICAL_FILE="manifests/mega/mega-verticals.txt"
HUB_FILE="manifests/hubs/hub-inventory.txt"

OUT="manifests/mega/million-engine.csv"
LOG="logs/million-engine.log"

mkdir -p logs

echo "type,slug,title,vertical,parent" > "$OUT"

ROWS=0

slug_to_title () {
echo "$1" | tr '-' ' '
}

while IFS= read -r vertical
do

[ -z "$vertical" ] && continue

echo "Processing vertical: $vertical"

while IFS= read -r hub
do

[ -z "$hub" ] && continue

title=$(slug_to_title "$hub")

echo "hub,$hub,$title,$vertical,root" >> "$OUT"
ROWS=$((ROWS+1))

echo "problem,what-is-$hub,what is $title,$vertical,$hub" >> "$OUT"
echo "problem,how-does-$hub-work,how does $title work,$vertical,$hub" >> "$OUT"
echo "problem,benefits-of-$hub,benefits of $title,$vertical,$hub" >> "$OUT"

echo "comparison,$hub-vs-traditional,$title vs traditional,$vertical,$hub" >> "$OUT"
echo "comparison,best-$hub-tools,best $title tools,$vertical,$hub" >> "$OUT"

echo "local,$hub-san-diego,$title san diego,$vertical,$hub" >> "$OUT"
echo "local,$hub-california,$title california,$vertical,$hub" >> "$OUT"

ROWS=$((ROWS+7))

done < "$HUB_FILE"

done < "$VERTICAL_FILE"

STAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "[$STAMP] Manifest rows generated: $ROWS" >> "$LOG"

echo ""
echo "Manifest engine complete."
echo "Rows: $ROWS"
echo "Output: $OUT"
echo ""
