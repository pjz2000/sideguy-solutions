#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX="$ROOT/docs/index/page-metadata.tsv"
OUTPUT="$ROOT/recent-pages.html"

echo "Building recent pages discovery..."

{
echo "<html><head><title>Recent SideGuy Pages</title></head><body>"
echo "<h1>Newest SideGuy Pages</h1>"
echo "<ul>"

tail -n +2 "$INDEX" | sort -t$'\t' -k5 -r | head -500 | while IFS=$'\t' read slug words links h2 lastmod
do
echo "<li><a href=\"/$slug\">$slug</a> — $lastmod</li>"
done

echo "</ul>"
echo "</body></html>"
} > "$OUTPUT"

echo "Recent pages built."

