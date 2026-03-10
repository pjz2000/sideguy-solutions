#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
MANIFEST="$ROOT/docs/lattice/lattice-manifest.tsv"
TEMPLATE="$ROOT/seo-template.html"
LIMIT="${1:-500}"

if [ ! -f "$MANIFEST" ]; then
  echo "Missing manifest: $MANIFEST"
  exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
  echo "Missing template: $TEMPLATE"
  exit 1
fi

created=0

tail -n +2 "$MANIFEST" | while IFS=$'\t' read -r type parent child modifier slug
do
  if [ "$created" -ge "$LIMIT" ]; then
    break
  fi

  file="$ROOT/$slug"

  if [ -f "$file" ]; then
    continue
  fi

  cp "$TEMPLATE" "$file"

  title="${child} | SideGuy"
  heading="$child"

  canonical="https://sideguysolutions.com/$slug"
  perl -0pi -e "s~PAGE_TITLE~$title~g; s~PAGE_HEADING~$heading~g" "$file"
  perl -0pi -e "s~https://sideguysolutions.com/seo-template.html~$canonical~g" "$file"

  echo "CREATE $slug"
  created=$((created + 1))
done

echo ""
echo "Batch complete. Created up to $LIMIT new pages."
