#!/usr/bin/env bash

########################################
# SIDEGUY CLOSE THE LOOP ENGINE v1
# Manual feedback collection system
# Pure observation - no auto-modification
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit

LOG_DIR="docs/pj-feedback"
OUT="$LOG_DIR/feedback-log.csv"
DATE="$(date +"%Y-%m-%d %H:%M:%S")"

mkdir -p "$LOG_DIR"

echo "---------------------------------------"
echo "🔁 CLOSE THE LOOP ENGINE"
echo "---------------------------------------"

########################################
# INIT CSV IF NEEDED
########################################

if [ ! -f "$OUT" ]; then
  echo "timestamp,page,question,intent,confusion,outcome" > "$OUT"
fi

########################################
# INPUT (manual for now)
########################################

echo ""
echo "Enter page URL (or filename):"
read -r PAGE

echo ""
echo "Enter user question:"
read -r QUESTION

echo ""
echo "Intent (cost/decision/compare/call/general):"
read -r INTENT

echo ""
echo "Confusion point (what wasn't clear):"
read -r CONFUSION

echo ""
echo "Outcome (quote/helped/left/called/unclear):"
read -r OUTCOME

########################################
# SAVE
########################################

# Escape quotes in input
PAGE="${PAGE//\"/\"\"}"
QUESTION="${QUESTION//\"/\"\"}"
INTENT="${INTENT//\"/\"\"}"
CONFUSION="${CONFUSION//\"/\"\"}"
OUTCOME="${OUTCOME//\"/\"\"}"

echo "\"$DATE\",\"$PAGE\",\"$QUESTION\",\"$INTENT\",\"$CONFUSION\",\"$OUTCOME\"" >> "$OUT"

echo ""
echo "✅ Feedback logged"
echo "📊 Total entries: $(tail -n +2 "$OUT" | wc -l)"
echo ""
echo "Review at: $OUT"
