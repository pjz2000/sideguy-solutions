#!/usr/bin/env bash

########################################
# SIDEGUY HYPER PRODUCTIZE v1
# Query-specific interactive tools
# Injects calculators, decision widgets,
# comparison tools based on query intent
########################################

set -e

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/gsc/query-pages.csv"
OUT_DIR="docs/hyper-productize"
LOG="$OUT_DIR/productize-log.txt"
REPORT="$OUT_DIR/productize-report.md"

# Safety: dry-run by default
DRY_RUN="${DRY_RUN:-true}"

# Limit: max pages to update per run
MAX_UPDATES="${MAX_UPDATES:-50}"

########################################
# PREFLIGHT
########################################

echo ""
echo "---------------------------------------"
echo "🛠️  SIDEGUY HYPER PRODUCTIZE v1"
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
  local q="$1"
  q=$(echo "$q" | tr '[:upper:]' '[:lower:]')

  if [[ "$q" =~ hvac|air\ conditioning|mini\ split|furnace|heat\ pump ]]; then
    echo "hvac"
  elif [[ "$q" =~ tesla|ev\ charger|charger\ install|level\ 2 ]]; then
    echo "tesla"
  elif [[ "$q" =~ stripe|square|merchant|payment|pos ]]; then
    echo "payments"
  elif [[ "$q" =~ solar|battery|powerwall ]]; then
    echo "solar"
  elif [[ "$q" =~ plumb|water\ heater|drain ]]; then
    echo "plumbing"
  elif [[ "$q" =~ electric|panel|wiring ]]; then
    echo "electrical"
  else
    echo "general"
  fi
}

detect_intent() {
  local q="$1"
  q=$(echo "$q" | tr '[:upper:]' '[:lower:]')

  if [[ "$q" =~ cost|price|how\ much|estimate|quote ]]; then
    echo "cost"
  elif [[ "$q" =~ vs|versus|compare|comparison|better ]]; then
    echo "compare"
  elif [[ "$q" =~ repair|replace|worth|should\ i|should\ you ]]; then
    echo "decision"
  elif [[ "$q" =~ who|call|service|help ]]; then
    echo "call"
  else
    echo "general"
  fi
}

########################################
# TOOL GENERATORS
########################################

build_hvac_cost_tool() {
cat <<'EOF'
<section data-sg-productized="hvac-cost-v1" style="background:var(--card,#f4fbff);padding:20px 24px;border-radius:var(--r,14px);margin:24px 0;border:1px solid rgba(7,48,68,.08);box-shadow:0 2px 8px rgba(7,48,68,.04);">
<h2 style="margin:0 0 12px 0;color:var(--ink,#073044);font-size:1.1rem;">⚡ HVAC Cost Estimator</h2>
<p style="margin:0 0 16px 0;color:var(--ink-mid,#0e5472);font-size:0.95rem;">Get a directional range before calling contractors.</p>
<div style="display:flex;gap:8px;margin:12px 0;flex-wrap:wrap;">
  <input type="number" id="hvacSize" placeholder="Home size (sq ft)" style="padding:10px 14px;border:1px solid rgba(7,48,68,.15);border-radius:8px;font-size:1rem;flex:1;min-width:180px;">
  <button onclick="calcHVAC()" style="padding:10px 20px;background:var(--mint,#21d3a1);color:#fff;border:0;border-radius:8px;font-weight:600;cursor:pointer;font-size:1rem;">Calculate</button>
</div>
<p id="hvacResult" style="font-weight:600;color:var(--ink,#073044);margin:12px 0 0 0;min-height:24px;"></p>
<script>
function calcHVAC(){
  let size = parseInt(document.getElementById('hvacSize').value);
  if (!size || size < 400) {
    document.getElementById('hvacResult').innerText = "Enter a valid size (400+ sq ft)";
    return;
  }
  let base = Math.round(size * 8);
  let low = base.toLocaleString();
  let high = (base + 3500).toLocaleString();
  document.getElementById('hvacResult').innerText = "Estimated range: $" + low + " - $" + high;
}
</script>
<p style="margin:16px 0 0 0;font-size:0.9rem;color:var(--ink-mid,#0e5472);"><strong>Need a real quote? Text PJ → 773-544-1231</strong></p>
</section>
EOF
}

