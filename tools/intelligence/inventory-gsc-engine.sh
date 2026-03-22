#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"

cd "$PROJECT_ROOT" || return

echo "---------------------------------------"
echo "SideGuy Inventory Engine v7.5 (GSC Mode)"
echo "---------------------------------------"

QUEUE_FILE="seo-reserve/queue.csv"
mkdir -p seo-reserve

########################################
# REAL QUERIES (FROM YOUR SCREEN)
########################################

BASE_QUERIES=(
"emergency-hvac-san-diego|hvac"
"square-vs-stripe|payments"
"ai-consulting-services-san-diego|ai"
"electric-panel-upgrade-san-diego|energy"
"hvac-replacement-cost-san-diego|hvac"
"workflow-automation-san-diego|ai"
"low-water-pressure-san-diego|home-services"
"payment-timeout-issues|payments"
"shopify-troubleshooting|ecommerce"
"ai-lead-generation-near-me|ai"
"sink-repair-cost|home-services"
)

########################################
# CHILD INTENTS (HIGH ROI)
########################################

INTENTS=(
"best"
"how-to"
"cost-of"
"who-to-hire-for"
"is-it-worth"
"near-me"
"fix"
"problems-with"
"alternatives-to"
"guide-to"
)

########################################
# DEEP VARIANTS
########################################

VARIANTS=(
"for-small-business"
"for-homeowners"
"for-contractors"
"for-restaurants"
"for-startups"
)

########################################
# HELPERS
########################################

titleize() {
  echo "$1" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g'
}

append_if_missing() {
  ROW="$1"
  SLUG="$(echo "$ROW" | cut -d',' -f1)"
  if ! grep -q "^$SLUG," "$QUEUE_FILE"; then
    echo "$ROW" >> "$QUEUE_FILE"
    echo "Added: $SLUG"
  fi
}

########################################
# GENERATE
########################################

for ITEM in "${BASE_QUERIES[@]}"
do
  BASE="$(echo "$ITEM" | cut -d'|' -f1)"
  VERTICAL="$(echo "$ITEM" | cut -d'|' -f2)"

  CITY="$(echo "$BASE" | grep -o 'san-diego\|encinitas\|carlsbad\|oceanside')"

  ########################################
  # CORE PAGE (BOOST SIGNAL)
  ########################################

  TITLE="$(titleize "$BASE")"
  KEYWORD="$(echo "$BASE" | tr '-' ' ')"
  ROW="$BASE,$TITLE,$CITY,$KEYWORD,$VERTICAL,core,pending"
  append_if_missing "$ROW"

  ########################################
  # INTENT CHILDREN
  ########################################

  for INTENT in "${INTENTS[@]}"
  do
    SLUG="$INTENT-$BASE"
    TITLE="$(titleize "$INTENT $BASE")"
    KEYWORD="$(echo "$INTENT $BASE" | tr '-' ' ')"

    ROW="$SLUG,$TITLE,$CITY,$KEYWORD,$VERTICAL,$INTENT,pending"
    append_if_missing "$ROW"
  done

  ########################################
  # DEEP VARIANTS
  ########################################

  for VARIANT in "${VARIANTS[@]}"
  do
    SLUG="$BASE-$VARIANT"
    TITLE="$(titleize "$BASE $VARIANT")"
    KEYWORD="$(echo "$BASE $VARIANT" | tr '-' ' ')"

    ROW="$SLUG,$TITLE,$CITY,$KEYWORD,$VERTICAL,deep,pending"
    append_if_missing "$ROW"
  done

done

echo "---------------------------------------"
echo "Inventory Expansion Complete"
echo "---------------------------------------"
