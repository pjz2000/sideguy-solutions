#!/usr/bin/env bash

########################################
# SIDEGUY SWARM v9 UNIFIED
# Best of v8.1 safety + v3 automation
# Human-first with intelligent assistance
########################################

set -euo pipefail

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATA_DIR="$PROJECT_ROOT/data"
DOCS_DIR="$PROJECT_ROOT/docs"
LOG_DIR="$DOCS_DIR/swarm-logs"
QUEUE_DIR="$PROJECT_ROOT/seo-reserve"
PUBLIC_DIR="$PROJECT_ROOT"
SWARM_DIR="$PROJECT_ROOT/docs/swarm"

STAMP="$(date +"%Y-%m-%d-%H%M%S")"
TODAY="$(date +"%Y-%m-%d")"

SITEMAP_FILE="$PUBLIC_DIR/sitemap.xml"
INDEX_FILE="$PUBLIC_DIR/index.html"

cd "$PROJECT_ROOT" || exit 1

mkdir -p "$DATA_DIR" "$DOCS_DIR" "$LOG_DIR" "$QUEUE_DIR" "$SWARM_DIR"

RUN_LOG="$LOG_DIR/swarm-v9-$STAMP.md"
QUEUE_FILE="$QUEUE_DIR/swarm-queue.csv"
REPORT_FILE="$SWARM_DIR/swarm-v9-report-$STAMP.md"

DOMAIN="https://www.sideguysolutions.com"

########################################
# CONFIG
########################################

# Execution mode
DRY_RUN="${DRY_RUN:-0}"
AUTO_COMMIT="${AUTO_COMMIT:-0}"

# Caps (combine both strategies)
MAX_UPGRADES=25        # In-place HTML upgrades
MAX_CHILDREN=15        # New child pages
MAX_REWRITES=10        # Title tag rewrites
MAX_SITEMAP=30         # Sitemap additions
MAX_INDEX=30           # Index additions

# Scoring thresholds (from v8.1)
SCORE_HIGH=15.0
SCORE_MEDIUM=8.0
SCORE_LOW=5.0

# GSC gold zone (from v3)
MIN_IMPRESSIONS=5
MIN_POSITION=4
MAX_POSITION=30

########################################
# HELPERS
########################################

safe_num() {
  local num="${1:-0}"
  num=$(echo "$num" | tr -cd '0-9.')
  echo "${num:-0}"
}

slug_from_url() {
  echo "$1" | sed 's#https\?://[^/]*/##' | sed 's#.html##'
}

slugify() {
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | sed 's/--*/-/g' \
    | sed 's/^-//;s/-$//'
}

intent() {
  local Q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  if echo "$Q" | grep -Eq 'cost|price|how much|pricing|rate|fee|estimate'; then 
    echo "money"
    return
  fi
  
  if echo "$Q" | grep -Eq 'urgent|emergency|same day|who do i call|call|help me|need'; then 
    echo "call"
    return
  fi
  
  if echo "$Q" | grep -Eq 'vs|versus|compare|best|better|which|should i'; then 
    echo "compare"
    return
  fi
  
  if echo "$Q" | grep -Eq 'near me|service|repair|install|fix|replace'; then 
    echo "service"
    return
  fi

  echo "info"
}

score() {
  local impressions="$1"
  local clicks="$2"
  local ctr="$3"
  
  awk "BEGIN {printf \"%.2f\", ($impressions/30)+($clicks*5)+($ctr*10)}"
}

pattern_detect() {
  local Q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  if echo "$Q" | grep -Eq 'how much|cost|price|pricing'; then echo "cost"; return; fi
  if echo "$Q" | grep -Eq ' vs | versus '; then echo "vs"; return; fi
  if echo "$Q" | grep -Eq 'best |top |review'; then echo "best"; return; fi
  if echo "$Q" | grep -Eq 'how to|guide|tutorial|step'; then echo "guide"; return; fi
  if echo "$Q" | grep -Eq 'near me|in san diego|local'; then echo "local"; return; fi
  if echo "$Q" | grep -Eq 'who do i call|should i|do i need'; then echo "decision"; return; fi

  echo "general"
}

########################################
# INIT REPORT
########################################

