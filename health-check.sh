#!/usr/bin/env bash

# =========================================
# SIDEGUY — REPO HEALTH CHECK
# =========================================
# Run: ./health-check.sh
# No writes. Read-only audit.
# =========================================

PASS=0
WARN=0
FAIL=0

ok()   { echo "  ✅ $1"; ((PASS++)); }
warn() { echo "  ⚠️  $1"; ((WARN++)); }
fail() { echo "  ❌ $1"; ((FAIL++)); }

echo ""
echo "🔍 SideGuy Health Check — $(date '+%Y-%m-%d %H:%M')"
echo "=================================================="

# ------------------------------------------
echo ""
echo "📄 Pages"
# ------------------------------------------

HTML_COUNT=$(find . -maxdepth 1 -name "*.html" ! -name "*.tmp" ! -name "*.bak" | wc -l | tr -d ' ')
ok "$HTML_COUNT HTML pages at root"

# Check for any .html files newer than sitemap.xml
if [ -f sitemap.xml ]; then
  STALE=$(find . -maxdepth 1 -name "*.html" -newer sitemap.xml | wc -l | tr -d ' ')
  if [ "$STALE" -eq 0 ]; then
    ok "sitemap.xml is up to date"
  else
    warn "$STALE page(s) newer than sitemap.xml — consider regenerating"
  fi
else
  fail "sitemap.xml not found"
fi

# ------------------------------------------
echo ""
echo "🗺️  SEO Infrastructure"
# ------------------------------------------

if [ -f robots.txt ]; then
  ok "robots.txt present"
  if grep -q "sitemap" robots.txt; then
    ok "robots.txt references sitemap"
  else
    fail "robots.txt missing Sitemap: directive"
  fi
else
  fail "robots.txt missing"
fi

if [ -f CNAME ]; then
  DOMAIN=$(cat CNAME | tr -d '[:space:]')
  ok "CNAME present ($DOMAIN)"
else
  warn "CNAME not found"
fi

if [ -f sitemap-index.xml ]; then
  ok "sitemap-index.xml present"
else
  warn "sitemap-index.xml not found"
fi

# Duplicate sitemap index
if [ -f sitemap_index.xml ] && [ -f sitemap-index.xml ]; then
  warn "Both sitemap-index.xml and sitemap_index.xml exist — possible duplicate"
fi

# ------------------------------------------
echo ""
echo "🧹 Git Cleanliness"
# ------------------------------------------

DIRTY=$(git status --short | wc -l | tr -d ' ')
if [ "$DIRTY" -eq 0 ]; then
  ok "Working tree clean (no uncommitted changes)"
else
  warn "$DIRTY uncommitted change(s)"
fi

TRACKED_TMP=$(git ls-files "*.tmp" | wc -l | tr -d ' ')
if [ "$TRACKED_TMP" -eq 0 ]; then
  ok "No .tmp files tracked in git"
else
  warn "$TRACKED_TMP .tmp file(s) tracked in git (should be gitignored)"
fi

TRACKED_LOGS=$(git ls-files "*.log" | wc -l | tr -d ' ')
if [ "$TRACKED_LOGS" -eq 0 ]; then
  ok "No .log files tracked in git"
else
  warn "$TRACKED_LOGS .log file(s) tracked in git (.gitignore covers new ones, but old ones are committed)"
fi

# ------------------------------------------
echo ""
echo "🔒 Lock / State Files"
# ------------------------------------------

if [ -f SYSTEM_LOCK.md ]; then
  STATUS=$(head -3 SYSTEM_LOCK.md | grep "SYSTEM STATE" | sed 's/SYSTEM STATE: //')
  ok "SYSTEM_LOCK.md present — ${STATUS:-active}"
else
  warn "SYSTEM_LOCK.md not found"
fi

if [ -f STATIC_LOCK.txt ]; then
  ok "STATIC_LOCK.txt present"
fi

if [ -f SIDEGUY_CORE.md ]; then
  ok "SIDEGUY_CORE.md present"
else
  fail "SIDEGUY_CORE.md missing — core philosophy file"
fi

# ------------------------------------------
echo ""
echo "📦 Key Support Files"
# ------------------------------------------

for f in _template.html sideguy-include.js; do
  if [ -f "$f" ]; then
    ok "$f present"
  else
    warn "$f not found"
  fi
done

# ------------------------------------------
echo ""
echo "=================================================="
echo "  ✅ $PASS passed   ⚠️  $WARN warnings   ❌ $FAIL failures"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo "  ⛔  Action needed — review failures above."
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo "  👀 Repo healthy with minor notes. Review warnings."
  exit 0
else
  echo "  🟢 All clear."
  exit 0
fi
