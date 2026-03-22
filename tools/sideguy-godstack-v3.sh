#!/usr/bin/env bash

echo ""
echo "===================================================="
echo "SIDEGUY GODSTACK v3"
echo "Civilization + Local + UI + Expansion Engine"
echo "===================================================="
echo ""

cd /workspaces/sideguy-solutions || exit 1

########################################
# CORE STRUCTURE
########################################

mkdir -p tools/master logs docs seo-reserve public

########################################
# TECH TREE SYSTEM
########################################

mkdir -p docs/tech-tree/maps docs/tech-tree/logs seo-reserve/tech-tree

if [ ! -f docs/tech-tree/README.md ]; then
  echo "# SideGuy Technology Tree" > docs/tech-tree/README.md
  echo "[✓] docs/tech-tree/README.md"
else
  echo "[SKIP] docs/tech-tree/README.md (exists)"
fi

echo "Tech tree ready. $(date '+%Y-%m-%d %H:%M:%S')" >> docs/tech-tree/logs/tech-tree.log

########################################
# FOOD SYSTEMS
########################################

mkdir -p docs/food-systems/logs seo-reserve/food-systems

if [ ! -f docs/food-systems/README.md ]; then
  echo "# Automated Food Systems Research" > docs/food-systems/README.md
  echo "[✓] docs/food-systems/README.md"
else
  echo "[SKIP] docs/food-systems/README.md (exists)"
fi

echo "Food systems ready. $(date '+%Y-%m-%d %H:%M:%S')" >> docs/food-systems/logs/food.log

########################################
# CITY × INDUSTRY × SYSTEM ENGINE
########################################

mkdir -p seo-reserve/system-expansion docs/system-expansion/logs

OUTPUT="seo-reserve/system-expansion/pages.md"

if [ ! -f "$OUTPUT" ]; then
  CITIES=(san-diego los-angeles phoenix austin miami chicago new-york)
  INDUSTRIES=(restaurants contractors real-estate small-business ecommerce logistics)
  SYSTEMS=(automation ai-tools payments-systems workflow-automation)

  COUNT=0
  {
    echo "# System Expansion Pages"
    echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    for city in "${CITIES[@]}"; do
      for industry in "${INDUSTRIES[@]}"; do
        for system in "${SYSTEMS[@]}"; do
          echo "/${city}-${industry}-${system}/"
          COUNT=$((COUNT+1))
        done
      done
    done
  } > "$OUTPUT"

  echo "Pages: $COUNT — $(date '+%Y-%m-%d %H:%M:%S')" >> docs/system-expansion/logs/system.log
  echo "[✓] $OUTPUT ($COUNT URLs)"
else
  echo "[SKIP] $OUTPUT (exists)"
fi

########################################
# ROBOT ECONOMY
########################################

mkdir -p seo-reserve/robot-economy docs/robot-economy/logs

if [ ! -f seo-reserve/robot-economy/core.md ]; then
  echo "/robot-economy/" > seo-reserve/robot-economy/core.md
  echo "[✓] seo-reserve/robot-economy/core.md"
else
  echo "[SKIP] seo-reserve/robot-economy/core.md (exists)"
fi

echo "Robot economy ready. $(date '+%Y-%m-%d %H:%M:%S')" >> docs/robot-economy/logs/log.txt

########################################
# FUTURE TECH
########################################

mkdir -p seo-reserve/future-tech docs/future-tech/logs

if [ ! -f seo-reserve/future-tech/core.md ]; then
  echo "/ai-agents/" > seo-reserve/future-tech/core.md
  echo "[✓] seo-reserve/future-tech/core.md"
else
  echo "[SKIP] seo-reserve/future-tech/core.md (exists)"
fi

echo "Future tech ready. $(date '+%Y-%m-%d %H:%M:%S')" >> docs/future-tech/logs/log.txt

########################################
# SIGNAL SYSTEM
########################################

mkdir -p docs/signals/inbox docs/signals/ideas docs/signals/research docs/signals/logs

if [ ! -f docs/signals/inbox/README.md ]; then
  echo "Signal system live" > docs/signals/inbox/README.md
  echo "[✓] docs/signals/inbox/README.md"
else
  echo "[SKIP] docs/signals/inbox/README.md (exists)"
fi

########################################
# PREMIUM UI ENGINE
# WARNING: upgrade-ui.sh injects a dark body theme via sed -i
# across ALL production HTML pages. This conflicts with the
# existing light ocean CSS design system (--bg0, --ink variables).
# DO NOT run without explicit --confirm flag.
########################################

mkdir -p tools/ui
# upgrade-ui.sh is written by the dedicated script below — see
# tools/ui/upgrade-ui.sh (requires --confirm to execute safely)

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
echo "Available tools:"
echo "  bash tools/sideguy-signal-scanner.sh"
echo "  bash tools/sideguy-priority-engine.sh"
echo "  bash tools/sideguy-command-center-godmode.sh"
echo ""
echo "UI upgrade (review warning first):"
echo "  bash tools/ui/upgrade-ui.sh --confirm"
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
# DONE
########################################

echo ""
echo "===================================================="
echo "SIDEGUY GODSTACK v3 DEPLOYED"
echo "===================================================="
echo ""
echo "NOTE: UI upgrade NOT run automatically."
echo "Review tools/ui/upgrade-ui.sh before executing."
echo ""
