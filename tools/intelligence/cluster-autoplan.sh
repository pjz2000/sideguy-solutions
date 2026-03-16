#!/bin/bash

TOPIC="$1"

if [ -z "$TOPIC" ]; then
  echo "Usage: ./tools/intelligence/cluster-autoplan.sh \"topic name\""
  exit
fi

slug=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
OUT="docs/clusters/$slug-cluster-plan.md"

cat <<EOF2 > "$OUT"
# SideGuy Cluster Plan

## Core Topic
$TOPIC

## Hub Candidate
/$slug.html

## Support Pages
/$slug-explained.html
/$slug-for-business.html
/$slug-faq.html
/future-of-$slug.html
/$slug-sideguy-guide.html

## Optional Local Variants
/$slug-san-diego.html
/$slug-for-small-business.html
/$slug-for-operators.html

## Internal Linking Plan
- all support pages link to /$slug.html
- /$slug.html links back to homepage
- /$slug.html links to relevant category hub
- FAQ page links to guide page
- business page links to future page
- local page links to operator pages

## Monetization / Action Layer
- Text PJ CTA
- consultation / explanation layer
- future payments or implementation support
EOF2

echo "Created cluster plan:"
echo "$OUT"
