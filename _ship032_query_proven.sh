#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

echo "======================================="
echo "SideGuy Query-Proven Improvement v1"
echo "======================================="

DATE=$(date +%F)
SITEMAP="sitemap.xml"
INDEX="index.html"

########################################
# LIVE WINNER ROUTES FROM GSC
########################################

QUERIES=(
  "stripe-vs-square|payments"
  "zapier-vs-make|automation"
  "ai-storage-solutions|ai"
  "payment-processing-san-diego|local"
  "electric-panel-upgrade-san-diego|local"
  "enterprise-software-consulting|b2b"
)

########################################
# PAGE TEMPLATE BUILDER
########################################

build_page() {
  SLUG="$1"
  VERTICAL="$2"
  FILE="${SLUG}.html"
  TITLE=$(echo "$SLUG" | tr '-' ' ' | sed 's/\b\(.\)/\u\1/g')

  cat > "$FILE" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>${TITLE} | SideGuy Solutions</title>
<meta name="description" content="${TITLE} help, pricing logic, calculators, next steps, and real human resolution.">
<link rel="canonical" href="https://www.sideguysolutions.com/${FILE}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 40px; line-height: 1.7; }
.hero { font-size: 2rem; margin-bottom: 20px; }
.box { padding: 20px; border: 1px solid #ddd; margin: 20px 0; border-radius: 12px; }
.cta { position: fixed; bottom: 20px; right: 20px; background: #111; color: #fff; padding: 16px 22px; border-radius: 999px; }
</style>
</head>
<body>

<h1 class="hero">${TITLE}</h1>

<p>SideGuy listens to real internet demand and builds the exact clarity layer users need. This page exists because real search signals proved repeated confusion around <strong>${TITLE}</strong>.</p>

<div class="box">
<h2>Decision Framework</h2>
<p>Compare pricing, migration effort, urgency, local availability, long-term ROI, and implementation risk.</p>
</div>

<div class="box">
<h2>Next Best Tool</h2>
<p>Add calculator, checklist, worksheet, or routing logic here based on real demand telemetry.</p>
</div>

<div class="box">
<h2>Human Resolution Lane</h2>
<p>Need help making the right move? Text PJ before wasting time or money on the wrong vendor.</p>
</div>

<a class="cta" href="sms:+17735441231">Text PJ</a>

</body>
</html>
EOF

  echo "Built: $FILE"

  grep -q "$FILE" "$SITEMAP" || sed -i "/<\/urlset>/i <url><loc>https://www.sideguysolutions.com/${FILE}</loc><lastmod>${DATE}</lastmod></url>" "$SITEMAP"

  grep -q "$FILE" "$INDEX" || sed -i "/<\/body>/i <p><a href=\"${FILE}\">${TITLE}</a></p>" "$INDEX"
}

########################################
# CHILD PAGE SPAWNER
########################################

spawn_children() {
  BASE="$1"

  build_page "${BASE}-calculator" "tool"
  build_page "${BASE}-checklist" "tool"
  build_page "${BASE}-pricing-guide" "tool"
}

########################################
# RUN
########################################

for row in "${QUERIES[@]}"; do
  IFS="|" read -r SLUG VERTICAL <<< "$row"

  build_page "$SLUG" "$VERTICAL"
  spawn_children "$SLUG"
done

########################################
# LOG + COMMIT
########################################

git add .
git commit -m "Query-proven improvement cycle: winner routes + child product lanes"

echo "======================================="
echo "DONE: Query-Proven routes upgraded"
echo "Winner routes now compounding"
echo "======================================="
