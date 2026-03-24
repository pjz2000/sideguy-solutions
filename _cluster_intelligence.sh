#!/usr/bin/env bash

########################################
# SIDEGUY CLUSTER INTELLIGENCE + AUTO PRODUCTIZE v2
# 
# PHASE 1: Cluster Analysis
#   - Groups GSC data into topic clusters
#   - Detects user intent patterns
#   - Maps geographic demand
#   - Identifies missing pages
#
# PHASE 2: Smart Productization
#   - Upgrades top opportunity pages
#   - Injects cluster-aware product blocks
#   - Prioritizes by cluster strength + intent match
#
# INPUT: docs/gsc/query-pages.csv
# COLUMNS: page,query,clicks,impressions,ctr,position
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || return

DATE="$(date +"%Y-%m-%d-%H%M%S")"
HUMAN_DATE="$(date +"%Y-%m-%d %H:%M:%S")"

INPUT_DIR="docs/gsc"
INPUT_CSV="$INPUT_DIR/query-pages.csv"

OUT_DIR="docs/cluster-intelligence"
mkdir -p "$INPUT_DIR" "$OUT_DIR"

CLUSTER_CSV="$OUT_DIR/clusters-$DATE.csv"
INTENT_CSV="$OUT_DIR/intents-$DATE.csv"
GEO_CSV="$OUT_DIR/geos-$DATE.csv"
OPPS_CSV="$OUT_DIR/opportunities-$DATE.csv"
MISSING_CSV="$OUT_DIR/missing-pages-$DATE.csv"
REPORT_MD="$OUT_DIR/cluster-report-$DATE.md"

echo "---------------------------------------"
echo "🧠 SIDEGUY CLUSTER INTELLIGENCE LAYER v1"
echo "---------------------------------------"
echo "Timestamp: $HUMAN_DATE"
echo ""

if [ ! -f "$INPUT_CSV" ]; then
  echo "Missing input: $INPUT_CSV"
  echo "Expected columns:"
  echo "page,query,clicks,impressions,ctr,position"
  return
fi

########################################
# RESET OUTPUTS
########################################

echo "cluster,queries,impressions,avg_position,top_query" > "$CLUSTER_CSV"
echo "intent,queries,impressions,avg_position" > "$INTENT_CSV"
echo "geo,queries,impressions,avg_position" > "$GEO_CSV"
echo "page,query,cluster,intent,geo,clicks,impressions,ctr,position,opportunity_score" > "$OPPS_CSV"
echo "suggested_page,cluster,intent,geo,reason" > "$MISSING_CSV"

TMP_RAW="$OUT_DIR/raw-$DATE.csv"
cp "$INPUT_CSV" "$TMP_RAW"

########################################
# HELPERS
########################################

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/ /g' \
    | xargs \
    | tr ' ' '-'
}

detect_intent() {
  local q="$1"
  local blob
  blob="$(echo "$q" | tr '[:upper:]' '[:lower:]')"

  # Decision-making queries
  if echo "$blob" | grep -Eiq 'repair|replace|worth it|should i|fix|decision|vs|versus|better|choose'; then
    echo "decision"
  
  # Cost/pricing queries
  elif echo "$blob" | grep -Eiq 'cost|price|pricing|estimate|quote|how much|budget|afford|cheap|expensive'; then
    echo "cost"
  
  # Comparison queries
  elif echo "$blob" | grep -Eiq 'compare|comparison|difference between|which is better|alternative'; then
    echo "compare"
  
  # Service-seeking/call queries
  elif echo "$blob" | grep -Eiq 'who do i call|who should i call|call for|service|help|hire|find|near me|contractor'; then
    echo "call"
  
  # How-to/DIY queries
  elif echo "$blob" | grep -Eiq 'how to|how do i|diy|myself|tutorial|guide|step by step'; then
    echo "how-to"
  
  # Problem/troubleshooting queries
  elif echo "$blob" | grep -Eiq 'not working|broken|problem|issue|error|trouble|fail|wont|doesnt|stopped'; then
    echo "troubleshoot"
  
  # Everything else (informational)
  else
    echo "general"
  fi
}

detect_geo() {
  local q="$1"
  local blob
  blob="$(echo "$q" | tr '[:upper:]' '[:lower:]')"

  for city in "san diego" "encinitas" "carlsbad" "oceanside" "del mar" "la jolla" "cardiff" "solana beach" "coronado"; do
    if echo "$blob" | grep -Fqi "$city"; then
      echo "$city"
      return
    fi
  done

  echo "non-geo"
}

