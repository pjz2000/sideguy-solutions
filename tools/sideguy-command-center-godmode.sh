#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "=================================================="
echo "SIDEGUY COMMAND CENTER GOD MODE"
echo "Signals → Pages → Authority → Deals"
echo "=================================================="
echo ""

DATE=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p docs/command-center logs

REPORT="docs/command-center/command-center.md"

{
  echo "# SideGuy Command Center"
  echo "Generated: $DATE"
  echo ""

  ########################################
  # 1. SEARCH SIGNALS (YOUR DATA)
  ########################################

  echo "## Live Search Signals"
  echo ""
  cat <<'EOF'
merchant services san diego (2)
square payment vs stripe (2)
make vs zapier (2)
automation mktg (2)
stripe vs square vs paypal (2)
ai lead generation real estate san diego (1)
paypal business setup issues (1)
EOF
  echo ""

  ########################################
  # 2. OPPORTUNITY ENGINE (ACTIONABLE)
  ########################################

  echo "## Immediate Opportunities"
  echo ""
  echo "BUILD:"
  echo "- merchant services san diego"
  echo "- stripe vs square vs paypal"
  echo "- ai lead generation real estate san diego"
  echo ""
  echo "EXPAND:"
  echo "- square vs stripe"
  echo "- make vs zapier"
  echo ""

  ########################################
  # 3. RUN YOUR ENGINES (SAFE)
  ########################################

  echo "## Systems Run"
  echo ""

} > "$REPORT"

run_if_exists () {
  if [ -f "$1" ]; then
    if bash "$1" >/dev/null 2>&1; then
      echo "[✓] $1" >> "$REPORT"
    else
      echo "[FAIL] $1 — exited non-zero" >> "$REPORT"
    fi
  else
    echo "[SKIP] $1 — not found" >> "$REPORT"
  fi
}

run_if_exists tools/authority-gravity/run-authority-gravity.sh
run_if_exists tools/priority/run-priority.sh
run_if_exists tools/autonomous/run-autonomous.sh
run_if_exists tools/deal-os/run-deal-os.sh

{
  echo ""

  ########################################
  # 4. MONEY FOCUS (CRITICAL)
  ########################################

  echo "## Money Focus"
  echo ""
  echo "Top Targets:"
  echo "- payments (stripe, square, merchant services)"
  echo "- local services (hvac, plumbing)"
  echo "- real estate AI leads"
  echo ""

  ########################################
  # 5. DAILY EXECUTION PLAN
  ########################################

  echo "## Daily Actions"
  echo ""
  echo "1. Build 2 pages from BUILD list"
  echo "2. Upgrade 2 pages from EXPAND list"
  echo "3. Add 5 internal links"
  echo "4. Respond to any texts (priority)"
  echo ""

} >> "$REPORT"

########################################
# 6. REAL-TIME OUTPUT
########################################

echo ""
echo "=================================================="
echo "WHAT YOU SHOULD DO RIGHT NOW"
echo "=================================================="
echo ""
echo "1. BUILD THIS FIRST:"
echo "   merchant services san diego"
echo ""
echo "2. THEN:"
echo "   stripe vs square vs paypal"
echo ""
echo "3. THEN:"
echo "   ai lead generation real estate san diego"
echo ""
echo "4. IGNORE EVERYTHING ELSE"
echo ""
echo "Report saved: $REPORT"
echo ""
