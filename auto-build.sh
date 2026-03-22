#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "---------------------------------------"
echo "SideGuy Auto Build Engine v2 (Drip Mode)"
echo "---------------------------------------"

DATE=$(date +"%Y-%m-%d-%H%M")
QUEUE_FILE="seo-reserve/queue.csv"
LOG_FILE="docs/build-log.jsonl"

mkdir -p seo-reserve
mkdir -p docs

########################################
# AUTO LONGTAIL GENERATOR
########################################

CITIES=("san-diego" "carlsbad" "encinitas" "oceanside")
SERVICES=("ai-consulting" "payment-processing" "hvac-help" "plumbing-help")

for CITY in "${CITIES[@]}"; do
  for SERVICE in "${SERVICES[@]}"; do

    SLUG="$CITY-$SERVICE"
    TITLE="$(echo $SERVICE | tr '-' ' ' | sed 's/\b\(.*\)/\u\1/g') $(echo $CITY | tr '-' ' ' | sed 's/\b\(.*\)/\u\1/g')"
    KEYWORD="$SERVICE $CITY"

    if ! grep -q "$SLUG" "$QUEUE_FILE"; then
      echo "$SLUG,$TITLE,$CITY,$KEYWORD,pending" >> "$QUEUE_FILE"
    fi

  done
done

########################################
# RUN BUILDER (LIMIT DAILY OUTPUT)
########################################

bash auto-build.sh

########################################
# BUILD STATUS PAGE
########################################

STATUS_PAGE="build-status.html"

echo "<h1>SideGuy Build Status</h1>" > "$STATUS_PAGE"
echo "<p>Last Run: $DATE</p>" >> "$STATUS_PAGE"

echo "<h3>Recent Builds</h3><ul>" >> "$STATUS_PAGE"
tail -n 10 "$LOG_FILE" | while read LINE
do
  SLUG=$(echo "$LINE" | grep -o '"slug":"[^"]*' | cut -d'"' -f4)
  echo "<li><a href='/$SLUG/'>$SLUG</a></li>" >> "$STATUS_PAGE"
done
echo "</ul>" >> "$STATUS_PAGE"

echo "---------------------------------------"
echo "Drip Complete"
echo "---------------------------------------"