detect_cluster() {
  local q="$1"
  local p="$2"
  local blob
  blob="$(printf '%s %s' "$q" "$p" | tr '[:upper:]' '[:lower:]')"

  # HVAC & Climate Control
  if echo "$blob" | grep -Eiq 'hvac|air conditioning|mini split|furnace|heat pump|ac repair|ac not cooling'; then
    echo "hvac"
  
  # AI & Automation
  elif echo "$blob" | grep -Eiq 'ai business|ai lead generation|ai automation|ai consulting|ai service|ai process|machine learning|ai system|artificial intelligence'; then
    echo "ai-automation"
  
  # IT & Tech Support
  elif echo "$blob" | grep -Eiq 'it help|it support|it service|tech support|network|business networking|website help|tech consulting'; then
    echo "it-support"
  
  # Payment Processing
  elif echo "$blob" | grep -Eiq 'payment processing|credit card processing|merchant service|pos system|stripe|square|debit card|mobile payment|ecommerce payment|payment solution'; then
    echo "payments"
  
  # Marketing & Digital Services
  elif echo "$blob" | grep -Eiq 'marketing automation|seo|web design|google business|digital marketing|lead generation(?!.*ai)'; then
    echo "digital-marketing"
  
  # EV & Charging
  elif echo "$blob" | grep -Eiq 'tesla|ev charger|charger install|level 2|electric vehicle'; then
    echo "ev-charging"
  
  # Solar & Energy Storage
  elif echo "$blob" | grep -Eiq 'solar|battery backup|powerwall|energy storage|backup power'; then
    echo "energy"
  
  # Roofing
  elif echo "$blob" | grep -Eiq 'roof|leak|roofer|roofing'; then
    echo "roofing"
  
  # Plumbing
  elif echo "$blob" | grep -Eiq 'plumb|water heater|drain|pipe|water pressure|leak(?!.*roof)'; then
    echo "plumbing"
  
  # Electrical
  elif echo "$blob" | grep -Eiq 'electric|panel|outlet|wiring|electrician'; then
    echo "electrical"
  
  # Home Services (general)
  elif echo "$blob" | grep -Eiq 'home repair|home service|handyman|home guy|home maintenance'; then
    echo "home-services"
  
  # Lawn & Landscaping
  elif echo "$blob" | grep -Eiq 'lawn care|landscaping|yard service|lawn service'; then
    echo "landscaping"
  
  # Everything else
  else
    echo "misc"
  fi
}

score_opportunity() {
  local clicks="$1"
  local impressions="$2"
  local position="$3"

  [ -z "$clicks" ] && clicks=0
  [ -z "$impressions" ] && impressions=0
  [ -z "$position" ] && position=99

  local bonus=0
  local pos_bonus=0

  if awk "BEGIN {exit !($clicks == 0)}"; then
    bonus=20
  elif awk "BEGIN {exit !($clicks <= 2)}"; then
    bonus=10
  fi

  if awk "BEGIN {exit !($position >= 8 && $position <= 40)}"; then
    pos_bonus=40
  elif awk "BEGIN {exit !($position > 40 && $position <= 70)}"; then
    pos_bonus=20
  fi

  awk "BEGIN {printf \"%.2f\", $impressions + $bonus + $pos_bonus}"
}

########################################
# BUILD ENRICHED OPPORTUNITY FILE
########################################

tail -n +2 "$TMP_RAW" | while IFS=, read -r page query clicks impressions ctr position rest; do
  [ -z "$page" ] && continue

  cluster="$(detect_cluster "$query" "$page")"
  intent="$(detect_intent "$query")"
  geo="$(detect_geo "$query")"
  score="$(score_opportunity "${clicks:-0}" "${impressions:-0}" "${position:-99}")"

  printf '"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' \
    "$page" "$query" "$cluster" "$intent" "$geo" "$clicks" "$impressions" "$ctr" "$position" "$score" \
    >> "$OPPS_CSV"
done

########################################
# CLUSTER SUMMARY
########################################

python3 - <<PY
import csv
from collections import defaultdict
from statistics import mean
from pathlib import Path

