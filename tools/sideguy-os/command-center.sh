#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "==============================="
echo " SideGuy Command Center"
echo "==============================="
echo ""
echo "  1  Run Alive Discovery Engine"
echo "  2  Generate Million Page Matrix"
echo "  3  Build Pages"
echo "  4  Authority Upgrades"
echo "  5  Gravity Ranking Scan"
echo "  6  Nervous System (freshness + clusters)"
echo "  7  Run Everything"
echo ""
read -rp "Select option: " OPTION

case "$OPTION" in
  1) bash tools/sideguy-os/run-alive.sh ;;
  2) bash tools/sideguy-os/run-million.sh ;;
  3) bash tools/sideguy-os/build-pages.sh ;;
  4) bash tools/sideguy-os/run-authority.sh ;;
  5) bash tools/sideguy-os/gravity-engine.sh ;;
  6) bash tools/nervous/nervous-system.sh ;;
  7)
    bash tools/sideguy-os/run-alive.sh
    bash tools/sideguy-os/run-million.sh
    bash tools/sideguy-os/run-authority.sh
    bash tools/nervous/nervous-system.sh
    bash tools/sideguy-os/gravity-engine.sh
    ;;
  *) echo "Invalid option: $OPTION" ;;
esac
