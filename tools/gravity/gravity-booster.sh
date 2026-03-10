#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
REPORT="$ROOT/docs/gravity/gravity-report.txt"

echo "Running Gravity Booster..."

top_pages=$(head -20 "$REPORT" | awk -F'|' '{print $2}' | xargs)

find "$ROOT" -maxdepth 1 -name "*.html" | while read -r f
do

for p in $top_pages
do

if ! grep -q "$p" "$f"; then

sed -i "/<\/body>/i \
<li><a href=\"/$p\">Related SideGuy Guide</a></li>" "$f"

fi

done

done

echo "Gravity links injected."
