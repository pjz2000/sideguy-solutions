#!/usr/bin/env python3
"""
GSC Page-2 Opportunity Engine — read-only.
Reads a Google Search Console CSV export and identifies pages
ranked 8–20 with meaningful impressions as upgrade candidates.
Does not modify any HTML files.

Usage:
  1. Export "Pages" report from GSC (date range: 3 months)
  2. Save as data/gsc/search-console-pages.csv
  3. python3 tools/gsc-opportunity/page2_opportunity_engine.py

Expected CSV columns: Page, Clicks, Impressions, CTR, Position
"""
import csv, os

INPUT = "data/gsc/search-console-pages.csv"
OUT = "docs/gsc-opportunity/page2-opportunities.tsv"


def run():
    if not os.path.exists(INPUT):
        print(f"No data file found. Export GSC pages report to: {INPUT}")
        print("Expected columns: Page, Clicks, Impressions, CTR, Position")
        return

    rows = list(csv.DictReader(open(INPUT, encoding="utf-8")))
    if not rows:
        print("CSV is empty.")
        return

    opportunities = []
    for r in rows:
        try:
            pos = float(r.get("Position", 0))
            imp = float(r.get("Impressions", 0))
            ctr = float(str(r.get("CTR", "0")).replace("%", ""))
        except ValueError:
            continue

        if 8 <= pos <= 20 and imp > 20:
            # Score: higher impressions and positions closer to page 1 rank higher
            score = imp / 10 + (20 - pos) * 3 + max(0, 2 - ctr)
            opportunities.append((score, pos, imp, ctr, r.get("Page", "")))

    opportunities.sort(reverse=True)

    os.makedirs("docs/gsc-opportunity", exist_ok=True)
    with open(OUT, "w") as f:
        f.write("score\tposition\timpressions\tctr\tpage\n")
        for score, pos, imp, ctr, page in opportunities:
            f.write(f"{score:.2f}\t{pos}\t{imp:.0f}\t{ctr:.2f}%\t{page}\n")

    print(f"Page-2 opportunity report written: {OUT}")
    print(f"Pages identified: {len(opportunities)}")


if __name__ == "__main__":
    run()
