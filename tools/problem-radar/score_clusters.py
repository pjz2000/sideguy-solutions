#!/usr/bin/env python3
"""
SideGuy Problem Radar — Cluster Scorer
----------------------------------------
Reads radar-signals.tsv, groups rows by seed topic, and produces a
priority-ranked list of clusters to build next.

Scoring factors (all contribute to composite_score):
  avg_signal_score  — median quality of signals in the cluster (from TSV)
  signal_count      — breadth (log-scaled bonus; more variations = stronger demand)
  pillar_fit        — alignment with SideGuy's core content pillars (0–10)
  coverage_penalty  — deduction if a root-level page already covers this cluster

Output:
  docs/problem-radar/cluster-rankings.tsv   — machine-readable
  docs/problem-radar/cluster-rankings.md    — human-readable markdown table
"""

import csv
import math
from pathlib import Path
from collections import defaultdict

# ── paths ────────────────────────────────────────────────────────────────────
ROOT        = Path(__file__).parent.parent.parent.resolve()
TSV_IN      = ROOT / "docs" / "problem-radar" / "radar-signals.tsv"
TSV_OUT     = ROOT / "docs" / "problem-radar" / "cluster-rankings.tsv"
MD_OUT      = ROOT / "docs" / "problem-radar" / "cluster-rankings.md"

# ── pillar alignment map ──────────────────────────────────────────────────────
# Buckets that appear in the TSV → SideGuy pillar fit score (0–10)
PILLAR_FIT = {
    "payments":   10,   # core pillar
    "automation": 10,   # core pillar (AI automation)
    "ai":         10,
    "energy":      8,   # HVAC, EV, solar
    "hvac":        8,
    "crypto":      7,
    "local":       6,
    "money":       9,   # commercial intent, high conversion value
    "home":        7,
    "legal":       5,
    "health":      6,
    "software":    7,
}
DEFAULT_PILLAR_FIT = 4


def pillar_score(bucket: str) -> int:
    if not bucket:
        return DEFAULT_PILLAR_FIT
    for key, val in PILLAR_FIT.items():
        if key in bucket.lower():
            return val
    return DEFAULT_PILLAR_FIT


# ── page coverage check ───────────────────────────────────────────────────────
def page_exists_for_seed(seed: str) -> bool:
    """Check if any root HTML page roughly covers this seed topic."""
    slug = seed.lower().strip().replace(" ", "-").replace("/", "-")
    # Direct match
    if (ROOT / f"{slug}-san-diego.html").exists():
        return True
    if (ROOT / f"{slug}.html").exists():
        return True
    # Partial match: check if slug words all appear in any root html filename
    words = [w for w in slug.split("-") if len(w) > 3]
    if len(words) >= 2:
        for f in ROOT.glob("*.html"):
            name = f.stem.lower()
            if all(w in name for w in words[:3]):
                return True
    return False


# ── read TSV ──────────────────────────────────────────────────────────────────
clusters: dict[str, dict] = defaultdict(lambda: {
    "scores": [],
    "buckets": set(),
    "signal_types": set(),
    "count": 0,
})

