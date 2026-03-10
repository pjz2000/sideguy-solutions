#!/bin/bash

# =========================================
# SIDEGUY — PROBLEM PAGE BUILDER
# =========================================
# Generates pages from docs/problem-engine/problem-page-ideas.txt
# Uses seo-template.html as base. Skips existing pages (safe to re-run).
# =========================================

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

TEMPLATE="seo-template.html"
IDEAS="docs/problem-engine/problem-page-ideas.txt"

if [ ! -f "$TEMPLATE" ]; then
  echo "❌ Template not found: $TEMPLATE"
  exit 1
fi

if [ ! -f "$IDEAS" ]; then
  echo "❌ Problem ideas file not found: $IDEAS"
  exit 1
fi

CREATED=0
SKIPPED=0

while IFS= read -r problem || [ -n "$problem" ]; do
  [ -z "$problem" ] && continue

  slug=$(echo "$problem" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -d '?.,')
  file="$slug.html"

  if [ -f "$file" ]; then
    echo "  skip  $file"
    ((SKIPPED++))
    continue
  fi

  cp "$TEMPLATE" "$file"
  sed -i "s|PAGE_TITLE|$problem|g" "$file"
  sed -i "s|PAGE_HEADING|$problem|g" "$file"

  echo "  created  $file"
  ((CREATED++))

done < "$IDEAS"

echo ""
echo "✅ Done — $CREATED created, $SKIPPED skipped."
echo "Next: add new pages to sitemap.xml and index.html."
