#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================="
echo "SideGuy Money Calculator Injector v6"
echo "======================================="

PAGES=(
  "ai-storage-solutions.html"
  "ai-business-solutions-san-diego.html"
  "electric-panel-upgrade-san-diego.html"
)

for FILE in "${PAGES[@]}"; do
  [ -f "$FILE" ] || continue

  if ! grep -q "Quick Savings Calculator" "$FILE"; then
    sed -i '/<\/body>/i \
<div class="box">\
<h2>Quick Savings Calculator</h2>\
<p>If the wrong choice costs \$500/month in lost efficiency, downtime, or bad vendor fees, that is <strong>\$6,000/year</strong> in preventable leakage.</p>\
<p>Use this as the baseline before deciding your next move.</p>\
</div>' "$FILE"
  fi

  echo "Calculator block injected into $FILE"
done

git add .
git commit -m "Money calculator injector v6 for top CTR-lift routes"

echo "======================================="
echo "DONE: money calculators added"
echo "======================================="