opp_path = Path("$OPPS_CSV")
cluster_csv = Path("$CLUSTER_CSV")
intent_csv = Path("$INTENT_CSV")
geo_csv = Path("$GEO_CSV")
missing_csv = Path("$MISSING_CSV")

rows = []
with opp_path.open() as f:
    reader = csv.DictReader(f)
    rows = list(reader)

cluster_data = defaultdict(list)
intent_data = defaultdict(list)
geo_data = defaultdict(list)

for r in rows:
    cluster_data[r["cluster"]].append(r)
    intent_data[r["intent"]].append(r)
    geo_data[r["geo"]].append(r)

with cluster_csv.open("a", newline="") as f:
    w = csv.writer(f)
    for cluster, items in sorted(cluster_data.items(), key=lambda kv: sum(float(x["impressions"] or 0) for x in kv[1]), reverse=True):
        imps = sum(float(x["impressions"] or 0) for x in items)
        avg_pos = mean(float(x["position"] or 99) for x in items)
        top = sorted(items, key=lambda x: float(x["impressions"] or 0), reverse=True)[0]["query"]
        w.writerow([cluster, len(items), round(imps, 2), round(avg_pos, 2), top])

with intent_csv.open("a", newline="") as f:
    w = csv.writer(f)
    for intent, items in sorted(intent_data.items(), key=lambda kv: sum(float(x["impressions"] or 0) for x in kv[1]), reverse=True):
        imps = sum(float(x["impressions"] or 0) for x in items)
        avg_pos = mean(float(x["position"] or 99) for x in items)
        w.writerow([intent, len(items), round(imps, 2), round(avg_pos, 2)])

with geo_csv.open("a", newline="") as f:
    w = csv.writer(f)
    for geo, items in sorted(geo_data.items(), key=lambda kv: sum(float(x["impressions"] or 0) for x in kv[1]), reverse=True):
        imps = sum(float(x["impressions"] or 0) for x in items)
        avg_pos = mean(float(x["position"] or 99) for x in items)
        w.writerow([geo, len(items), round(imps, 2), round(avg_pos, 2)])

existing_files = {p.name for p in Path(".").glob("*.html")}

ideas = set()
for r in rows:
    cluster = r["cluster"]
    intent = r["intent"]
    geo = r["geo"]

    if cluster == "misc":
        continue
    if intent == "general":
        continue

    slug_parts = [cluster]
    if intent != "general":
        slug_parts.append(intent)
    if geo != "non-geo":
        slug_parts.append(geo.replace(" ", "-"))

    slug = "-".join(slug_parts) + ".html"

    if slug not in existing_files:
        reason = f"Detected repeated {cluster} + {intent} demand"
        ideas.add((slug, cluster, intent, geo, reason))

with missing_csv.open("a", newline="") as f:
    w = csv.writer(f)
    for row in sorted(ideas):
        w.writerow(row)
PY

########################################
# PHASE 1 COMPLETE - CLUSTER ANALYSIS DONE
########################################

TOP_CLUSTER="$(tail -n +2 "$CLUSTER_CSV" | head -n 1 | cut -d, -f1)"
TOP_INTENT="$(tail -n +2 "$INTENT_CSV" | head -n 1 | cut -d, -f1)"
TOP_GEO="$(tail -n +2 "$GEO_CSV" | head -n 1 | cut -d, -f1)"

echo ""
echo "✅ Phase 1: Cluster analysis complete"
echo "   Top cluster: $TOP_CLUSTER"
echo "   Top intent: $TOP_INTENT"
echo "   Top geo: $TOP_GEO"
echo ""

########################################
# PHASE 2: PRODUCTIZATION ENGINE
########################################

echo "---------------------------------------"
echo "⚡ Phase 2: Auto Productize Top Pages"
echo "---------------------------------------"
echo ""

PRODUCTIZE_LOG="$OUT_DIR/productize-log-$DATE.txt"
OUTCOMES_FILE="$OUT_DIR/outcomes-$DATE.txt"

echo "" > "$PRODUCTIZE_LOG"
echo "" > "$OUTCOMES_FILE"

########################################
# PRODUCT BLOCK BUILDERS
########################################

