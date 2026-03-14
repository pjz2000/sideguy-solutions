#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "Running SideGuy Gravity Engine"
echo ""

mkdir -p docs/sideguy-os/logs
REPORT="docs/sideguy-os/logs/gravity-report-$(date +%Y%m%d-%H%M%S).txt"

{
  echo "# SideGuy Gravity Report — $(date)"
  echo "# score,links,size_bytes,file"
  echo ""

  find public -name "*.html" | while IFS= read -r file; do
    SIZE="$(wc -c < "$file" 2>/dev/null || echo 0)"
    LINKS="$(grep -c '<a ' "$file" 2>/dev/null; true)"
    LINKS="${LINKS:-0}"
    SIZE="${SIZE:-0}"
    SCORE=$(( SIZE + LINKS * 500 ))
    printf '%s,%s,%s,%s\n' "$SCORE" "$LINKS" "$SIZE" "$file"
  done | sort -t, -k1,1nr | head -50
} > "$REPORT"

echo "Top 50 authority pages saved → $REPORT"
echo ""
head -10 "$REPORT"
