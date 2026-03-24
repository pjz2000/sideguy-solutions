#!/usr/bin/env bash

########################################
# SIDEGUY HYPER AUTO-ADAPT v1
# Detect winning patterns + apply globally
# Analyzes GSC performance, identifies
# high-performing content patterns, and
# replicates them across similar pages
########################################

set -e

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/gsc/query-pages.csv"
OUT_DIR="docs/auto-adapt"
LOG="$OUT_DIR/adapt-log.txt"
REPORT="$OUT_DIR/adapt-report.md"
PATTERN_FILE="$OUT_DIR/winning-patterns.txt"

# Safety: dry-run by default
DRY_RUN="${DRY_RUN:-true}"

# Thresholds for "winning" patterns
MIN_CLICKS="${MIN_CLICKS:-20}"
MIN_IMPRESSIONS="${MIN_IMPRESSIONS:-300}"

# Max pages to update
MAX_UPDATES="${MAX_UPDATES:-100}"

########################################
# PREFLIGHT
########################################

echo ""
echo "---------------------------------------"
echo "🧠 SIDEGUY HYPER AUTO-ADAPT v1"
echo "---------------------------------------"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "⚠️  DRY RUN MODE — Preview only (set DRY_RUN=false to apply)"
  echo ""
fi

if [[ ! -f "$INPUT" ]]; then
  echo "❌ Missing: $INPUT"
  exit 1
fi

mkdir -p "$OUT_DIR"

echo "📂 Input:  $INPUT"
echo "📂 Output: $OUT_DIR"
echo "🎯 Thresholds: $MIN_CLICKS clicks, $MIN_IMPRESSIONS impressions"
echo "🎯 Max updates: $MAX_UPDATES"
echo ""

########################################
# HELPERS
########################################

normalize_url() {
  local url="$1"
  url="${url#https://www.sideguysolutions.com/}"
  url="${url#https://sideguysolutions.com/}"
  url="${url%%\?*}"
  url="${url%%\#*}"
  [ -z "$url" ] && echo "index.html" && return
  [[ "$url" != *.html ]] && url="$url.html"
  echo "$url"
}

detect_cluster() {
  local text="$1"
  text=$(echo "$text" | tr '[:upper:]' '[:lower:]')

  if [[ "$text" =~ hvac|air\ conditioning|mini\ split|furnace|heat\ pump ]]; then
    echo "hvac"
  elif [[ "$text" =~ tesla|ev\ charger|charger\ install ]]; then
    echo "tesla"
  elif [[ "$text" =~ stripe|square|merchant|payment ]]; then
    echo "payments"
  elif [[ "$text" =~ solar|battery|powerwall ]]; then
    echo "solar"
  elif [[ "$text" =~ plumb|water\ heater|drain ]]; then
    echo "plumbing"
  else
    echo "general"
  fi
}

########################################
# PHASE 1: DETECT WINNING PATTERNS
########################################

echo "🔍 Phase 1: Detecting winning patterns..."
echo ""

HVAC_WIN=false
TESLA_WIN=false
PAYMENTS_WIN=false
SOLAR_WIN=false
PLUMBING_WIN=false

> "$PATTERN_FILE"  # Clear pattern file

tail -n +2 "$INPUT" | while IFS=, read -r page query clicks impressions ctr position; do

  # Skip if below thresholds
  [ -z "$clicks" ] || [ "$clicks" -lt "$MIN_CLICKS" ] && continue
  [ -z "$impressions" ] || [ "$impressions" -lt "$MIN_IMPRESSIONS" ] && continue

  FILE=$(normalize_url "$page")
  [ ! -f "$FILE" ] && continue

  CLUSTER=$(detect_cluster "$page $query")

  case "$CLUSTER" in
    hvac)
      echo "WINNER|hvac|$FILE|$clicks|$impressions" >> "$PATTERN_FILE"
      ;;
    tesla)
      echo "WINNER|tesla|$FILE|$clicks|$impressions" >> "$PATTERN_FILE"
      ;;
    payments)
      echo "WINNER|payments|$FILE|$clicks|$impressions" >> "$PATTERN_FILE"
      ;;
    solar)
      echo "WINNER|solar|$FILE|$clicks|$impressions" >> "$PATTERN_FILE"
      ;;
    plumbing)
      echo "WINNER|plumbing|$FILE|$clicks|$impressions" >> "$PATTERN_FILE"
      ;;
  esac

done

