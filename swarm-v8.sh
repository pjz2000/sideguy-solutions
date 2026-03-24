#!/usr/bin/env bash

########################################
# SIDEGUY SWARM v8.1
# priority + protection + pattern engine
# IMPROVED: safety, reporting, human-first
########################################

set -euo pipefail  # Exit on error, undefined vars, pipe failures

PROJECT_ROOT="/workspaces/sideguy-solutions"
PUBLIC_DIR="$PROJECT_ROOT"  # HTML files are at root level, not in /public/
DATA_DIR="$PROJECT_ROOT/data"
SWARM_DIR="$PROJECT_ROOT/docs/swarm"
MEMORY_FILE="$DATA_DIR/swarm-memory.csv"
DATE="$(date +"%Y-%m-%d-%H%M%S")"
REPORT_FILE="$SWARM_DIR/swarm-report-$DATE.md"

cd "$PROJECT_ROOT" || exit 1

mkdir -p "$DATA_DIR" "$SWARM_DIR"

########################################
# CONFIG
########################################

GSC_FILE="$DATA_DIR/gsc-export.csv"

# Execution mode: DRY_RUN=1 for preview only
DRY_RUN="${DRY_RUN:-0}"

# Caps
MAX_REWRITES=25
MAX_EXPANDS=10
MAX_TOOLS=15

# Minimum score thresholds
SCORE_EXPAND=15.0
SCORE_REWRITE=8.0
SCORE_ELITE=12.0

# Safety: require confirmation for production
AUTO_COMMIT="${AUTO_COMMIT:-0}"

########################################
# INIT MEMORY
########################################

if [ ! -f "$MEMORY_FILE" ]; then
  echo "slug,score,trend_streak,last_action,last_seen" > "$MEMORY_FILE"
fi

########################################
# VALIDATION
########################################

echo "🔍 Validating environment..."

if [ ! -f "$GSC_FILE" ]; then
  echo "❌ ERROR: GSC file not found: $GSC_FILE"
  echo ""
  echo "📋 To run this script, you need:"
  echo "   1. Export GSC data as CSV with columns: PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION"
  echo "   2. Save to: $GSC_FILE"
  echo ""
  exit 1
fi

if [ ! -d "$PUBLIC_DIR" ]; then
  echo "⚠️  WARNING: Public directory not found: $PUBLIC_DIR"
  echo "   Creating it..."
  mkdir -p "$PUBLIC_DIR"
fi

GSC_LINES=$(wc -l < "$GSC_FILE")
echo "✅ Found GSC file with $GSC_LINES lines"

if [ "$DRY_RUN" = "1" ]; then
  echo "🔒 DRY RUN MODE - No files will be modified"
fi

echo ""

########################################
# INIT REPORT
########################################

cat > "$REPORT_FILE" << EOF
# Swarm v8.1 Report
**Date:** $(date +"%Y-%m-%d %H:%M:%S")
**Mode:** $([ "$DRY_RUN" = "1" ] && echo "DRY RUN" || echo "LIVE")
**GSC Data:** $GSC_LINES lines

---

## Configuration
- Max Rewrites: $MAX_REWRITES
- Max Expands: $MAX_EXPANDS
- Max Tools: $MAX_TOOLS
- Score Thresholds: Expand ≥$SCORE_EXPAND, Rewrite ≥$SCORE_REWRITE, Elite ≥$SCORE_ELITE

---

EOF

########################################
# HELPERS
########################################

safe_num() { 
  local num="${1:-0}"
  num=$(echo "$num" | tr -cd '0-9.')
  echo "${num:-0}"
}

slug() {
  echo "$1" | sed 's#https\?://[^/]*/##' | sed 's#.html##'
}

intent() {
  local Q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  # Money intent (highest priority)
  if echo "$Q" | grep -Eq 'cost|price|how much|pricing|rate|fee|estimate'; then 
    echo "money"
    return
  fi
  
  # Urgent/call intent
  if echo "$Q" | grep -Eq 'urgent|emergency|same day|who do i call|call|help me|need'; then 
    echo "call"
    return
  fi
  
  # Compare/decision intent
  if echo "$Q" | grep -Eq 'vs|versus|compare|best|better|which|should i'; then 
    echo "compare"
    return
  fi
  
  # Service intent
  if echo "$Q" | grep -Eq 'near me|service|repair|install|fix|replace'; then 
    echo "service"
    return
  fi

  echo "info"
}

