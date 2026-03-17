#!/usr/bin/env bash
# tools/sideguy-os.sh
# SIDEGUY OS — FULL SYSTEM RUN
# Content → Clusters → Traffic → Deals → Authority
#
# Usage:
#   bash tools/sideguy-os.sh           # run all enabled steps
#   bash tools/sideguy-os.sh --dry-run # show what would run, no execution

set -uo pipefail

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

DATE=$(date +"%Y-%m-%d-%H-%M")
LOG_DIR="logs/os"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/run-${DATE}.log"

echo "=================================================="
echo "  SIDEGUY OS — FULL SYSTEM RUN"
echo "  Content → Clusters → Traffic → Deals → Authority"
echo "  $(date)"
echo "  $($DRY_RUN && echo 'MODE: DRY RUN' || echo 'MODE: LIVE')"
echo "=================================================="
echo ""

#################################################
# HELPERS
#################################################

PASS=0; SKIP=0; FAIL=0

step() {
  # step <number> <label> <script-path>
  local num=$1 label=$2 script=$3
  printf "  [%s] %s\n" "$num" "$label"

  if [ ! -f "$script" ]; then
    printf "      SKIP — %s not found\n" "$script"
    SKIP=$((SKIP + 1))
    echo "${DATE} SKIP  $script" >> "$LOG_FILE"
    return 0
  fi

  if $DRY_RUN; then
    printf "      DRY  — would run: %s\n" "$script"
    return 0
  fi

  if bash "$script" >> "$LOG_FILE" 2>&1; then
    printf "      OK\n"
    PASS=$((PASS + 1))
    echo "${DATE} PASS  $script" >> "$LOG_FILE"
  else
    local code=$?
    printf "      FAIL (exit %s) — check %s\n" "$code" "$LOG_FILE"
    FAIL=$((FAIL + 1))
    echo "${DATE} FAIL  $script (exit ${code})" >> "$LOG_FILE"
  fi
}

#################################################
# 1. SIGNAL + INTELLIGENCE
#################################################

echo "── 1. Signal / Intelligence ──────────────────────"
step "1a" "Trend Radar"          "tools/intelligence/trend-radar.sh"
step "1b" "Opportunity Score"    "tools/intelligence/opportunity-score.sh"
echo ""

#################################################
# 2. CLUSTER SYSTEM (AUTHORITY)
#################################################

echo "── 2. Cluster System ─────────────────────────────"
step "2a" "Build Clusters"       "tools/cluster-engine/build-clusters.sh"
step "2b" "Expand Clusters"      "tools/scale/generate-100k-batch.sh"
echo ""

#################################################
# 3. PAGE GENERATION (CONTROLLED)
#################################################

echo "── 3. Page Generation ────────────────────────────"
step "3 " "Auto Builder"         "tools/autobuilder/autobuilder.sh"
echo ""

#################################################
# 4. SCALE PAGES (HIGH INTENT MONEY PAGES)
#################################################

echo "── 4. Deal Router / Scale Pages ──────────────────"
step "4 " "Deal Router Engine"   "tools/deal-router-engine.sh"
echo ""

#################################################
# 5. INTERNAL LINKING + AUTHORITY
#################################################

echo "── 5. Internal Linking + Gravity ─────────────────"
step "5a" "Link Engine"          "tools/internal-links/run_link_engine.sh"
step "5b" "Gravity Engine"       "tools/gravity/gravity-engine.sh"
echo ""

#################################################
# 6. PRIORITY ENGINE (FOCUS)
#################################################

echo "── 6. Priority Engine ────────────────────────────"
step "6 " "Priority Engine"      "tools/intelligence/priority/priority-engine.sh"
echo ""

#################################################
# 7. PUBLISH (INDEX + SITEMAP)
#################################################

echo "── 7. Publish / Sitemap ──────────────────────────"
step "7 " "Sitemap Generator"    "generate-sitemap-failsafe.sh"
echo ""

#################################################
# 8. DEAL ROUTING SYSTEM
#################################################

echo "── 8. Deal Routing ───────────────────────────────"
step "8a" "High Value Detector"  "tools/escalation/high-value.sh"
step "8b" "Intent → Deal Map"    "tools/fusion/map.sh"
echo ""

#################################################
# 9. MILLION PAGE SYSTEM (MANUAL GATE)
#################################################

echo "── 9. Million Page System ────────────────────────"
echo "   GATED — manual approval required before running"
echo "   When ready:  bash tools/million/build-million-hub-pages.sh"
echo ""

#################################################
# 10. AUTONOMOUS LOOP
#################################################

echo "── 10. Autonomous Builder ────────────────────────"
step "10" "Autonomous Builder"   "tools/autonomous-builder/run_autonomous_builder.sh"
echo ""

#################################################
# SUMMARY
#################################################

echo "=================================================="
echo "  SIDEGUY OS COMPLETE"
echo "  Passed : ${PASS}"
echo "  Skipped: ${SKIP}"
echo "  Failed : ${FAIL}"
echo "  Log    : ${LOG_FILE}"
echo "=================================================="
echo ""
echo "  NEXT ACTIONS:"
echo "  1. Review priority report  → ls -lt logs/intelligence/priority/"
echo "  2. Answer texts            → sms:+17735441231"
echo "  3. Improve top 5 pages     → bash tools/intelligence/priority/priority-engine.sh"
$([[ "$FAIL" -gt 0 ]] && echo "  ⚠  $FAIL step(s) failed — check $LOG_FILE")
echo ""
