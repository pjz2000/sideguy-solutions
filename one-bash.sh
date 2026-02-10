
#!/usr/bin/env bash

# ============================================================

# SIDEGUY ONE-BASH — FORCE GIT ROOT + BUILD + COMMIT + PUSH

# ============================================================



BASE="/workspaces/sideguy-solutions"

DOCS="$BASE/docs"

PAGES="$DOCS/pages"

LOG="$BASE/logs/auto-build-$(date +%Y%m%d-%H%M%S).log"



mkdir -p "$PAGES" "$(dirname "$LOG")"



# --- FORCE GIT ROOT ---

cd "$BASE" || exit 0



echo "SIDEGUY START" | tee "$LOG"

echo "PWD: $(pwd)" | tee -a "$LOG"



# --- BUILD (best effort) ---

[ -f seo-engine.js ] && node seo-engine.js >>"$LOG" 2>&1 || true

[ -f seo-router.js ] && node seo-router.js >>"$LOG" 2>&1 || true



# --- HARD EMIT (guarantee pages) ---

COUNT=$(ls "$PAGES"/*.html 2>/dev/null | wc -l | tr -d ' ')

if [ "$COUNT" -eq 0 ]; then

  find "$BASE" -maxdepth 1 -name "*.html" ! -name "index.html" -exec cp {} "$PAGES/" \;

  [ -d "$BASE/seo-pages" ] && find "$BASE/seo-pages" -name "*.html" -exec cp {} "$PAGES/" \;

fi



COUNT=$(ls "$PAGES"/*.html 2>/dev/null | wc -l | tr -d ' ')

echo "PAGES BUILT: $COUNT" | tee -a "$LOG"



# --- GIT (GUARANTEED CONTEXT) ---

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

git add docs/pages logs

git commit -m "Auto build: emit pages" || true

git push origin main || true



echo "SIDEGUY DONE" | tee -a "$LOG"

echo "LOG: $LOG"

