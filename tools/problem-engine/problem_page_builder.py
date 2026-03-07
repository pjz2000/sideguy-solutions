"""
problem_page_builder.py
-----------------------
Expands each signal into 3 page idea variants and writes
docs/problem-engine/problem-page-ideas.txt.
"""
import os

signals_file = "docs/problem-engine/problem-signals.txt"

if not os.path.exists(signals_file):
    print("No signals file — run problem_collector.py first")
    exit(1)

signals = [l for l in open(signals_file).read().splitlines() if l.strip()]

ideas = []
seen = set()

for s in signals:
    slug = s.replace(" ", "-")
    variants = [
        f"how-to-fix-{slug}",
        f"{slug}-solutions",
        f"{slug}-automation-options",
    ]
    for v in variants:
        if v not in seen:
            seen.add(v)
            ideas.append(v)

with open("docs/problem-engine/problem-page-ideas.txt", "w") as f:
    for i in ideas:
        f.write(i + "\n")

print(f"Page ideas generated: {len(ideas)}")
print(f"  ({len(signals)} signals × 3 variants, deduplicated)")