build_tesla_charger_tool() {
cat <<'EOF'
<section data-sg-productized="tesla-charger-v1" style="background:var(--card,#f4fbff);padding:20px 24px;border-radius:var(--r,14px);margin:24px 0;border:1px solid rgba(7,48,68,.08);box-shadow:0 2px 8px rgba(7,48,68,.04);">
<h2 style="margin:0 0 12px 0;color:var(--ink,#073044);font-size:1.1rem;">⚡ Tesla Charger Install Estimator</h2>
<p style="margin:0 0 16px 0;color:var(--ink-mid,#0e5472);font-size:0.95rem;">Quick estimate based on install type.</p>
<select id="teslaType" style="padding:10px 14px;border:1px solid rgba(7,48,68,.15);border-radius:8px;font-size:1rem;width:100%;margin:8px 0;">
  <option value="1200">Basic Home Install (near panel)</option>
  <option value="2200">Home Install (50+ ft run)</option>
  <option value="3500">Commercial Install</option>
</select>
<button onclick="calcTesla()" style="padding:10px 20px;background:var(--mint,#21d3a1);color:#fff;border:0;border-radius:8px;font-weight:600;cursor:pointer;margin:8px 0;font-size:1rem;">Calculate</button>
<p id="teslaResult" style="font-weight:600;color:var(--ink,#073044);margin:12px 0 0 0;min-height:24px;"></p>
<script>
function calcTesla(){
  let base = parseInt(document.getElementById('teslaType').value);
  let low = base.toLocaleString();
  let high = (base + 1800).toLocaleString();
  document.getElementById('teslaResult').innerText = "Estimated range: $" + low + " - $" + high;
}
</script>
<p style="margin:16px 0 0 0;font-size:0.9rem;color:var(--ink-mid,#0e5472);"><strong>Need a real quote? Text PJ → 773-544-1231</strong></p>
</section>
EOF
}

build_decision_tool() {
cat <<'EOF'
<section data-sg-productized="decision-v1" style="background:var(--card,#f4fbff);padding:20px 24px;border-radius:var(--r,14px);margin:24px 0;border:1px solid rgba(7,48,68,.08);box-shadow:0 2px 8px rgba(7,48,68,.04);">
<h2 style="margin:0 0 12px 0;color:var(--ink,#073044);font-size:1.1rem;">⚡ Quick Decision Tool</h2>
<p style="margin:0 0 16px 0;color:var(--ink-mid,#0e5472);font-size:0.95rem;">Fast guidance before you spend.</p>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin:12px 0;">
  <button onclick="sgDecide('repair')" style="padding:10px 18px;background:#fff;border:2px solid var(--mint,#21d3a1);color:var(--ink,#073044);border-radius:8px;cursor:pointer;font-weight:600;font-size:0.95rem;">Repair</button>
  <button onclick="sgDecide('replace')" style="padding:10px 18px;background:#fff;border:2px solid var(--mint,#21d3a1);color:var(--ink,#073044);border-radius:8px;cursor:pointer;font-weight:600;font-size:0.95rem;">Replace</button>
</div>
<p id="sgDecisionResult" style="font-weight:600;color:var(--ink,#073044);margin:12px 0 0 0;min-height:40px;"></p>
<script>
function sgDecide(choice){
  let result = choice === 'repair'
    ? "✓ Repair makes sense if: issue is isolated, recent, and repair costs < 50% of replacement."
    : "✓ Replace makes sense if: costs are stacking, unit is old (10+ years), or efficiency is poor.";
  document.getElementById('sgDecisionResult').innerText = result;
}
</script>
<p style="margin:16px 0 0 0;font-size:0.9rem;color:var(--ink-mid,#0e5472);"><strong>Need a real answer? Text PJ → 773-544-1231</strong></p>
</section>
EOF
}

build_comparison_tool() {
cat <<'EOF'
<section data-sg-productized="compare-v1" style="background:var(--card,#f4fbff);padding:20px 24px;border-radius:var(--r,14px);margin:24px 0;border:1px solid rgba(7,48,68,.08);box-shadow:0 2px 8px rgba(7,48,68,.04);">
<h2 style="margin:0 0 12px 0;color:var(--ink,#073044);font-size:1.1rem;">⚖️ Quick Comparison</h2>
<table style="width:100%;border-collapse:collapse;margin:12px 0;">
<tr style="background:rgba(33,211,161,.08);">
  <th style="padding:10px;text-align:left;border:1px solid rgba(7,48,68,.1);">Option A (Lower upfront)</th>
  <th style="padding:10px;text-align:left;border:1px solid rgba(7,48,68,.1);">Option B (Better long-term)</th>
</tr>
<tr>
  <td style="padding:10px;border:1px solid rgba(7,48,68,.1);">✓ Faster install</td>
  <td style="padding:10px;border:1px solid rgba(7,48,68,.1);">✓ Higher efficiency</td>
</tr>
<tr style="background:rgba(0,0,0,.02);">
  <td style="padding:10px;border:1px solid rgba(7,48,68,.1);">✓ Simpler setup</td>
  <td style="padding:10px;border:1px solid rgba(7,48,68,.1);">✓ Lower operating costs</td>
</tr>
<tr>
  <td style="padding:10px;border:1px solid rgba(7,48,68,.1);">— Higher running costs</td>
  <td style="padding:10px;border:1px solid rgba(7,48,68,.1);">— More complex</td>
</tr>
</table>
<p style="margin:16px 0 0 0;font-size:0.9rem;color:var(--ink-mid,#0e5472);"><strong>Need help deciding? Text PJ → 773-544-1231</strong></p>
</section>
EOF
}

