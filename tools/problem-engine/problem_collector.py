"""
problem_collector.py
--------------------
Aggregates problem signals from all known signal sources into
docs/problem-engine/problem-signals.txt for downstream processing.
Also pulls from the gravity and growth-engine outputs already on disk.
"""
import os

sources = [
    "docs/trend-radar/trend-signals.txt",
    "docs/query-capture/page-ideas.txt",
    "docs/operator-layer/operator-report.txt",
    # additional sources from existing pipelines
    "docs/problem-gravity/gravity_sources.txt",
    "docs/recursive-builder/all-signals.txt",
    "data/query-capture/page-ideas.txt",
    "data/future-signals/future-problems.tsv",
]

signals = []

for s in sources:
    if os.path.exists(s):
        for line in open(s):
            line = line.strip()
            # skip TSV headers and empty lines
            if line and not line.startswith("problem\t") and not line.startswith("#"):
                # strip TSV columns — keep first field only
                signals.append(line.split("\t")[0].lower())
        print(f"  Loaded: {s}")
    else:
        print(f"  [skip] {s}")

# deduplicate while preserving order
seen = set()
unique = []
for s in signals:
    if s not in seen:
        seen.add(s)
        unique.append(s)

os.makedirs("docs/problem-engine", exist_ok=True)
with open("docs/problem-engine/problem-signals.txt", "w") as f:
    for s in unique:
        f.write(s + "\n")

print(f"\nSignals collected: {len(unique)}")