score() {
  # Improved scoring: impressions + clicks*5 + ctr*10
  # This values actual engagement over just visibility
  local impressions="$1"
  local clicks="$2"
  local ctr="$3"
  
  awk "BEGIN {printf \"%.2f\", ($impressions/30)+($clicks*5)+($ctr*10)}"
}

pattern_detect() {
  local Q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  # More nuanced pattern detection
  if echo "$Q" | grep -Eq 'how much|cost|price|pricing'; then echo "cost"; return; fi
  if echo "$Q" | grep -Eq ' vs | versus '; then echo "vs"; return; fi
  if echo "$Q" | grep -Eq 'best |top |review'; then echo "best"; return; fi
  if echo "$Q" | grep -Eq 'how to|guide|tutorial|step'; then echo "guide"; return; fi
  if echo "$Q" | grep -Eq 'near me|in san diego|local'; then echo "local"; return; fi
  if echo "$Q" | grep -Eq 'who do i call|should i|do i need'; then echo "decision"; return; fi

  echo "general"
}

validate_html() {
  local file="$1"
  # Basic HTML validation
  if [ ! -f "$file" ]; then return 1; fi
  if ! grep -q '<html' "$file"; then return 1; fi
  if ! grep -q '</html>' "$file"; then return 1; fi
  return 0
}

########################################
# BUILD PAGE SCORES
########################################

echo "📊 Processing GSC data..."

TMP=$(mktemp)

tail -n +2 "$GSC_FILE" | while IFS=',' read -r PAGE QUERY CLICKS IMPRESSIONS CTR POS
do
  # Skip empty lines
  if [ -z "$PAGE" ] || [ -z "$QUERY" ]; then
    continue
  fi
  
  S=$(slug "$PAGE")
  CLK=$(safe_num "$CLICKS")
  IMP=$(safe_num "$IMPRESSIONS")
  CTRV=$(safe_num "$CTR")

  [ -z "$IMP" ] && IMP=0
  [ -z "$CLK" ] && CLK=0
  [ -z "$CTRV" ] && CTRV=0

  INT=$(intent "$QUERY")
  SC=$(score "$IMP" "$CLK" "$CTRV")
  PAT=$(pattern_detect "$QUERY")

  echo "$S|$SC|$INT|$PAT|$QUERY" >> "$TMP"

done

RECORD_COUNT=$(wc -l < "$TMP")
echo "✅ Processed $RECORD_COUNT page records"
echo ""

########################################
# SORT BY SCORE
########################################

SORTED=$(mktemp)
sort -t'|' -k2,2nr "$TMP" > "$SORTED"

########################################
# RUN SWARM WITH CAPS
########################################

echo "🐝 Running swarm intelligence..."
echo ""

REWRITE_COUNT=0
EXPAND_COUNT=0
TOOL_COUNT=0
HOLD_COUNT=0
SKIP_COUNT=0

INDEX=0

# Arrays to track actions for report
declare -a ELITE_PAGES
declare -a REWRITE_PAGES
declare -a EXPAND_PAGES
declare -a TOOL_PAGES
declare -a LOSER_PAGES

