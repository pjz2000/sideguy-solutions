#!/usr/bin/env bash

########################################
# SIDEGUY HERMES MASTER ENGINE v1
# self-learning + geo routing + authority gravity
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DOCS_DIR="docs/hermes-master"
DATE="$(date +"%Y-%m-%d-%H%M")"
REPORT_FILE="$DOCS_DIR/hermes-master-$DATE.md"

cd "$PROJECT_ROOT" || return
mkdir -p "$DOCS_DIR"

echo "---------------------------------------"
echo "🧠🌍 SIDEGUY HERMES MASTER ENGINE v1"
echo "---------------------------------------"
echo ""

########################################
# CONFIG
########################################

VERTICALS=(
"hvac"
"solar"
"payments"
"ai-automation"
"website-help"
"tesla-charging"
"mini-split"
"crypto-help"
"relocation"
"vacation-rentals"
)

LOCATIONS=(
"san-diego"
"encinitas"
"carlsbad"
"oceanside"
"del-mar"
"la-jolla"
"solana-beach"
"coronado"
)

########################################
# REPORT HEADER
########################################

cat > "$REPORT_FILE" <<EOF
# SideGuy Hermes Master Report
Generated: $DATE

## Sections
- Winner scoring
- Child spawning
- Geo routing
- Authority gravity
EOF

########################################
# HERMES LOOP (SCORING + CHILDREN)
########################################

echo "🔍 Scoring current pages..."

PAGES=$(find . -maxdepth 1 -name "*.html" \
  ! -name "index.html" \
  ! -name "seo-template.html" \
  | sort)

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

  if [ "$SCORE" -ge 2 ]; then
    KEEP_COUNT=$((KEEP_COUNT + 1))
    echo "- KEEP: $NAME" >> "$REPORT_FILE"

    for SUFFIX in faq comparison cost; do
      CHILD="${NAME}-${SUFFIX}.html"
      if [ ! -f "$CHILD" ]; then
        cp seo-template.html "$CHILD"
        sed -i "s|SEO_TITLE|${CHILD%.html}|g" "$CHILD"
        SPAWN_COUNT=$((SPAWN_COUNT + 1))
        echo "Created $CHILD"
      fi
    done
  else
    DISCARD_COUNT=$((DISCARD_COUNT + 1))
    echo "- DISCARD: $NAME" >> "$REPORT_FILE"
  fi
done

########################################
# HERMES ROUTING (GEO + VERTICAL)
########################################

echo ""
echo "🌍 Building geo routes..."

ROUTES=0

for VERTICAL in "${VERTICALS[@]}"; do
  for CITY in "${LOCATIONS[@]}"; do
    PAGE="${VERTICAL}-${CITY}.html"

    if [ ! -f "$PAGE" ]; then
      cp seo-template.html "$PAGE"

      TITLE="$(echo "$VERTICAL in $CITY" | tr '-' ' ')"

      sed -i "s|SEO_TITLE|$TITLE|g" "$PAGE"
      sed -i "s|SEO_DESCRIPTION|Fast trusted ${VERTICAL//-/ } routing in ${CITY//-/ }.|g" "$PAGE"

      cat >> "$PAGE" <<EOF

<section>
  <h2>${VERTICAL//-/ } help in ${CITY//-/ }</h2>
  <p>
    SideGuy routes internet confusion into the best-fit local
    vendor, operator, tool, or human resolution path.
  </p>
</section>
EOF

      ROUTES=$((ROUTES + 1))
      echo "- ROUTE: $PAGE" >> "$REPORT_FILE"
      echo "Created $PAGE"
    fi
  done
done

########################################
# INDEX APPEND
########################################

echo ""
echo "🧲 Strengthening index gravity..."

for PAGE in *.html; do
  grep -q "$PAGE" index.html || \
    echo "<li><a href=\"$PAGE\">$PAGE</a></li>" >> index.html
done

########################################
# OPTIONAL HUB + LINK ENGINES
########################################

echo ""
echo "🕸️ Running hub/link gravity if available..."

[ -f tools/hubs/run-hub-engine.sh ] && bash tools/hubs/run-hub-engine.sh
[ -f tools/link-engine/auto-link-engine.sh ] && bash tools/link-engine/auto-link-engine.sh

########################################
# REPORT FOOTER
########################################

cat >> "$REPORT_FILE" <<EOF

## Totals
- KEEP: $KEEP_COUNT
- DISCARD: $DISCARD_COUNT
- CHILDREN: $SPAWN_COUNT
- GEO ROUTES: $ROUTES

## System Meaning
The web sends confusion.
Hermes classifies intent.
Geo routes map trust.
SideGuy resolves reality.
EOF

########################################
# FINAL COMMIT
########################################

git add .
git commit -m "Hermes master v1: scoring + routing + gravity"

echo ""
echo "✅ Hermes master complete"
echo "📄 Report: $REPORT_FILE"
echo "🧠 KEEP: $KEEP_COUNT | 🚀 CHILDREN: $SPAWN_COUNT | 🌍 ROUTES: $ROUTES"
