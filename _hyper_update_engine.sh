#!/usr/bin/env bash

########################################
# SIDEGUY HYPER UPDATE ENGINE v2
# Query-level precision content injection
# Injects micro-blocks after H1 based on
# Google Search Console query intent
########################################

set -e  # Exit on error

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

INPUT="docs/gsc/query-pages.csv"
OUT_DIR="docs/hyper-update"
LOG="$OUT_DIR/hyper-log.txt"
REPORT="$OUT_DIR/hyper-report.md"

# Dry run mode: set to "true" to preview without making changes
DRY_RUN="${DRY_RUN:-false}"

########################################
# PREFLIGHT CHECKS
########################################

echo ""
echo "---------------------------------------"
echo "🎯 SIDEGUY HYPER UPDATE ENGINE v2"
echo "---------------------------------------"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "⚠️  DRY RUN MODE — No files will be modified"
  echo ""
fi

if [[ ! -f "$INPUT" ]]; then
  echo "❌ ERROR: Input file not found: $INPUT"
  echo ""
  echo "Expected CSV format:"
  echo "  page,query,clicks,impressions,ctr,position"
  echo ""
  echo "Create this file from Google Search Console:"
  echo "  Performance > Pages > Export > CSV"
  exit 1
fi

mkdir -p "$OUT_DIR"

echo "📂 Input:  $INPUT"
echo "📂 Output: $OUT_DIR"
echo "📋 Log:    $LOG"
echo ""

########################################
# HELPERS
########################################

normalize_url() {
  local url="$1"
  # Strip domain variations
  url="${url#https://www.sideguysolutions.com/}"
  url="${url#https://sideguysolutions.com/}"
  url="${url#http://www.sideguysolutions.com/}"
  url="${url#http://sideguysolutions.com/}"
  url="${url#www.sideguysolutions.com/}"
  url="${url#sideguysolutions.com/}"
  
  # Strip query params and anchors
  url="${url%%\?*}"
  url="${url%%\#*}"
  
  # Handle root
  [ -z "$url" ] && echo "index.html" && return
  
  # Add .html if missing
  [[ "$url" != *.html ]] && url="$url.html"
  
  echo "$url"
}

detect_intent() {
  local q="$1"
  q=$(echo "$q" | tr '[:upper:]' '[:lower:]')

  # Cost queries (check first - high priority)
  if [[ "$q" =~ (cost|price|how\ much|estimate|expensive|cheap|afford) ]]; then
    echo "cost"
    return
  fi
  
  # Emergency/urgent queries
  if [[ "$q" =~ (emergency|urgent|immediate|asap|now|help|broke) ]]; then
    echo "emergency"
    return
  fi
  
  # Decision queries (repair vs replace, should I, worth it)
  if [[ "$q" =~ (repair|replace|worth|should|when\ to|is\ it) ]]; then
    echo "decision"
    return
  fi
  
  # Comparison queries
  if [[ "$q" =~ (vs|versus|compare|comparison|better|best|which|difference) ]]; then
    echo "compare"
    return
  fi
  
  # Who to call queries
  if [[ "$q" =~ (who|call|contact|service|find|hire) ]]; then
    echo "call"
    return
  fi
  
  # Default
  echo "general"
}

########################################
# BUILD CONTENT BLOCK
########################################

build_block() {
  local query="$1"
  local intent="$2"
  
  # Style matches existing SideGuy inline patterns
  # Uses :root variables for consistency
  local block="<section data-hyper-update='v2' data-query-intent='$intent' style='background:var(--card,#ffffffcc);padding:20px 24px;border-radius:var(--r,12px);margin:24px 0;border:1px solid var(--stroke,rgba(7,48,68,.10));box-shadow:0 2px 12px rgba(7,48,68,.06);'>
  <div style='font-size:14px;font-weight:600;color:var(--mint,#21d3a1);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;'>Quick Answer</div>
  <div style='font-size:15px;line-height:1.6;color:var(--ink,#073044);'>"

  case "$intent" in
    decision)
      block="$block<p><strong>Should you repair or replace?</strong> If the issue is minor or recent, repair usually makes sense. If costs are stacking up or the system is 12+ years old, replacement becomes the better long-term move.</p>"
      ;;
    cost)
      block="$block<p><strong>What will this cost?</strong> Prices vary by scope and location, but most jobs fall into predictable ranges based on size, labor, and complexity. Use this as a directional guide before calling for quotes.</p>"
      ;;
    compare)
      block="$block<p><strong>Which option is better?</strong> It depends on how you're using it and what you value. One approach tends to be simpler upfront; the other delivers better long-term results.</p>"
      ;;
    call)
      block="$block<p><strong>Who should you contact?</strong> Start with a specialist for the specific system. If you're not sure who that is, text PJ for fast routing to the right person.</p>"
      ;;
    emergency)
      block="$block<p><strong>Is this a real emergency?</strong> If there's active flooding, gas smell, or immediate safety risk — yes, call now. If it's inconvenient but stable, you can wait for regular hours and save 50%+ on after-hours fees.</p>"
      ;;
    *)
      block="$block<p>Looking for clarity on <em>\"$query\"</em>? Most questions come down to cost, timeline, and whether you need a pro or can DIY. This page walks through what actually matters.</p>"
      ;;
  esac

  block="$block  </div>
  <div style='margin-top:16px;padding-top:16px;border-top:1px solid var(--stroke2,rgba(7,48,68,.07));'>
    <p style='margin:0;font-size:14px;color:var(--muted,#3f6173);'><strong style='color:var(--ink,#073044);'>Need a real answer?</strong> Text PJ → <a href='tel:+17735441231' style='color:var(--mint,#21d3a1);text-decoration:none;font-weight:600;'>773-544-1231</a></p>
  </div>
