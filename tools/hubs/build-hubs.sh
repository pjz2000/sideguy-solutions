#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INPUT="$ROOT/docs/hubs/topic-hub-candidates.txt"
TEMPLATE="$ROOT/seo-template.html"

LIMIT="${1:-20}"

count=0

while read -r line
do

slug=$(echo "$line" | awk '{print $2}')

hub="$slug-knowledge-hub.html"

if [ -f "$hub" ]; then
    continue
fi

cp "$TEMPLATE" "$hub"

title=$(echo "$slug" | tr '-' ' ')

perl -0pi -e "s|PAGE_TITLE|$title Knowledge Hub | SideGuy|g" "$hub"
perl -0pi -e "s|PAGE_HEADING|$title Knowledge Hub|g" "$hub"

echo "CREATE HUB $hub"

count=$((count+1))

if [ "$count" -ge "$LIMIT" ]; then
    break
fi

done < "$INPUT"
