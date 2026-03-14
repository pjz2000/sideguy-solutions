#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p docs/million-page/publish-logs
STAMP="$(date +%Y%m%d-%H%M%S)"
SELECTION="docs/million-page/selected/wave-selection.csv"
LOG="docs/million-page/publish-logs/wave-${STAMP}.md"

COUNT=0
[ -f "$SELECTION" ] && COUNT=$(( $(wc -l < "$SELECTION") - 1 ))

{
  echo "# Million Wave Publish Log"
  echo ""
  echo "- Timestamp: ${STAMP}"
  echo "- Selected pages: ${COUNT}"
  echo "- Category sitemap index: /sitemaps/sitemap-million-index.xml"
  echo ""
  echo "## Notes"
  echo "- Phase 2 uses scoring + dedupe + theme/state/industry caps."
  echo "- This keeps the system controlled instead of sloppy."
  echo "- Next phase can add page-quality upgrades and auto-refresh logic."
} > "$LOG"

echo "Wrote $LOG"