########################################
# MAIN PROCESS
########################################

UPDATED=0
SKIPPED=0
TOTAL=0

echo "🔍 Scanning query-page pairs..."
echo ""

tail -n +2 "$INPUT" | while IFS=, read -r page query clicks impressions ctr position; do

  [ -z "$page" ] || [ -z "$query" ] && continue
  
  TOTAL=$((TOTAL + 1))
  
  # Stop at max limit
  if [ $UPDATED -ge $MAX_UPDATES ]; then
    echo "⚠️  Reached max updates ($MAX_UPDATES). Stopping."
    break
  fi

  FILE=$(normalize_url "$page")
  
  # Skip if file doesn't exist
  [ ! -f "$FILE" ] && continue
  
  # Skip if already productized
  if grep -q "data-sg-productized" "$FILE"; then
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  CLUSTER=$(detect_cluster "$query")
  INTENT=$(detect_intent "$query")
  
  TOOL_BLOCK=""
  TOOL_TYPE="none"

  ########################################
  # MATCH TOOL TO QUERY
  ########################################

  if [ "$CLUSTER" = "hvac" ] && [ "$INTENT" = "cost" ]; then
    TOOL_BLOCK=$(build_hvac_cost_tool)
    TOOL_TYPE="hvac-cost"
    
  elif [ "$CLUSTER" = "tesla" ]; then
    TOOL_BLOCK=$(build_tesla_charger_tool)
    TOOL_TYPE="tesla-charger"
    
  elif [ "$INTENT" = "decision" ]; then
    TOOL_BLOCK=$(build_decision_tool)
    TOOL_TYPE="decision"
    
  elif [ "$INTENT" = "compare" ]; then
    TOOL_BLOCK=$(build_comparison_tool)
    TOOL_TYPE="compare"
    
  else
    continue  # No matching tool
  fi

  ########################################
  # INJECT TOOL AFTER H1
  ########################################

  if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY RUN] Would inject: $TOOL_TYPE → $FILE (query: $query)"
  else
    awk -v block="$TOOL_BLOCK" '
    BEGIN { added=0 }
    {
      print $0
      if (!added && $0 ~ /<h1/) {
        print block
        added=1
      }
    }' "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"
    
    echo "  ✓ Injected: $TOOL_TYPE → $FILE"
    echo "UPDATED|$FILE|$query|$TOOL_TYPE" >> "$LOG"
  fi
  
  UPDATED=$((UPDATED + 1))

done

########################################
# REPORT
########################################

cat > "$REPORT" <<EOF
# Hyper Productize Report

**Run:** $(date +"%Y-%m-%d %H:%M:%S")  
**Mode:** $([ "$DRY_RUN" = "true" ] && echo "DRY RUN" || echo "LIVE")

## Summary

- **Updated:** $UPDATED pages
- **Skipped:** $SKIPPED (already had productized tools)
- **Max limit:** $MAX_UPDATES

## Tools Deployed

$(grep "^UPDATED" "$LOG" 2>/dev/null | awk -F'|' '{print "- " $4 " → [" $2 "](" $2 ")"}' || echo "None")

## Next Steps

$(if [ "$DRY_RUN" = "true" ]; then
  echo "Run with \`DRY_RUN=false ./hyper-productize.sh\` to apply changes."
else
  echo "- Validate injected tools on live pages"
  echo "- Monitor GSC for engagement changes"
  echo "- Consider expanding tool types based on query patterns"
fi)

EOF

echo ""
echo "---------------------------------------"
echo "✅ PRODUCTIZE COMPLETE"
echo "---------------------------------------"
echo ""
echo "Updated: $UPDATED"
echo "Skipped: $SKIPPED"
echo ""
echo "📋 Report: $REPORT"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "💡 To apply changes: DRY_RUN=false ./hyper-productize.sh"
  echo ""
fi
