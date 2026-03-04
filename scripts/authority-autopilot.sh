#!/usr/bin/env bash
# ============================================================
# SIDEGUY — AUTHORITY AUTOPILOT shell wrapper
# Env knobs:
#   AUTH_MIN_PAGES=12   minimum cluster size to mint a hub
#   AUTH_TOP_N=60       max links per hub page
#   AUTH_MAX_HUBS=24    max hubs per run
#   AUTH_MODE=smart     smart | aggressive
#   AUTH_DRY_RUN=0      1 = preview only, no files written
# ============================================================

set -euo pipefail

cd "$(dirname "$0")/.."

AUTH_MIN_PAGES="${AUTH_MIN_PAGES:-12}"
AUTH_TOP_N="${AUTH_TOP_N:-60}"
AUTH_MAX_HUBS="${AUTH_MAX_HUBS:-24}"
AUTH_MODE="${AUTH_MODE:-smart}"
AUTH_DRY_RUN="${AUTH_DRY_RUN:-0}"

export AUTH_MIN_PAGES AUTH_TOP_N AUTH_MAX_HUBS AUTH_MODE AUTH_DRY_RUN

echo "=== Authority Autopilot ==="
echo "  MIN_PAGES : $AUTH_MIN_PAGES"
echo "  TOP_N     : $AUTH_TOP_N"
echo "  MAX_HUBS  : $AUTH_MAX_HUBS"
echo "  MODE      : $AUTH_MODE"
echo "  DRY_RUN   : $AUTH_DRY_RUN"
echo ""

python3 scripts/authority-autopilot.py

echo ""
echo "=== Authority Autopilot complete ==="
