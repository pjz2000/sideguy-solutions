#!/usr/bin/env bash

echo ""
echo "=================================================="
echo "SIDEGUY PRIORITY + MONEY ENGINE (ELITE)"
echo "Signals → Pages → Value → Next Moves"
echo "=================================================="
echo ""

cd /workspaces/sideguy-solutions || exit 1

mkdir -p tools/priority
mkdir -p docs/priority
mkdir -p logs

########################################
# 0. KEYWORD SIGNAL INPUT (YOUR DATA)
########################################

KEYWORDS="docs/priority/keyword-signals.txt"

cat > "$KEYWORDS" <<'EOF'
ai storage solutions|11
stripe vs square|9
square vs stripe|5
payment processing san diego|4
instant settlement|4
workflow automation san diego|3
auto repair shop pillar pages|2
plumbing issues|2
water main repair|2
san diego hvac answering service|2
EOF

########################################
# 1. PRIORITY ENGINE (SCORING FIXED)
########################################

PRIORITY_REPORT="docs/priority/page-priority-report.txt"

echo "Building page priority..."

{
  echo "SideGuy Page Priority Report"
  echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
} > "$PRIORITY_REPORT"

DATA_TMP=$(mktemp)

while IFS= read -r file; do

  words=$(wc -w < "$file")
  links=$(grep -o "<a " "$file" | wc -l | tr -d ' ')
  pj=$(grep -c "Text PJ" "$file" || true)

  score=0

  # CONTENT DEPTH
  if [ "$words" -gt 800 ]; then score=$((score+3))
  elif [ "$words" -gt 400 ]; then score=$((score+2))
  fi

  # LINKING
  if [ "$links" -gt 8 ]; then score=$((score+3))
  elif [ "$links" -gt 4 ]; then score=$((score+2))
  fi

  # CTA
  if [ "$pj" -gt 0 ]; then score=$((score+4)); fi

  echo "$score | $file | words:$words links:$links pj:$pj"

done < <(find public -name "*.html") | sort -rn >> "$DATA_TMP"

cat "$DATA_TMP" >> "$PRIORITY_REPORT"
rm -f "$DATA_TMP"

echo "[✓] Priority report ready → $PRIORITY_REPORT"

########################################
# 2. MONEY PAGE DETECTION (UPGRADED)
########################################

MONEY_REPORT="docs/priority/money-pages.txt"

echo "Scanning money pages..."

{
  echo "High Intent Pages"
  echo ""
} > "$MONEY_REPORT"

MONEY_TMP=$(mktemp)

while IFS= read -r file; do

  if grep -qiE "repair|replace|cost|price|install|should i|worth it" "$file"; then
    words=$(wc -w < "$file")
    echo "$words | $file"
  fi

done < <(find public -name "*.html") | sort -rn >> "$MONEY_TMP"

cat "$MONEY_TMP" >> "$MONEY_REPORT"
rm -f "$MONEY_TMP"

echo "[✓] Money pages → $MONEY_REPORT"

########################################
# 3. KEYWORD → PAGE OPPORTUNITY MATCH
########################################

OPPS="docs/priority/opportunities.txt"

echo "Matching keywords to pages..."

{
  echo "Keyword Opportunities"
  echo ""
} > "$OPPS"

while IFS="|" read -r keyword volume; do

  # -F = fixed string (safe for spaces/special chars in keywords)
  matches=$(grep -riF "$keyword" public --include="*.html" -l 2>/dev/null | wc -l | tr -d ' ')

  if [ "$matches" -eq 0 ]; then
    echo "BUILD: $keyword (vol:$volume)"
  else
    echo "EXPAND: $keyword → $matches pages"
  fi

done < "$KEYWORDS" >> "$OPPS"

echo "[✓] Opportunities → $OPPS"

########################################
# 4. VALUE SIGNAL (REAL MONEY PRIORITY)
########################################

VALUE="docs/priority/high-value-focus.txt"

echo "Calculating high-value focus..."

{
  echo "HIGH VALUE FOCUS"
  echo ""
  grep -Ei "payment|hvac|plumbing|solar|repair|install" "$OPPS" || echo "  (none matched)"
} > "$VALUE"

echo "[✓] Value focus → $VALUE"

########################################
# 5. FINAL OUTPUT (WHAT TO ACTUALLY DO)
########################################

echo ""
echo "=================================================="
echo "WHAT TO DO NEXT"
echo "=================================================="
echo ""

echo "1. BUILD THESE (no pages exist):"
grep "^BUILD:" "$OPPS" || echo "  (none — all keywords have pages)"

echo ""
echo "2. EXPAND THESE (already have pages):"
grep "^EXPAND:" "$OPPS" || echo "  (none)"

echo ""
echo "3. PRIORITY MONEY PAGES:"
head -10 "$MONEY_REPORT"

echo ""
echo "4. TOP PERFORMING PAGES:"
head -15 "$PRIORITY_REPORT"

echo ""
echo "=================================================="
echo "ENGINE COMPLETE"
echo "=================================================="
echo ""
