#!/bin/bash
# SideGuy Discovery → Index Upgrader
# Safe operations only — reads repo at /Users/kromeon/sideguy-solutions

echo "🚀 Discovery → Index upgrade engine"

ROOT="/Users/kromeon/sideguy-solutions"
STAMP=$(date +"%Y-%m-%d %H:%M:%S PT")
LOG="$ROOT/logs/discovery-index-upgrader-$(date +%Y%m%d-%H%M%S).log"

echo "run started: $STAMP" > "$LOG"

# 1) Add defensive CSS for empty media placeholders to index.html
python3 - <<'PY'
from pathlib import Path
p = Path("/Users/kromeon/sideguy-solutions/index.html")
html = p.read_text()
if ".hero-media:empty" not in html:
    inject = """<style>
.hero-media:empty,.media-placeholder:empty,.freshness-media:empty{
  display:none!important;height:0!important;min-height:0!important;
  padding:0!important;margin:0!important;border:0!important;overflow:hidden!important;
}
</style>
"""
    html = html.replace("</head>", inject + "</head>")
    p.write_text(html)
    print("✅ defensive CSS added")
else:
    print("✅ defensive CSS already present")
PY

# 2) Canonical audit — find pages missing canonical (non-www only)
echo "" | tee -a "$LOG"
echo "=== Pages missing canonical ===" | tee -a "$LOG"
find "$ROOT" -maxdepth 1 -name "*.html" ! -name "index.html" | while read -r file; do
    grep -q 'rel="canonical"' "$file" || echo "MISSING: $file" | tee -a "$LOG"
done

echo "" | tee -a "$LOG"
echo "✅ upgrades complete — see $LOG" | tee -a "$LOG"
