#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/index/page-metadata.tsv"

echo "Building page metadata index..."

echo -e "slug\twords\tlinks\th2\tlastmod" > "$OUTPUT"

find "$ROOT" -maxdepth 1 -name "*.html" -print0 | while IFS= read -r -d '' file
do

slug=$(basename "$file")

words=$(wc -w < "$file")
links=$(grep -c "<a " "$file")
sections=$(grep -ic "<h2" "$file")
lastmod=$(date -r "$file" +"%Y-%m-%d")

echo -e "$slug\t$words\t$links\t$sections\t$lastmod" >> "$OUTPUT"

done

echo "Index written to:"
echo "$OUTPUT"

wc -l "$OUTPUT"

