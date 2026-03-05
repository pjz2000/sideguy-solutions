#!/usr/bin/env python3
"""
SideGuy Opportunity Heatmap
-----------------------------
Reads docs/knowledge-graph/site-graph.tsv (col0=rel_path, col1=dir/cluster)
and builds a Markdown heatmap of cluster sizes with build recommendations.

Output: docs/mission-control/opportunity_heatmap.md

Filters out backup/quarantine directories so they don't skew the map.
"""

import csv
from collections import defaultdict
from pathlib import Path

ROOT     = Path(__file__).parent.parent.resolve()
INPUT    = ROOT / "docs" / "knowledge-graph" / "site-graph.tsv"
OUT_DIR  = ROOT / "docs" / "mission-control"
OUT_MD   = OUT_DIR / "opportunity_heatmap.md"

# Directories whose pages are not live content — exclude from heatmap
SKIP_CLUSTERS = {
    "backups_20251230_191613",
    "backups/pre-blanket",
    "backup_pages",
    "backup_old_pages",
    ".sideguy-backups",
    "_quarantine_backups",
}

def rec(count: int) -> str:
    if count > 5000:
        return "Build 40–50 new pages"
    if count > 1000:
        return "Build 20–30 new pages"
    if count > 200:
        return "Build 5–10 new pages"
    if count > 50:
        return "Add 2–5 intent variations"
    return "Seed cluster — monitor signals"

def main():
    if not INPUT.exists():
        print(f"Site graph not found: {INPUT.relative_to(ROOT)}")
        print("Run: python3 scripts/tools-intelligence-engine.py  to generate it.")
        return

    clusters: dict[str, int] = defaultdict(int)
    with open(INPUT, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)  # skip header
        for row in reader:
            if len(row) < 2:
                continue
            cluster = row[1].strip()
            if cluster and cluster not in SKIP_CLUSTERS:
                clusters[cluster] += 1

    heatmap = sorted(clusters.items(), key=lambda x: -x[1])
    total   = sum(clusters.values())

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        "# SideGuy Opportunity Heatmap",
        "",
        f"Live content clusters: **{len(clusters)}**  |  Total pages: **{total:,}**",
        "",
        "| Rank | Cluster | Pages | Recommendation |",
        "|---:|---|---:|---|",
    ]
    for i, (cluster, count) in enumerate(heatmap[:30], 1):
        lines.append(f"| {i} | `{cluster}` | {count:,} | {rec(count)} |")

    lines += [
        "",
        "---",
        "",
        "## Full cluster list",
        "",
    ]
    for cluster, count in heatmap:
        lines.append(f"### {cluster}  ({count:,} pages)")
        lines.append(f"Recommendation: {rec(count)}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Opportunity heatmap built")
    print(f"  Clusters : {len(clusters)}")
    print(f"  Pages    : {total:,} (live content only)")
    print(f"  Output   : {OUT_MD.relative_to(ROOT)}")
    print()
    print("Top 10 clusters:")
    for cluster, count in heatmap[:10]:
        print(f"  {count:>6,}  {cluster}  — {rec(count)}")

if __name__ == "__main__":
    main()
