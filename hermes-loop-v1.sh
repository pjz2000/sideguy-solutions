#!/usr/bin/env bash

########################################
# SIDEGUY HERMES LOOP v1
# hypothesis -> modify -> evaluate -> keep/discard -> repeat
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DOCS_DIR="docs/hermes"
DATE="$(date +"%Y-%m-%d-%H%M")"
REPORT_FILE="$DOCS_DIR/hermes-loop-$DATE.md"

cd "$PROJECT_ROOT" || return

mkdir -p "$DOCS_DIR"

echo "---------------------------------------"
echo "🧠 SIDEGUY HERMES LOOP v1"
echo "---------------------------------------"
echo ""

########################################
# PAGE INVENTORY
########################################

echo "🔍 Building page inventory..."

PAGES=$(find . -maxdepth 1 -name "*.html" \
  ! -name "index.html" \
  ! -name "seo-template.html" \
  | sort)

PAGE_COUNT=$(echo "$PAGES" | sed '/^$/d' | wc -l)

echo "Found $PAGE_COUNT pages"
echo ""

########################################
# REPORT HEADER
########################################

cat > "$REPORT_FILE" <<EOF
# SideGuy Hermes Loop Report
Generated: $DATE

## Summary
- Pages scanned: $PAGE_COUNT

## Decisions
EOF

########################################
# SIMPLE HERMES SCORING
########################################

KEEP_COUNT=0
DISCARD_COUNT=0
SPAWN_COUNT=0

for PAGE in $PAGES; do
  NAME=$(basename "$PAGE" .html)

  WORDS=$(wc -w < "$PAGE" | tr -d ' ')
  LINKS=$(grep -o "href=" "$PAGE" | wc -l | tr -d ' ')

  SCORE=0
  [ "$WORDS" -gt 700 ] && SCORE=$((SCORE + 1))
  [ "$LINKS" -gt 8 ] && SCORE=$((SCORE + 1))
  echo "$NAME" | grep -Eq "san-diego|cost|repair|replace|compare|vs|ai|payments|solar|hvac" && SCORE=$((SCORE + 1))

  ########################################
  # KEEP BRANCH
  ########################################
  if [ "$SCORE" -ge 2 ]; then
    KEEP_COUNT=$((KEEP_COUNT + 1))

    echo "- KEEP: $NAME (score=$SCORE)" >> "$REPORT_FILE"

    CHILD_1="${NAME}-faq.html"
    CHILD_2="${NAME}-comparison.html"
    CHILD_3="${NAME}-cost.html"

    for CHILD in "$CHILD_1" "$CHILD_2" "$CHILD_3"; do
      if [ ! -f "$CHILD" ]; then
        cp seo-template.html "$CHILD"
        sed -i "s|SEO_TITLE|${CHILD%.html} |g" "$CHILD"
        echo "Created $CHILD"
        SPAWN_COUNT=$((SPAWN_COUNT + 1))
      fi
    done

  ########################################
  # DISCARD BRANCH
  ########################################
  else
    DISCARD_COUNT=$((DISCARD_COUNT + 1))
    echo "- DISCARD: $NAME (score=$SCORE)" >> "$REPORT_FILE"
  fi
done

########################################
# REPORT FOOTER
########################################

cat >> "$REPORT_FILE" <<EOF

## Totals
- KEEP: $KEEP_COUNT
- DISCARD: $DISCARD_COUNT
- CHILD PAGES SPAWNED: $SPAWN_COUNT

## Philosophy
Hermes loop favors pages with:
- strong word depth
- internal links
- high commercial/local intent
- expansion potential
EOF

########################################
# GIT VISIBLE PROGRESS
########################################

git add .
git commit -m "Hermes loop v1: scored pages and spawned winning child clusters"

echo ""
echo "✅ Hermes loop complete"
echo "📄 Report: $REPORT_FILE"
echo "🧠 KEEP: $KEEP_COUNT | DISCARD: $DISCARD_COUNT | SPAWNED: $SPAWN_COUNT"
