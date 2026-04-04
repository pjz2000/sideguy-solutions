#!/bin/bash

# ============================================================
# GSC Winners → Solder Map Bridge
# Reads data/gsc-winners.json, scores each winner,
# and appends them to a new stamped solder map TSV.
# ============================================================

echo ""
echo "🔗 GSC WINNERS → SOLDER MAP BRIDGE"
echo "==================================="
echo "  $(date '+%Y-%m-%d %I:%M%p %Z')"
echo ""

WINNERS="data/gsc-winners.json"
STAMP=$(date +"%Y-%m-%d_%H-%M-%S")
MAP="data/solder/search-page-map-$STAMP.tsv"

if [ ! -f "$WINNERS" ]; then
  echo "ERROR: $WINNERS not found. Run GSC export first."
  exit 1
fi

python3 - <<PYEOF
import json
from pathlib import Path
from datetime import date

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

STAMP = "$STAMP"
MAP   = f"data/solder/search-page-map-{STAMP}.tsv"

# ── Confidence scoring ────────────────────────────────────────
# Score = weighted blend of position rank + impression signal
# position score: 1.0 at pos 1, 0.5 at pos 10, 0.0 at pos 50
# impression score: 0.0 at 0 impr, 1.0 at 30+ impr
# confidence = 0.6*pos_score + 0.4*impr_score, clamped 0.50–0.99

def confidence(pos, impr):
    pos_score  = max(0.0, 1.0 - (pos - 1) / 49)
    impr_score = min(1.0, impr / 30)
    raw = 0.6 * pos_score + 0.4 * impr_score
    return round(max(0.50, min(0.99, raw)), 2)

# ── Cluster detection ─────────────────────────────────────────
CLUSTER_MAP = {
    "zapier":      "ai-automation",
    "webhook":     "ai-automation",
    "n8n":         "ai-automation",
    "workflow":    "ai-automation",
    "automation":  "ai-automation",
    "agent":       "ai-automation",
    "ai":          "ai-automation",
    "stripe":      "payments",
    "square":      "payments",
    "payment":     "payments",
    "solana":      "payments",
    "settlement":  "payments",
    "fees":        "payments",
    "hvac":        "hvac",
    "repair":      "hvac",
    "heating":     "hvac",
    "cooling":     "hvac",
    "san diego":   "local-sd",
    "north county":"local-sd",
    "encinitas":   "local-sd",
    "twilio":      "dev-tools",
    "sms":         "dev-tools",
    "api":         "dev-tools",
    "drywall":     "contractor",
    "contractor":  "contractor",
    "roofing":     "contractor",
    "plumb":       "contractor",
}

def cluster(query):
    q = query.lower()
    for keyword, cat in CLUSTER_MAP.items():
        if keyword in q:
            return cat
    return "general"

# ── Next action logic ─────────────────────────────────────────
def next_action(pos, impr, clust):
    if pos <= 3 and impr == 0:
        return "title-surgery-cycle-3"
    if pos <= 5:
        return "spawn-comparison-child"
    if pos <= 10:
        return "spawn-cost-guide" if clust in ("payments","hvac","contractor") else "title-surgery-cycle-2"
    if pos <= 20:
        return "spawn-local-geo-variant"
    return "title-surgery-cycle-1"

# ── Write TSV ─────────────────────────────────────────────────
lines = ["query\turl\tcluster\tconfidence\tnext_action\tposition\timpressions\tpulled_date"]

for w in sorted(winners, key=lambda x: x.get("position", 999)):
    q     = w.get("query", "")
    page  = w.get("page", "").lstrip("/")
    pos   = w.get("position", 50)
    impr  = w.get("impressions", 0)
    dt    = w.get("pulled_date", str(date.today()))
    clust = cluster(q)
    conf  = confidence(pos, impr)
    na    = next_action(pos, impr, clust)

    lines.append(f"{q}\t{page}\t{clust}\t{conf}\t{na}\t{pos}\t{impr}\t{dt}")

Path(MAP).write_text("\n".join(lines) + "\n")
print(f"Written: {MAP}")
print(f"Routes:  {len(lines)-1}")
print()

# ── Print summary table ───────────────────────────────────────
print(f"{'Query':<42} {'Cluster':<16} {'Conf':>5}  {'Next Action'}")
print("-" * 95)
for line in lines[1:]:
    parts = line.split("\t")
    q, url, clust, conf, na, pos, impr, dt = parts
    print(f"  {q:<40} {clust:<16} {conf:>5}  {na}")
PYEOF

echo ""
echo "✅ Solder map written: $MAP"
echo "🧠 Run tools/solder/run-search-page-solder-rig.sh to view seed routes"
echo ""

# ── Append scan to solder doc ─────────────────────────────────
python3 - <<PYEOF2
import json
from datetime import datetime
from pathlib import Path

now  = datetime.now().strftime("%Y-%m-%d %H:%M PDT")
STAMP = "$STAMP"
MAP   = f"data/solder/search-page-map-{STAMP}.tsv"

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

entry  = f"\n---\n\n## GSC → Solder Scan — {now}\n\n"
entry += f"- **Winners routed:** {len(winners)}\n"
entry += f"- **Map file:** {MAP}\n\n"
entry += "| Query | Position | Confidence | Next Action |\n"
entry += "|---|---|---|---|\n"

def conf(pos, impr):
    ps = max(0.0, 1.0 - (pos-1)/49)
    ims = min(1.0, impr/30)
    return round(max(0.50, min(0.99, 0.6*ps + 0.4*ims)), 2)

def na(pos, impr, clust):
    if pos <= 3 and impr == 0: return "title-surgery-cycle-3"
    if pos <= 5:  return "spawn-comparison-child"
    if pos <= 10: return "spawn-cost-guide" if clust in ("payments","hvac") else "title-surgery-cycle-2"
    if pos <= 20: return "spawn-local-geo-variant"
    return "title-surgery-cycle-1"

for w in sorted(winners, key=lambda x: x.get("position", 999)):
    q    = w.get("query","")
    pos  = w.get("position", 50)
    impr = w.get("impressions", 0)
    c    = conf(pos, impr)
    n    = na(pos, impr, "general")
    entry += f"| {q} | {pos} | {c} | {n} |\n"

entry += "\n"
doc = Path("docs/solder/search-page-soldering.md")
doc.write_text(doc.read_text() + entry)
print(f"Appended scan to docs/solder/search-page-soldering.md")
PYEOF2
