#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"

cd "$PROJECT_ROOT" || return

echo "---------------------------------------"
echo "SideGuy Inventory Engine v7"
echo "---------------------------------------"

QUEUE_FILE="seo-reserve/queue.csv"
DATE=$(date +"%Y-%m-%d-%H%M")

mkdir -p seo-reserve

########################################
# INIT QUEUE
########################################

if [ ! -f "$QUEUE_FILE" ]; then
  echo "slug,title,city,keyword,vertical,intent,status" > "$QUEUE_FILE"
fi

########################################
# REAL SIGNAL QUERIES (FROM YOUR GSC)
########################################

BASE_QUERIES=(
"payment-processing-san-diego|payments"
"ai-storage-solutions|ai"
"electric-panel-upgrade-san-diego|energy"
"plumbing-issues|home-services"
"workflow-automation-san-diego|ai"
)

########################################
# INTENT CHILD PATTERNS
########################################

INTENTS=(
"best"
"how-to"
"cost-of"
"who-to-hire-for"
"is-it-worth"
"near-me"
"vs"
"alternatives-to"
"problems-with"
"fix-vs-replace"
)

########################################
# HELPER
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
# GENERATE CHILDREN
########################################

for ITEM in "${BASE_QUERIES[@]}"
do
  BASE="$(echo "$ITEM" | cut -d'|' -f1)"
  VERTICAL="$(echo "$ITEM" | cut -d'|' -f2)"

  CITY="$(echo "$BASE" | grep -o 'san-diego\|encinitas\|carlsbad\|oceanside')"

  for INTENT in "${INTENTS[@]}"
  do

    ########################################
    # STANDARD CHILD
    ########################################

    SLUG="$INTENT-$BASE"
    TITLE="$(titleize "$INTENT $BASE")"
    KEYWORD="$(echo "$INTENT $BASE" | tr '-' ' ')"

    ROW="$SLUG,$TITLE,$CITY,$KEYWORD,$VERTICAL,$INTENT,pending"
    append_if_missing "$ROW"

    ########################################
    # COMPARISON VERSION
    ########################################

    if [ "$INTENT" = "vs" ]; then
      ALT="stripe-vs-square-$CITY"
      TITLE_ALT="$(titleize "$ALT")"
      KEYWORD_ALT="$(echo "$ALT" | tr '-' ' ')"
      ROW_ALT="$ALT,$TITLE_ALT,$CITY,$KEYWORD_ALT,$VERTICAL,comparison,pending"
      append_if_missing "$ROW_ALT"
    fi

  done

  ########################################
  # DEEP LONGTAIL VARIANTS
  ########################################

  DEEP_VARIANTS=(
    "for-small-business"
    "for-restaurants"
    "for-contractors"
    "for-startups"
    "for-homeowners"
  )

  for VARIANT in "${DEEP_VARIANTS[@]}"
  do
    SLUG="$BASE-$VARIANT"
    TITLE="$(titleize "$BASE $VARIANT")"
    KEYWORD="$(echo "$BASE $VARIANT" | tr '-' ' ')"

    ROW="$SLUG,$TITLE,$CITY,$KEYWORD,$VERTICAL,deep,pending"
    append_if_missing "$ROW"
  done

done

echo "---------------------------------------"
echo "Inventory Build Complete"
echo "---------------------------------------"