echo "---------------------------------------"
echo "🧠 SIDEGUY SWARM v9 UNIFIED"
echo "---------------------------------------"
echo "Timestamp: $STAMP"
echo "Mode: $([ "$DRY_RUN" = "1" ] && echo "DRY RUN" || echo "LIVE")"
echo ""

cat > "$REPORT_FILE" << EOF
# 🧠 SideGuy Swarm v9 Unified Report

**Date:** $TODAY $STAMP  
**Mode:** $([ "$DRY_RUN" = "1" ] && echo "DRY RUN (no changes)" || echo "LIVE")  
**Project:** $PROJECT_ROOT  
**Domain:** $DOMAIN

---

## Configuration

| Setting | Value |
|---------|-------|
| Max Upgrades | $MAX_UPGRADES |
| Max Children | $MAX_CHILDREN |
| Max Rewrites | $MAX_REWRITES |
| Max Sitemap Adds | $MAX_SITEMAP |
| Max Index Adds | $MAX_INDEX |
| Score High | ≥$SCORE_HIGH |
| Score Medium | ≥$SCORE_MEDIUM |
| Score Low | ≥$SCORE_LOW |

---

EOF

########################################
# VALIDATION
########################################

echo "🔍 Validating environment..."
echo "## Prechecks" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

GSC_FILE="$DATA_DIR/gsc.csv"

if [ -f "$GSC_FILE" ]; then
  GSC_LINES=$(wc -l < "$GSC_FILE")
  echo "✅ Found GSC data: $GSC_LINES lines"
  echo "- GSC file: $GSC_FILE ($GSC_LINES lines)" >> "$REPORT_FILE"
  USE_GSC=1
else
  echo "⚠️  No GSC data - will use inventory scan fallback"
  echo "- No GSC file found (using inventory scan)" >> "$REPORT_FILE"
  USE_GSC=0
fi

[ -f "$INDEX_FILE" ] && echo "- Found index.html ✓" >> "$REPORT_FILE" || echo "- Missing index.html ⚠️" >> "$REPORT_FILE"
[ -f "$SITEMAP_FILE" ] && echo "- Found sitemap.xml ✓" >> "$REPORT_FILE" || echo "- Missing sitemap.xml ⚠️" >> "$REPORT_FILE"

if [ "$DRY_RUN" = "1" ]; then
  echo "🔒 DRY RUN MODE - No files will be modified"
  echo "" >> "$REPORT_FILE"
  echo "**🔒 DRY RUN MODE ACTIVE**" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"
echo ""

########################################
# INGEST & SCORE
########################################

echo "📊 Processing signals..."
echo "## Signal Intelligence" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

TMP_SCORED=$(mktemp)

if [ "$USE_GSC" = "1" ]; then
  # GSC-based processing with v8.1 scoring
  # Support two CSV formats: PAGE,QUERY,... or QUERY,CLICKS,...
  FIRST_LINE=$(head -2 "$GSC_FILE" | tail -1)
  
  if echo "$FIRST_LINE" | grep -q "^https\?://"; then
    # Format: PAGE,QUERY,CLICKS,IMPRESSIONS,CTR,POSITION
    tail -n +2 "$GSC_FILE" | while IFS=',' read -r PAGE QUERY CLICKS IMPRESSIONS CTR POSITION
    do
      [ -z "$QUERY" ] && continue
      
      CLK=$(safe_num "$CLICKS")
      IMP=$(safe_num "$IMPRESSIONS")
      CTRV=$(safe_num "$CTR")
      POS=$(safe_num "$POSITION")
      
      # Filter to gold zone
      if awk "BEGIN {exit !($IMP >= $MIN_IMPRESSIONS && $POS >= $MIN_POSITION && $POS <= $MAX_POSITION)}"; then
        INT=$(intent "$QUERY")
        SC=$(score "$IMP" "$CLK" "$CTRV")
        PAT=$(pattern_detect "$QUERY")
        
        echo "$SC|$QUERY|$CLK|$IMP|$CTRV|$POS|$PAGE|$INT|$PAT" >> "$TMP_SCORED"
      fi
    done
  else
    # Format: QUERY,CLICKS,IMPRESSIONS,CTR,POSITION,PAGE
    tail -n +2 "$GSC_FILE" | while IFS=',' read -r QUERY CLICKS IMPRESSIONS CTR POSITION PAGE
    do
      [ -z "$QUERY" ] && continue
      
      CLK=$(safe_num "$CLICKS")
      IMP=$(safe_num "$IMPRESSIONS")
      CTRV=$(safe_num "$CTR")
      POS=$(safe_num "$POSITION")
      
      # Filter to gold zone
      if awk "BEGIN {exit !($IMP >= $MIN_IMPRESSIONS && $POS >= $MIN_POSITION && $POS <= $MAX_POSITION)}"; then
        INT=$(intent "$QUERY")
        SC=$(score "$IMP" "$CLK" "$CTRV")
        PAT=$(pattern_detect "$QUERY")
        
        echo "$SC|$QUERY|$CLK|$IMP|$CTRV|$POS|$PAGE|$INT|$PAT" >> "$TMP_SCORED"
      fi
    done
  fi
