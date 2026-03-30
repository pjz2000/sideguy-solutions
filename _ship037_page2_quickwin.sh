#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================="
echo "SideGuy Page-2 Quick Win v9"
echo "======================================="

########################################
# FASTEST PAGE-2 WINNERS FROM PIC DATA
########################################

PAGES=(
  "plumbing-issues-san-diego.html|Plumbing Issues San Diego: Cost, Fast Fixes & Who to Call"
  "ai-business-solutions-san-diego.html|AI Business Solutions San Diego: Save Time, Reduce Labor Costs"
)

########################################
# SAFE TITLE + META + INTERNAL LINK BOOST
########################################

for row in "${PAGES[@]}"; do
  IFS="|" read -r FILE TITLE <<< "$row"

  [ -f "$FILE" ] || continue

  # safer title replace (use @ as delimiter to avoid pipe conflicts)
  perl -0pi -e "s@<title>.*?</title>@<title>${TITLE} \\| SideGuy Solutions</title>@s" "$FILE"

  # add meta if missing
  if ! grep -q 'name="description"' "$FILE"; then
    sed -i "/<title>/a <meta name=\"description\" content=\"Fast clarity on ${TITLE,,}. Compare costs, urgency, best next move, and text PJ for the fastest human resolution.\">" "$FILE"
  fi

  # inject quick internal win block
  if ! grep -q "Quick Win Upgrade" "$FILE"; then
    sed -i '/<\/body>/i \
<div class="box">\
<h2>Quick Win Upgrade</h2>\
<p>This page is actively optimized from live Google demand signals and designed to help you make the fastest correct move.</p>\
<p>Compare repair cost, replacement risk, timing urgency, and the best local next step.</p>\
</div>' "$FILE"
  fi

  echo "Quick-win optimized: $FILE"
done

git add .
git commit -m "Page-2 quick win v9: title meta and internal boost for position 28 routes"

echo "======================================="
echo "DONE: position 28 routes optimized"
echo "Target: push page 2 -> page 1"
echo "======================================="
