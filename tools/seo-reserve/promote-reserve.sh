#!/usr/bin/env bash
# tools/seo-reserve/promote-reserve.sh
# Wrapper around promote-reserve.py

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "========================================"
echo "SideGuy :: Promote Reserve Pages"
echo "========================================"
echo ""

# Pass all args through to Python script
# Examples:
#   bash tools/seo-reserve/promote-reserve.sh                    # dry-run all
#   bash tools/seo-reserve/promote-reserve.sh --deploy           # deploy all
#   bash tools/seo-reserve/promote-reserve.sh --deploy --limit 50
#   bash tools/seo-reserve/promote-reserve.sh --deploy --dir prediction-markets

python3 tools/seo-reserve/promote-reserve.py "$@"
