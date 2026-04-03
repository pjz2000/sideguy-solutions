#!/bin/bash

# ============================================================
# SideGuy Page 1 Watchtower
# Run after each GSC export drop.
# Input:  data/gsc-winners.json  (positions + impressions)
# Output: terminal report + appends to docs/reports/page1-watchtower.md
# ============================================================

echo ""
echo "========================================"
echo "  SIDEGUY PAGE 1 WATCHTOWER"
echo "  $(date '+%Y-%m-%d %I:%M%p %Z')"
echo "========================================"
echo ""

WINNERS="data/gsc-winners.json"
WATCHTOWER="docs/reports/page1-watchtower.md"

if [ ! -f "$WINNERS" ]; then
  echo "ERROR: $WINNERS not found."
  echo "Run GSC export + update gsc-winners.json first."
  exit 1
fi

echo "--- CLOSEST TO PAGE 1 ---"
echo ""

# Parse and display from gsc-winners.json using python3
python3 - <<'PYEOF'
import json, sys

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

# Sort by position ascending
winners_sorted = sorted(winners, key=lambda x: x.get("position", 999))

CRACK_ZONE   = []   # pos < 5
CLOSE_ZONE   = []   # 5 <= pos < 10
WATCH_ZONE   = []   # 10 <= pos < 30
DEEP_ZONE    = []   # pos >= 30

for w in winners_sorted:
    p = w.get("position", 999)
    if p < 5:
        CRACK_ZONE.append(w)
    elif p < 10:
        CLOSE_ZONE.append(w)
    elif p < 30:
        WATCH_ZONE.append(w)
    else:
        DEEP_ZONE.append(w)

def fmt(w):
    pos   = w.get("position", "?")
    impr  = w.get("impressions", 0)
    query = w.get("query", "?")
    page  = w.get("page", "?")
    date  = w.get("pulled_date", "?")
    print(f"  pos {pos:>6.2f}  |  {impr:>4} impr  |  {query}")
    print(f"           {page}")
    print(f"           pulled: {date}")
    print()

print("🔥  CRACK ZONE  (pos < 5.0) — one push away from page 1")
print("-" * 60)
if CRACK_ZONE:
    for w in CRACK_ZONE: fmt(w)
else:
    print("  None in crack zone yet.\n")

print("👀  CLOSE ZONE  (pos 5.0–9.9) — on page 1, CTR low")
print("-" * 60)
if CLOSE_ZONE:
    for w in CLOSE_ZONE: fmt(w)
else:
    print("  None in close zone.\n")

print("📋  WATCH ZONE  (pos 10–29) — needs title pass or link equity")
print("-" * 60)
if WATCH_ZONE:
    for w in WATCH_ZONE: fmt(w)
else:
    print("  None in watch zone.\n")

print("📦  DEEP ZONE   (pos 30+) — early signal, monitor only")
print("-" * 60)
if DEEP_ZONE:
    for w in DEEP_ZONE: fmt(w)
else:
    print("  None in deep zone.\n")

# CTR gain ranking
print("=" * 60)
print("MOST LIKELY CTR GAIN PAGES")
print("=" * 60)
ranked = sorted(winners_sorted, key=lambda x: (
    x.get("position", 999),
    -x.get("impressions", 0)
))
for i, w in enumerate(ranked[:5], 1):
    pos   = w.get("position", "?")
    impr  = w.get("impressions", 0)
    query = w.get("query", "?")
    print(f"  {i}. pos {pos} | {impr} impr | {query}")
print()

# Pages needing title cycle
print("=" * 60)
print("PAGES NEEDING TITLE/META CYCLE")
print("=" * 60)
TITLE_SURGERY = []
for w in winners_sorted:
    p = w.get("position", 999)
    # Flag: close zone + no title refresh signal, or deep zone with impressions
    if (5 <= p < 30) and w.get("impressions", 0) >= 1:
        TITLE_SURGERY.append(w)
if TITLE_SURGERY:
    for w in TITLE_SURGERY:
        print(f"  {w.get('query')}  (pos {w.get('position')}, {w.get('impressions')} impr)")
        print(f"  → {w.get('page')}")
        print()
else:
    print("  All near-winners have recent title passes.\n")

# Homepage card status
print("=" * 60)
print("HOMEPAGE PROOF FEED STATUS")
print("=" * 60)
for w in winners_sorted:
    marker = "✅" if w.get("impressions", 0) > 0 else "—"
    print(f"  {marker} {w.get('query'):45s} pos {w.get('position')}")
print()

print("Watchtower scan complete.")
PYEOF

echo ""
echo "--- WATCHTOWER LOG ENTRY ---"
echo "$(date '+%Y-%m-%d %H:%M %Z') — scan complete. See docs/reports/page1-watchtower.md for full detail."
echo ""

# Append a timestamped scan entry to the watchtower doc
python3 - <<'PYEOF'
import json
from datetime import datetime

with open("data/gsc-winners.json") as f:
    winners = json.load(f)

now = datetime.now().strftime("%Y-%m-%d %H:%M PDT")
winners_sorted = sorted(winners, key=lambda x: x.get("position", 999))

entry = f"\n---\n\n## Watchtower Scan — {now}\n\n"
entry += "| Query | Position | Impressions | Page |\n"
entry += "|---|---|---|---|\n"
for w in winners_sorted:
    entry += f"| {w.get('query')} | {w.get('position')} | {w.get('impressions', 0)} | {w.get('page')} |\n"
entry += "\n"

with open("docs/reports/page1-watchtower.md", "a") as f:
    f.write(entry)

print(f"Appended scan entry to docs/reports/page1-watchtower.md")
PYEOF
