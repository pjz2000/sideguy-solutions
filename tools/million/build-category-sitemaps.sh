#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

SELECTION="docs/million-page/selected/wave-selection.csv"
[ -f "$SELECTION" ] || { echo "No wave-selection.csv found."; exit 1; }

mkdir -p public/sitemaps docs/million-page/sitemaps

# Build per-theme URL lists
tail -n +2 "$SELECTION" | while IFS=, read -r url title h1 theme rest; do
  clean_url="$(echo "$url"   | tr -d '"')"
  clean_theme="$(echo "$theme" | tr -d '"' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
  [ -z "$clean_theme" ] && continue
  echo "$clean_url" >> "docs/million-page/sitemaps/${clean_theme}.urls.txt"
done

# Build per-theme XML sitemaps
for f in docs/million-page/sitemaps/*.urls.txt; do
  [ -f "$f" ] || continue
  theme="$(basename "$f" .urls.txt)"
  out="public/sitemaps/${theme}.xml"
  {
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    while IFS= read -r url; do
      [ -n "$url" ] || continue
      echo "  <url><loc>https://sideguysolutions.com${url}</loc></url>"
    done < "$f"
    echo '</urlset>'
  } > "$out"
  echo "Built $out"
done
