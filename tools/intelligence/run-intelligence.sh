#!/usr/bin/env bash

ROOT="${1:-.}"

mkdir -p logs/intelligence
mkdir -p docs/intelligence

bash tools/intelligence/priority-engine.sh "$ROOT"
bash tools/intelligence/news-radar.sh

LATEST_TOP="$(grep -E '^[0-9]+\.' logs/intelligence/priority-report.txt 2>/dev/null | head -n 10 | sed 's/^[0-9]\+\. //' | awk '{print $1}' | head -n 1)"

{
  echo "# SideGuy Intelligence Summary"
  echo
  echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
  echo
  echo "## Outputs"
  echo "- logs/intelligence/priority-report.txt"
  echo "- logs/intelligence/news-radar.txt"
  echo "- data/intelligence/news-page-ideas.txt"
  echo
  echo "## Suggested Next Move"
  echo "1. Open priority-report.txt"
  echo "2. Upgrade the top 3 pages"
  echo "3. Pick 1 page idea from news-page-ideas.txt"
  echo "4. Ship one clean win"
  echo
  echo "## Top Candidate"
  if [ -n "$LATEST_TOP" ]; then
    echo "- $LATEST_TOP"
  else
    echo "- No candidate detected yet"
  fi
} > docs/intelligence/README.md

echo "Intelligence run complete."
echo "Open docs/intelligence/README.md"
