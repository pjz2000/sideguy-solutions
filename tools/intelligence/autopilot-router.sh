#!/bin/bash

TOPIC="$1"

if [ -z "$TOPIC" ]; then
  echo "Usage: ./tools/intelligence/autopilot-router.sh \"topic name\""
  exit
fi

slug=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
REPORT="reports/autopilot-$slug-report.md"

./tools/intelligence/auto-brief.sh "$TOPIC"
./tools/intelligence/cluster-autoplan.sh "$TOPIC"

cat <<EOF2 > "$REPORT"
# SidePalantir Autopilot Report

## Topic
$TOPIC

## Created
- docs/briefs/$slug-brief.md
- docs/clusters/$slug-cluster-plan.md

## Next Operator Step
Give the brief to Claude / CPU-GPT to create:

- /$slug.html
- optional support pages from cluster plan

## After Build
1. add /$slug.html to sitemap.xml
2. add internal link from correct hub
3. add homepage link if high-value
4. run log-signal.sh

## Example
./tools/intelligence/log-signal.sh "$TOPIC" "Created brief + cluster plan" "$slug.html"
EOF2

echo "Autopilot route created:"
echo "$REPORT"
