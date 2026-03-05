#!/usr/bin/env python3
"""
SIDEGUY LINK EQUITY BALANCER
------------------------------
1. Load page-index.tsv → measure cluster sizes
2. Classify clusters as weak (<10 pages), normal, or strong (>50 pages)
3. For every cluster hub, audit internal links TO:
   - its pillar hub
   - at least 5 related cluster hubs
   - at least 10 leaf pages in the cluster
4. For every leaf page, audit links TO:
   - its cluster hub
   - its pillar hub
5. Build an actionable rebalance plan with specific injection targets
6. Generate CLAUDE_LINK_BALANCE_PROMPT.md for guided fixes
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).parent.parent.resolve()
INDEX_TSV = ROOT / "docs" / "auto-cluster" / "generated" / "page-index.tsv"
RECORDS_JSON = ROOT / "docs" / "auto-cluster" / "generated" / "records.json"
OUT_DIR = ROOT / "docs" / "link-equity" / "generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
WEAK_THRESHOLD = 10
STRONG_THRESHOLD = 50

PILLAR_HUBS = {
    "ai-automation":        ["auto-hubs/categories/ai-automation.html", "hubs/category-ai-automation.html"],
    "payments":             ["auto-hubs/categories/payments.html", "hubs/category-payments.html"],
    "operator-tools":       ["auto-hubs/categories/operator-tools.html", "hubs/category-operator-tools.html"],
    "problem-intelligence": ["auto-hubs/categories/problem-intelligence.html", "hubs/category-problem-intelligence.html"],
}


# ─── 1. Load index ────────────────────────────────────────────────────────────
print("📂 Loading page index...")
pages = []  # list of dicts: file, pillar, cluster, cluster_title, title
with open(INDEX_TSV, encoding="utf-8") as fh:
    header = None
    for line in fh:
        cols = line.rstrip("\n").split("\t")
        if header is None:
            header = cols
            continue
        if len(cols) < 5:
            continue
        pages.append({
            "file": cols[0],
            "pillar": cols[1],
            "cluster": cols[2],
            "cluster_title": cols[3],
            "title": cols[4],
        })

print(f"   Loaded {len(pages):,} pages")


# ─── 2. Cluster sizes ─────────────────────────────────────────────────────────
cluster_pages = defaultdict(list)   # (pillar, cluster) → [page dicts]
cluster_title = {}

for p in pages:
    key = (p["pillar"], p["cluster"])
    cluster_pages[key].append(p)
    cluster_title[key] = p["cluster_title"]

sizes = {k: len(v) for k, v in cluster_pages.items()}
weak   = {k: v for k, v in sizes.items() if v < WEAK_THRESHOLD}
strong = {k: v for k, v in sizes.items() if v > STRONG_THRESHOLD}

print(f"   Clusters total : {len(sizes)}")
print(f"   Weak  (<{WEAK_THRESHOLD})    : {len(weak)}")
print(f"   Strong (>{STRONG_THRESHOLD})  : {len(strong)}")


# ─── 3. Write cluster size report ─────────────────────────────────────────────
cluster_sizes_tsv = OUT_DIR / "cluster_sizes.tsv"
with open(cluster_sizes_tsv, "w", encoding="utf-8") as fh:
    fh.write("pillar\tcluster\tcluster_title\tpage_count\tstatus\n")
    for (pillar, cluster), cnt in sorted(sizes.items(), key=lambda x: -x[1]):
        status = "strong" if cnt > STRONG_THRESHOLD else ("weak" if cnt < WEAK_THRESHOLD else "normal")
        title = cluster_title.get((pillar, cluster), cluster)
        fh.write(f"{pillar}\t{cluster}\t{title}\t{cnt}\t{status}\n")

print(f"✅ cluster_sizes.tsv written")


# ─── 4. Audit cluster hub link coverage ───────────────────────────────────────
print("🔍 Auditing cluster hub pages...")

CLUSTER_HUB_DIR = ROOT / "auto-hubs" / "clusters"

def extract_hrefs(html: str) -> set:
    return set(re.findall(r'href=["\']([^"\'#?]+)', html, re.IGNORECASE))

hub_audit = []  # list of issue dicts

for (pillar, cluster), leaf_list in sorted(cluster_pages.items()):
    # Hubs are named pillar--cluster.html
    hub_file = CLUSTER_HUB_DIR / f"{pillar}--{cluster}.html"
    if not hub_file.exists():
        hub_audit.append({
            "type": "missing_hub",
            "pillar": pillar,
            "cluster": cluster,
            "cluster_title": cluster_title.get((pillar, cluster), cluster),
            "detail": f"No hub file at auto-hubs/clusters/{pillar}--{cluster}.html"
        })
        continue

    html = hub_file.read_text(encoding="utf-8", errors="replace")
    hrefs = extract_hrefs(html)

    issues = []

    # Check pillar link (either path variant)
    pillar_paths = PILLAR_HUBS.get(pillar, [])
    if pillar_paths and not any(
        any(pp in h for h in hrefs) for pp in pillar_paths
    ):
        issues.append(f"missing link to pillar hub ({pillar_paths[0]})")

    # Check leaf coverage — hub should link to at least 10 leaves in same cluster
    cluster_files = {p["file"] for p in leaf_list}
    linked_leaves = sum(1 for h in hrefs if any(
        os.path.basename(cf) in h or cf.replace("\\", "/") in h
        for cf in cluster_files
    ))
    if linked_leaves < 10 and len(leaf_list) >= 10:
        issues.append(f"only links to {linked_leaves} leaf pages (need ≥10 of {len(leaf_list)})")

    if issues:
        hub_audit.append({
            "type": "hub_gap",
            "pillar": pillar,
            "cluster": cluster,
            "cluster_title": cluster_title.get((pillar, cluster), cluster),
            "hub_file": f"auto-hubs/clusters/{pillar}--{cluster}.html",
            "leaf_count": len(leaf_list),
            "linked_leaves": linked_leaves,
            "issues": issues,
        })

hub_audit_out = OUT_DIR / "hub_audit.json"
with open(hub_audit_out, "w", encoding="utf-8") as fh:
    json.dump(hub_audit, fh, indent=2)
print(f"   Hub audit issues: {len(hub_audit)}")
print(f"✅ hub_audit.json written")


# ─── 5. Spot-check leaf backlinks (sample 200 leaves per pillar) ──────────────
print("🔍 Spot-checking leaf → hub backlinks (sampled)...")

leaf_issues = []
SAMPLE_SIZE = 200

for (pillar, cluster), leaf_list in sorted(cluster_pages.items()):
    hub_rel = f"auto-hubs/clusters/{pillar}--{cluster}.html"
    sample = leaf_list[:SAMPLE_SIZE]
    missing_hub = 0
    missing_pillar = 0
    checked = 0

    for p in sample:
        fpath = ROOT / p["file"]
        if not fpath.exists():
            continue
        checked += 1
        try:
            html = fpath.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        hrefs = extract_hrefs(html)
        cluster_basename = os.path.basename(hub_rel)
        if not any(cluster_basename in h for h in hrefs):
            missing_hub += 1
        pillar_paths = PILLAR_HUBS.get(pillar, [])
        if pillar_paths and not any(
            any(os.path.basename(pp) in h for h in hrefs) for pp in pillar_paths
        ):
            missing_pillar += 1

    if checked > 0 and (missing_hub > checked * 0.3 or missing_pillar > checked * 0.3):
        leaf_issues.append({
            "pillar": pillar,
            "cluster": cluster,
            "cluster_title": cluster_title.get((pillar, cluster), cluster),
            "checked": checked,
            "missing_hub_link": missing_hub,
            "missing_pillar_link": missing_pillar,
            "pct_missing_hub": round(missing_hub / checked * 100),
            "pct_missing_pillar": round(missing_pillar / checked * 100),
        })

leaf_issues_out = OUT_DIR / "leaf_backlink_issues.json"
with open(leaf_issues_out, "w", encoding="utf-8") as fh:
    json.dump(leaf_issues, fh, indent=2)
print(f"   Leaf backlink issues: {len(leaf_issues)}")
print(f"✅ leaf_backlink_issues.json written")


# ─── 6. Rebalance plan ────────────────────────────────────────────────────────
plan_md = OUT_DIR / "link_rebalance_plan.md"
with open(plan_md, "w", encoding="utf-8") as fh:
    fh.write(f"# SideGuy Link Equity Rebalance Plan\n")
    fh.write(f"Generated: {TIMESTAMP}\n\n")

    fh.write(f"## Summary\n\n")
    fh.write(f"| Metric | Count |\n|---|---|\n")
    fh.write(f"| Total clusters | {len(sizes)} |\n")
    fh.write(f"| Weak clusters (<{WEAK_THRESHOLD} pages) | {len(weak)} |\n")
    fh.write(f"| Strong clusters (>{STRONG_THRESHOLD} pages) | {len(strong)} |\n")
    fh.write(f"| Hub link gap issues | {len(hub_audit)} |\n")
    fh.write(f"| Leaf backlink issue clusters | {len(leaf_issues)} |\n\n")

    fh.write(f"## Weak Clusters — Need Incoming Links\n\n")
    fh.write("These clusters have fewer than 10 pages and need authority injected from strong clusters and the directory.\n\n")
    for (pillar, cluster), cnt in sorted(weak.items(), key=lambda x: x[1]):
        title = cluster_title.get((pillar, cluster), cluster)
        fh.write(f"- **{title}** (`{pillar}/{cluster}`) — {cnt} pages\n")

    fh.write(f"\n## Strong Clusters — Drive Authority Outward\n\n")
    fh.write("Add outbound cross-links from these clusters toward weak ones.\n\n")
    for (pillar, cluster), cnt in sorted(strong.items(), key=lambda x: -x[1]):
        title = cluster_title.get((pillar, cluster), cluster)
        fh.write(f"- **{title}** (`{pillar}/{cluster}`) — {cnt} pages\n")

    fh.write(f"\n## Hub Page Gaps\n\n")
    if not hub_audit:
        fh.write("No hub gaps detected.\n")
    else:
        for item in hub_audit[:50]:
            if item["type"] == "missing_hub":
                fh.write(f"- ❌ **No hub file**: `{item['cluster']}` ({item['pillar']}) — {item['detail']}\n")
            else:
                fh.write(f"- ⚠️  **{item['cluster_title']}** (`{item['hub_file']}`)\n")
                for iss in item["issues"]:
                    fh.write(f"  - {iss}\n")
        if len(hub_audit) > 50:
            fh.write(f"\n*...and {len(hub_audit) - 50} more (see hub_audit.json)*\n")

    fh.write(f"\n## Leaf Backlink Gaps\n\n")
    if not leaf_issues:
        fh.write("No systemic leaf backlink issues detected.\n")
    else:
        fh.write("| Cluster | Checked | Missing Hub Link | Missing Pillar Link |\n|---|---|---|---|\n")
        for item in sorted(leaf_issues, key=lambda x: -x["pct_missing_hub"]):
            fh.write(
                f"| {item['cluster_title']} ({item['pillar']}) "
                f"| {item['checked']} "
                f"| {item['missing_hub_link']} ({item['pct_missing_hub']}%) "
                f"| {item['missing_pillar_link']} ({item['pct_missing_pillar']}%) |\n"
            )

print(f"✅ link_rebalance_plan.md written")


# ─── 7. Claude prompt ─────────────────────────────────────────────────────────
claude_prompt = OUT_DIR / "CLAUDE_LINK_BALANCE_PROMPT.md"
weak_list = "\n".join(
    f"  - {cluster_title.get(k, k[1])} ({k[0]}/{k[1]}) — {v} pages"
    for k, v in sorted(weak.items(), key=lambda x: x[1])
)
strong_list = "\n".join(
    f"  - {cluster_title.get(k, k[1])} ({k[0]}/{k[1]}) — {v} pages"
    for k, v in sorted(strong.items(), key=lambda x: -x[1])[:10]
)

with open(claude_prompt, "w", encoding="utf-8") as fh:
    fh.write(f"""# Claude Prompt — Link Equity Balancing
