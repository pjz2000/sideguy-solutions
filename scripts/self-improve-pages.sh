#!/usr/bin/env bash
# SIDEGUY SELF-IMPROVING PAGES ENGINE
# Non-destructive marker-based page upgrades: meta, canonical, H1, FAQ schema, breadcrumbs, CTA
#
# Env knobs:
#   IMPROVE_LIMIT=120   pages per run (default 120)

set -euo pipefail
cd "$(dirname "$0")/.."

IMPROVE_LIMIT="${IMPROVE_LIMIT:-120}"
export IMPROVE_LIMIT

echo "=== SIDEGUY SELF-IMPROVING PAGES ==="
echo "    IMPROVE_LIMIT=$IMPROVE_LIMIT"
echo ""

python3 scripts/self-improve-pages.py

echo ""
echo "Report  : reports/self-improve-report.json"
echo "Backups : reports/self-improve-backups/"
