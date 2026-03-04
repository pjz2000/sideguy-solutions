#!/usr/bin/env bash
# SIDEGUY TRAFFIC GRAVITY ENGINE (idempotent, no-hands)
# Goal: make the site "self-linking" via gravity scoring + targeted internal link wiring
# Usage: bash scripts/traffic-gravity-engine.sh
# Knobs: LIMIT=300 PER_PAGE=8 DRY_RUN=1 bash scripts/traffic-gravity-engine.sh

set -e

echo "=== SIDEGUY TRAFFIC GRAVITY ENGINE ==="
echo "Repo: $(pwd)"
date

PHONE_SMS="sms:+17735441231"
PHONE_TEL="tel:+17735441231"
export LIMIT="${LIMIT:-300}"
export PER_PAGE="${PER_PAGE:-8}"
export DRY_RUN="${DRY_RUN:-0}"
export PHONE_SMS
export PHONE_TEL

# ── 0) Phone enforcement ─────────────────────────────────────────────────────
echo ""
echo "[0/6] Phone sanity (expected: ${PHONE_SMS})"
if [ -f "scripts/enforce-phone.py" ]; then
  python3 scripts/enforce-phone.py
else
  echo "  scripts/enforce-phone.py not found (ok). Skipping."
fi

# ── 1) Sitemap (crawl map) ────────────────────────────────────────────────────
echo ""
echo "[1/6] Regenerate sitemap (source of truth crawl map)"
if [ -f "scripts/generate-sitemap.py" ]; then
  python3 scripts/generate-sitemap.py
elif [ -f "scripts/generate_sitemap.py" ]; then
  python3 scripts/generate_sitemap.py
else
  echo "  No sitemap generator found in scripts/. Skipping."
fi

# ── 2) Site inventory ─────────────────────────────────────────────────────────
echo ""
echo "[2/6] Build inventory (page lists / buckets / orphans)"
if [ -f "scripts/site-inventory.py" ]; then
  python3 scripts/site-inventory.py
else
  echo "  scripts/site-inventory.py not found (ok). Skipping."
fi

# ── 3) Traffic Gravity scoring ────────────────────────────────────────────────
echo ""
echo "[3/6] Run Traffic Gravity Engine"
if [ -f "scripts/traffic-gravity.py" ]; then
  python3 scripts/traffic-gravity.py
else
  echo "  scripts/traffic-gravity.py not found."
fi

# ── 4) Wire gravity links into content pages ──────────────────────────────────
echo ""
echo "[4/6] Wire gravity links into pages (idempotent)"
if [ -f "scripts/wire-traffic-gravity.py" ]; then
  python3 scripts/wire-traffic-gravity.py
else
  echo "  scripts/wire-traffic-gravity.py not found."
fi

# ── 5) Sitemap refresh post-wiring ───────────────────────────────────────────
echo ""
echo "[5/6] Sitemap refresh after wiring"
if [ -f "scripts/generate-sitemap.py" ]; then
  python3 scripts/generate-sitemap.py
elif [ -f "scripts/generate_sitemap.py" ]; then
  python3 scripts/generate_sitemap.py
else
  echo "  No sitemap generator found (ok)."
fi

# ── 6) Smoke checks ───────────────────────────────────────────────────────────
echo ""
echo "[6/6] Smoke checks"

echo ""
echo "Phone check (sample 50 files):"
find . -type f -name "*.html" | head -n 50 | \
  xargs -I{} sh -c "grep -q '${PHONE_SMS}' '{}' && echo '  OK {}'" 2>/dev/null | head -n 10

echo ""
echo "Sitemap index:"
if [ -f "sitemap-index.xml" ]; then
  echo "  OK: sitemap-index.xml present"
  grep -o "sitemaps/sitemap-[0-9]*\.xml" sitemap-index.xml 2>/dev/null | wc -l | xargs -I{} echo "  Chunks: {}"
else
  echo "  NOTE: sitemap-index.xml not found."
fi

echo ""
echo "=== DONE: Traffic Gravity Engine pass complete ==="
echo "Dry-run mode: DRY_RUN=1 LIMIT=500 PER_PAGE=10 bash scripts/traffic-gravity-engine.sh"