skipped = 0
with open(TSV_IN, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        seed = (row.get("seed") or row.get("topic") or "").strip()
        if not seed:
            skipped += 1
            continue
        try:
            score = float(row.get("score") or 0)
        except ValueError:
            score = 0.0
        bucket = (row.get("bucket") or "").strip().lower()
        sig_type = (row.get("signal_type") or "").strip().lower()

        c = clusters[seed]
        c["scores"].append(score)
        c["buckets"].add(bucket)
        c["signal_types"].add(sig_type)
        c["count"] += 1

# ── score each cluster ────────────────────────────────────────────────────────
ranked = []
for seed, data in clusters.items():
    scores = data["scores"]
    avg    = sum(scores) / len(scores) if scores else 0
    best   = max(scores) if scores else 0
    count  = data["count"]

    # signal_count bonus: log2 scale, capped
    count_bonus = min(math.log2(count + 1) * 4, 20)

    # best pillar fit across all buckets for this cluster
    fit = max((pillar_score(b) for b in data["buckets"]), default=DEFAULT_PILLAR_FIT)

    # coverage penalty: if we already have a page, deprioritize
    covered = page_exists_for_seed(seed)
    coverage_penalty = 15 if covered else 0

    composite = round(avg + count_bonus + fit - coverage_penalty, 1)

    ranked.append({
        "seed":            seed,
        "composite_score": composite,
        "avg_signal_score": round(avg, 1),
        "best_signal_score": round(best, 1),
        "signal_count":    count,
        "pillar_fit":      fit,
        "buckets":         "|".join(sorted(b for b in data["buckets"] if b)),
        "signal_types":    "|".join(sorted(t for t in data["signal_types"] if t)),
        "page_exists":     "yes" if covered else "no",
    })

ranked.sort(key=lambda x: x["composite_score"], reverse=True)

# ── write TSV ─────────────────────────────────────────────────────────────────
fieldnames = [
    "rank", "composite_score", "seed", "avg_signal_score", "best_signal_score",
    "signal_count", "pillar_fit", "page_exists", "buckets", "signal_types",
]
with open(TSV_OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
    writer.writeheader()
    for i, row in enumerate(ranked, 1):
        row["rank"] = i
        writer.writerow(row)

# ── write markdown ────────────────────────────────────────────────────────────
TOP_N = 50
lines = [
    "# SideGuy Problem Radar — Cluster Priority Rankings",
    "",
    f"_Generated 2026-03-10 · {len(ranked)} clusters scored · top {TOP_N} shown_",
    "",
    "**Composite score** = avg signal quality + signal breadth bonus + pillar fit − coverage penalty",
    "",
    "| Rank | Score | Cluster Topic | Signals | Pillar Fit | Has Page | Buckets |",
    "|-----:|------:|---------------|--------:|-----------:|----------|---------|",
]
for row in ranked[:TOP_N]:
    page_badge = "✅" if row["page_exists"] == "yes" else "🔲"
    lines.append(
        f"| {row['rank']} "
        f"| {row['composite_score']} "
        f"| {row['seed']} "
        f"| {row['signal_count']} "
        f"| {row['pillar_fit']} "
        f"| {page_badge} "
        f"| {row['buckets']} |"
    )

lines += [
    "",
    "## Build Recommendations",
    "",
    "**Top 5 uncovered clusters** (no root page yet, highest composite score):",
    "",
]
uncovered = [r for r in ranked if r["page_exists"] == "no"][:5]
for i, row in enumerate(uncovered, 1):
    lines.append(f"{i}. **{row['seed']}** — score {row['composite_score']}, {row['signal_count']} signals, buckets: {row['buckets']}")

lines += [
    "",
    "**Top 5 clusters with existing pages** (candidates for hub-depth upgrade):",
    "",
]
covered = [r for r in ranked if r["page_exists"] == "yes"][:5]
for i, row in enumerate(covered, 1):
    lines.append(f"{i}. **{row['seed']}** — score {row['composite_score']}, {row['signal_count']} signals")

lines.append("")
MD_OUT.write_text("\n".join(lines), encoding="utf-8")

# ── console output ────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"SideGuy Cluster Rankings — {len(ranked)} clusters scored")
print(f"{'='*60}")
print(f"{'Rank':<5} {'Score':<7} {'Signals':<8} {'Page?':<6} Cluster")
print("-" * 60)
for row in ranked[:20]:
    flag = "✓" if row["page_exists"] == "yes" else " "
    print(f"{row['rank']:<5} {row['composite_score']:<7} {row['signal_count']:<8} {flag:<6} {row['seed']}")

print(f"\n{'='*60}")
print(f"Top 5 clusters to BUILD (no page yet):")
for i, row in enumerate(uncovered, 1):
    print(f"  {i}. {row['seed']}  [{row['buckets']}]  score={row['composite_score']}")

print(f"\nTop 5 clusters to DEEPEN (page exists, high demand):")
for i, row in enumerate(covered, 1):
    print(f"  {i}. {row['seed']}  [{row['buckets']}]  score={row['composite_score']}")

print(f"\nFull rankings → {TSV_OUT.relative_to(ROOT)}")
print(f"Markdown report → {MD_OUT.relative_to(ROOT)}")
print(f"(skipped {skipped} rows with no seed)")