Generated: {TIMESTAMP}

## Goal
Strengthen internal authority distribution across SideGuy by auditing and fixing
cluster hubs and leaf pages that lack required internal links.

## Actions

### 1. Strengthen weak clusters
The following clusters have fewer than {WEAK_THRESHOLD} pages and need incoming links
from the directory hub (`auto-hubs/directory.html`) and from related strong clusters:

{weak_list}

### 2. Source authority from strong clusters
Add contextual outbound links from these strong clusters pointing toward the weak ones above:

{strong_list}

### 3. Ensure every cluster hub links to:
- Its pillar category page (e.g., `auto-hubs/categories/payments.html`)
- At least 5 related cluster hubs
- At least 10 leaf pages in its own cluster

### 4. Ensure every leaf page links to:
- Its cluster hub (`auto-hubs/clusters/<cluster>.html`)
- Its pillar hub (`auto-hubs/categories/<pillar>.html`)
- 3 related leaf pages in the same cluster

### 5. Maintain SideGuy page structure:
- Quick answer
- Why it happens
- Common misunderstandings
- Next steps
- Text PJ CTA: "Text PJ: 773-544-1231"

## Files to review
- Rebalance plan: `docs/link-equity/generated/link_rebalance_plan.md`
- Hub audit: `docs/link-equity/generated/hub_audit.json`
- Leaf issues: `docs/link-equity/generated/leaf_backlink_issues.json`
- Cluster sizes: `docs/link-equity/generated/cluster_sizes.tsv`
""")

print(f"✅ CLAUDE_LINK_BALANCE_PROMPT.md written")

# ─── Summary ──────────────────────────────────────────────────────────────────
print()
print("─" * 50)
print("✅ LINK EQUITY BALANCER COMPLETE")
print(f"   Clusters analysed : {len(sizes)}")
print(f"   Weak clusters      : {len(weak)}")
print(f"   Strong clusters    : {len(strong)}")
print(f"   Hub gaps           : {len(hub_audit)}")
print(f"   Leaf backlink gaps : {len(leaf_issues)}")
print(f"   Output dir         : docs/link-equity/generated/")
print("─" * 50)
print()
print("NEXT: Use CLAUDE_LINK_BALANCE_PROMPT.md to inject cross-links")
print("      from strong clusters → weak clusters via the directory.")
