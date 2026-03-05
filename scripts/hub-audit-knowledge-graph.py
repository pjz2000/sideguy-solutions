#!/usr/bin/env python3
"""
SIDEGUY HUB AUDIT + KNOWLEDGE GRAPH ENGINE
-------------------------------------------
1. Audits all real hub files (hubs/, auto-hubs/categories/, auto-hubs/clusters/)
   for: FAQPage schema, BreadcrumbList schema, cluster chips, Text PJ CTA, canonical, meta description
2. Builds knowledge graph from real cluster/pillar data:
   - data/entity-map.json        — pillars + clusters as entities
   - data/related-topics.json    — pillar-level cross-links
   - docs/knowledge-graph/       — graph index + adjacency list
3. Writes audit report to docs/hub-audit/generated/
"""

import re
import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT      = Path(__file__).parent.parent.resolve()
INDEX_TSV = ROOT / "docs" / "auto-cluster" / "generated" / "page-index.tsv"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

AUDIT_DIR = ROOT / "docs" / "hub-audit" / "generated"
KG_DIR    = ROOT / "docs" / "knowledge-graph"
DATA_DIR  = ROOT / "data"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
KG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

HUB_DIRS = [
    ROOT / "hubs",
    ROOT / "auto-hubs" / "categories",
    ROOT / "auto-hubs" / "clusters",
    ROOT / "pillars",
]

print("🔍 SIDEGUY HUB AUDIT + KNOWLEDGE GRAPH ENGINE")
print(f"Timestamp: {TIMESTAMP}")
print()


# ─── 1. Audit all hub HTML files ──────────────────────────────────────────────
print("📋 Auditing hub files...")

CHECKS = {
    "faq_schema":        re.compile(r'"FAQPage"',           re.IGNORECASE),
    "breadcrumb_schema": re.compile(r'"BreadcrumbList"',    re.IGNORECASE),
    "cluster_chips":     re.compile(r'class=["\'][^"\']*chip|cluster-nav|cluster-chip', re.IGNORECASE),
    "text_pj_cta":       re.compile(r'Text PJ|773.544.1231|sms:\+17735441231', re.IGNORECASE),
    "canonical":         re.compile(r'rel=["\']canonical["\']',  re.IGNORECASE),
    "meta_desc":         re.compile(r'<meta[^>]+name=["\']description["\']', re.IGNORECASE),
}

audit_results = []

# pillars/ pages are concept/industry guides - cluster_chips not required
PILLARS_DIR_KEY = "pillars"

for hub_dir in HUB_DIRS:
    if not hub_dir.exists():
        continue
    is_pillars = hub_dir.name == PILLARS_DIR_KEY
    for html_file in sorted(hub_dir.glob("*.html")):
        try:
            content = html_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        rel = str(html_file.relative_to(ROOT))
        row = {"file": rel, "dir": str(hub_dir.relative_to(ROOT))}
        for check_name, pattern in CHECKS.items():
            if check_name == "cluster_chips" and is_pillars:
                row[check_name] = True  # not required for pillars pages
            else:
                row[check_name] = bool(pattern.search(content))
        audit_results.append(row)

# Score: count of checks passed (out of 6)
for row in audit_results:
    row["score"] = sum(1 for k in CHECKS if row[k])

total     = len(audit_results)
perfect   = sum(1 for r in audit_results if r["score"] == len(CHECKS))
needs_fix = [r for r in audit_results if r["score"] < len(CHECKS)]

print(f"   Hub files scanned : {total}")
print(f"   Perfect (6/6)     : {perfect}")
print(f"   Need fixes        : {len(needs_fix)}")

# Group by what's missing most
missing_counts = defaultdict(int)
for r in needs_fix:
    for k in CHECKS:
        if not r[k]:
            missing_counts[k] += 1

print()
print("   Most common gaps:")
for k, cnt in sorted(missing_counts.items(), key=lambda x: -x[1]):
    print(f"   - {k}: missing on {cnt} hubs")


# ─── 2. Write audit report TSV ────────────────────────────────────────────────
audit_tsv = AUDIT_DIR / "hub_audit.tsv"
with open(audit_tsv, "w", encoding="utf-8") as fh:
    headers = ["file", "dir", "score"] + list(CHECKS.keys())
    fh.write("\t".join(headers) + "\n")
    for row in sorted(audit_results, key=lambda x: x["score"]):
        vals = [str(row[h]) for h in headers]
        fh.write("\t".join(vals) + "\n")

