import os

signals = []
files = [
    "data/future-signals/future-problems.tsv",
    "docs/growth-engine/page-expansion.txt",
    "data/query-capture/page-ideas.txt"
]

for f in files:
    if os.path.exists(f):
        for line in open(f):
            signals.append(line.strip())

signals = list(set(signals))

with open("docs/recursive-builder/all-signals.txt", "w") as out:
    for s in signals:
        out.write(s + "\n")

print("Signals merged:", len(signals))
