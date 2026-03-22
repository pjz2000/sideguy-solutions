#!/usr/bin/env bash

echo ""
echo "=================================================="
echo "SIDEGUY GOD STACK v2"
echo "Signals + Pages + Economy + UI + Galaxy"
echo "=================================================="
echo ""

cd /workspaces/sideguy-solutions || exit 1

########################################
# CORE STRUCTURE
########################################

mkdir -p tools/master logs docs seo-reserve public

########################################
# ROBOT ECONOMY ENGINE
########################################

mkdir -p seo-reserve/robot-economy docs/robot-economy/logs

if [ ! -f seo-reserve/robot-economy/robot-economy-core.md ]; then
cat > seo-reserve/robot-economy/robot-economy-core.md <<'EOF'
/robot-economy/
/future-robot-economy/
/robot-economics/
/robot-labor-market/
/automation-economics/
EOF
echo "[✓] seo-reserve/robot-economy/robot-economy-core.md"
else
echo "[SKIP] seo-reserve/robot-economy/robot-economy-core.md (exists)"
fi

echo "Robot economy ready. $(date '+%Y-%m-%d %H:%M:%S')" >> docs/robot-economy/logs/robot.log

########################################
# FUTURE TECH DEMAND ENGINE
########################################

mkdir -p seo-reserve/future-tech docs/future-tech/logs

if [ ! -f seo-reserve/future-tech/ai-agents.md ]; then
cat > seo-reserve/future-tech/ai-agents.md <<'EOF'
/ai-agents/
/ai-agent-automation/
/ai-agent-workflows/
/ai-agent-economy/
EOF
echo "[✓] seo-reserve/future-tech/ai-agents.md"
else
echo "[SKIP] seo-reserve/future-tech/ai-agents.md (exists)"
fi

echo "Future tech ready. $(date '+%Y-%m-%d %H:%M:%S')" >> docs/future-tech/logs/future.log

########################################
# SIGNAL SCANNER SYSTEM
########################################

mkdir -p docs/signals/inbox docs/signals/ideas docs/signals/research docs/signals/logs

if [ ! -f docs/signals/inbox/README.md ]; then
echo "Signal system ready" > docs/signals/inbox/README.md
echo "[✓] docs/signals/inbox/README.md"
else
echo "[SKIP] docs/signals/inbox/README.md (exists)"
fi

########################################
# PREMIUM UI ENGINE
# IMPORTANT: upgrade-ui.sh modifies ALL production HTML pages.
# It forces a dark body theme that conflicts with existing light
# ocean CSS. DO NOT run without reviewing tools/ui/upgrade-ui.sh
# and passing --confirm explicitly.
########################################

mkdir -p tools/ui
bash tools/sideguy-godstack-v2.sh --write-ui-only 2>/dev/null || true

# Write upgrade-ui.sh (safe to generate; dangerous to execute)
if [ ! -f tools/ui/upgrade-ui.sh ]; then
  bash "$(dirname "$0")/sideguy-godstack-v2.sh" --write-ui-only 2>/dev/null || true
fi

########################################
# MASTER RUNNER
########################################

if [ ! -f run-sideguy.sh ]; then
cat > run-sideguy.sh <<'EOF'
#!/usr/bin/env bash

echo ""
echo "====================================="
echo "SIDEGUY COMMAND CENTER"
echo "====================================="
echo ""
echo "Available:"
echo "  bash tools/ui/upgrade-ui.sh --confirm   (UI theme — see warning inside)"
echo ""
echo "System ready."
echo ""
EOF
chmod +x run-sideguy.sh
echo "[✓] run-sideguy.sh"
else
echo "[SKIP] run-sideguy.sh (exists)"
fi

########################################
# COMPLETE
########################################

echo ""
echo "=========================================="
echo "SIDEGUY GOD STACK v2 DEPLOYED"
echo "=========================================="
echo ""
echo "NOTE: UI upgrade NOT run automatically."
echo "Review tools/ui/upgrade-ui.sh before executing."
echo ""
