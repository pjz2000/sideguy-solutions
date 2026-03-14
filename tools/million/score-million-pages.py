#!/usr/bin/env python3
"""Fast replacement for score-million-pages.sh — pure Python, no subshells."""

import csv
import os
import re
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
os.chdir(ROOT)

HIGH_CITY = {"san-diego", "los-angeles", "san-francisco", "new-york", "chicago", "miami", "austin", "seattle"}

def load_weights(path):
    weights = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            keys = list(row.keys())
            weights[row[keys[0]].strip()] = int(row[keys[1]].strip())
    return weights

theme_w    = load_weights("docs/million-page/config/theme-weights.csv")
state_w    = load_weights("docs/million-page/config/state-priority.csv")
industry_w = load_weights("docs/million-page/config/industry-priority.csv")
pagetype_w = load_weights("docs/million-page/config/page-type-priority.csv")

HIGH_MODIFIER  = re.compile(r'pricing|comparison|security|compliance|implementation|buyer.guide|guide', re.I)
HIGH_USE_CASE  = re.compile(r'pricing|comparison|security|compliance|implementation', re.I)

scored_dir = Path("docs/million-page/scored")
scored_dir.mkdir(parents=True, exist_ok=True)

manifests = sorted(Path("docs/million-page/manifests").glob("*.csv"))
if not manifests:
    print("No manifests found in docs/million-page/manifests/")
    raise SystemExit(1)

for manifest in manifests:
    out_path = scored_dir / manifest.name
    rows_written = 0

    with open(manifest, newline="") as fin, open(out_path, "w", newline="") as fout:
        reader = csv.reader(fin)
        header = next(reader)
        writer = csv.writer(fout)
        writer.writerow(header + ["score"])

        for row in reader:
            if len(row) < 12:
                continue
            url, title, h1, theme, audience, use_case, industry, city, state, modifier, page_type, intent = row[:12]

            def clean(s): return s.strip().strip('"').lower().replace(" ", "-")

            tw = theme_w.get(clean(theme), 5)
            sw = state_w.get(clean(state), 5)
            iw = industry_w.get(clean(industry), 5)
            pw = pagetype_w.get(clean(page_type), 5)

            mod_bonus  = 8 if HIGH_MODIFIER.search(modifier)  else 0
            uc_bonus   = 8 if HIGH_USE_CASE.search(use_case)   else 0
            city_bonus = 4 if clean(city) in HIGH_CITY          else 0

            score = tw + sw + iw + pw + mod_bonus + uc_bonus + city_bonus
            writer.writerow(row[:12] + [str(score)])
            rows_written += 1

    print(f"Scored {out_path.name}: {rows_written} rows")

print("Done scoring.")
