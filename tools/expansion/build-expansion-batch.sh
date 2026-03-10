#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
MANIFEST="$ROOT/docs/manifests/expansion/expansion-manifest.tsv"
TEMPLATE="$ROOT/seo-template.html"

LIMIT="${1:-500}"

if [ ! -f "$MANIFEST" ]; then
  echo "Missing expansion manifest."
  exit 1
fi

created=0
skipped=0

tail -n +2 "$MANIFEST" | head -n "$LIMIT" | while IFS=$'\t' read -r type slug
do

file="$ROOT/$slug"

if [ -f "$file" ]; then
  echo "SKIP $slug"
  skipped=$((skipped+1))
  continue
fi

cp "$TEMPLATE" "$file"

title=$(echo "$slug" | sed 's/.html//' | tr '-' ' ')
heading=$(echo "$title" | sed 's/\b\(.\)/\u\1/g')

canonical="https://sideguysolutions.com/$slug"
perl -0pi -e "s~PAGE_TITLE~$heading | SideGuy~g" "$file"
perl -0pi -e "s~PAGE_HEADING~$heading~g" "$file"
perl -0pi -e "s~https://sideguysolutions.com/seo-template.html~$canonical~g" "$file"

echo "CREATE $slug"

done

echo "Expansion batch complete."
