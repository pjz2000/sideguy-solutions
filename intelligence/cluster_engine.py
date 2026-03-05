#!/usr/bin/env python3
"""
SideGuy Cluster Expansion Engine
----------------------------------
Reads intelligence/signals/gsc_pages.txt — a list of ranking/near-ranking page
slugs — and maps each to its real cluster from the page-index.tsv.

Outputs:
  intelligence/output/cluster_expansion_plan.md  — prioritized expansion plan
  intelligence/output/cluster_summary.tsv         — machine-readable rollup

Usage:
  python3 intelligence/cluster_engine.py

Feed it more pages by editing intelligence/signals/gsc_pages.txt (one slug per line).
"""

import csv, re, datetime
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent.resolve()
NOW  = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

INPUT   = ROOT / "intelligence" / "signals" / "gsc_pages.txt"
OUT_DIR = ROOT / "intelligence" / "output"
OUT_MD  = OUT_DIR / "cluster_expansion_plan.md"
OUT_TSV = OUT_DIR / "cluster_summary.tsv"
PAGE_INDEX = ROOT / "docs" / "auto-cluster" / "generated" / "page-index.tsv"
ENTITY_MAP = ROOT / "data" / "entity-map.json"

OUT_DIR.mkdir(parents=True, exist_ok=True)

SITE = "https://sideguysolutions.com"
PHONE = "773-544-1231"

# ── Keyword → cluster fallback (when page not in page-index) ─────────────────
CLUSTER_RULES = [
    ("payments",           "payments",           re.compile(r"payment|merchant|processing|chargeback|credit.card|stripe|fees|pos|gateway", re.I)),
    ("ai-automation",      "ai-automation",      re.compile(r"\bai\b|automation|agent|workflow|lead.gen|ai.tools|ai.scheduling|chatbot", re.I)),
    ("business-software",  "business-software",  re.compile(r"crm|erp|saas|software.dev|quickbooks|accounting|inventory|billing", re.I)),
    ("local-operator-tech","operator-tools",     re.compile(r"tech.help|software.dev|saas|development", re.I)),
    ("energy-ev",          "energy-ev",           re.compile(r"ev.charger|charging|tesla|solar|energy", re.I)),
    ("home-systems",       "home-systems",        re.compile(r"hvac|ac\b|furnace|heat.pump|plumbing", re.I)),
    ("crypto-web3",        "crypto-web3",         re.compile(r"crypto|wallet|bitcoin|solana|web3|nft", re.I)),
    ("prediction-markets", "prediction-markets",  re.compile(r"prediction.market|kalshi|polymarket", re.I)),
]

# ── Expansion recommendations ─────────────────────────────────────────────────
def expansion_rec(hits: int, cluster_total: int) -> tuple[int, str]:
    """Return (leaf_count, recommendation_string)."""
    if hits >= 5:
        return 50, "HUB AUTHORITY UPGRADE + 40–50 new leaf pages"
    if hits >= 3:
        return 25, "Hub update + 20–30 new leaf pages"
    if hits >= 2:
        return 15, "5–15 new leaf pages"
    return 8, "3–8 new leaf pages"