else
  # Fallback: inventory scan with estimated scores
  find "$PUBLIC_DIR" -maxdepth 1 -name "*.html" \
    | sed 's#^\./##' \
    | grep -E "hvac|solar|payment|repair|cost|san-diego|automation|ai|plumbing|electrical|foundation|roof" \
    | head -n 30 \
    | while read -r FILE; do
        QUERY=$(echo "$FILE" | sed 's/.html$//' | tr '-' ' ')
        INT=$(intent "$QUERY")
        PAT=$(pattern_detect "$QUERY")
        echo "25.00|$QUERY|2|100|0.02|12|$FILE|$INT|$PAT" >> "$TMP_SCORED"
      done
fi

# Sort by score
SORTED=$(mktemp)
sort -t'|' -k1,1nr "$TMP_SCORED" > "$SORTED"

SIGNAL_COUNT=$(wc -l < "$SORTED")
echo "- Total signals: $SIGNAL_COUNT" >> "$REPORT_FILE"
echo "✅ Processed $SIGNAL_COUNT signals"
echo "" >> "$REPORT_FILE"
echo ""

########################################
# BUILD QUEUE
########################################

echo "🧾 Building queue..."
echo "## Queue Build" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ ! -f "$QUEUE_FILE" ]; then
  echo "priority,score,query,clicks,impressions,ctr,position,page,intent,pattern,action,status" > "$QUEUE_FILE"
fi

# Convert sorted signals to queue
awk -F'|' -v high="$SCORE_HIGH" -v med="$SCORE_MEDIUM" '
{
  score=$1
  query=$2
  clicks=$3
  impressions=$4
  ctr=$5
  position=$6
  page=$7
  intent=$8
  pattern=$9
  
  priority="LOW"
  if (score >= high) priority="HIGH"
  else if (score >= med) priority="MEDIUM"
  
  action="upgrade_and_spawn"
  status="queued"
  
  print priority "," score "," query "," clicks "," impressions "," ctr "," position "," page "," intent "," pattern "," action "," status
}
' "$SORTED" > "$QUEUE_DIR/swarm-working.csv"

QUEUE_COUNT=$(wc -l < "$QUEUE_DIR/swarm-working.csv")
echo "- Queue items: $QUEUE_COUNT" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo ""

########################################
# SELECT TOP TARGETS
########################################

echo "🎯 Selecting targets..."

TOP_FILE="$DATA_DIR/swarm-top-targets.csv"
head -n 25 "$QUEUE_DIR/swarm-working.csv" > "$TOP_FILE"

echo "## Top 25 Targets" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| Priority | Score | Query | Intent | Pattern |" >> "$REPORT_FILE"
echo "|----------|-------|-------|--------|---------|" >> "$REPORT_FILE"

head -n 25 "$QUEUE_DIR/swarm-working.csv" | while IFS=',' read -r PRIORITY SCORE QUERY REST; do
  INTENT=$(echo "$REST" | cut -d',' -f7)
  PATTERN=$(echo "$REST" | cut -d',' -f8)
  echo "| $PRIORITY | $SCORE | $QUERY | $INTENT | $PATTERN |" >> "$REPORT_FILE"
done

echo "" >> "$REPORT_FILE"
echo ""

########################################
# COUNTERS & TRACKING
########################################

UPGRADE_COUNT=0
CHILD_COUNT=0
REWRITE_COUNT=0
SITEMAP_COUNT=0
INDEX_COUNT=0

declare -a UPGRADED_PAGES
declare -a CREATED_CHILDREN
declare -a REWRITTEN_TITLES
declare -a SITEMAP_ADDS
declare -a INDEX_ADDS

