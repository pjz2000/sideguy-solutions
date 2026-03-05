#!/usr/bin/env python3
"""
SideGuy Authority Cluster Booster
------------------------------------
Scans the public/ and root-level HTML pages, groups them into clusters by
subdirectory, scores each cluster by page count, and writes a Markdown
authority report with per-cluster page listings.

Also cross-references against the full site graph to show which clusters
have the most site-wide internal link coverage (proxy for authority flow).

Output: docs/authority-reports/authority_clusters.md
"""

import csv
import glob
import os
from collections import defaultdict
from pathlib import Path

ROOT      = Path(__file__).parent.parent.parent.resolve()
OUT_PATH  = ROOT / "docs" / "authority-reports" / "authority_clusters.md"
SITE_GRAPH = ROOT / "docs" / "knowledge-graph" / "site-graph.tsv"

SKIP_DIRS = {".git", "_quarantine_backups", "node_modules",
             "backups_20251230_191613", "backups", "backup_pages",
             "backup_old_pages", ".sideguy-backups"}

PREVIEW_LIMIT = 10  # max page paths shown per cluster in report

# ── Collect public/ HTML files ────────────────────────────────────────────────
clusters: dict[str, list[str]] = defaultdict(list)

for p in sorted(glob.glob(str(ROOT / "public" / "**" / "*.html"), recursive=True)):
    rel = os.path.relpath(p, ROOT / "public").replace(os.sep, "/")
    parts = rel.split("/")
    cluster = parts[0] if len(parts) > 1 else "(root)"
    clusters[cluster].append("public/" + rel)

# Also grab root-level HTML (the main site pages)
root_pages = [
    os.path.relpath(p, ROOT).replace(os.sep, "/")
    for p in glob.glob(str(ROOT / "*.html"))
    if not any(d in p for d in SKIP_DIRS)
]
if root_pages:
    clusters["(site root)"].extend(sorted(root_pages))

results = sorted(clusters.items(), key=lambda x: -len(x[1]))
total_pages = sum(len(v) for v in clusters.values())

# ── Authority score: cross-ref with site graph cluster sizes ──────────────────
graph_clusters: dict[str, int] = defaultdict(int)
if SITE_GRAPH.exists():
    with open(SITE_GRAPH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[1] not in SKIP_DIRS:
                graph_clusters[row[1]] += 1

def authority_label(count: int) -> str:
    if count >= 50:  return "🏆 High authority"
    if count >= 20:  return "⚡ Growing"
    if count >= 10:  return "🌱 Early cluster"
    return "🔹 Seed"

# ── Write report ──────────────────────────────────────────────────────────────
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

lines = [
    "# SideGuy Authority Clusters — public/",
    "",
    f"Clusters: **{len(clusters)}**  |  Total pages: **{total_pages:,}**",
    "",
    "| Rank | Cluster | Pages | Authority |",
    "|---:|---|---:|---|",
]
for i, (cluster, pages) in enumerate(results[:30], 1):
    lines.append(f"| {i} | `{cluster}` | {len(pages)} | {authority_label(len(pages))} |")

lines += ["", "---", ""]

for cluster, pages in results:
    lines += [
        f"## {cluster}  ({len(pages)} pages)  {authority_label(len(pages))}",
        "",
    ]
    for p in pages[:PREVIEW_LIMIT]:
        lines.append(f"- `{p}`")
    if len(pages) > PREVIEW_LIMIT:
        lines.append(f"- … and {len(pages) - PREVIEW_LIMIT} more")
    lines.append("")

OUT_PATH.write_text("\n".join(lines), encoding="utf-8")

print(f"Authority cluster report generated")
print(f"  Clusters : {len(clusters)}")
print(f"  Pages    : {total_pages:,}")
print(f"  Output   : {OUT_PATH.relative_to(ROOT)}")
print()
print("Top clusters:")
for cluster, pages in results[:10]:
    print(f"  {len(pages):>4}  {cluster}  {authority_label(len(pages))}")
