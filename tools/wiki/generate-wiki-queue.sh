#!/usr/bin/env bash

CATEGORIES="manifests/wiki/categories/categories.txt"
SKILLS="manifests/wiki/skills/skills.txt"
OPERATORS="manifests/wiki/operators/operators.txt"

OUT="manifests/wiki/wiki-queue.csv"
LOG="logs/wiki-generation.log"

echo "page_type,slug,title,category,parent,notes" > "$OUT"

ROWS=0

slug_to_title() {
echo "$1" | tr '-' ' '
}

while IFS= read -r category
do

[ -z "$category" ] && continue

pretty=$(slug_to_title "$category")

echo "category,$category,$pretty,$category,root,category hub" >> "$OUT"
ROWS=$((ROWS+1))

echo "problem,what-is-$category,what is $pretty,$category,$category,definition page" >> "$OUT"
echo "problem,how-does-$category-work,how does $pretty work,$category,$category,mechanics page" >> "$OUT"

echo "resolution,best-$category-options,best $pretty options,$category,$category,decision page" >> "$OUT"

echo "system,$category-systems,$pretty systems,$category,$category,system overview" >> "$OUT"

ROWS=$((ROWS+4))

while IFS= read -r skill
do
[ -z "$skill" ] && continue
title=$(slug_to_title "$skill")

echo "skill,$skill,$title,$category,$category,skill page candidate" >> "$OUT"
ROWS=$((ROWS+1))

done < "$SKILLS"

while IFS= read -r operator
do
[ -z "$operator" ] && continue
title=$(slug_to_title "$operator")

echo "operator,$operator,$title,$category,$category,operator profile" >> "$OUT"
ROWS=$((ROWS+1))

done < "$OPERATORS"

done < "$CATEGORIES"

STAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "[$STAMP] Wiki queue rows: $ROWS" >> "$LOG"

echo ""
echo "Wiki queue generated"
echo "Rows: $ROWS"
echo "File: $OUT"
