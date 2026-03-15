#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

OUTPUT="docs/brain/queues/internal-link-gravity.csv"
echo "page,inbound_links" > "$OUTPUT"

# Count inbound <a href="..."> references per HTML page at root level
declare -A link_count

# Collect all hrefs from all HTML pages
while IFS= read -r href; do
  # Normalize: strip leading ./ and trailing .html if needed
  page="${href##*/}"
  [[ "$page" =~ \.html$ ]] || continue
  link_count["$page"]=$(( ${link_count["$page"]:-0} + 1 ))
done < <(grep -roh 'href="[^"]*\.html"' *.html 2>/dev/null | sed 's/href="//;s/"//')

# Sort by count descending
for page in "${!link_count[@]}"; do
  echo "$page,${link_count[$page]}"
done | sort -t, -k2,2nr >> "$OUTPUT"

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Internal link gravity scored — $COUNT pages"
