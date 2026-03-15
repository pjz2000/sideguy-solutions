#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

TOPICS="docs/million-engine/topics.txt"
MODS="docs/million-engine/modifiers.txt"

OUT="docs/problem-reserve/generated-page-ideas.txt"

if [ ! -f "$TOPICS" ]; then
 echo "Missing topics file"
 exit
fi

if [ ! -f "$MODS" ]; then
 echo "Missing modifiers file"
 exit
fi

echo "" > "$OUT"

while read topic; do
 while read mod; do
   slug="$topic-$mod"
   echo "$slug" >> "$OUT"
 done < "$MODS"
done < "$TOPICS"

echo "Generated page ideas saved to $OUT"
