"""
Cluster Authority Flywheel
Scans web-accessible HTML pages, groups them by first path segment (cluster),
ranks by page count, and outputs a cluster authority map.
"""
import os
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "authority-flywheel" / "cluster_authority_map.md"

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
        rel = path.relative_to(ROOT)
        parts = rel.parts
        cluster = parts[0] if len(parts) > 1 else "(root)"
        clusters[cluster].append(str(rel))

ranked = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w") as f:
    f.write("# SideGuy Cluster Authority Map\n\n")
    f.write(f"Total clusters: {len(ranked)}\n")
    f.write(f"Total pages: {sum(len(v) for v in clusters.values())}\n\n")
    for cluster, pages in ranked:
        f.write(f"## {cluster}\n")
        f.write(f"Pages: {len(pages)}\n\n")
        hub = pages[0]
        f.write(f"Hub page: {hub}\n\n")
        f.write("Related pages:\n")
        for p in pages[1:10]:
            f.write(f"- {p}\n")
        f.write("\n")

print("Cluster authority map generated")
print(f"Clusters : {len(ranked)}")
print(f"Pages    : {sum(len(v) for v in clusters.values())}")
print(f"Report   : {OUTPUT.relative_to(ROOT)}")