# Analyze patterns
if grep -q "^WINNER|hvac" "$PATTERN_FILE"; then
  HVAC_WIN=true
  echo "  ✓ HVAC cluster showing strong performance"
fi

if grep -q "^WINNER|tesla" "$PATTERN_FILE"; then
  TESLA_WIN=true
  echo "  ✓ Tesla cluster showing strong performance"
fi

if grep -q "^WINNER|payments" "$PATTERN_FILE"; then
  PAYMENTS_WIN=true
  echo "  ✓ Payments cluster showing strong performance"
fi

if grep -q "^WINNER|solar" "$PATTERN_FILE"; then
  SOLAR_WIN=true
  echo "  ✓ Solar cluster showing strong performance"
fi

if grep -q "^WINNER|plumbing" "$PATTERN_FILE"; then
  PLUMBING_WIN=true
  echo "  ✓ Plumbing cluster showing strong performance"
fi

echo ""

########################################
# PATTERN BLOCKS
########################################

DECISION_BLOCK='
<section data-auto-adapt="decision-v1" style="background:var(--card,#f4fbff);padding:18px 22px;border-radius:var(--r,12px);margin:20px 0;border:1px solid rgba(7,48,68,.08);">
<h3 style="margin:0 0 10px 0;color:var(--ink,#073044);font-size:1rem;">Quick Decision Check</h3>
<div style="display:flex;gap:8px;margin:10px 0;">
  <button onclick="sgAutoDecide(`repair`)" style="padding:8px 16px;background:#fff;border:2px solid var(--mint,#21d3a1);color:var(--ink,#073044);border-radius:8px;cursor:pointer;font-weight:600;font-size:0.9rem;">Repair</button>
  <button onclick="sgAutoDecide(`replace`)" style="padding:8px 16px;background:#fff;border:2px solid var(--mint,#21d3a1);color:var(--ink,#073044);border-radius:8px;cursor:pointer;font-weight:600;font-size:0.9rem;">Replace</button>
</div>
<p id="sgAutoDecideOut" style="margin:10px 0 0 0;font-size:0.9rem;color:var(--ink-mid,#0e5472);min-height:30px;"></p>
<script>
function sgAutoDecide(choice) {
  document.getElementById("sgAutoDecideOut").innerText = choice === "repair"
    ? "Repair makes sense if: costs are low, issue is isolated, unit is <10 years old."
    : "Replace makes sense if: repair costs >50% of replacement, unit is old, or efficiency is poor.";
}
</script>
<p style="margin:12px 0 0 0;font-size:0.85rem;"><strong>Text PJ → 773-544-1231</strong></p>
</section>
'

COST_BLOCK='
<section data-auto-adapt="cost-v1" style="background:var(--card,#f4fbff);padding:18px 22px;border-radius:var(--r,12px);margin:20px 0;border:1px solid rgba(7,48,68,.08);">
<h3 style="margin:0 0 10px 0;color:var(--ink,#073044);font-size:1rem;">Quick Cost Check</h3>
<input type="number" id="sgAutoSize" placeholder="Size or scope" style="padding:8px 12px;border:1px solid rgba(7,48,68,.15);border-radius:6px;width:100%;max-width:200px;margin:8px 0;">
<button onclick="sgAutoCalc()" style="padding:8px 16px;background:var(--mint,#21d3a1);color:#fff;border:0;border-radius:6px;font-weight:600;cursor:pointer;margin:8px 0;">Estimate</button>
<p id="sgAutoCalcOut" style="margin:10px 0 0 0;font-weight:600;color:var(--ink,#073044);min-height:24px;"></p>
<script>
function sgAutoCalc() {
  let size = parseInt(document.getElementById("sgAutoSize").value);
  if (!size || size < 1) {
    document.getElementById("sgAutoCalcOut").innerText = "Enter a valid number";
    return;
  }
  let est = Math.round(size * 150);
  document.getElementById("sgAutoCalcOut").innerText = "Directional estimate: $" + est.toLocaleString() + " - $" + (est + 2000).toLocaleString();
}
</script>
<p style="margin:12px 0 0 0;font-size:0.85rem;"><strong>Text PJ → 773-544-1231</strong></p>
</section>
'

########################################
# PHASE 2: APPLY PATTERNS
########################################

echo "🚀 Phase 2: Applying winning patterns globally..."
echo ""

UPDATED=0
SKIPPED=0

