#!/usr/bin/env bash

########################################
# SIDEGUY ONE ENGINE
# Authority + AI + Deals + Feedback Loop
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

echo "=================================================="
echo "SIDEGUY ONE ENGINE"
echo "Content → Authority → Leads → Deals → Expansion"
echo "=================================================="

########################################
# SAFE SETUP
########################################

mkdir -p tools/outbound
mkdir -p public/ai-mode
mkdir -p data/deals
mkdir -p docs/feedback
mkdir -p logs/responder

########################################
# ENSURE DEAL FILE EXISTS
########################################

DEALS_FILE="data/deals/deals.json"

if [ ! -f "$DEALS_FILE" ]; then
  echo "[]" > "$DEALS_FILE"
fi

########################################
# 1. AI MODE PAGE BUILDER (SAFE)
########################################

build_ai_page () {

  FILE=$1
  TITLE=$2

  if [ -f "$FILE" ]; then
    echo "SKIP $FILE"
    return
  fi

cat > "$FILE" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<title>$TITLE | SideGuy</title>
<meta name="viewport" content="width=device-width">
<meta name="description" content="$TITLE explained simply with real-world clarity.">
<link rel="canonical" href="https://sideguy.solutions/ai-mode/$(basename $FILE)">
</head>

<body style="font-family:Arial;background:#0a0f1c;color:#e6f0ff;padding:30px;">

<h1>$TITLE</h1>
<p><strong>Updated:</strong> $(date)</p>

<h2>🔍 The Shift</h2>
<p>Search is moving from links to answers.</p>

<h2>🧠 What AI Wants</h2>
<ul>
<li>clear answers</li>
<li>structured info</li>
<li>consistent topics</li>
</ul>

<h2>⚡ SideGuy Insight</h2>
<p>We build content AI can USE — not just rank.</p>

<h2>💬 Need clarity?</h2>
<p>Text PJ before you spend money.</p>

<a href="sms:+17735441231"
style="position:fixed;bottom:20px;right:20px;background:#00ffaa;padding:15px;border-radius:50px;font-weight:bold;">
💬 Text PJ
</a>

</body>
</html>
HTML

echo "[✓] Built $FILE"
}

echo ""
echo "Building AI Authority Pages..."

build_ai_page public/ai-mode/what-is-google-ai-mode.html "What Is Google AI Mode"
build_ai_page public/ai-mode/how-to-get-cited-by-ai.html "How To Get Cited By AI"
build_ai_page public/ai-mode/ai-seo-vs-traditional-seo.html "AI SEO vs Traditional SEO"
build_ai_page public/ai-mode/what-makes-content-ai-credible.html "What Makes Content AI Credible"
build_ai_page public/ai-mode/future-of-search-ai-first.html "Future of AI Search"

########################################
# 2. OUTBOUND AUTHORITY INJECTOR (SAFE)
########################################

OUTBOUND="tools/outbound/outbound-block.html"

if [ ! -f "$OUTBOUND" ]; then
cat > "$OUTBOUND" <<'EOF'
<div class="sideguy-outbound">

<hr/>

<h2>🔗 Related Resources</h2>

<ul>
<li><a href="https://en.wikipedia.org/wiki/HVAC" target="_blank">HVAC Overview</a></li>
<li><a href="https://www.energy.gov/" target="_blank">Energy.gov</a></li>
</ul>

<h3>🧠 SideGuy Take</h3>
<p>Most advice is generic. SideGuy helps YOU decide what actually matters.</p>

</div>
EOF
fi

inject_outbound () {

  FILE=$1

  if grep -q "sideguy-outbound" "$FILE"; then
    return
  fi

  TMP=$(mktemp)

  awk '
  /<\/body>/ {
    print "<!-- OUTBOUND AUTHORITY -->"
    system("cat tools/outbound/outbound-block.html")
  }
  {print}
  ' "$FILE" > "$TMP"

  mv "$TMP" "$FILE"

  echo "[✓] Outbound added → $FILE"
}

echo ""
echo "Injecting outbound authority..."

while IFS= read -r file; do
  inject_outbound "$file"
done < <(find public -name "*.html")

########################################
# 3. SCALE PAGE GENERATOR (MONEY PAGES)
########################################

echo ""
echo "Generating high-intent pages..."

topics=("hvac" "solar" "plumbing")
locations=("san-diego" "encinitas")
patterns=("repair-or-replace" "cost-of")

mkdir -p public/scale-pages

for topic in "${topics[@]}"; do
  for location in "${locations[@]}"; do
    for pattern in "${patterns[@]}"; do

      slug="$topic-$pattern-$location"
      file="public/scale-pages/$slug.html"

      if [ -f "$file" ]; then continue; fi

cat > "$file" <<HTML
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>$slug | SideGuy</title>
<meta name="description" content="Get clarity on $slug before you spend money. Real human help from SideGuy.">
</head>
<body style="background:#07131f;color:#eaf6ff;padding:30px;">

<h1>$slug</h1>

<p>Before you spend money, get clarity.</p>

<a href="sms:+17735441231">💬 Text PJ</a>

</body>
</html>
HTML

echo "[✓] Built $file"

    done
  done
done

########################################
# 4. DEAL → CONTENT FEEDBACK LOOP
########################################

echo ""
echo "Analyzing deals → content expansion..."

FEEDBACK="docs/feedback/build-next.txt"

if command -v jq >/dev/null 2>&1; then
  jq -r '
  group_by(.category)[] |
  "EXPAND: \(.[0].category) | deals: \(length)"
  ' "$DEALS_FILE" > "$FEEDBACK"
  echo "[✓] Feedback → $FEEDBACK"
else
  echo "[SKIP] jq not installed — skipping deal analysis"
fi

########################################
# 5. HIGH VALUE SIGNAL DETECTION
########################################

INPUT="logs/responder/inbox.txt"
OUTPUT="logs/high-value.txt"

if [ -f "$INPUT" ]; then

> "$OUTPUT"

while IFS= read -r line; do
  if echo "$line" | grep -qiE "cost|price|repair|replace|install"; then
    echo "$line" >> "$OUTPUT"
  fi
done < "$INPUT"

echo "[✓] High-value leads extracted"

fi

########################################
# 6. SUMMARY
########################################

echo ""
echo "=================================================="
echo "SIDEGUY ENGINE COMPLETE"
echo "=================================================="
echo ""

echo "NEXT STEPS:"
echo "1. Check texts"
echo "2. Log deals"
echo "3. Expand winning categories"
echo ""
