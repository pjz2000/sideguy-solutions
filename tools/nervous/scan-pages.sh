#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

OUTPUT="docs/nervous/page-scan.csv"
echo "file,last_modified,age_days" > "$OUTPUT"

NOW=$(date +%s)

find public -name "*.html" | while IFS= read -r file; do
  mod=$(stat -c %Y "$file" 2>/dev/null || stat -f %m "$file" 2>/dev/null || echo 0)
  age=$(( (NOW - mod) / 86400 ))
  echo "$file,$mod,$age" >> "$OUTPUT"
done

COUNT=$(( $(wc -l < "$OUTPUT") - 1 ))
echo "Page scan complete — $COUNT pages scanned"
