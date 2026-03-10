#!/bin/bash

# =========================================
# SIDEGUY — LONG-TAIL CLUSTER BUILDER
# =========================================
# Generates topic cluster pages from docs/cluster-engine/cluster-topics.txt
# Safe to re-run — skips existing pages.
# =========================================

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TOPICS="$ROOT/docs/cluster-engine/cluster-topics.txt"
TEMPLATE="$ROOT/seo-template.html"

if [ ! -f "$TOPICS" ]; then
  echo "❌ Cluster topics file missing: $TOPICS"
  exit 1
fi

if [ ! -f "$TEMPLATE" ]; then
  echo "❌ seo-template.html missing: $TEMPLATE"
  exit 1
fi

SUFFIXES=(
  "for-startups"
  "for-small-business"
  "for-contractors"
  "for-saas"
  "breakdown"
  "per-hour"
  "per-feature"
)

created=0
skipped=0

while IFS= read -r topic || [ -n "$topic" ]; do
  [ -z "$topic" ] && continue

  slug=$(echo "$topic" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -d '?.,')

  for suffix in "${SUFFIXES[@]}"; do
    file="$ROOT/$slug-$suffix.html"
    title="$topic $suffix"

    if [ -f "$file" ]; then
      skipped=$((skipped+1))
      continue
    fi

    cp "$TEMPLATE" "$file"
    sed -i "s|PAGE_TITLE|$title|g" "$file"
    sed -i "s|PAGE_HEADING|$title|g" "$file"

    echo "  created  $slug-$suffix.html"
    created=$((created+1))
  done

done < "$TOPICS"

echo ""
echo "✅ Cluster build complete — $created created, $skipped skipped."
echo "Next: add new pages to sitemap.xml and index.html."
