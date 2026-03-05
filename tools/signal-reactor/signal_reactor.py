"""
Signal Reactor
Reads GSC pages CSV and generates a prioritised expansion plan —
topics with real impressions get 10 suggested derivative pages each.
Falls back to a placeholder plan if no GSC data is available yet.
"""
import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "docs" / "gsc" / "gsc_pages.csv"
OUTPUT = ROOT / "docs" / "signal-reactor" / "signal_expansion_plan.md"

signals = {}

if INPUT.exists():
    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # GSC exports vary: "Top pages"/"page", "Impressions"/"impressions"
        for row in reader:
            page_key = next((k for k in row if k.lower() in ("top pages", "page")), None)
            imp_key  = next((k for k in row if k.lower() == "impressions"), None)
            click_key = next((k for k in row if k.lower() == "clicks"), None)
            if not page_key:
                continue
            try:
                impressions = int(row.get(imp_key, 0)) if imp_key else 0
                clicks      = int(row.get(click_key, 0)) if click_key else 0
            except (ValueError, TypeError):
                continue
            page = row.get(page_key, "")
            if not page or page.lower() == "top pages":
                continue
            topic = Path(page.rstrip("/")).stem or "(root)"
            if impressions > 0 or clicks > 0:
                signals[topic] = signals.get(topic, 0) + max(impressions, 1)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w") as f:
    f.write("# SideGuy Signal Reactor Expansion Plan\n\n")

    if not signals:
        f.write("⚠️  No GSC data found yet.\n\n")
        f.write(f"Export GSC → Performance → Pages → Export CSV\n")
        f.write(f"Save as: `docs/gsc/gsc_pages.csv`\n\n")
        f.write("Then re-run this tool to generate the full expansion plan.\n")
    else:
        ranked = sorted(signals.items(), key=lambda x: x[1], reverse=True)
        f.write(f"Topics with signal: {len(ranked)}\n\n")
        for topic, impressions in ranked[:100]:  # top 100
            f.write(f"## {topic}\n")
            f.write(f"Impressions: {impressions:,}\n\n")
            f.write("Expansion Pages:\n")
            suffixes = [
                "guide", "checklist", "cost", "faq", "near-me",
                "san-diego", "tips", "vs-alternatives", "how-it-works", "reviews"
            ]
            for suffix in suffixes:
                f.write(f"- {topic}-{suffix}\n")
            f.write("\n")

if signals:
    print(f"Signal reactor expansion plan generated")
    print(f"Topics with signal : {len(signals)}")
else:
    print("Signal reactor ready — awaiting docs/gsc/gsc_pages.csv")
print(f"Output: {OUTPUT.relative_to(ROOT)}")
