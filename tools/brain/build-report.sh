#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
REPORT_FILE="docs/brain/reports/brain-report-$(date -u +%Y%m%d-%H%M%S).md"

MOMENTUM_COUNT=$(awk -F, 'NR>1' docs/brain/queues/topic-momentum.csv 2>/dev/null | wc -l)
DOMINANT_COUNT=$(awk -F, 'NR>1' docs/brain/queues/cluster-dominance.csv 2>/dev/null | wc -l)
BUILD_COUNT=$(awk -F, 'NR>1' docs/brain/queues/build-recommendations.csv 2>/dev/null | wc -l)
UPGRADE_COUNT=$(awk -F, 'NR>1' docs/brain/queues/upgrade-recommendations.csv 2>/dev/null | wc -l)
GRAVITY_COUNT=$(awk -F, 'NR>1' docs/brain/queues/internal-link-gravity.csv 2>/dev/null | wc -l)

TOP_THEMES=$(awk -F, 'NR>1 && NR<=6 { print "- "$1" ("$2" pages)" }' \
  docs/brain/queues/cluster-dominance.csv 2>/dev/null)

TOP_GRAVITY=$(awk -F, 'NR>1 && NR<=6 { print "- "$1" ("$2" inbound links)" }' \
  docs/brain/queues/internal-link-gravity.csv 2>/dev/null)

cat > "$REPORT_FILE" <<EOF
# SideGuy Brain Engine Report
**Generated:** $TIMESTAMP

## Summary
| Signal | Count |
|--------|-------|
| Themes with momentum | $MOMENTUM_COUNT |
| Dominant clusters (eligible to expand) | $DOMINANT_COUNT |
| Build recommendations | $BUILD_COUNT |
| Upgrade recommendations | $UPGRADE_COUNT |
| Pages scored for link gravity | $GRAVITY_COUNT |

## Top Dominant Clusters
$TOP_THEMES

## Top Link Gravity Pages
$TOP_GRAVITY

## Actions Queued
- Build queue: \`docs/brain/queues/build-recommendations.csv\`
- Upgrade queue: \`docs/brain/queues/upgrade-recommendations.csv\`
- Discovery feed: \`docs/alive/inbox/brain-discovery.txt\`
EOF

echo "Brain report saved → $REPORT_FILE"