########################################
# FUNCTIONS: UPGRADE PAGES
########################################

upgrade_page() {
  local PAGE_PATH="$1"
  local QUERY="$2"
  local SCORE="$3"
  local INTENT="$4"
  
  [ -f "$PAGE_PATH" ] || return
  [ "$UPGRADE_COUNT" -ge "$MAX_UPGRADES" ] && return
  
  local MODIFIED=0
  
  # Add swarm note if missing
  if ! grep -q "sg-swarm-note" "$PAGE_PATH"; then
    if [ "$DRY_RUN" != "1" ]; then
      cp "$PAGE_PATH" "${PAGE_PATH}.bak.${STAMP}"
      sed -i '/<\/body>/i\
<section class="sg-swarm-note" style="margin:40px auto;max-width:900px;padding:24px;border:1px solid rgba(255,255,255,.12);border-radius:18px;background:rgba(255,255,255,.03);">\
<h2>Need a clear next step?</h2>\
<p>This page is being actively improved based on real search demand. If your situation is specific, urgent, or confusing, text PJ for a human-first answer.</p>\
<p><strong>Text PJ:</strong> 773-544-1231</p>\
</section>' "$PAGE_PATH"
    fi
    MODIFIED=1
  fi
  
  # Add cost block for money intent
  if [ "$INTENT" = "money" ] && ! grep -q "sg-cost-block" "$PAGE_PATH"; then
    if [ "$DRY_RUN" != "1" ]; then
      [ ! -f "${PAGE_PATH}.bak.${STAMP}" ] && cp "$PAGE_PATH" "${PAGE_PATH}.bak.${STAMP}"
      sed -i '/<\/body>/i\
<section class="sg-cost-block" style="margin:40px auto;max-width:900px;padding:24px;border:1px solid rgba(255,255,255,.12);border-radius:18px;background:rgba(255,255,255,.02);">\
<h2>Cost, timing, and what changes the answer</h2>\
<p>The real answer usually depends on urgency, scope, access, and whether this is a repair, replacement, setup, or comparison situation.</p>\
<p>Text PJ if you want the fast version without calling five random companies.</p>\
</section>' "$PAGE_PATH"
    fi
    MODIFIED=1
  fi
  
  # Add contact orb
  if ! grep -q "773-544-1231" "$PAGE_PATH"; then
    if [ "$DRY_RUN" != "1" ]; then
      [ ! -f "${PAGE_PATH}.bak.${STAMP}" ] && cp "$PAGE_PATH" "${PAGE_PATH}.bak.${STAMP}"
      sed -i '/<\/body>/i\
<div style="position:fixed;right:18px;bottom:18px;z-index:9999;padding:14px 18px;border-radius:999px;background:#ffffff;color:#111;font-weight:700;box-shadow:0 10px 30px rgba(0,0,0,.25);">💬 Text PJ • 773-544-1231</div>' "$PAGE_PATH"
    fi
    MODIFIED=1
  fi
  
  if [ "$MODIFIED" = "1" ]; then
    UPGRADE_COUNT=$((UPGRADE_COUNT + 1))
    UPGRADED_PAGES+=("$PAGE_PATH (score: $SCORE, intent: $INTENT)")
    if [ "$DRY_RUN" = "1" ]; then
      echo "🔍 [DRY RUN] Would upgrade: $PAGE_PATH"
    else
      echo "✏️  Upgraded: $PAGE_PATH"
    fi
  fi
}

########################################
# FUNCTIONS: CREATE CHILDREN
########################################

