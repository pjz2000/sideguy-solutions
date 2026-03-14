#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

STAMP="$(date +%Y%m%d-%H%M%S)"
REPORT="docs/nervous/reports/nervous-report-${STAMP}.md"

PAGES=$(find public -name "*.html" 2>/dev/null | wc -l)
STALE=0
CLUSTERS=0
[ -f docs/nervous/queues/stale-pages.csv ]    && STALE=$(( $(wc -l < docs/nervous/queues/stale-pages.csv) - 1 ))
[ -f docs/nervous/queues/cluster-winners.csv ] && CLUSTERS=$(( $(wc -l < docs/nervous/queues/cluster-winners.csv) - 1 ))

cat > "$REPORT" <<EOF
# SideGuy Nervous System Report

Timestamp: ${STAMP}

Pages scanned:        ${PAGES}
Stale pages detected: ${STALE}
Cluster signals:      ${CLUSTERS}

## Meaning

SideGuy is now running feedback loops:

- detecting stale content
- refreshing outdated pages
- identifying cluster growth
- triggering new discovery signals

The system now adapts as the site grows.
EOF

echo "Report generated → $REPORT"
