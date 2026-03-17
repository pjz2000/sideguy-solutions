#!/bin/bash

TOPIC="$1"

if [ -z "$TOPIC" ]; then
  echo "Usage:"
  echo "bash tools/intelligence/topic-expander.sh 'topic name'"
  exit
fi

slug=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')

DATE=$(date +"%Y-%m-%d")
STAMP=$(date +"%Y-%m-%d %H:%M:%S")

OUT="manifests/expansion/$slug-expansion.csv"
LOG="logs/expansion/$slug-expansion.log"
REPORT="reports/expansion/$slug-expansion-report.md"

mkdir -p manifests/expansion logs/expansion reports/expansion docs/expansion

echo "" >> "$LOG"
echo "=== Topic Expansion Run $STAMP ===" >> "$LOG"

#########################################
# CSV HEADER
#########################################

echo "page_type,slug,title,parent,category,intent" > "$OUT"


#########################################
# CORE VARIATIONS
#########################################

echo "hub,$slug,$TOPIC,$slug,core,hub" >> "$OUT"

echo "support,what-is-$slug,What Is $TOPIC,$slug,core,info" >> "$OUT"
echo "support,how-$slug-works,How $TOPIC Works,$slug,core,info" >> "$OUT"
echo "support,$slug-explained,$TOPIC Explained,$slug,core,info" >> "$OUT"

#########################################
# USE CASES
#########################################

for x in business small-business contractors startups developers operators
do
echo "support,$slug-for-$x,$TOPIC for $x,$slug,use-case,info" >> "$OUT"
done

#########################################
# COMPARISONS
#########################################

for x in traditional-systems stripe manual-processes legacy-systems
do
echo "comparison,$slug-vs-$x,$TOPIC vs $x,$slug,comparison,decision" >> "$OUT"
done

#########################################
# PROBLEMS
#########################################

for x in problems issues risks challenges limitations
do
echo "support,$slug-$x,$TOPIC $x,$slug,problems,info" >> "$OUT"
done

#########################################
# DECISION
#########################################

for x in should-you-use when-to-use best-options alternatives
do
echo "decision,$x-$slug,$x $TOPIC,$slug,decision,decision" >> "$OUT"
done

#########################################
# COST + FAQ
#########################################

echo "faq,$slug-faq,$TOPIC FAQ,$slug,faq,faq" >> "$OUT"
echo "pricing,$slug-cost,$TOPIC Cost,$slug,pricing,commercial" >> "$OUT"

#########################################
# FUTURE + INFRA
#########################################

echo "future,future-of-$slug,Future of $TOPIC,$slug,future,future" >> "$OUT"
echo "future,$slug-infrastructure,$TOPIC Infrastructure,$slug,future,future" >> "$OUT"

#########################################
# LOCAL VARIANTS
#########################################

for x in san-diego california usa
do
echo "local,$slug-$x,$TOPIC $x,$slug,local,local" >> "$OUT"
done

#########################################
# OUTPUT
#########################################

COUNT=$(($(wc -l < "$OUT") - 1))

cat > "$REPORT" <<EOF2
# SideGuy Topic Expansion Report

## Topic
$TOPIC

## Slug
$slug

## Timestamp
$STAMP

## Pages Generated
$COUNT

## Output
$OUT

## Next Steps

1. Run page factory:
   bash tools/factory/page-factory.sh $OUT

2. Strengthen pages:
   bash tools/factory/strengthen-pages.sh

3. Run link engine:
   bash tools/link-engine/auto-link-engine.sh

4. Inject links:
   bash tools/link-engine/auto-link-injector.sh

5. Run gravity engine:
   bash tools/gravity/gravity-engine.sh

6. Run publish gate:
   bash tools/intelligence/publish-gate.sh

7. Promote pages:
   bash tools/factory/promote-pages.sh
EOF2

echo ""
echo "======================================"
echo "SIDEGUY UNIVERSE EXPANSION COMPLETE"
echo "======================================"
echo ""
echo "Topic: $TOPIC"
echo "Pages Generated: $COUNT"
echo ""
echo "Manifest:"
echo "$OUT"
echo ""
echo "Next Step:"
echo "bash tools/factory/page-factory.sh $OUT"
