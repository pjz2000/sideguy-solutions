"""
Problem Graph Builder
Builds a TSV of cluster→page and sequential page→page edges
for visualizing the site's internal linking topology.
"""
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "problem-graph" / "problem_graph_edges.tsv"

SKIP_DIRS = {
    ".git", "node_modules", "public", "docs", "seo-reserve",
    "signals", "data", "tools", "scripts", "backups",
    "_BACKUPS", ".sideguy-backups", "reports", "reasoning", "routing",
}

clusters = defaultdict(list)

for dirpath, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if not f.endswith(".html"):
            continue
        path = Path(dirpath) / f
        rel = str(path.relative_to(ROOT))
        parts = Path(rel).parts
        cluster = parts[0] if len(parts) > 1 else "(root)"
        clusters[cluster].append(rel)

edges = []
BASE = "https://sideguysolutions.com"
for cluster, pages in clusters.items():
    cluster_url = f"{BASE}/{cluster}"
    for p in pages:
        edges.append((cluster_url, f"{BASE}/{p}"))
    for i in range(len(pages) - 1):
        edges.append((f"{BASE}/{pages[i]}", f"{BASE}/{pages[i+1]}"))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w") as f:
    f.write("source\ttarget\n")
    for a, b in edges:
        f.write(f"{a}\t{b}\n")

print("Problem graph edges generated")
print(f"Clusters : {len(clusters)}")
print(f"Edges    : {len(edges)}")
print(f"Output   : {OUTPUT.relative_to(ROOT)}")
