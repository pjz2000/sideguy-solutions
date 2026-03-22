#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"

cd "$PROJECT_ROOT" || return

echo "---------------------------------------"
echo "SideGuy Manifest Generator v4"
echo "---------------------------------------"

QUEUE_FILE="seo-reserve/queue.csv"
DATE=$(date +"%Y-%m-%d")

mkdir -p seo-reserve

########################################
# INTENT PATTERNS
########################################

INTENTS=(
"should-i"
"best-way-to"
"how-to"
"how-much-does"
"is-it-worth"
"who-do-i-call-for"
"fix-vs-replace"
"near-me"
)

########################################
# VERTICALS + SERVICES
########################################

declare -A SERVICES

SERVICES[payment-processing]="payment-processing merchant-fees pos-system credit-card-processing"
SERVICES[hvac]="hvac-help ac-repair mini-split air-conditioning furnace"
SERVICES[ai]="ai-consulting ai-automation chatgpt-for-business business-automation ai-tools"

########################################
# CITIES
########################################

CITIES=("san-diego" "encinitas" "carlsbad" "oceanside")

########################################
# GENERATE LONGTAIL
########################################

for CITY in "${CITIES[@]}"
do
  for VERTICAL in "${!SERVICES[@]}"
  do
    for SERVICE in ${SERVICES[$VERTICAL]}
    do
      for INTENT in "${INTENTS[@]}"
      do

        SLUG="$INTENT-$SERVICE-$CITY"

        TITLE="$(echo "$INTENT $SERVICE $CITY" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')"

        KEYWORD="$(echo "$INTENT $SERVICE $CITY" | tr '-' ' ')"

        ROW="$SLUG,$TITLE,$CITY,$KEYWORD,$VERTICAL,$INTENT,pending"

        if ! grep -q "^$SLUG," "$QUEUE_FILE"; then
          echo "$ROW" >> "$QUEUE_FILE"
        fi

      done
    done
  done
done

echo "---------------------------------------"
echo "Manifest v4 Complete"
echo "---------------------------------------"