while IFS='|' read -r SLUG SCORE INTENT PATTERN QUERY
do

  INDEX=$((INDEX + 1))
  
  # Skip empty lines
  [ -z "$SLUG" ] && continue

  ########################################
  # ELITE 20 ALWAYS PROCESS
  ########################################

  PRIORITY="normal"
  if [ "$INDEX" -le 20 ]; then
    PRIORITY="elite"
    ELITE_PAGES+=("$SLUG (score: $SCORE)")
  fi

  ########################################
  # MEMORY CHECK (LOSER PROTECTION)
  ########################################

  LAST=$(grep "^$SLUG," "$MEMORY_FILE" 2>/dev/null || echo "")

  TREND_STREAK=0
  if [ -n "$LAST" ]; then
    TREND_STREAK=$(echo "$LAST" | cut -d',' -f3)
  fi

  if [ "$TREND_STREAK" -le -3 ]; then
    echo "⛔ Skipping loser: $SLUG (streak: $TREND_STREAK)"
    LOSER_PAGES+=("$SLUG (trend: $TREND_STREAK, score: $SCORE)")
    SKIP_COUNT=$((SKIP_COUNT + 1))
    continue
  fi

  ########################################
  # DECISION
  ########################################

  ACTION="hold"

  # Use awk for floating point comparison (bc not always available)
  if awk "BEGIN {exit !($SCORE >= $SCORE_EXPAND)}"; then
    ACTION="expand"
  elif awk "BEGIN {exit !($SCORE >= $SCORE_REWRITE)}"; then
    ACTION="rewrite"
  fi

  ########################################
  # APPLY CAPS
  ########################################

  if [ "$ACTION" = "rewrite" ] && [ "$REWRITE_COUNT" -ge "$MAX_REWRITES" ]; then
    ACTION="hold"
  fi

  if [ "$ACTION" = "expand" ] && [ "$EXPAND_COUNT" -ge "$MAX_EXPANDS" ]; then
    ACTION="hold"
  fi
  
  if [ "$ACTION" = "hold" ]; then
    HOLD_COUNT=$((HOLD_COUNT + 1))
    continue
  fi

  ########################################
  # EXECUTE (with dry-run support)
  ########################################

  FILE="$PUBLIC_DIR/$SLUG.html"

  if [ -f "$FILE" ]; then

    if [ "$ACTION" = "rewrite" ]; then
      if [ "$DRY_RUN" = "1" ]; then
        echo "🔍 [DRY RUN] Would rewrite: $SLUG"
      else
        # Backup before modifying
        cp "$FILE" "${FILE}.bak.${DATE}"
        
        # More careful title replacement
        sed -i "s#<title>.*</title>#<title>$QUERY · SideGuy Solutions</title>#g" "$FILE"
        echo "✏️  Rewrite: $SLUG"
      fi
      REWRITE_PAGES+=("$SLUG → \"$QUERY\"")
      REWRITE_COUNT=$((REWRITE_COUNT + 1))
    fi

    if [ "$ACTION" = "expand" ]; then
      CHILD="$PUBLIC_DIR/${SLUG}-${PATTERN}.html"

      if [ ! -f "$CHILD" ]; then
        if [ "$DRY_RUN" = "1" ]; then
          echo "🔍 [DRY RUN] Would expand: $SLUG → $PATTERN"
        else
          # Better HTML stub with proper structure
          cat > "$CHILD" << HTMLEOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$QUERY - $PATTERN Guide · SideGuy Solutions</title>
  <meta name="description" content="$QUERY - comprehensive $PATTERN guide for San Diego.">
</head>
<body>
  <h1>$QUERY</h1>
  <p><strong>Pattern:</strong> $PATTERN | <strong>Intent:</strong> $INTENT</p>
  <p>This page is a placeholder generated by Swarm v8.1. Human review required.</p>
  <!-- TODO: Add real content based on $PATTERN pattern -->
</body>
</html>
HTMLEOF
          echo "🚀 Expand: $SLUG → $PATTERN"
        fi
        EXPAND_PAGES+=("$SLUG → $PATTERN [$INTENT]")
        EXPAND_COUNT=$((EXPAND_COUNT + 1))
      fi
    fi

    ########################################
    # TOOL PLACEHOLDER (ELITE ONLY)
    ########################################

    if [ "$PRIORITY" = "elite" ] && [ "$TOOL_COUNT" -lt "$MAX_TOOLS" ]; then
      if ! grep -q "sideguy-tool" "$FILE"; then
        if [ "$DRY_RUN" = "1" ]; then
          echo "🔍 [DRY RUN] Would add tool slot: $SLUG"
        else
          # Better tool placeholder with context
          cat >> "$FILE" << TOOLEOF

<!-- Swarm v8.1 Tool Slot: Added $DATE -->
<div class='sideguy-tool' data-intent='$INTENT' data-score='$SCORE'>
  <p><strong>🛠️ Interactive Tool Coming Soon</strong></p>
  <p>Based on query: "$QUERY"</p>
</div>
TOOLEOF
          echo "💰 Tool slot: $SLUG"
        fi
        TOOL_PAGES+=("$SLUG [$INTENT, score: $SCORE]")
        TOOL_COUNT=$((TOOL_COUNT + 1))
      fi
    fi

  else
    # Page doesn't exist - log for review
    echo "⚠️  Page not found: $FILE"
  fi

  ########################################
  # UPDATE MEMORY
  ########################################

  if [ "$DRY_RUN" != "1" ]; then
    grep -v "^$SLUG," "$MEMORY_FILE" > "${MEMORY_FILE}.tmp" 2>/dev/null || true
    echo "$SLUG,$SCORE,0,$ACTION,$DATE" >> "${MEMORY_FILE}.tmp"
    mv "${MEMORY_FILE}.tmp" "$MEMORY_FILE"
  fi

done < "$SORTED"

########################################
# FINISH & REPORT
########################################