build_decision_block() {
  cat <<'DECISION_EOF'
<section class="sg-product-block sg-decision-tool" data-sg-productized="v2" style="background:#f4fbff;padding:20px;border-radius:16px;margin:18px 0;border:1px solid rgba(0,0,0,.06);box-shadow:0 10px 30px rgba(0,0,0,.04);">
  <h2>⚡ Quick Decision Tool</h2>
  <p>Not sure what to do yet? Use this fast check before spending money.</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin:12px 0;">
    <button onclick="sgDecisionTool('repair')" style="padding:10px 16px;border-radius:999px;border:0;cursor:pointer;background:#21d3a1;color:#fff;">Repair</button>
    <button onclick="sgDecisionTool('replace')" style="padding:10px 16px;border-radius:999px;border:0;cursor:pointer;background:#073044;color:#fff;">Replace</button>
  </div>
  <p id="sg-decision-result" style="font-weight:600;margin-top:12px;"></p>
  <script>
    function sgDecisionTool(choice){
      var el = document.getElementById('sg-decision-result');
      if (!el) return;
      if(choice === 'repair'){
        el.innerText = '✓ Repair usually makes sense when the issue is isolated, the system is not very old, and the fix is small relative to replacement.';
      } else {
        el.innerText = '✓ Replace usually makes sense when repairs keep stacking up, efficiency is poor, or the total fix cost is too close to a new system.';
      }
    }
  </script>
  <p style="margin-top:12px;"><strong>Still unsure? Text PJ → 773-544-1231</strong></p>
</section>
DECISION_EOF
}

build_cost_block() {
  cat <<'COST_EOF'
<section class="sg-product-block sg-cost-tool" data-sg-productized="v2" style="background:#f4fbff;padding:20px;border-radius:16px;margin:18px 0;border:1px solid rgba(0,0,0,.06);box-shadow:0 10px 30px rgba(0,0,0,.04);">
  <h2>💰 Quick Cost Estimator</h2>
  <p>Use this lightweight estimate before calling around.</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin:12px 0;">
    <input type="number" id="sg-cost-input" placeholder="Enter size / scope" style="padding:10px 12px;border-radius:12px;border:1px solid #cfe3ee;min-width:220px;">
    <button onclick="sgCostCalc()" style="padding:10px 16px;border-radius:999px;border:0;cursor:pointer;background:#21d3a1;color:#fff;">Estimate</button>
  </div>
  <p id="sg-cost-result" style="font-weight:600;margin-top:12px;"></p>
  <script>
    function sgCostCalc(){
      var raw = document.getElementById('sg-cost-input');
      var out = document.getElementById('sg-cost-result');
      if (!raw || !out) return;
      var v = parseFloat(raw.value || '0');
      if (!v || v <= 0) {
        out.innerText = '⚠ Enter a rough size or scope first.';
        return;
      }
      var estimate = Math.round(v * 150);
      out.innerText = '✓ Rough estimate: $' + estimate.toLocaleString();
    }
  </script>
  <p style="margin-top:12px;"><strong>Want a clearer answer? Text PJ → 773-544-1231</strong></p>
</section>
COST_EOF
}

build_compare_block() {
  cat <<'COMPARE_EOF'
<section class="sg-product-block sg-compare-tool" data-sg-productized="v2" style="background:#f4fbff;padding:20px;border-radius:16px;margin:18px 0;border:1px solid rgba(0,0,0,.06);box-shadow:0 10px 30px rgba(0,0,0,.04);">
  <h2>⚖️ Quick Comparison</h2>
  <p>Here's the fast version before you dig deeper.</p>
  <div style="overflow-x:auto;margin:12px 0;">
    <table style="width:100%;border-collapse:collapse;">
      <tr>
        <th style="text-align:left;padding:10px;border-bottom:2px solid #073044;background:#eef8fc;">Option A</th>
        <th style="text-align:left;padding:10px;border-bottom:2px solid #073044;background:#eef8fc;">Option B</th>
      </tr>
      <tr>
        <td style="padding:10px;border-bottom:1px solid #eef5f8;">Usually lower upfront cost</td>
        <td style="padding:10px;border-bottom:1px solid #eef5f8;">Usually better long-term efficiency</td>
      </tr>
      <tr>
        <td style="padding:10px;border-bottom:1px solid #eef5f8;">Can be faster to start</td>
        <td style="padding:10px;border-bottom:1px solid #eef5f8;">May reduce repeat problems</td>
      </tr>
      <tr>
        <td style="padding:10px;">Best for short-term simplicity</td>
        <td style="padding:10px;">Best for long-term planning</td>
      </tr>
    </table>
  </div>
  <p style="margin-top:12px;"><strong>Need help deciding? Text PJ → 773-544-1231</strong></p>
</section>
COMPARE_EOF
}

