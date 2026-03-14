#!/usr/bin/env python3
"""Fast wave selector — properly handles quoted CSV fields."""

import csv
import os
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
os.chdir(ROOT)

# Load config
cfg = {}
for line in Path("docs/million-page/config/publish-quota.env").read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()

MIN_SCORE        = int(cfg.get("MIN_SCORE_TO_PUBLISH", 40))
WAVE_QUOTA       = int(cfg.get("WAVE_PUBLISH_QUOTA", 250))
MAX_THEME        = int(cfg.get("MAX_PAGES_PER_THEME_PER_WAVE", 40))
MAX_STATE        = int(cfg.get("MAX_PAGES_PER_STATE_PER_WAVE", 30))
MAX_INDUSTRY     = int(cfg.get("MAX_PAGES_PER_INDUSTRY_PER_WAVE", 25))

scored_dir  = Path("docs/million-page/scored-deduped")
out_dir     = Path("docs/million-page/selected")
out_dir.mkdir(parents=True, exist_ok=True)

all_rows = []
header   = None

for csv_file in sorted(scored_dir.glob("*.csv")):
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        h = next(reader)
        if header is None:
            header = h
        for row in reader:
            if len(row) < 2:
                continue
            all_rows.append(row)

if not all_rows:
    print("No scored rows found.")
    raise SystemExit(1)

# Score is last column
def get_score(row):
    try:
        return int(row[-1].strip().strip('"'))
    except (ValueError, IndexError):
        return 0

# Filter by min score and sort descending
candidates = [r for r in all_rows if get_score(r) >= MIN_SCORE]
candidates.sort(key=get_score, reverse=True)

# Apply caps
theme_count    = {}
state_count    = {}
industry_count = {}
selected       = []

# Column indices (0-based): url=0, theme=3, industry=6, state=8
for row in candidates:
    if len(row) < 9:
        continue
    theme    = row[3].strip().strip('"').lower()
    industry = row[6].strip().strip('"').lower()
    state    = row[8].strip().strip('"').lower()

    if theme_count.get(theme, 0)       >= MAX_THEME:    continue
    if state_count.get(state, 0)       >= MAX_STATE:    continue
    if industry_count.get(industry, 0) >= MAX_INDUSTRY: continue
    if len(selected)                   >= WAVE_QUOTA:   break

    selected.append(row)
    theme_count[theme]       = theme_count.get(theme, 0) + 1
    state_count[state]       = state_count.get(state, 0) + 1
    industry_count[industry] = industry_count.get(industry, 0) + 1

final_path = out_dir / "wave-selection.csv"
with open(final_path, "w", newline="") as f:
    writer = csv.writer(f)
    if header:
        writer.writerow(header)
    writer.writerows(selected)

print(f"Built {final_path} — {len(selected)} pages selected")
