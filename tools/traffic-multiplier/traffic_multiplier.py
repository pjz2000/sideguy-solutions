#!/usr/bin/env python3
"""
SideGuy Traffic Multiplier
----------------------------
Reads the GSC Pages export (docs/gsc/gsc_pages.csv) and builds a
structured expansion plan: for each page with impressions, suggest
5 intent-variation pages to multiply traffic.

Output: docs/traffic-signals/traffic_expansion_plan.md
        docs/traffic-signals/expansion_queue.tsv

If GSC CSV is missing, writes a placeholder and exits gracefully.
"""

import csv
import os
import re
from pathlib import Path

ROOT   = Path(__file__).parent.parent.parent.resolve()
INPUT  = ROOT / "docs" / "gsc" / "gsc_pages.csv"
OUT_MD = ROOT / "docs" / "traffic-signals" / "traffic_expansion_plan.md"
OUT_TSV = ROOT / "docs" / "traffic-signals" / "expansion_queue.tsv"

INTENTS = ["cost", "how-it-works", "checklist", "mistakes", "tools"]

def clean_int(s) -> int:
    return int(str(s).replace(",", "").strip() or "0")

def normalize(raw: str) -> str:
    raw = re.sub(r"^https?://[^/]+", "", raw.strip()).lstrip("/")
    return raw

def slug_label(page: str) -> str:
    base = os.path.basename(page).replace(".html", "")
    return base.replace("-", " ").replace("_", " ").strip()

OUT_MD.parent.mkdir(parents=True, exist_ok=True)

if not INPUT.exists():
    OUT_MD.write_text(
        "# Traffic Expansion Plan\n\n"
        "> GSC CSV not found. Export from Search Console → Performance → Pages → Export CSV\n"
        "> Save as: `docs/gsc/gsc_pages.csv` and re-run.\n",
        encoding="utf-8"
    )
    OUT_TSV.write_text("page\timpressions\tclix\tintent\tslug_hint\n", encoding="utf-8")
    print("GSC CSV missing — placeholder written. Add docs/gsc/gsc_pages.csv and re-run.")
    exit(0)

rows = []
with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        page = (r.get("Page") or r.get("page") or r.get("URL") or
                r.get("Landing Page") or r.get("Landing page") or "").strip()
        if not page:
            continue
        imp = clean_int(r.get("Impressions") or r.get("impressions") or "0")
        clk = clean_int(r.get("Clicks") or r.get("clicks") or "0")
        if imp > 1:
            rows.append({"page": normalize(page), "impressions": imp, "clicks": clk})

rows.sort(key=lambda x: -x["impressions"])

md_lines = [
    "# Traffic Expansion Plan",
    "",
    f"Source pages with impressions > 1: **{len(rows)}**",
    f"Expansion ideas generated: **{len(rows) * len(INTENTS)}**",
    "",
    "---",
    "",
]
tsv_rows = []

for r in rows:
    label = slug_label(r["page"])
    slug  = os.path.basename(r["page"]).replace(".html", "")
    md_lines += [
        f"## {label}",
        f"Impressions: {r['impressions']}  |  Clicks: {r['clicks']}",
        "",
        "Suggested expansion pages:",
    ]
    for intent in INTENTS:
        topic     = f"{label} {intent}"
        slug_hint = f"{slug}-{intent}"
        md_lines.append(f"- `{slug_hint}` — {topic}")
        tsv_rows.append([r["page"], r["impressions"], r["clicks"], intent, slug_hint])
    md_lines.append("")

OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")

with open(OUT_TSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["page", "impressions", "clicks", "intent", "slug_hint"])
    for row in tsv_rows:
        w.writerow(row)

print(f"Traffic expansion plan generated")
print(f"  Source pages : {len(rows)}")
print(f"  Ideas total  : {len(tsv_rows)}")
print(f"  Markdown     : {OUT_MD.relative_to(ROOT)}")
print(f"  TSV queue    : {OUT_TSV.relative_to(ROOT)}")