# ── Load real page index ──────────────────────────────────────────────────────
page_index: dict[str, dict] = {}   # normalized_slug → row
if PAGE_INDEX.exists():
    with open(PAGE_INDEX, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            fname = Path(row["file"]).name.lower()
            page_index[fname] = row

# ── Load entity-map cluster metadata ─────────────────────────────────────────
import json
entity_map = json.loads(ENTITY_MAP.read_text(encoding="utf-8"))
cluster_meta: dict[str, dict] = {}   # cluster_slug → {pillar, title, pages, hub_url}
for c in entity_map.get("clusters", []):
    cluster_meta[c["cluster"]] = c

# also index by pillar+cluster for hubs found via fallback
pillar_cluster_hubs: dict[str, str] = {}
for c in entity_map.get("clusters", []):
    pillar_cluster_hubs[f"{c['pillar']}/{c['cluster']}"] = c.get("hub_url", "")

# ── Read input pages ──────────────────────────────────────────────────────────
input_pages = []
if INPUT.exists():
    for line in INPUT.read_text(encoding="utf-8").splitlines():
        slug = line.strip()
        if slug and not slug.startswith("#"):
            input_pages.append(slug)

if not input_pages:
    print("No input pages found in intelligence/signals/gsc_pages.txt")
    exit(0)

# ── Map each page to a cluster ────────────────────────────────────────────────
# cluster_key → [{slug, pillar, cluster, cluster_title, matched_via}]
cluster_hits: dict[str, list] = defaultdict(list)
unmatched: list[str] = []

for slug in input_pages:
    fname = slug.lower()
    if not fname.endswith(".html"):
        fname += ".html"

    # 1. Exact match in real page-index
    if fname in page_index:
        row = page_index[fname]
        cluster_key = row["cluster"]
        cluster_hits[cluster_key].append({
            "slug": slug,
            "pillar": row["pillar"],
            "cluster": row["cluster"],
            "cluster_title": row.get("cluster_title", row["cluster"]),
            "matched_via": "page-index",
        })
        continue

    # 2. Keyword fallback
    matched = False
    for cluster_key, pillar_key, rx in CLUSTER_RULES:
        if rx.search(slug):
            meta = cluster_meta.get(cluster_key, {})
            cluster_hits[cluster_key].append({
                "slug": slug,
                "pillar": pillar_key,
                "cluster": cluster_key,
                "cluster_title": meta.get("title", cluster_key.replace("-", " ").title()),
                "matched_via": "keyword-fallback",
            })
            matched = True
            break

    if not matched:
        unmatched.append(slug)

# ── Sort clusters by hit count ────────────────────────────────────────────────
sorted_clusters = sorted(cluster_hits.items(), key=lambda x: -len(x[1]))

# ── Write TSV ────────────────────────────────────────────────────────────────
with open(OUT_TSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["cluster", "pillar", "hits", "existing_pages", "expansion_rec", "hub_url"])
    for cluster_key, hits in sorted_clusters:
        meta = cluster_meta.get(cluster_key, {})
        leaf_count, rec = expansion_rec(len(hits), meta.get("pages", 0))
        hub = meta.get("hub_url", f"/auto-hubs/clusters/{hits[0]['pillar']}--{cluster_key}.html")
        w.writerow([cluster_key, hits[0]["pillar"], len(hits), meta.get("pages", "?"), rec, hub])

# ── Write Markdown expansion plan ────────────────────────────────────────────
lines = [
    "# SideGuy Cluster Expansion Plan",
    "",
    f"Generated: {NOW}",
    f"Input pages: {len(input_pages)}  |  Clusters hit: {len(cluster_hits)}  |  Unmatched: {len(unmatched)}",
    "",
    "---",
    "",
    "## Priority clusters (most signal first)",
    "",
]

for i, (cluster_key, hits) in enumerate(sorted_clusters, 1):
    meta     = cluster_meta.get(cluster_key, {})
    pillar   = hits[0]["pillar"]
    ctitle   = hits[0]["cluster_title"]
    existing = meta.get("pages", "?")
    hub_url  = meta.get("hub_url", f"/auto-hubs/clusters/{pillar}--{cluster_key}.html")
    leaf_count, rec = expansion_rec(len(hits), existing if isinstance(existing, int) else 0)

    lines += [
        f"### {i}. {ctitle}",
        f"- **Pillar:** `{pillar}`  **Cluster:** `{cluster_key}`",
        f"- **Signal pages:** {len(hits)}  **Existing leaves:** {existing}",
        f"- **Recommendation:** {rec}",
        f"- **Hub:** [{hub_url}]({SITE}{hub_url})",
        "",
        "**Pages detected:**",
    ]
    for h in hits:
        tag = " _(page-index)_" if h["matched_via"] == "page-index" else " _(keyword match)_"
        lines.append(f"- `{h['slug']}`{tag}")
    lines.append("")

    # Expansion slug suggestions
    lines.append("**Expansion slug ideas:**")
    base_slugs = [
        f"{cluster_key}-guide-san-diego",
        f"{cluster_key}-cost-san-diego",
        f"best-{cluster_key}-san-diego",
        f"{cluster_key}-checklist-san-diego",
        f"who-do-i-call-for-{cluster_key}-san-diego",
    ]
    for s in base_slugs[:5]:
        lines.append(f"- `{s}.html`")
    lines += ["", "---", ""]

if unmatched:
    lines += [
        "## Unmatched pages (no cluster assigned)",
        "",
        "_These pages didn't match any known cluster. Add them to the radar seeds or reclassify manually._",
        "",
    ]
    for u in unmatched:
        lines.append(f"- `{u}`")
    lines.append("")

lines += [
    "---",
    "",
    f"> **Next step:** Add new leaf slugs to the appropriate cluster and run the auto-cluster engine.",
    f"> Questions? Text PJ: {PHONE}",
]

OUT_MD.write_text("\n".join(lines), encoding="utf-8")

# ── Console summary ───────────────────────────────────────────────────────────
print(f"Cluster expansion plan generated")
print(f"  Input pages : {len(input_pages)}")
print(f"  Clusters hit: {len(cluster_hits)}")
print(f"  Unmatched   : {len(unmatched)}")
print()
for cluster_key, hits in sorted_clusters:
    meta = cluster_meta.get(cluster_key, {})
    _, rec = expansion_rec(len(hits), meta.get("pages", 0) if isinstance(meta.get("pages"), int) else 0)
    print(f"  {cluster_key:<28} hits={len(hits)}  → {rec}")
print()
print(f"Outputs:")
print(f"  {OUT_MD.relative_to(ROOT)}")
print(f"  {OUT_TSV.relative_to(ROOT)}")
