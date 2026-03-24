#!/usr/bin/env bash

########################################
# SIDEGUY AUTOPILOT ORCHESTRATOR v1
# Master controller for query-driven automation
# Coordinates:
# - Hyper updates (quick answer blocks)
# - Productize (interactive tools)
# - Auto-adapt (winning pattern replication)
# - Sitemap regeneration
# - Summary reports
########################################

set -e

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

DATE="$(date +"%Y-%m-%d-%H%M%S")"
HUMAN_DATE="$(date +"%Y-%m-%d %H:%M:%S")"

DOMAIN="https://www.sideguysolutions.com"
INPUT_CSV="docs/gsc/query-pages.csv"

DOCS_DIR="docs"
AUTO_DIR="$DOCS_DIR/autopilot"
RUN_DIR="$AUTO_DIR/runs/$DATE"

LOG_FILE="$RUN_DIR/autopilot.log"
SUMMARY_FILE="$RUN_DIR/summary.md"
OUTCOMES_FILE="$RUN_DIR/outcomes.txt"

# Safety: require explicit override
DRY_RUN="${DRY_RUN:-true}"

# Component toggles (can disable individual steps)
RUN_HYPER="${RUN_HYPER:-true}"
RUN_PRODUCTIZE="${RUN_PRODUCTIZE:-true}"
RUN_ADAPT="${RUN_ADAPT:-false}"  # Most aggressive, disabled by default
RUN_SITEMAP="${RUN_SITEMAP:-false}"  # Only if changes were made

mkdir -p "$DOCS_DIR" "$AUTO_DIR/runs" "$RUN_DIR" "docs/gsc"

########################################
# BANNER
########################################

echo ""
echo "======================================="
echo "🤖 SIDEGUY AUTOPILOT ORCHESTRATOR v1"
echo "======================================="
echo ""
echo "Timestamp: $HUMAN_DATE"
echo "Run ID: $DATE"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
  echo "⚠️  DRY RUN MODE — No files will be modified"
  echo "   Set DRY_RUN=false to run live"
  echo ""
fi

########################################
# PREFLIGHT CHECKS
########################################

log() {
  echo "$1" | tee -a "$LOG_FILE"
}

log "🔍 Preflight checks..."

if [ ! -f "$INPUT_CSV" ]; then
  log "❌ ERROR: Missing input CSV: $INPUT_CSV"
  log ""
  log "Expected format:"
  log "  page,query,clicks,impressions,ctr,position"
  log ""
  log "Get this from Google Search Console:"
  log "  Performance > Pages > Export > CSV"
  exit 1
fi

log "✓ Input CSV found: $INPUT_CSV"

