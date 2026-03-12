#!/usr/bin/env python3
"""
Page 2 Opportunity Seeds — static keyword list.
Replace with real GSC data using tools/gsc-opportunity/page2_opportunity_engine.py
once you have a Search Console CSV export.
"""
import os

opportunities = [
    "software development san diego",
    "mobile payment processing san diego",
    "ai lead generation san diego",
    "tech help san diego",
    "payment processing comparison",
]

os.makedirs("docs/intel-reports", exist_ok=True)
out = "docs/intel-reports/page2_targets.txt"

with open(out, "w") as f:
    f.write("# Page 2 keyword targets (seeds — replace with real GSC data)\n")
    for o in opportunities:
        f.write(o + "\n")

print(f"Page 2 seed list written to {out}")
print("Tip: run tools/gsc-opportunity/page2_opportunity_engine.py with a real GSC export for live data.")