# Markdown report
audit_md = AUDIT_DIR / "HUB_AUDIT_REPORT.md"
with open(audit_md, "w", encoding="utf-8") as fh:
    fh.write(f"# SideGuy Hub Audit Report\nGenerated: {TIMESTAMP}\n\n")
    fh.write(f"## Summary\n\n| Metric | Count |\n|---|---|\n")
    fh.write(f"| Hubs scanned | {total} |\n")
    fh.write(f"| Perfect (all checks pass) | {perfect} |\n")
    fh.write(f"| Need at least one fix | {len(needs_fix)} |\n\n")
    fh.write("## Most Common Gaps\n\n")
    for k, cnt in sorted(missing_counts.items(), key=lambda x: -x[1]):
        label = k.replace("_", " ").title()
        fh.write(f"- **{label}**: missing on {cnt} hubs\n")
    fh.write("\n## Hubs Needing Fixes (lowest score first)\n\n")
    fh.write("| File | Score | Missing |\n|---|---|---|\n")
    for row in sorted(needs_fix, key=lambda x: x["score"])[:100]:
        missing = ", ".join(k for k in CHECKS if not row[k])
        fh.write(f"| `{row['file']}` | {row['score']}/6 | {missing} |\n")
    if len(needs_fix) > 100:
        fh.write(f"\n*...and {len(needs_fix)-100} more (see hub_audit.tsv)*\n")

print(f"\n✅ Hub audit written to docs/hub-audit/generated/")


# ─── 3. Load cluster index for knowledge graph ────────────────────────────────
print("\n🧠 Building knowledge graph...")

cluster_data   = defaultdict(list)  # (pillar, cluster) → [pages]
cluster_titles = {}

if INDEX_TSV.exists():
    with open(INDEX_TSV, encoding="utf-8") as fh:
        header = None
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if header is None:
                header = cols
                continue
            if len(cols) < 5:
                continue
            pillar, cluster, ctitle = cols[1], cols[2], cols[3]
            key = (pillar, cluster)
            cluster_data[key].append(cols[0])
            cluster_titles[key] = ctitle

pillars     = sorted({p for p, _ in cluster_data})
clusters_by = defaultdict(list)
for (p, c) in cluster_data:
    clusters_by[p].append(c)


# ─── 4. Entity map ────────────────────────────────────────────────────────────
entity_map = {
    "site":     "SideGuy Solutions",
    "domain":   "https://sideguysolutions.com",
    "pillars":  pillars,
    "clusters": [
        {
            "pillar":  p,
            "cluster": c,
            "title":   cluster_titles.get((p, c), c),
            "pages":   len(cluster_data[(p, c)]),
            "hub_url": f"/auto-hubs/clusters/{p}--{c}.html",
        }
        for (p, c) in sorted(cluster_data.keys(), key=lambda x: -len(cluster_data[x]))
    ],
    "generated": TIMESTAMP,
}

entity_map_out = DATA_DIR / "entity-map.json"
with open(entity_map_out, "w", encoding="utf-8") as fh:
    json.dump(entity_map, fh, indent=2)
print(f"✅ data/entity-map.json written ({len(entity_map['clusters'])} clusters)")


# ─── 5. Related topics (cross-pillar graph) ───────────────────────────────────
# Define semantic adjacency between pillars and clusters
PILLAR_ADJACENCY = {
    "ai-automation":        ["operator-tools", "payments", "problem-intelligence"],
    "payments":             ["ai-automation", "operator-tools"],
    "operator-tools":       ["ai-automation", "payments"],
    "problem-intelligence": ["ai-automation", "operator-tools"],
}

CLUSTER_ADJACENCY = {
    # ai-automation
    ("ai-automation", "ai-cost"):           [("ai-automation", "ai-overview"), ("ai-automation", "ai-tools"), ("payments", "payments-overview")],
    ("ai-automation", "ai-overview"):       [("ai-automation", "ai-cost"), ("ai-automation", "ai-tools"), ("operator-tools", "operator-tools-overview")],
    ("ai-automation", "ai-tools"):          [("ai-automation", "ai-overview"), ("ai-automation", "ai-agent-workflows"), ("ai-automation", "ai-scheduling")],
    ("ai-automation", "ai-scheduling"):     [("ai-automation", "ai-tools"), ("ai-automation", "ai-overview"), ("operator-tools", "operator-tools-overview")],
    ("ai-automation", "ai-agent-workflows"):[("ai-automation", "ai-tools"), ("ai-automation", "ai-scheduling"), ("ai-automation", "ai-consulting")],
    ("ai-automation", "ai-consulting"):     [("ai-automation", "ai-overview"), ("ai-automation", "ai-tools"), ("operator-tools", "operator-tools-overview")],
    ("ai-automation", "ai-restaurants"):    [("ai-automation", "ai-scheduling"), ("payments", "payments-overview"), ("operator-tools", "operator-tools-overview")],
    ("ai-automation", "ai-healthcare"):     [("ai-automation", "ai-scheduling"), ("ai-automation", "ai-overview"), ("problem-intelligence", "general")],
    ("ai-automation", "ai-customer-service"):[("ai-automation", "ai-overview"), ("ai-automation", "ai-agent-workflows"), ("operator-tools", "operator-tools-overview")],
    ("ai-automation", "ai-city-pages"):     [("ai-automation", "ai-overview"), ("ai-automation", "ai-cost"), ("operator-tools", "operator-tools-overview")],
    # payments
    ("payments", "payments-overview"):      [("payments", "payment-fees"), ("ai-automation", "ai-tools"), ("operator-tools", "operator-tools-overview")],
    ("payments", "payment-fees"):           [("payments", "payments-overview"), ("payments", "stripe"), ("payments", "chargebacks")],
    ("payments", "stripe"):                 [("payments", "payment-fees"), ("payments", "payments-overview"), ("ai-automation", "ai-tools")],
    ("payments", "chargebacks"):            [("payments", "stripe"), ("payments", "payment-fees"), ("payments", "payments-overview")],
    # operator-tools
    ("operator-tools", "operator-tools-overview"): [("ai-automation", "ai-tools"), ("payments", "payments-overview"), ("ai-automation", "ai-scheduling")],
    # problem-intelligence
    ("problem-intelligence", "general"):    [("ai-automation", "ai-overview"), ("operator-tools", "operator-tools-overview"), ("payments", "payments-overview")],
}

