#!/usr/bin/env bash

########################################
# SIDEGUY SWARM v8
# priority + protection + pattern engine
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
PUBLIC_DIR="$PROJECT_ROOT/public"
DATA_DIR="$PROJECT_ROOT/data"
SWARM_DIR="$PROJECT_ROOT/docs/swarm"
MEMORY_FILE="$DATA_DIR/swarm-memory.csv"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || return

mkdir -p "$DATA_DIR" "$SWARM_DIR"

########################################
# CONFIG
########################################

GSC_FILE="$DATA_DIR/gsc-export.csv"

MAX_REWRITES=25
MAX_EXPANDS=10
MAX_TOOLS=15

########################################
# INIT MEMORY
########################################

if [ ! -f "$MEMORY_FILE" ]; then
  echo "slug,score,trend_streak,last_action,last_seen" > "$MEMORY_FILE"
fi

########################################
# HELPERS
########################################

safe_num() { echo "$1" | tr -cd '0-9.'; }

slug() {
  echo "$1" | sed 's#https\?://[^/]*/##' | sed 's#.html##'
}

intent() {
  Q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  if echo "$Q" | grep -Eq 'cost|price'; then echo "money"; return; fi
  if echo "$Q" | grep -Eq 'vs|best|compare'; then echo "compare"; return; fi
  if echo "$Q" | grep -Eq 'near me|service|repair'; then echo "service"; return; fi

  echo "info"
}

score() {
  awk "BEGIN {printf \"%.2f\", ($1/30)+($2*2)+($3)}"
}

pattern_detect() {
  Q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  if echo "$Q" | grep -q 'cost'; then echo "cost"; return; fi
  if echo "$Q" | grep -q 'vs'; then echo "vs"; return; fi
  if echo "$Q" | grep -q 'best'; then echo "best"; return; fi

  echo "general"
}

########################################
# BUILD PAGE SCORES
########################################

TMP=$(mktemp)

tail -n +2 "$GSC_FILE" | while IFS=',' read -r PAGE QUERY CLICKS IMPRESSIONS CTR POS
do
  S=$(slug "$PAGE")
  CLK=$(safe_num "$CLICKS")
  IMP=$(safe_num "$IMPRESSIONS")
  CTRV=$(safe_num "$CTR")

  [ -z "$IMP" ] && IMP=0
  [ -z "$CLK" ] && CLK=0
  [ -z "$CTRV" ] && CTRV=0

  INT=$(intent "$QUERY")
  SC=$(score "$IMP" "$CLK" "$CTRV")
  PAT=$(pattern_detect "$QUERY")

  echo "$S|$SC|$INT|$PAT|$QUERY" >> "$TMP"

done

########################################
# SORT BY SCORE
########################################

SORTED=$(mktemp)
sort -t'|' -k2,2nr "$TMP" > "$SORTED"

########################################
# RUN SWARM WITH CAPS
########################################

REWRITE_COUNT=0
EXPAND_COUNT=0
TOOL_COUNT=0

INDEX=0

while IFS='|' read -r SLUG SCORE INTENT PATTERN QUERY
do

  INDEX=$((INDEX + 1))

  ########################################
  # ELITE 20 ALWAYS PROCESS
  ########################################

  PRIORITY="normal"
  if [ "$INDEX" -le 20 ]; then
    PRIORITY="elite"
  fi

  ########################################
  # MEMORY CHECK (LOSER PROTECTION)
  ########################################

  LAST=$(grep "^$SLUG," "$MEMORY_FILE")

  TREND_STREAK=0
  if [ -n "$LAST" ]; then
    TREND_STREAK=$(echo "$LAST" | cut -d',' -f3)
  fi

  if [ "$TREND_STREAK" -le -3 ]; then
    echo "⛔ Skipping loser: $SLUG"
    continue
  fi

  ########################################
  # DECISION
  ########################################

  ACTION="hold"

  if (( $(echo "$SCORE > 15" | bc -l) )); then
    ACTION="expand"
  elif (( $(echo "$SCORE > 8" | bc -l) )); then
    ACTION="rewrite"
  fi

  ########################################
  # APPLY CAPS
  ########################################

  if [ "$ACTION" = "rewrite" ] && [ "$REWRITE_COUNT" -ge "$MAX_REWRITES" ]; then
    continue
  fi

  if [ "$ACTION" = "expand" ] && [ "$EXPAND_COUNT" -ge "$MAX_EXPANDS" ]; then
    continue
  fi

  ########################################
  # EXECUTE
  ########################################

  FILE="$PUBLIC_DIR/$SLUG.html"

  if [ -f "$FILE" ]; then

    if [ "$ACTION" = "rewrite" ]; then
      sed -i "s#<title>.*</title>#<title>$QUERY | SideGuy</title>#g" "$FILE"
      REWRITE_COUNT=$((REWRITE_COUNT + 1))
      echo "✏️ Rewrite: $SLUG"
    fi

    if [ "$ACTION" = "expand" ]; then

      CHILD="$PUBLIC_DIR/${SLUG}-${PATTERN}.html"

      if [ ! -f "$CHILD" ]; then
        echo "<h1>$QUERY - $PATTERN guide</h1>" > "$CHILD"
        EXPAND_COUNT=$((EXPAND_COUNT + 1))
        echo "🚀 Expand: $SLUG → $PATTERN"
      fi

    fi

    ########################################
    # TOOL PLACEHOLDER (ELITE ONLY)
    ########################################

    if [ "$PRIORITY" = "elite" ] && [ "$TOOL_COUNT" -lt "$MAX_TOOLS" ]; then

      if ! grep -q "sideguy-tool" "$FILE"; then
        echo "<div class='sideguy-tool'>Future tool here</div>" >> "$FILE"
        TOOL_COUNT=$((TOOL_COUNT + 1))
        echo "💰 Tool slot: $SLUG"
      fi

    fi

  fi

  ########################################
  # UPDATE MEMORY
  ########################################

  grep -v "^$SLUG," "$MEMORY_FILE" > tmp.csv

  echo "$SLUG,$SCORE,0,$ACTION,$DATE" >> tmp.csv

  mv tmp.csv "$MEMORY_FILE"

done < "$SORTED"

########################################
# FINISH
########################################

echo "--------------------------------"
echo "Swarm v8 Complete"
echo "Rewrites: $REWRITE_COUNT"
echo "Expands: $EXPAND_COUNT"
echo "Tools: $TOOL_COUNT"
echo "--------------------------------"

git add .
git commit -m "swarm v8: priority brain + caps + protection ($DATE)"
