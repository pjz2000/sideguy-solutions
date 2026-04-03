#!/bin/bash
# ============================================================
# SideGuy Skill Launcher: Cluster Spawn
# Reads gsc-winners.json + GSC export to identify spawn
# opportunities: new hub pages, cluster children, geo expansions.
# See docs/skills/cluster-spawn.md for full doctrine.
# ============================================================

echo ""
echo "========================================"
echo "  CLUSTER SPAWN — SKILL LAUNCHER"
echo "  $(date '+%Y-%m-%d %I:%M%p %Z')"
echo "========================================"
echo ""

WINNERS="data/gsc-winners.json"

# ── STEP 1: Load winners and find gaps ───────────────────────
echo "--- Step 1: Scanning winners for cluster gaps ---"
echo ""

if [ ! -f "$WINNERS" ]; then
  echo "ERROR: $WINNERS not found. Run GSC export first."
  exit 1
fi

python3 - <<'PYEOF'
import json
from pathlib import Path

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

print(f"Winners loaded: {len(winners)}")
print()

# Group by root term to find cluster signals
from collections import defaultdict
clusters = defaultdict(list)

for w in winners:
    q = w.get("query", "").lower()
    # Extract root term (first 2 significant words)
    words = [x for x in q.split() if len(x) > 3 and x not in ("with","that","from","this","your","have","been","what","when","where","which","their")]
    root = " ".join(words[:2]) if len(words) >= 2 else words[0] if words else q
    clusters[root].append(w)

print("Potential cluster groups (2+ related winners):")
for root, items in sorted(clusters.items(), key=lambda x: -len(x[1])):
    if len(items) >= 2:
        print(f"\n  [{root}] — {len(items)} signals")
        for it in sorted(items, key=lambda x: x.get("position", 999)):
            print(f"    pos {it.get('position'):>6.1f} | {it.get('impressions',0):>4} impr | {it.get('query')}")
PYEOF

echo ""

# ── STEP 2: Scan for missing hub pages ───────────────────────
echo "--- Step 2: Hub page coverage scan ---"
echo ""

python3 - <<'PYEOF'
import json
from pathlib import Path

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

VERTICALS = {
    "payments":     ["payment","stripe","square","paypal","chargeback","settlement","interchange","fees","processing"],
    "ai-automation":["zapier","webhook","n8n","workflow","automation","ai","agent","claude","openai"],
    "hvac":         ["hvac","heater","cooling","ac","furnace","repair","replace","capacitor","refrigerant"],
    "local-sd":     ["san diego","north county","encinitas","solana","del mar","carlsbad"],
    "future-tech":  ["kalshi","polymarket","prediction","solana","blockchain","crypto"],
}

HUB_PAGES = list(Path("hubs").glob("*.html")) if Path("hubs").exists() else []
hub_names = [p.stem.lower() for p in HUB_PAGES]

print(f"Existing hub pages: {len(HUB_PAGES)}")
for h in sorted(hub_names)[:15]:
    print(f"  /hubs/{h}.html")
print()

print("Vertical coverage assessment:")
for vertical, keywords in VERTICALS.items():
    covered = any(k in h for h in hub_names for k in keywords)
    matching_winners = [w for w in winners if any(k in w.get("query","").lower() for k in keywords)]
    status = "✅ Hub exists" if covered else "⚠️  No hub page"
    print(f"  {status:20s} | {vertical:20s} | {len(matching_winners)} winners in feed")
PYEOF

echo ""

# ── STEP 3: Geo expansion scan ───────────────────────────────
echo "--- Step 3: Geo expansion opportunities ---"
echo ""

python3 - <<'PYEOF'
import json
from pathlib import Path

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

GEO_TARGETS = ["san diego","encinitas","solana beach","del mar","carlsbad","oceanside","north county"]
NON_GEO_WINNERS = [w for w in winners
                   if not any(g in w.get("query","").lower() for g in GEO_TARGETS)
                   and w.get("impressions", 0) >= 2
                   and w.get("position", 999) <= 30]

print("Non-geo winners that could spawn local geo pages:")
print("(pos ≤ 30, impr ≥ 2, no existing city modifier)")
print()
for w in sorted(NON_GEO_WINNERS, key=lambda x: x.get("position", 999)):
    q = w.get("query")
    pos = w.get("position")
    impr = w.get("impressions", 0)
    page = w.get("page")

    # Suggest geo expansion
    print(f"  {q}")
    print(f"    pos {pos} | {impr} impr | {page}")
    print(f"    → Suggested: /{page.strip('/').replace('.html','')}-san-diego.html")
    print()
PYEOF

echo ""

# ── STEP 4: Comparison page gaps ────────────────────────────
echo "--- Step 4: Comparison page gaps ---"
echo ""
python3 - <<'PYEOF'
import json
from pathlib import Path

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

# Queries suggesting comparison intent
comparison_winners = [w for w in winners
    if any(t in w.get("query","").lower()
           for t in ["vs", " or ", "versus", "compare", "difference", "better"])]

existing_comparisons = list(Path(".").glob("*-vs-*.html")) + list(Path(".").glob("*-or-*.html"))
existing_names = [p.stem.lower() for p in existing_comparisons]

print(f"Comparison page gaps (GSC demand, no existing page):")
print()
for w in sorted(comparison_winners, key=lambda x: x.get("position", 999)):
    q = w.get("query","").lower()
    page = w.get("page","")
    # Check if a comparison page already exists
    covered = any(q.replace(" vs ","_vs_").replace(" ","_")[:20] in n for n in existing_names)
    status = "✅ page exists" if covered else "⚠️  spawn needed"
    print(f"  {status} | pos {w.get('position'):>5.1f} | {w.get('query')}")
    if not covered:
        slug = q.replace(" vs ", "-vs-").replace(" or ", "-vs-").replace(" ", "-")
        print(f"          → /{slug}.html")
    print()
PYEOF

echo ""

# ── STEP 5: Spawn summary ────────────────────────────────────
echo "--- Spawn recommendation summary ---"
DATE=$(date +"%Y-%m-%d")
python3 - <<PYEOF
print("""
Priority spawn order:
  1. Fix pages for crack-zone queries (pos < 5, no existing page)
  2. Comparison pages for vs/or queries with impressions
  3. Local geo pages for pos 15-30 non-geo winners with impr >= 2
  4. Hub pages for verticals with 3+ winners and no hub
  5. Cost guide pages for 'how much / cost / fees' queries

See docs/skills/cluster-spawn.md for full spawn doctrine.
""")
PYEOF

echo "  Run 'tools/seo/page1-watchtower.sh' to see current position data."
echo ""
echo "========================================"
echo "  CLUSTER SPAWN SCAN COMPLETE"
echo "========================================"
echo ""
