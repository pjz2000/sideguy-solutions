#!/usr/bin/env bash

cd /workspaces/sideguy-solutions || exit 1

python3 tools/monetization/monetization_radar.py
python3 tools/monetization/monetization_upgrade_targets.py

echo
echo "Top 20 monetization pages:"
echo "--------------------------"
python3 - << 'PY'
import csv
rows = []
with open("docs/monetization/monetization-radar.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        row["score"] = int(row["score"])
        rows.append(row)

for i, r in enumerate(sorted(rows, key=lambda x: (-x["score"], x["page"]))[:20], start=1):
    print(f"{i:02d}. {r['page']} | {r['category']} | score={r['score']} | quick wins: {r['quick_wins']}")
PY