build_call_block() {
  cat <<'CALL_EOF'
<section class="sg-product-block sg-call-tool" data-sg-productized="v2" style="background:#f4fbff;padding:20px;border-radius:16px;margin:18px 0;border:1px solid rgba(0,0,0,.06);box-shadow:0 10px 30px rgba(0,0,0,.04);">
  <h2>📞 Who Should You Call?</h2>
  <p>If you're not sure who handles this, start here:</p>
  <ul style="margin:12px 0;padding-left:24px;">
    <li style="margin:8px 0;">Small or simple issue → general handyman or basic service pro</li>
    <li style="margin:8px 0;">System-specific problem → licensed specialist</li>
    <li style="margin:8px 0;">Still unsure → Text PJ and get pointed the right way</li>
  </ul>
  <p style="margin-top:12px;"><strong>Text PJ → 773-544-1231</strong></p>
</section>
CALL_EOF
}

get_block_for_intent() {
  local intent="$1"
  case "$intent" in
    decision) build_decision_block ;;
    cost) build_cost_block ;;
    compare) build_compare_block ;;
    call) build_call_block ;;
    *) build_decision_block ;;
  esac
}

normalize_url_to_file() {
  local url="$1"

  url="${url#https://www.sideguysolutions.com/}"
  url="${url#http://www.sideguysolutions.com/}"
  url="${url#https://sideguysolutions.com/}"
  url="${url#http://sideguysolutions.com/}"
  url="${url#https://www.sideguy.solutions/}"
  url="${url#http://www.sideguy.solutions/}"
  url="${url#https://sideguy.solutions/}"
  url="${url#http://sideguy.solutions/}"

  url="${url%%\?*}"
  url="${url%%\#*}"

  if [ -z "$url" ]; then
    echo "index.html"
    return
  fi

  if echo "$url" | grep -q '/$'; then
    url="${url%/}/index.html"
  fi

  if ! echo "$url" | grep -q '\.html$'; then
    url="${url}.html"
  fi

  echo "$url"
}

inject_block_after_h1() {
  local file="$1"
  local block_file="$2"

  awk -v blockfile="$block_file" '
    BEGIN {
      added = 0
      while ((getline line < blockfile) > 0) {
        block = block line "\n"
      }
      close(blockfile)
    }
    {
      print $0
      if (added == 0 && $0 ~ /<h1[^>]*>/) {
        print block
        added = 1
      }
    }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
}

########################################
# PRODUCTIZE TOP OPPORTUNITIES
########################################

MAX_PAGES=30
UPDATED=0
SKIPPED=0
MISSING=0
FAILED=0

echo "🛠 Processing top $MAX_PAGES cluster opportunities..."
echo ""

tail -n +2 "$OPPS_CSV" | sort -t, -k10,10nr | head -n "$MAX_PAGES" | while IFS=, read -r page query cluster intent geo clicks impressions ctr position score; do
  page="${page//\"/}"
  query="${query//\"/}"
  cluster="${cluster//\"/}"
  intent="${intent//\"/}"
  geo="${geo//\"/}"
  score="${score//\"/}"

  file="$(normalize_url_to_file "$page")"

  echo "---------------------------------------" | tee -a "$PRODUCTIZE_LOG"
  echo "PAGE: $page" | tee -a "$PRODUCTIZE_LOG"
  echo "FILE: $file" | tee -a "$PRODUCTIZE_LOG"
  echo "QUERY: $query" | tee -a "$PRODUCTIZE_LOG"
  echo "CLUSTER: $cluster" | tee -a "$PRODUCTIZE_LOG"
  echo "INTENT: $intent" | tee -a "$PRODUCTIZE_LOG"
  echo "GEO: $geo" | tee -a "$PRODUCTIZE_LOG"
  echo "SCORE: $score" | tee -a "$PRODUCTIZE_LOG"

  if [ ! -f "$file" ]; then
    echo "❌ Missing file" | tee -a "$PRODUCTIZE_LOG"
    echo "MISSING|$cluster|$intent|$page|$file|$score" >> "$OUTCOMES_FILE"
    MISSING=$((MISSING + 1))
    continue
  fi

  if grep -q 'data-sg-productized="v2"' "$file"; then
    echo "⏭ Already productized" | tee -a "$PRODUCTIZE_LOG"
    echo "SKIPPED|$cluster|$intent|$page|$file|$score" >> "$OUTCOMES_FILE"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  TMP_BLOCK="$OUT_DIR/block-$DATE.html"
  get_block_for_intent "$intent" > "$TMP_BLOCK"

  inject_block_after_h1 "$file" "$TMP_BLOCK"

  if grep -q 'data-sg-productized="v2"' "$file"; then
    echo "✅ Injected $intent block" | tee -a "$PRODUCTIZE_LOG"
    echo "UPDATED|$cluster|$intent|$page|$file|$score" >> "$OUTCOMES_FILE"
    UPDATED=$((UPDATED + 1))
  else
    echo "⚠ Injection check failed" | tee -a "$PRODUCTIZE_LOG"
    echo "FAILED|$cluster|$intent|$page|$file|$score" >> "$OUTCOMES_FILE"
    FAILED=$((FAILED + 1))
  fi
