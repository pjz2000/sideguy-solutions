#!/usr/bin/env bash

echo ""
echo "===================================================="
echo "SIDEGUY INVENTORY + MOG ENGINE v10"
echo "GSC Signals + Comparison + Longtail Expansion"
echo "===================================================="
echo ""

cd /workspaces/sideguy-solutions || exit 0

QUEUE_FILE="seo-reserve/queue.csv"
mkdir -p seo-reserve logs

touch "$QUEUE_FILE"

DATE=$(date +"%Y-%m-%d")

########################################
# SETTINGS
########################################

CITIES=("san-diego" "encinitas" "carlsbad" "oceanside")

########################################
# HELPERS (IMPROVED)
########################################

slugify() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-'
}

titleize() {
  echo "$1" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g'
}

exists() {
  grep -q "^$1," "$QUEUE_FILE" 2>/dev/null
}

append() {
  if ! exists "$1"; then
    echo "$2" >> "$QUEUE_FILE"
    echo "[+] $1"
  fi
}

########################################
# 1. MOG (COMPARISON DOMINANCE)
########################################

echo "→ Building MOG comparisons..."

MATCHUPS=(
"stripe|square|payments"
"zapier|make|ai"
"shopify|woocommerce|ecommerce"
"quickbooks|xero|finance"
"mini-split|central-air|hvac"
"repair|replace|home-services"
"ai-consulting|automation-tools|ai"
"solar|grid-power|energy"
"tesla|gas-car|energy"
"contractor|diy|home-services"
)

VARIANTS=(
"which-is-better"
"pros-and-cons"
"cost-comparison"
"for-small-business"
"what-to-choose"
)

for MATCH in "${MATCHUPS[@]}"; do

  A=$(echo "$MATCH" | cut -d'|' -f1)
  B=$(echo "$MATCH" | cut -d'|' -f2)
  VERTICAL=$(echo "$MATCH" | cut -d'|' -f3)

  BASE=$(slugify "$A vs $B")

  ########################################
  # GLOBAL
  ########################################

  TITLE="$(titleize "$A vs $B") (Which Is Better?)"
  KEYWORD="$A vs $B"

  append "$BASE" "$BASE,$TITLE,global,$KEYWORD,$VERTICAL,comparison,pending"

  ########################################
  # LOCAL
  ########################################

  for CITY in "${CITIES[@]}"; do
    SLUG="$BASE-$CITY"
    TITLE="$(titleize "$A vs $B in $CITY")"

    append "$SLUG" "$SLUG,$TITLE,$CITY,$KEYWORD $CITY,$VERTICAL,local,pending"
  done

  ########################################
  # VARIANTS
  ########################################

  for VAR in "${VARIANTS[@]}"; do
    SLUG="$BASE-$VAR"
    TITLE="$(titleize "$A vs $B $VAR")"

    append "$SLUG" "$SLUG,$TITLE,global,$KEYWORD $VAR,$VERTICAL,decision,pending"
  done

done

########################################
# 2. GSC INVENTORY EXPANSION
########################################

echo ""
echo "→ Expanding GSC queries..."

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

INTENTS=(
"best"
"how-to"
"cost-of"
"who-to-hire"
"is-it-worth"
"near-me"
"fix"
"problems-with"
"alternatives"
"guide"
)

DEEP=(
"for-small-business"
"for-homeowners"
"for-contractors"
"for-restaurants"
"for-startups"
)

for ITEM in "${BASE_QUERIES[@]}"; do

  BASE=$(echo "$ITEM" | cut -d'|' -f1)
  VERTICAL=$(echo "$ITEM" | cut -d'|' -f2)

  SLUG="$BASE"
  TITLE="$(titleize "$BASE")"

  append "$SLUG" "$SLUG,$TITLE,local,$BASE,$VERTICAL,core,pending"

  ########################################
  # INTENT CHILDREN
  ########################################

  for INTENT in "${INTENTS[@]}"; do
    SLUG="$INTENT-$BASE"
    TITLE="$(titleize "$INTENT $BASE")"

    append "$SLUG" "$SLUG,$TITLE,local,$INTENT $BASE,$VERTICAL,intent,pending"
  done

  ########################################
  # DEEP VARIANTS
  ########################################

  for VAR in "${DEEP[@]}"; do
    SLUG="$BASE-$VAR"
    TITLE="$(titleize "$BASE $VAR")"

    append "$SLUG" "$SLUG,$TITLE,local,$BASE $VAR,$VERTICAL,deep,pending"
  done

done

########################################
# SUMMARY
########################################

TOTAL=$(wc -l < "$QUEUE_FILE")

echo ""
echo "===================================================="
echo "INVENTORY COMPLETE"
echo "Total pages queued: $TOTAL"
echo "===================================================="
echo ""

echo "$DATE inventory run → $TOTAL pages" >> logs/inventory.log