# Check required scripts exist
REQUIRED_SCRIPTS=(
  "_hyper_update_engine.sh"
  "hyper-productize.sh"
  "hyper-auto-adapt.sh"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
  if [ ! -f "$script" ]; then
    log "⚠️  Warning: $script not found, skipping that step"
  else
    log "✓ Found: $script"
  fi
done

log ""

########################################
# EXECUTION PHASES
########################################

CHANGES_MADE=false

log "---------------------------------------"
log "Phase 1: Hyper Updates"
log "---------------------------------------"
log ""

if [ "$RUN_HYPER" = true ] && [ -f "_hyper_update_engine.sh" ]; then
  log "Running hyper update engine..."
  
  if DRY_RUN="$DRY_RUN" bash _hyper_update_engine.sh >> "$LOG_FILE" 2>&1; then
    log "✓ Hyper updates complete"
    [ "$DRY_RUN" = false ] && CHANGES_MADE=true
  else
    log "⚠️  Hyper updates encountered errors (check log)"
  fi
else
  log "⊘ Hyper updates disabled or script missing"
fi

log ""

log "---------------------------------------"
log "Phase 2: Productize Tools"
log "---------------------------------------"
log ""

if [ "$RUN_PRODUCTIZE" = true ] && [ -f "hyper-productize.sh" ]; then
  log "Running productize engine..."
  
  if DRY_RUN="$DRY_RUN" bash hyper-productize.sh >> "$LOG_FILE" 2>&1; then
    log "✓ Productize complete"
    [ "$DRY_RUN" = false ] && CHANGES_MADE=true
  else
    log "⚠️  Productize encountered errors (check log)"
  fi
else
  log "⊘ Productize disabled or script missing"
fi

log ""

log "---------------------------------------"
log "Phase 3: Auto-Adapt Patterns"
log "---------------------------------------"
log ""

if [ "$RUN_ADAPT" = true ] && [ -f "hyper-auto-adapt.sh" ]; then
  log "⚠️  Auto-adapt is AGGRESSIVE — applying winning patterns globally"
  log "Running auto-adapt engine..."
  
  if DRY_RUN="$DRY_RUN" bash hyper-auto-adapt.sh >> "$LOG_FILE" 2>&1; then
    log "✓ Auto-adapt complete"
    [ "$DRY_RUN" = false ] && CHANGES_MADE=true
  else
    log "⚠️  Auto-adapt encountered errors (check log)"
  fi
else
  log "⊘ Auto-adapt disabled (set RUN_ADAPT=true to enable)"
fi

log ""

log "---------------------------------------"
log "Phase 4: Sitemap Update"
log "---------------------------------------"
log ""

if [ "$RUN_SITEMAP" = true ] && [ "$CHANGES_MADE" = true ] && [ -f "generate-sitemap-failsafe.sh" ]; then
  log "Changes were made — regenerating sitemap..."
  
  if bash generate-sitemap-failsafe.sh >> "$LOG_FILE" 2>&1; then
    log "✓ Sitemap regenerated"
  else
    log "⚠️  Sitemap generation encountered errors (check log)"
  fi
else
  log "⊘ Sitemap update skipped (no changes or disabled)"
fi

log ""

########################################
# SUMMARY REPORT
########################################

log "---------------------------------------"
log "Generating summary report..."
log "---------------------------------------"
log ""

cat > "$SUMMARY_FILE" <<EOF
# Autopilot Run Summary

**Run ID:** $DATE  
**Timestamp:** $HUMAN_DATE  
**Mode:** $([ "$DRY_RUN" = "true" ] && echo "DRY RUN (preview only)" || echo "LIVE (changes applied)")

## Configuration

- **Hyper Updates:** $([ "$RUN_HYPER" = true ] && echo "✓ Enabled" || echo "⊘ Disabled")
- **Productize Tools:** $([ "$RUN_PRODUCTIZE" = true ] && echo "✓ Enabled" || echo "⊘ Disabled")
- **Auto-Adapt:** $([ "$RUN_ADAPT" = true ] && echo "✓ Enabled" || echo "⊘ Disabled")
- **Sitemap Update:** $([ "$RUN_SITEMAP" = true ] && echo "✓ Enabled" || echo "⊘ Disabled")

## Input Data

- **Source:** \`$INPUT_CSV\`
- **Rows:** $(tail -n +2 "$INPUT_CSV" | wc -l)

## Execution Results

### Hyper Updates
$([ -f "docs/hyper-update/hyper-report.md" ] && cat "docs/hyper-update/hyper-report.md" || echo "No report generated")

### Productize Tools
$([ -f "docs/hyper-productize/productize-report.md" ] && cat "docs/hyper-productize/productize-report.md" || echo "No report generated")

### Auto-Adapt
$([ -f "docs/auto-adapt/adapt-report.md" ] && cat "docs/auto-adapt/adapt-report.md" || echo "No report generated")

## Outcomes

$([ -f "$OUTCOMES_FILE" ] && cat "$OUTCOMES_FILE" || echo "No outcomes recorded")

## Next Steps

$(if [ "$DRY_RUN" = "true" ]; then
  cat <<NEXTSTEPS
1. **Review this summary** and component reports
2. **Validate approach** with sample pages
3. **Run live:** \`DRY_RUN=false ./autopilot-orchestrator.sh\`
4. **Monitor GSC** for 2-4 weeks to measure impact
NEXTSTEPS
else
  cat <<NEXTSTEPS
1. **Validate changes** on live pages
2. **Monitor GSC** for engagement, clicks, CTR changes
3. **Document learnings** in signals/ or observations/
4. **Adjust thresholds** based on performance
NEXTSTEPS
fi)

---

**Full log:** [\`$LOG_FILE\`]($LOG_FILE)

EOF

########################################
# OUTCOMES TRACKING
########################################

cat > "$OUTCOMES_FILE" <<EOF
Autopilot Run: $DATE

Phase 1: Hyper Updates
  - Status: $([ "$RUN_HYPER" = true ] && echo "Executed" || echo "Skipped")
  - Report: docs/hyper-update/hyper-report.md

Phase 2: Productize Tools
  - Status: $([ "$RUN_PRODUCTIZE" = true ] && echo "Executed" || echo "Skipped")
  - Report: docs/hyper-productize/productize-report.md

Phase 3: Auto-Adapt
  - Status: $([ "$RUN_ADAPT" = true ] && echo "Executed" || echo "Skipped")
  - Report: docs/auto-adapt/adapt-report.md

Phase 4: Sitemap Update
  - Status: $([ "$RUN_SITEMAP" = true ] && [ "$CHANGES_MADE" = true ] && echo "Executed" || echo "Skipped")

Mode: $([ "$DRY_RUN" = "true" ] && echo "DRY RUN" || echo "LIVE")
Changes Applied: $([ "$CHANGES_MADE" = true ] && echo "Yes" || echo "No")
EOF

########################################
# FINAL OUTPUT
########################################

log ""
log "======================================="
log "✅ AUTOPILOT COMPLETE"
log "======================================="
log ""
log "📋 Summary: $SUMMARY_FILE"
log "📜 Full log: $LOG_FILE"
log "📊 Outcomes: $OUTCOMES_FILE"
log ""

if [ "$DRY_RUN" = "true" ]; then
  log "💡 This was a DRY RUN. No files were modified."
  log "   To run live: DRY_RUN=false ./autopilot-orchestrator.sh"
  log ""
fi

if [ "$CHANGES_MADE" = true ]; then
  log "⚠️  Changes were made to HTML files."
  log "   Review changes, test locally, then commit."
  log ""
fi

log "Human decision points:"
log "  - Review component reports before going live"
log "  - Validate sample pages match SideGuy philosophy"
log "  - Monitor GSC for unintended ranking impacts"
log "  - Document any new patterns in signals/"
log ""