</section>"

  echo "$block"
}

########################################
# MAIN PROCESSING
########################################

# Initialize counters and logs
> "$LOG"  # Clear log

# Initialize report
cat > "$REPORT" <<EOF
# Hyper Update Report
**Generated:** $(date)
**Mode:** $([ "$DRY_RUN" == "true" ] && echo "DRY RUN" || echo "LIVE")

## Summary
EOF

echo "Processing queries..."
echo ""

# Use process substitution to avoid subshell (preserves counters)
while IFS=, read -r page query clicks impressions ctr position; do
  
  # Skip empty lines
  [ -z "$page" ] && continue
  [ -z "$query" ] && continue
  
  TOTAL=$((TOTAL + 1))
  
  # Normalize URL to file path
  FILE=$(normalize_url "$page")
  
  # Check if file exists
  if [[ ! -f "$FILE" ]]; then
    echo "MISSING|$FILE|$query" >> "$LOG"
    MISSING=$((MISSING + 1))
    continue
  fi
  
  # Skip if already updated
  if grep -q "data-hyper-update" "$FILE"; then
    echo "SKIPPED|$FILE|already updated" >> "$LOG"
    SKIPPED=$((SKIPPED + 1))
    continue
  fi
  
  # Detect intent
  INTENT=$(detect_intent "$query")
  
  # Build content block
  BLOCK=$(build_block "$query" "$INTENT")
  
  # Inject after H1
  if [[ "$DRY_RUN" == "true" ]]; then
    echo "DRYRUN|$FILE|$query|$INTENT" >> "$LOG"
    echo "  [DRY] $FILE → $INTENT"
  else
    # Use awk to inject after H1
    awk -v block="$BLOCK" '
    BEGIN{added=0}
    {
      print $0
      if(!added && $0 ~ /<h1/){
        # Find the closing tag
        if($0 ~ /<\/h1>/){
          print block
          added=1
        }
      }
      if(!added && inserted && $0 ~ /<\/h1>/){
        print block
        added=1
      }
      if(!added && $0 ~ /<h1/ && $0 !~ /<\/h1>/){
        inserted=1
      }
    }' "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"
    
    echo "UPDATED|$FILE|$query|$INTENT" >> "$LOG"
    UPDATED=$((UPDATED + 1))
    echo "  ✅ $FILE → $INTENT"
  fi
  
done < <(tail -n +2 "$INPUT")

# Update counters display
TOTAL=$(grep -c "^" "$LOG" || echo "0")
UPDATED=$(grep -c "^UPDATED" "$LOG" || echo "0")
SKIPPED=$(grep -c "^SKIPPED" "$LOG" || echo "0")
MISSING=$(grep -c "^MISSING" "$LOG" || echo "0")

########################################
# FINAL REPORT
########################################

echo ""
echo "---------------------------------------"
echo "✅ HYPER UPDATE COMPLETE"
echo "---------------------------------------"
echo ""
echo "  Total Queries:  $TOTAL"
echo "  Updated:        $UPDATED"
echo "  Skipped:        $SKIPPED (already updated)"
echo "  Missing Files:  $MISSING"
echo ""
echo "📋 Full log: $LOG"
echo "📊 Report:   $REPORT"
echo ""

# Append stats to report
cat >> "$REPORT" <<EOF

- **Total Queries:** $TOTAL
- **Updated:** $UPDATED
- **Skipped:** $SKIPPED (already had hyper-update block)
- **Missing Files:** $MISSING

## Intent Distribution
EOF

if [[ -f "$LOG" ]]; then
  echo "" >> "$REPORT"
  echo "\`\`\`" >> "$REPORT"
  grep "^UPDATED" "$LOG" | cut -d'|' -f4 | sort | uniq -c | sort -rn >> "$REPORT"
  echo "\`\`\`" >> "$REPORT"
  
  echo "" >> "$REPORT"
  echo "## Updated Pages" >> "$REPORT"
  echo "" >> "$REPORT"
  grep "^UPDATED" "$LOG" | while IFS='|' read -r status file query intent; do
    echo "- **$file** → $intent: \"$query\"" >> "$REPORT"
  done
fi

echo ""
if [[ "$DRY_RUN" == "true" ]]; then
  echo "💡 To run for real: DRY_RUN=false $0"
  echo ""
fi