related_topics = {
    "pillar_adjacency":  PILLAR_ADJACENCY,
    "cluster_adjacency": {
        f"{p}/{c}": [f"{rp}/{rc}" for rp, rc in related]
        for (p, c), related in CLUSTER_ADJACENCY.items()
    },
    "generated": TIMESTAMP,
}

related_out = DATA_DIR / "related-topics.json"
with open(related_out, "w", encoding="utf-8") as fh:
    json.dump(related_topics, fh, indent=2)
print(f"✅ data/related-topics.json written")


# ─── 6. Graph index markdown ──────────────────────────────────────────────────
graph_idx = KG_DIR / "graph-index.md"
with open(graph_idx, "w", encoding="utf-8") as fh:
    fh.write(f"# SideGuy Knowledge Graph\nGenerated: {TIMESTAMP}\n\n")

    fh.write("## Pillars\n\n")
    for p in pillars:
        clusters = clusters_by[p]
        total_pages = sum(len(cluster_data[(p, c)]) for c in clusters)
        fh.write(f"- **{p}** — {len(clusters)} clusters, {total_pages:,} pages\n")

    fh.write("\n## Cluster Inventory\n\n")
    fh.write("| Cluster | Pillar | Pages | Hub |\n|---|---|---|---|\n")
    for (p, c) in sorted(cluster_data.keys(), key=lambda x: -len(cluster_data[x])):
        title = cluster_titles.get((p, c), c)
        pages = len(cluster_data[(p, c)])
        hub   = f"/auto-hubs/clusters/{p}--{c}.html"
        fh.write(f"| {title} | {p} | {pages:,} | `{hub}` |\n")

    fh.write("\n## Cross-Pillar Relationships\n\n")
    fh.write("Pillars connect sideways when topics overlap:\n\n")
    for p, related in sorted(PILLAR_ADJACENCY.items()):
        fh.write(f"- **{p}** ↔ {', '.join(related)}\n")

    fh.write("\n## Cluster Cross-Links\n\n")
    fh.write("Each cluster hub links to related clusters in adjacent pillars:\n\n")
    for (p, c), related in sorted(CLUSTER_ADJACENCY.items()):
        src_title = cluster_titles.get((p, c), c)
        related_titles = [cluster_titles.get(k, k[1]) for k in related]
        fh.write(f"- **{src_title}** → {', '.join(related_titles)}\n")

    fh.write("\n## Leaf Page Link Rules\n\n")
    fh.write("Every leaf page links to:\n")
    fh.write("- Cluster hub (`auto-hubs/clusters/{pillar}--{cluster}.html`)\n")
    fh.write("- Pillar category hub (`auto-hubs/categories/{pillar}.html`)\n")
    fh.write("- 3 related leaf pages (same cluster)\n")
    fh.write("- 3 related cluster hubs (from cluster adjacency above)\n")
    fh.write("- Directory (`auto-hubs/directory.html`)\n")

print(f"✅ docs/knowledge-graph/graph-index.md written")


# ─── 7. Summary ───────────────────────────────────────────────────────────────
print()
print("─" * 52)
print("✅ HUB AUDIT + KNOWLEDGE GRAPH COMPLETE")
print(f"   Hub audit report : docs/hub-audit/generated/HUB_AUDIT_REPORT.md")
print(f"   Hub audit data   : docs/hub-audit/generated/hub_audit.tsv")
print(f"   Entity map       : data/entity-map.json")
print(f"   Related topics   : data/related-topics.json")
print(f"   Graph index      : docs/knowledge-graph/graph-index.md")
print()
print("   Top gaps to fix:")
for k, cnt in sorted(missing_counts.items(), key=lambda x: -x[1])[:3]:
    label = k.replace("_", " ").title()
    print(f"   - {label}: {cnt} hubs missing")
print("─" * 52)
print()
print("NEXT: Internal Link Contextualizer — inject 2–4 in-body")
print("      contextual links per intent page automatically.")