for FILE in *.html; do

  # Stop at max limit
  [ $UPDATED -ge $MAX_UPDATES ] && break

  # Skip if already adapted
  grep -q "data-auto-adapt" "$FILE" && { SKIPPED=$((SKIPPED + 1)); continue; }

  CLUSTER=$(detect_cluster "$FILE")
  APPLIED=false
  BLOCK=""
  PATTERN=""

  ########################################
  # HVAC → decision tool
  ########################################
  
  if [ "$HVAC_WIN" = true ] && [ "$CLUSTER" = "hvac" ]; then
    BLOCK="$DECISION_BLOCK"
    PATTERN="hvac-decision"
    APPLIED=true
  fi

  ########################################
  # TESLA → cost tool
  ########################################
  
  if [ "$TESLA_WIN" = true ] && [ "$CLUSTER" = "tesla" ]; then
    BLOCK="$COST_BLOCK"
    PATTERN="tesla-cost"
    APPLIED=true
  fi

  ########################################
  # PAYMENTS → decision tool
  ########################################
  
  if [ "$PAYMENTS_WIN" = true ] && [ "$CLUSTER" = "payments" ]; then
    BLOCK="$DECISION_BLOCK"
    PATTERN="payments-decision"
    APPLIED=true
  fi

  # Skip if no pattern matched
  [ "$APPLIED" = false ] && continue

  ########################################
  # INJECT AFTER H1
  ########################################

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY RUN] Would apply: $PATTERN → $FILE"
  else
    awk -v block="$BLOCK" '
    BEGIN { added=0 }
    {
      print $0
      if (!added && $0 ~ /<h1/) {
        print block
        added=1
      }
    }' "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"
    
    echo "  ✓ Applied: $PATTERN → $FILE"
    echo "ADAPTED|$FILE|$PATTERN" >> "$LOG"
  fi

  UPDATED=$((UPDATED + 1))

done

########################################
# REPORT
########################################

cat > "$REPORT" <<EOF
# Auto-Adapt Report

**Run:** $(date +"%Y-%m-%d %H:%M:%S")  
**Mode:** $([ "$DRY_RUN" = "true" ] && echo "DRY RUN" || echo "LIVE")

## Winning Patterns Detected

$([ "$HVAC_WIN" = true ] && echo "- **HVAC:** $(grep -c "^WINNER|hvac" "$PATTERN_FILE" 2>/dev/null || echo 0) high-performing pages" || echo "")
$([ "$TESLA_WIN" = true ] && echo "- **Tesla:** $(grep -c "^WINNER|tesla" "$PATTERN_FILE" 2>/dev/null || echo 0) high-performing pages" || echo "")
$([ "$PAYMENTS_WIN" = true ] && echo "- **Payments:** $(grep -c "^WINNER|payments" "$PATTERN_FILE" 2>/dev/null || echo 0) high-performing pages" || echo "")
$([ "$SOLAR_WIN" = true ] && echo "- **Solar:** $(grep -c "^WINNER|solar" "$PATTERN_FILE" 2>/dev/null || echo 0) high-performing pages" || echo "")
$([ "$PLUMBING_WIN" = true ] && echo "- **Plumbing:** $(grep -c "^WINNER|plumbing" "$PATTERN_FILE" 2>/dev/null || echo 0) high-performing pages" || echo "")

## Application Summary

- **Updated:** $UPDATED pages
- **Skipped:** $SKIPPED (already adapted)
- **Max limit:** $MAX_UPDATES

## Pattern Details

$(cat "$PATTERN_FILE" 2>/dev/null | awk -F'|' '{print "- **" $2 ":** " $3 " (" $4 " clicks, " $5 " impressions)"}' || echo "No patterns detected")

## Next Steps

$(if [ "$DRY_RUN" = "true" ]; then
  echo "Run with \`DRY_RUN=false ./hyper-auto-adapt.sh\` to apply globally."
else
  echo "- Monitor adapted pages in GSC for 2-4 weeks"
  echo "- Compare performance vs control group"
  echo "- Refine thresholds based on results"
fi)

EOF

echo ""
echo "---------------------------------------"
echo "✅ AUTO-ADAPT COMPLETE"
echo "---------------------------------------"
echo ""
echo "Patterns detected: $(wc -l < "$PATTERN_FILE")"
echo "Pages updated: $UPDATED"
echo "Pages skipped: $SKIPPED"
echo ""
echo "📋 Report: $REPORT"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "💡 To apply changes: DRY_RUN=false ./hyper-auto-adapt.sh"
  echo ""
fi
