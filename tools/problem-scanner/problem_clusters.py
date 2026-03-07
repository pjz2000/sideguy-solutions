"""
problem_clusters.py
-------------------
Cross-joins detected problem signals with industries to generate
cluster page slugs → docs/problem-scanner/problem-clusters.txt.
"""
import os

signals_file = "docs/problem-scanner/problem-signals.txt"

if not os.path.exists(signals_file):
    print("No problem signals — run problem_detector.py first")
    exit(1)

signals = [l for l in open(signals_file).read().splitlines() if l.strip()]

industries = [
    "hvac", "plumbing", "restaurants", "contractors", "construction",
    "real-estate", "retail", "salons", "dental", "landscaping",
    "electricians", "auto-repair", "roofing",
]

ideas = []
seen = set()

for s in signals:
    base = s.replace(" ", "-")
    for industry in industries:
        slug = f"{base}-{industry}"
        if slug not in seen:
            seen.add(slug)
            ideas.append(slug)

with open("docs/problem-scanner/problem-clusters.txt", "w") as f:
    for i in ideas:
        f.write(i + "\n")

print(f"Cluster ideas generated: {len(ideas)}")
print(f"  ({len(signals)} signals × {len(industries)} industries)")
