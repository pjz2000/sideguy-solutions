#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================="
echo "SideGuy Safe Layered Upgrade Engine v7"
echo "======================================="

PAGES=(
  "ai-storage-solutions.html"
  "square-vs-stripe.html"
  "ai-business-solutions-san-diego.html"
)

########################################
# SAFE APPEND HELPERS
########################################

append_block_if_missing() {
  FILE="$1"
  KEY="$2"
  BLOCK="$3"

  [ -f "$FILE" ] || return

  if ! grep -q "$KEY" "$FILE"; then
    sed -i "/<\/body>/i $BLOCK" "$FILE"
    echo "Layer added: $KEY -> $FILE"
  else
    echo "Already exists: $KEY -> $FILE"
  fi
}

########################################
# RUN SAFE LAYERS
########################################

for FILE in "${PAGES[@]}"; do
  append_block_if_missing "$FILE" "Quick Savings Calculator" \
'<div class="box"><h2>Quick Savings Calculator</h2><p>If the wrong choice leaks $500/month, that is <strong>$6,000/year</strong> in preventable loss.</p></div>'

  append_block_if_missing "$FILE" "Fast Human Shortcut" \
'<div class="box"><h2>Fast Human Shortcut</h2><p>Text PJ for the fastest correct implementation path.</p></div>'

  append_block_if_missing "$FILE" "Best Next Move Selector" \
'<div class="box"><h2>Best Next Move Selector</h2><p>Choose by urgency, ROI, migration complexity, and long-term operating leverage.</p></div>'
done

git add .
git commit -m "Safe layered upgrade v7: preserve winners and append monetization blocks"

echo "======================================="
echo "DONE: safe upgrades applied"
echo "No winner pages overwritten"
echo "======================================="