create_child_page() {
  local SOURCE_PAGE="$1"
  local CHILD_FILE="$2"
  local CHILD_TITLE="$3"
  local CHILD_H1="$4"
  local CHILD_DESC="$5"
  
  [ "$CHILD_COUNT" -ge "$MAX_CHILDREN" ] && return
  
  if [ -f "$CHILD_FILE" ]; then
    echo "⏭️  Exists: $CHILD_FILE"
    return
  fi
  
  if [ "$DRY_RUN" = "1" ]; then
    echo "🔍 [DRY RUN] Would create: $CHILD_FILE"
    CHILD_COUNT=$((CHILD_COUNT + 1))
    CREATED_CHILDREN+=("$CHILD_FILE")
    return
  fi
  
  # Create HTML
  if [ -f "$SOURCE_PAGE" ]; then
    cp "$SOURCE_PAGE" "$CHILD_FILE"
  else
    cat > "$CHILD_FILE" << 'EOF'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>TITLE_PLACEHOLDER</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="DESC_PLACEHOLDER">
<link rel="canonical" href="CANONICAL_PLACEHOLDER">
<style>
:root {
  --bg0:#eefcff;
  --ink:#073044;
  --mint:#21d3a1;
}
body {
  font-family:-apple-system,system-ui,sans-serif;
  background:linear-gradient(to bottom,var(--bg0),#fff);
  color:var(--ink);
  margin:0;
  padding:0;
}
main {
  max-width:900px;
  margin:60px auto;
  padding:24px;
}
</style>
</head>
<body>
<main>
  <h1>H1_PLACEHOLDER</h1>
  <p>DESC_PLACEHOLDER</p>
  <p><strong>Text PJ for human-first guidance:</strong> 773-544-1231</p>
  <p><a href="/index.html">← Back to Home</a></p>
</main>
</body>
</html>
EOF
  fi
  
  # Replace placeholders
  sed -i "s#<title>.*</title>#<title>$CHILD_TITLE</title>#g" "$CHILD_FILE"
  sed -i "s#TITLE_PLACEHOLDER#$CHILD_TITLE#g" "$CHILD_FILE"
  sed -i "s#DESC_PLACEHOLDER#$CHILD_DESC#g" "$CHILD_FILE"
  sed -i "s#H1_PLACEHOLDER#$CHILD_H1#g" "$CHILD_FILE"
  sed -i "s#CANONICAL_PLACEHOLDER#$DOMAIN/$CHILD_FILE#g" "$CHILD_FILE"
  
  # Update meta description
  if grep -q '<meta name="description"' "$CHILD_FILE"; then
    sed -i "s#<meta name=\"description\" content=\".*\">#<meta name=\"description\" content=\"$CHILD_DESC\">#g" "$CHILD_FILE"
  fi
  
  # Update canonical
  if grep -q '<link rel="canonical"' "$CHILD_FILE"; then
    sed -i "s#<link rel=\"canonical\" href=\".*\">#<link rel=\"canonical\" href=\"$DOMAIN/$CHILD_FILE\">#g" "$CHILD_FILE"
  fi
  
  # Update h1
  if grep -q '<h1>' "$CHILD_FILE"; then
    sed -i "0,/<h1>.*<\/h1>/s#<h1>.*</h1>#<h1>$CHILD_H1</h1>#" "$CHILD_FILE"
  fi
  
  # Add swarm generation note
  if ! grep -q "Generated by Swarm v9" "$CHILD_FILE"; then
    sed -i '/<\/body>/i\
<!-- Generated by Swarm v9 on '"$TODAY"' - Human review required -->' "$CHILD_FILE"
  fi
  
  CHILD_COUNT=$((CHILD_COUNT + 1))
  CREATED_CHILDREN+=("$CHILD_FILE")
  echo "🚀 Created: $CHILD_FILE"
}

########################################
# EXECUTE: PROCESS TOP TARGETS
########################################

echo "⚙️  Processing targets..."
echo "## Actions" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

while IFS=',' read -r PRIORITY SCORE QUERY CLICKS IMPRESSIONS CTR POSITION PAGE INTENT PATTERN ACTION STATUS
do
  BASE_SLUG="$(slugify "$QUERY")"
  PAGE_CLEAN="$(slug_from_url "$PAGE")"
  
  # Determine source page
  if [ -z "$PAGE_CLEAN" ]; then
    SOURCE_PAGE="$BASE_SLUG.html"
  else
    SOURCE_PAGE="$PAGE_CLEAN.html"
  fi
  
  # UPGRADE existing page
  if [ -f "$SOURCE_PAGE" ]; then
    upgrade_page "$SOURCE_PAGE" "$QUERY" "$SCORE" "$INTENT"
  fi
  
  # CREATE child pages
  create_child_page "$SOURCE_PAGE" "${BASE_SLUG}-cost.html" \
    "$QUERY Cost | SideGuy Solutions" \
    "$QUERY Cost" \
    "Cost guide, real-world variables, and human-first help for $QUERY."
  
  create_child_page "$SOURCE_PAGE" "${BASE_SLUG}-near-me.html" \
    "$QUERY Near Me | SideGuy Solutions" \
    "$QUERY Near Me" \
    "Local help, what to look for, and how to avoid wasting time on $QUERY."
  
  create_child_page "$SOURCE_PAGE" "${BASE_SLUG}-worth-it.html" \
    "Is $QUERY Worth It? | SideGuy Solutions" \
    "Is $QUERY Worth It?" \
    "Decision help, replacement vs repair framing, and clear next steps for $QUERY."
  
done < "$TOP_FILE"

echo "" >> "$REPORT_FILE"
echo ""

########################################
# INTERNAL LINKING
########################################

if [ "$CHILD_COUNT" -gt 0 ]; then
  echo "🔗 Building internal links..."
  echo "## Internal Links" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  
  for CHILD in "${CREATED_CHILDREN[@]}"; do
    [ -f "$CHILD" ] || continue
    [ "$DRY_RUN" = "1" ] && continue
    
    if ! grep -q "Related SideGuy Help" "$CHILD"; then
      {
        echo '<section style="margin:40px auto;max-width:900px;padding:24px;">'
        echo '<h3>Related SideGuy Help</h3>'
        echo '<ul>'
        for OTHER in "${CREATED_CHILDREN[@]}"; do
          [ "$CHILD" != "$OTHER" ] && echo "<li><a href=\"/$OTHER\">$OTHER</a></li>"
        done
        echo '</ul>'
        echo '</section>'
      } > /tmp/sg-links-${STAMP}.html
      
      sed -i '/<\/body>/e cat /tmp/sg-links-'"${STAMP}"'.html' "$CHILD"
      echo "- Linked: $CHILD" >> "$REPORT_FILE"
    fi
  done
  
  echo "" >> "$REPORT_FILE"
fi

echo ""

########################################
# SITEMAP UPDATES
########################################

if [ -f "$SITEMAP_FILE" ] && [ "$CHILD_COUNT" -gt 0 ]; then
  echo "🗺️  Updating sitemap..."
  echo "## Sitemap Updates" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  
  for CHILD in "${CREATED_CHILDREN[@]}"; do
    [ "$SITEMAP_COUNT" -ge "$MAX_SITEMAP" ] && break
    [ "$DRY_RUN" = "1" ] && { SITEMAP_COUNT=$((SITEMAP_COUNT + 1)); continue; }
    
    FULL_URL="$DOMAIN/$CHILD"
    
    if ! grep -q "$FULL_URL" "$SITEMAP_FILE"; then
      TMP_SITEMAP="/tmp/sg-sitemap-${STAMP}.xml"
      
      awk -v url="$FULL_URL" -v d="$TODAY" '
        /<\/urlset>/ && !done {
          print "  <url>"
          print "    <loc>" url "</loc>"
          print "    <lastmod>" d "</lastmod>"
          print "    <changefreq>weekly</changefreq>"
          print "    <priority>0.7</priority>"
          print "  </url>"
          done=1
        }
        { print }
      ' "$SITEMAP_FILE" > "$TMP_SITEMAP"
      
      mv "$TMP_SITEMAP" "$SITEMAP_FILE"
      SITEMAP_COUNT=$((SITEMAP_COUNT + 1))
      SITEMAP_ADDS+=("$CHILD")
      echo "- Added: $CHILD" >> "$REPORT_FILE"
    fi
  done
  
  echo "" >> "$REPORT_FILE"
fi

echo ""

########################################
# INDEX UPDATES
########################################

if [ -f "$INDEX_FILE" ] && [ "$CHILD_COUNT" -gt 0 ]; then
  echo "🏠 Updating index..."
  echo "## Index Updates" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  
  if [ "$DRY_RUN" != "1" ]; then
    if ! grep -q "swarm-fresh-links" "$INDEX_FILE"; then
      sed -i '/<\/body>/i\
<section class="swarm-fresh-links" style="max-width:1100px;margin:60px auto;padding:24px;">\
<h2>Fresh Help Paths</h2>\
<ul id="swarm-links-list"></ul>\
</section>' "$INDEX_FILE"
    fi
  fi
  
  for CHILD in "${CREATED_CHILDREN[@]}"; do
    [ "$INDEX_COUNT" -ge "$MAX_INDEX" ] && break
    
    if [ "$DRY_RUN" = "1" ]; then
      INDEX_COUNT=$((INDEX_COUNT + 1))
    elif ! grep -q "/$CHILD" "$INDEX_FILE"; then
      sed -i "/<ul id=\"swarm-links-list\">/a <li><a href=\"/$CHILD\">$CHILD</a></li>" "$INDEX_FILE"
      INDEX_COUNT=$((INDEX_COUNT + 1))
      INDEX_ADDS+=("$CHILD")
      echo "- Added: $CHILD" >> "$REPORT_FILE"
    fi
  done
  
  echo "" >> "$REPORT_FILE"
fi

echo ""

########################################
# FINAL REPORT
########################################

echo "📝 Generating report..."

cat >> "$REPORT_FILE" << EOF
## Summary

| Metric | Count | Cap |
|--------|-------|-----|
| Pages Upgraded | $UPGRADE_COUNT | $MAX_UPGRADES |
| Children Created | $CHILD_COUNT | $MAX_CHILDREN |
| Sitemap Adds | $SITEMAP_COUNT | $MAX_SITEMAP |
| Index Adds | $INDEX_COUNT | $MAX_INDEX |

---

EOF

if [ "$UPGRADE_COUNT" -gt 0 ]; then
  echo "### Upgraded Pages ($UPGRADE_COUNT)" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  for page in "${UPGRADED_PAGES[@]}"; do
    echo "- $page" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
fi

if [ "$CHILD_COUNT" -gt 0 ]; then
  echo "### Created Children ($CHILD_COUNT)" >> "$REPORT_FILE"
  echo "" >> "$REPORT_FILE"
  for page in "${CREATED_CHILDREN[@]}"; do
    echo "- $page" >> "$REPORT_FILE"
  done
  echo "" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF
---

## Recommendations

### Human Review Required

1. **Child pages** - Add unique, helpful content to replace placeholders
2. **Upgraded sections** - Verify tone matches brand voice
3. **Internal links** - Check relevance and flow
4. **Cost blocks** - Ensure accuracy for money-intent pages

### Next Intelligence Moves

- Review top queries for emerging themes
- Add calculators for high-scoring cost queries  
- Expand comparison pages for position 5-15 with low CTR
- Monitor upgraded pages for engagement lift

### To Revert Changes

All modified files backed up with \`.bak.$STAMP\` extension.

\`\`\`bash
# Restore all backups
find "$PUBLIC_DIR" -name "*.bak.$STAMP" -exec bash -c 'mv "\$0" "\${0%.bak.$STAMP}"' {} \;

# Remove created children
$(for f in "${CREATED_CHILDREN[@]}"; do echo "rm $f"; done)
\`\`\`

---

**Generated:** $(date)  
**Mode:** $([ "$DRY_RUN" = "1" ] && echo "DRY RUN" || echo "LIVE")  
**Log:** $RUN_LOG

EOF

########################################
# OUTPUT SUMMARY
########################################

echo ""
echo "================================"
echo "✨ Swarm v9 Unified Complete"
echo "================================"
echo "Upgraded:   $UPGRADE_COUNT / $MAX_UPGRADES"
echo "Children:   $CHILD_COUNT / $MAX_CHILDREN"
echo "Sitemap:    $SITEMAP_COUNT / $MAX_SITEMAP"
echo "Index:      $INDEX_COUNT / $MAX_INDEX"
echo "================================"
echo ""
echo "📄 Report: $REPORT_FILE"
echo ""

########################################
# GIT HANDLING
########################################

if [ "$DRY_RUN" = "1" ]; then
  echo "🔒 Dry run complete - no git operations"
  echo "   Run without DRY_RUN=1 to apply changes"
elif [ "$AUTO_COMMIT" = "1" ]; then
  echo "🔄 Auto-committing..."
  git add .
  git commit -m "🧠 Swarm v9: $UPGRADE_COUNT upgrades, $CHILD_COUNT children ($STAMP)" || {
    echo "⚠️  Git commit failed (possibly no changes)"
  }
else
  echo "⏸️  Changes ready for review"
  echo ""
  echo "   Review files, then commit:"
  echo "   git add . && git commit -m 'swarm v9: intelligent assistance'"
  echo ""
  echo "   Or auto-commit next time:"
  echo "   AUTO_COMMIT=1 ./swarm-v9-unified.sh"
fi

echo ""
echo "✨ Done. Review the report for next steps."
