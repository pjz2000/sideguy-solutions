#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================="
echo "SideGuy Zero-Click CTR Lift v4"
echo "======================================="

########################################
# TOP LIVE ZERO-CLICK WINNERS
########################################

PAGES=(
  "ai-storage-solutions.html"
  "ai-business-solutions-san-diego.html"
  "electric-panel-upgrade-san-diego.html"
  "plumbing-issues-san-diego.html"
)

########################################
# CTR + CONVERSION BLOCK INJECTOR
########################################

for FILE in "${PAGES[@]}"; do
  [ -f "$FILE" ] || continue

  if ! grep -q "Best Next Move Selector" "$FILE"; then
    sed -i '/<\/body>/i \
<div class="box">\
<h2>Best Next Move Selector</h2>\
<p>Choose based on urgency, total cost, migration effort, long-term ROI, and vendor reliability.</p>\
</div>\
<div class="box">\
<h2>Expected Savings / Risk</h2>\
<p>Show users the cost of waiting, wrong vendor choices, downtime, or missed automation upside.</p>\
</div>\
<div class="box">\
<h2>Fast Human Shortcut</h2>\
<p>Want the fastest correct answer? Text PJ and skip the expensive wrong turn.</p>\
</div>' "$FILE"
  fi

  echo "CTR-lift blocks injected into $FILE"
done

git add .
git commit -m "CTR lift v4: inject selector + savings + human shortcut blocks"

echo "======================================="
echo "DONE: zero-click pages upgraded for CTR"
echo "======================================="
