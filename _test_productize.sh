#!/usr/bin/env bash

########################################
# SIDEGUY AUTO PRODUCTIZE ENGINE v1 - TEST MODE
# Tests on 5 pages only
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo "---------------------------------------"
echo "⚡ SIDEGUY AUTO PRODUCTIZE ENGINE v1 TEST"
echo "---------------------------------------"

DATE=$(date +"%Y-%m-%d %H:%M:%S")

########################################
# TARGET PAGES (LIMITED TO 5 FOR TESTING)
########################################

TARGETS=$(find . -maxdepth 1 -name "*.html" \
  | grep -E "repair|replace|cost|price|vs|compare|who|call|hvac|solar|tesla|stripe|square" \
  | head -n 5)

COUNT=$(echo "$TARGETS" | wc -l)
echo "🎯 Testing on $COUNT pages"
echo ""

if [ -z "$TARGETS" ]; then
  echo "❌ No matching pages found"
  exit 1
fi

########################################
# PRODUCT BLOCKS (PHONE: 773-544-1231)
########################################

DECISION_BLOCK='
<section style="background:#f4fbff;padding:20px;border-radius:12px;margin-bottom:20px;">
<h2>⚡ Quick Decision Tool</h2>
<p>Not sure what to do? Use this quick guide:</p>
<button style="background:#21d3a1;color:#073044;padding:10px 20px;border:none;border-radius:6px;cursor:pointer;margin:5px;" onclick="showDecision('"'repair'"')">Repair</button>
<button style="background:#21d3a1;color:#073044;padding:10px 20px;border:none;border-radius:6px;cursor:pointer;margin:5px;" onclick="showDecision('"'replace'"')">Replace</button>
<p id="decision-result" style="margin-top:15px;font-weight:bold;"></p>
<script>
function showDecision(choice){
 if(choice==="repair"){
  document.getElementById("decision-result").innerText="✓ Repair if under 8 years old and issue is minor.";
 } else {
  document.getElementById("decision-result").innerText="✓ Replace if repairs exceed 30% cost of new system.";
 }
}
</script>
<p style="margin-top:15px;"><strong>Still unsure? Text PJ → 773-544-1231</strong></p>
</section>
'

COST_BLOCK='
<section style="background:#f4fbff;padding:20px;border-radius:12px;margin-bottom:20px;">
<h2>💰 Quick Cost Estimator</h2>
<input type="number" id="size" placeholder="Enter size or scope" style="padding:10px;border:2px solid #21d3a1;border-radius:6px;width:200px;">
<button onclick="calcCost()" style="background:#21d3a1;color:#073044;padding:10px 20px;border:none;border-radius:6px;cursor:pointer;margin-left:10px;">Estimate</button>
<p id="cost-result" style="margin-top:15px;font-weight:bold;"></p>
<script>
function calcCost(){
 let v=document.getElementById("size").value;
 if(!v || v<=0){
  document.getElementById("cost-result").innerText="⚠️ Please enter a valid number";
  return;
 }
 let est=v*150;
 document.getElementById("cost-result").innerText="Estimated range: $"+est+" - $"+(est*1.3).toFixed(0);
}
</script>
<p style="margin-top:15px;"><strong>Want exact pricing? Text PJ → 773-544-1231</strong></p>
</section>
'

COMPARE_BLOCK='
<section style="background:#f4fbff;padding:20px;border-radius:12px;margin-bottom:20px;">
<h2>⚖️ Quick Comparison</h2>
<table border="1" cellpadding="8" style="border-collapse:collapse;width:100%;max-width:500px;">
<tr style="background:#21d3a1;color:#073044;">
<th>Option A</th>
<th>Option B</th>
</tr>
<tr>
<td>Lower upfront cost</td>
<td>Higher upfront cost</td>
</tr>
<tr>
<td>More maintenance</td>
<td>Less maintenance</td>
</tr>
<tr>
<td>Short-term fix</td>
<td>Long-term solution</td>
</tr>
</table>
<p style="margin-top:15px;"><strong>Need help choosing? Text PJ → 773-544-1231</strong></p>
</section>
'

CALL_BLOCK='
<section style="background:#f4fbff;padding:20px;border-radius:12px;margin-bottom:20px;">
<h2>📞 Who Should You Call?</h2>
<ul style="line-height:1.8;">
<li><strong>Small issue</strong> → handyman or DIY</li>
<li><strong>Complex issue</strong> → licensed specialist</li>
<li><strong>Not sure?</strong> → Text PJ for guidance</li>
</ul>
<p style="margin-top:15px;"><strong>📲 773-544-1231</strong></p>
</section>
'

########################################
# PROCESS PAGES
########################################

UPDATED=0

for PAGE in $TARGETS; do

  echo "🔧 Processing $PAGE"

  # Skip if already upgraded
  if grep -q "Quick Decision Tool\|Quick Cost Estimator\|Quick Comparison" "$PAGE"; then
    echo "⏭️  Already has interactive tools"
    continue
  fi

  BLOCK=""

  if echo "$PAGE" | grep -qE "repair|replace"; then
    BLOCK="$DECISION_BLOCK"
    echo "   → Adding Decision Tool"
  elif echo "$PAGE" | grep -qE "cost|price"; then
    BLOCK="$COST_BLOCK"
    echo "   → Adding Cost Estimator"
  elif echo "$PAGE" | grep -qE "vs|compare"; then
    BLOCK="$COMPARE_BLOCK"
    echo "   → Adding Comparison Table"
  elif echo "$PAGE" | grep -qE "who|call"; then
    BLOCK="$CALL_BLOCK"
    echo "   → Adding Call Guide"
  else
    BLOCK="$DECISION_BLOCK"
    echo "   → Adding Decision Tool (default)"
  fi

  # Create backup
  cp "$PAGE" "$PAGE.backup-$(date +%Y%m%d)"

  # Inject after first <h1> closing tag
  awk -v block="$BLOCK" '
  BEGIN{added=0}
  {
    print $0
    if(!added && $0 ~ /<\/h1>/){
      print block
      added=1
    }
  }' "$PAGE" > "$PAGE.tmp" && mv "$PAGE.tmp" "$PAGE"

  UPDATED=$((UPDATED+1))
  echo "   ✅ Updated"
  echo ""

done

########################################
# REPORT
########################################

echo "---------------------------------------"
echo "✅ TEST COMPLETE"
echo "Updated pages: $UPDATED"
echo "Timestamp: $DATE"
echo ""
echo "🔍 Review the changes, then run git diff to see modifications"
echo "📁 Backups saved with .backup-YYYYMMDD extension"
echo "---------------------------------------"
