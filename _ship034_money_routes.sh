#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================="
echo "SideGuy Money Route Optimizer v3"
echo "======================================="

DATE=$(date +%F)
INDEX="money-index.html"

########################################
# FRESH GSC MONEY WINNERS
########################################

WINNERS=(
  "ai-storage-solutions"
  "square-vs-stripe"
  "ai-business-solutions-san-diego"
)

########################################
# PAGE BUILDER
########################################

build_money_route() {
  SLUG="$1"
  FILE="${SLUG}.html"
  TITLE=$(echo "$SLUG" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

  cat > "$FILE" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>${TITLE} | SideGuy Money Engine</title>
<meta name="description" content="${TITLE} comparison logic, ROI calculator, implementation path, and human resolution.">
<link rel="canonical" href="https://www.sideguysolutions.com/${FILE}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 40px; line-height: 1.7; }
.box { padding: 20px; border: 1px solid #ddd; border-radius: 12px; margin: 20px 0; }
.cta { position: fixed; bottom: 20px; right: 20px; background: #111; color: white; padding: 16px 24px; border-radius: 999px; }
</style>
</head>
<body>

<h1>${TITLE}</h1>

<p>This route was built directly from live GSC demand telemetry and zero-click opportunity signals.</p>

<div class="box">
<h2>ROI / Cost Logic</h2>
<p>Show cost savings, migration effort, setup time, vendor risk, and operational upside.</p>
</div>

<div class="box">
<h2>Best Fit Decision</h2>
<p>Use this section to convert confusion into the best next business move.</p>
</div>

<div class="box">
<h2>Human Resolution</h2>
<p>Text PJ for implementation help, migration support, or local vendor routing.</p>
</div>

<a class="cta" href="sms:+17735441231">Text PJ</a>

</body>
</html>
EOF

  echo "Built: $FILE"

  grep -q "$FILE" "$INDEX" || sed -i "/<\/body>/i <p><a href=\"${FILE}\">${TITLE}</a></p>" "$INDEX"
}

########################################
# RUN
########################################

for route in "${WINNERS[@]}"; do
  build_money_route "$route"
done

git add .
git commit -m "Money route optimizer v3 from fresh GSC zero-click winners"

echo "======================================="
echo "DONE: money routes expanded from GSC"
echo "======================================="
