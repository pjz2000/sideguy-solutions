#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p public/sitemaps

OUT="public/sitemaps/sitemap-million-index.xml"

{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
  for f in public/sitemaps/*.xml; do
    [ -f "$f" ] || continue
    base="$(basename "$f")"
    [ "$base" = "sitemap-million-index.xml" ] && continue
    echo "  <sitemap><loc>https://sideguysolutions.com/sitemaps/${base}</loc></sitemap>"
  done
  echo '</sitemapindex>'
} > "$OUT"

echo "Built $OUT"
