#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
INDEX="$ROOT/docs/index/page-metadata.tsv"
OUTPUT="$ROOT/all-pages-index.html"

echo "Building full page index..."

{
echo "<html><head><title>All SideGuy Pages</title></head><body>"
echo "<h1>SideGuy Knowledge Index</h1>"
echo "<ul>"

tail -n +2 "$INDEX" | awk -F'\t' '{print $1}' | sort | while read slug
do
echo "<li><a href=\"/$slug\">$slug</a></li>"
done

echo "</ul>"
echo "</body></html>"
} > "$OUTPUT"

echo "Full index built."

