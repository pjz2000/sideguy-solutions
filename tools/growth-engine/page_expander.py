#!/usr/bin/env python3
"""
SideGuy Growth Engine — Page Expander
---------------------------------------
Reads the GSC pages CSV exported from Search Console → Performance → Pages.
For each page WITH impressions, generates 5 intent-expansion topic ideas:
  <topic> cost / tools / mistakes / checklist / troubleshooting

Output: docs/growth-engine/expansion-ideas.txt  (one idea per line)
        docs/growth-engine/expansion-ideas.tsv  (structured: page, intent, topic, slug_hint)

Place your GSC export at: docs/gsc/gsc_pages.csv
  Expected columns (any order, case-insensitive):
    Page | URL | Landing Page  → the page path
    Impressions                 → impression count
    Clicks                      → click count
"""

import csv
import os
import re
from pathlib import Path

ROOT   = Path(__file__).parent.parent.parent.resolve()
INPUT  = ROOT / "docs" / "gsc" / "gsc_pages.csv"
OUT_DIR = ROOT / "docs" / "growth-engine"
OUT_TXT = OUT_DIR / "expansion-ideas.txt"
OUT_TSV = OUT_DIR / "expansion-ideas.tsv"

INTENTS = ["cost", "tools", "mistakes", "checklist", "troubleshooting"]

def normalize_page(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^https?://[^/]+", "", raw)
    return raw.lstrip("/")

def clean_int(s: str) -> int:
    return int(str(s).replace(",", "").strip() or "0")

OUT_DIR.mkdir(parents=True, exist_ok=True)

if not INPUT.exists():
    print(f"GSC CSV not found at {INPUT.relative_to(ROOT)}")
    print("Export from: Search Console → Performance → Pages → Export CSV")
    print("Save to: docs/gsc/gsc_pages.csv  and re-run.")
    # Write placeholder outputs so the engine is always runnable
    OUT_TXT.write_text("# No GSC data yet. Export docs/gsc/gsc_pages.csv and re-run.\n")
    OUT_TSV.write_text("page\tintent\ttopic\tslug_hint\n")
    exit(0)

rows = []
with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        # Accept various column name capitalizations
        page = (r.get("Page") or r.get("page") or r.get("URL") or
                r.get("Url") or r.get("Landing Page") or r.get("Landing page") or "").strip()
        if not page:
            continue
        imp = clean_int(r.get("Impressions") or r.get("impressions") or "0")
        clk = clean_int(r.get("Clicks") or r.get("clicks") or "0")
        if imp > 0:
            rows.append({"page": normalize_page(page), "impressions": imp, "clicks": clk})

rows.sort(key=lambda x: -x["impressions"])

ideas_txt = []
ideas_tsv = []

for r in rows:
    slug = r["page"].replace(".html", "").replace("/", "--")
    base = os.path.basename(r["page"]).replace(".html", "").replace("-", " ").strip()
    for intent in INTENTS:
        topic = f"{base} {intent}".strip()
        slug_hint = slug.rstrip("-") + "-" + intent
        ideas_txt.append(topic)
        ideas_tsv.append({
            "page": r["page"],
            "impressions": r["impressions"],
            "clicks": r["clicks"],
            "intent": intent,
            "topic": topic,
            "slug_hint": slug_hint,
        })

OUT_TXT.write_text("\n".join(ideas_txt) + "\n", encoding="utf-8")

with open(OUT_TSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["page", "impressions", "clicks", "intent", "topic", "slug_hint"])
    for r in ideas_tsv:
        w.writerow([r["page"], r["impressions"], r["clicks"], r["intent"], r["topic"], r["slug_hint"]])

print(f"Expansion ideas generated: {len(ideas_txt)}")
print(f"Source pages: {len(rows)}")
print(f"Text output : {OUT_TXT.relative_to(ROOT)}")
print(f"TSV output  : {OUT_TSV.relative_to(ROOT)}")