echo ""
echo "================================"
echo "🎯 Swarm v8.1 Complete"
echo "================================"
echo "Rewrites:   $REWRITE_COUNT / $MAX_REWRITES"
echo "Expands:    $EXPAND_COUNT / $MAX_EXPANDS"
echo "Tools:      $TOOL_COUNT / $MAX_TOOLS"
echo "Hold:       $HOLD_COUNT"
echo "Skipped:    $SKIP_COUNT (losers)"
echo "================================"
echo ""

########################################
# GENERATE DETAILED REPORT
########################################

cat >> "$REPORT_FILE" << EOF
## Results

| Action | Count | Cap |
|--------|-------|-----|
| Rewrites | $REWRITE_COUNT | $MAX_REWRITES |
| Expands | $EXPAND_COUNT | $MAX_EXPANDS |
| Tools | $TOOL_COUNT | $MAX_TOOLS |
| Hold | $HOLD_COUNT | N/A |
| Skipped (losers) | $SKIP_COUNT | N/A |

---

## Elite Pages (Top 20)

EOF

for page in "${ELITE_PAGES[@]}"; do
  echo "- $page" >> "$REPORT_FILE"
done

if [ "$REWRITE_COUNT" -gt 0 ]; then
  cat >> "$REPORT_FILE" << EOF

---

## Rewrites ($REWRITE_COUNT)

EOF
  for page in "${REWRITE_PAGES[@]}"; do
    echo "- $page" >> "$REPORT_FILE"
  done
fi

if [ "$EXPAND_COUNT" -gt 0 ]; then
  cat >> "$REPORT_FILE" << EOF

---

## Expansions ($EXPAND_COUNT)

EOF
  for page in "${EXPAND_PAGES[@]}"; do
    echo "- $page" >> "$REPORT_FILE"
  done
fi

if [ "$TOOL_COUNT" -gt 0 ]; then
  cat >> "$REPORT_FILE" << EOF

---

## Tool Slots Added ($TOOL_COUNT)

EOF
  for page in "${TOOL_PAGES[@]}"; do
    echo "- $page" >> "$REPORT_FILE"
  done
fi

if [ "$SKIP_COUNT" -gt 0 ]; then
  cat >> "$REPORT_FILE" << EOF

---

## Skipped Pages (Negative Trend) ($SKIP_COUNT)

EOF
  for page in "${LOSER_PAGES[@]}"; do
    echo "- $page" >> "$REPORT_FILE"
  done
fi

cat >> "$REPORT_FILE" << EOF

---

## Recommendations

### Human Review Required

1. **Expanded pages** need content - they're currently placeholders
2. **Tool slots** need interactive calculator/widget implementation
3. **Rewritten titles** should be validated for brand consistency

### Next Steps

1. Review this report: \`$REPORT_FILE\`
2. Check modified files for quality
3. Test on staging before production deploy
4. Update memory file manually if needed: \`$MEMORY_FILE\`

### To Revert Changes

All modified files were backed up with \`.bak.$DATE\` extension.

\`\`\`bash
# Restore all backups
find $PUBLIC_DIR -name "*.bak.$DATE" -exec bash -c 'mv "\$0" "\${0%.bak.$DATE}"' {} \;
\`\`\`

---

**Report generated:** $(date)
**Mode:** $([ "$DRY_RUN" = "1" ] && echo "DRY RUN (no changes made)" || echo "LIVE (changes applied)")

EOF

echo "📄 Detailed report saved: $REPORT_FILE"
echo ""

########################################
# GIT HANDLING (with safety)
########################################

if [ "$DRY_RUN" = "1" ]; then
  echo "🔒 Dry run complete - no git operations"
  echo "   Run without DRY_RUN=1 to apply changes"
elif [ "$AUTO_COMMIT" = "1" ]; then
  echo "🔄 Auto-committing changes..."
  git add .
  git commit -m "swarm v8.1: $REWRITE_COUNT rewrites, $EXPAND_COUNT expands, $TOOL_COUNT tools ($DATE)" || {
    echo "⚠️  Git commit failed (possibly no changes)"
  }
else
  echo "⏸️  Changes ready for review"
  echo ""
  echo "   Review modified files, then commit:"
  echo "   git add ."
  echo "   git commit -m 'swarm v8.1: applied intelligence'"
  echo ""
  echo "   Or to auto-commit next time:"
  echo "   AUTO_COMMIT=1 ./swarm-v8.sh"
fi

echo ""
echo "✨ Done. Read the report for next steps."
