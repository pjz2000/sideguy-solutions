#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "SIDEGUY MILLION ENGINE — Phase 3: Authority Upgrade"
echo ""

bash tools/million/find-authority-candidates.sh
bash tools/million/build-authority-blocks.sh
bash tools/million/build-faq-schema.sh
bash tools/million/upgrade-authority-pages.sh
bash tools/million/authority-report.sh

echo ""
echo "Phase 3 complete."
echo ""
