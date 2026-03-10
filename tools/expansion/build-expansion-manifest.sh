#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
SIGNALS="$ROOT/docs/signals/page-ideas.txt"
OUTPUT="$ROOT/docs/manifests/expansion/expansion-manifest.tsv"

mkdir -p "$ROOT/docs/manifests/expansion"

echo -e "type\tslug" > "$OUTPUT"

while read -r idea
do
  [ -z "$idea" ] && continue

  slug=$(echo "$idea" | sed 's/.html//')

  echo -e "core\t$slug.html" >> "$OUTPUT"
  echo -e "faq\t$slug-faq.html" >> "$OUTPUT"
  echo -e "comparison\t$slug-vs-alternatives.html" >> "$OUTPUT"
  echo -e "cost\thow-much-does-$slug-cost.html" >> "$OUTPUT"

done < "$SIGNALS"

echo "Expansion manifest built:"
wc -l "$OUTPUT"