done

########################################
# FINAL REPORT
########################################

cat > "$REPORT_MD" <<EOF
# SideGuy Cluster Intelligence + Productization Report

**Timestamp:** $HUMAN_DATE

---

## Phase 1: Cluster Analysis

### Top Signals
- **Top cluster:** $TOP_CLUSTER
- **Top intent:** $TOP_INTENT
- **Top geo:** $TOP_GEO

### Output Files
- Clusters: \`$CLUSTER_CSV\`
- Intents: \`$INTENT_CSV\`
- Geos: \`$GEO_CSV\`
- Opportunities: \`$OPPS_CSV\`
- Missing pages: \`$MISSING_CSV\`

---

## Phase 2: Auto Productization

### Summary
- ✅ **Updated:** $UPDATED pages
- ⏭ **Skipped:** $SKIPPED (already productized)
- ❌ **Missing:** $MISSING files
- ⚠ **Failed:** $FAILED injection checks

### Productization Logic
- Sorted by opportunity score (impressions + position + clicks bonus)
- Clustered by topic for smarter block selection
- Intent-aware product blocks (decision/cost/compare/call)
- Injected after first H1 tag

### Logs
- Productize log: \`$PRODUCTIZE_LOG\`
- Outcomes: \`$OUTCOMES_FILE\`

---

## Recommended Next Steps

1. **Review updated pages** - spot check the injected product blocks
2. **Build missing pages** - use \`$MISSING_CSV\` for high-demand gaps
3. **Monitor cluster performance** - re-run weekly to track improvement
4. **Strengthen cluster hubs** - add internal links between related pages
5. **Analyze failed injections** - check H1 tags in pages that failed

---

## What This System Does

**Cluster Intelligence:**
- Groups GSC queries into semantic clusters (hvac, payments, tesla, etc.)
- Detects user intent patterns (decision, cost, compare, call)
- Maps geographic demand concentrations
- Identifies missing child pages based on query patterns

**Smart Productization:**
- Upgrades pages with interactive product blocks
- Matches block type to user intent
- Prioritizes by cluster opportunity score
- Preserves already-productized pages

**Result:** GSC impressions become product decisions, not just traffic metrics.

EOF

echo ""
echo "---------------------------------------"
echo "✅ COMPLETE - BOTH PHASES DONE"
echo "---------------------------------------"
echo ""
echo "📊 Cluster Analysis:"
echo "   Top cluster: $TOP_CLUSTER"
echo "   Top intent: $TOP_INTENT"
echo "   Top geo: $TOP_GEO"
echo ""
echo "⚡ Productization:"
echo "   Updated: $UPDATED"
echo "   Skipped: $SKIPPED"
echo "   Missing: $MISSING"
echo "   Failed:  $FAILED"
echo ""
echo "📄 Full report: $REPORT_MD"
echo "---------------------------------------"

########################################
# GIT COMMIT
########################################

git add "$OUT_DIR" ./*.html "$INPUT_CSV" 2>/dev/null
git commit -m "🧠⚡ Cluster Intelligence v2 - analyzed $TOP_CLUSTER cluster + productized $UPDATED pages" || true

echo ""
echo "🚀 SideGuy: GSC impressions → cluster insights → product decisions"
