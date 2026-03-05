#!/usr/bin/env python3
"""
SideGuy Self-Expanding SEO Tree Engine
----------------------------------------
Merges three signal sources into a prioritised BUILD_QUEUE:
  1. GSC export (real impression + position data)
  2. trends_notes.txt  (emerging topics)
  3. manual_seeds.txt  (things PJ wants to own)

Data lives in the canonical locations:
  docs/traffic-intel/gsc_export_template.csv
  docs/problem-radar/trends_notes.txt
  docs/problem-radar/manual_seeds.txt

Outputs to expansion/ (created if missing):
  expansion/BUILD_QUEUE.md
  expansion/SEED_CANDIDATES.tsv
  expansion/CLAUDE_PROMPT.md
  expansion/NEXT_ACTIONS.md

Usage:
  python3 scripts/seo-tree-engine.py
"""

import csv, os, re, datetime
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
NOW  = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

# ── Canonical input paths ─────────────────────────────────────────────────────
GSC    = ROOT / "docs" / "traffic-intel" / "gsc_export_template.csv"
TRENDS = ROOT / "docs" / "problem-radar" / "trends_notes.txt"
MANUAL = ROOT / "docs" / "problem-radar" / "manual_seeds.txt"

OUT_DIR    = ROOT / "expansion"
OUT_QUEUE  = OUT_DIR / "BUILD_QUEUE.md"
OUT_SEEDS  = OUT_DIR / "SEED_CANDIDATES.tsv"
OUT_PROMPT = OUT_DIR / "CLAUDE_PROMPT.md"
OUT_NEXT   = OUT_DIR / "NEXT_ACTIONS.md"

OUT_DIR.mkdir(exist_ok=True)

# ── Scoring knobs ─────────────────────────────────────────────────────────────
MIN_IMP       = 5         # include pages with ≥5 GSC impressions
POS_BONUS_20  = 200       # within page 2 — fastest to rank
POS_BONUS_30  = 80        # page 3 — near-ranking
TREND_BASE    = 120
MANUAL_BASE   = 90
BIZ_BONUS     = 40

BIZ_WORDS = [
    "cost", "calculator", "fees", "repair", "price", "install", "quote",
    "near me", "best", "compare", "rate", "demo", "setup", "integration",
    "savings", "alternatives", "checklist", "guide",
]

PHONE = "773-544-1231"
SMS   = "sms:+17735441231"

# ── Cluster rules ─────────────────────────────────────────────────────────────
CLUSTERS = [
    ("payments",           re.compile(r"payment|merchant|processing|stripe|terminal|pos|gateway|chargeback|credit.card|fee", re.I)),
    ("ai-automation",      re.compile(r"\bai\b|automation|agent|workflow|zapier|make\.com|integrat|blueprint|llm|gpt|scheduling", re.I)),
    ("operator-tools",     re.compile(r"operator|playbook|checklist|template|toolkit|runbook|calculator", re.I)),
    ("crypto-web3",        re.compile(r"crypto|solana|wallet|web3|stablecoin|token|bitcoin|usdc", re.I)),
    ("energy-ev",          re.compile(r"\bev\b|charger|charging|tesla|level\s*2|nema|j1772|supercharger|solar|rebate", re.I)),
    ("home-systems",       re.compile(r"hvac|ac\b|air.condition|furnace|thermostat|heat.pump|mini.?split|plumbing", re.I)),
    ("business-software",  re.compile(r"crm|erp|inventory|accounting|quickbooks|saas|billing|software|xero", re.I)),
    ("local-seo",          re.compile(r"seo|google.business|gmb|maps|local.search|review", re.I)),
    ("prediction-markets", re.compile(r"kalshi|polymarket|prediction.market|odds|hedge", re.I)),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:90].strip("-")

def classify(text: str) -> str:
    for name, rx in CLUSTERS:
        if rx.search(text):
            return name
    return "uncategorized"

def biz_bonus(text: str) -> int:
    t = text.lower()
    return BIZ_BONUS if any(w in t for w in BIZ_WORDS) else 0

def title_variants(seed: str):
    base = seed.strip()
    return [
        (f"{base} (Cost, Options, & Fixes)",          slugify(f"{base} cost options fixes")),
        (f"{base}: What to Do First",                  slugify(f"{base} what to do first")),
        (f"{base} — Common Causes & Quick Checks",     slugify(f"{base} common causes quick checks")),
        (f"{base}: Cheapest Path to Clarity",          slugify(f"{base} cheapest path to clarity")),
        (f"{base}: Best Next Steps (No Hype)",         slugify(f"{base} best next steps no hype")),
    ]

# ── Load GSC seeds ────────────────────────────────────────────────────────────
gsc_seeds = []
if GSC.exists():
    with open(GSC, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            q   = (row.get("top_query") or "").strip()
            url = (row.get("url")       or "").strip()
            if not q:
                continue
            try:
                imp = int(float(row.get("impressions", "0") or "0"))
                pos = float(row.get("position", "99") or "99")
            except Exception:
                continue
            if imp < MIN_IMP or pos > 35:
                continue
            bonus = POS_BONUS_20 if pos <= 20 else POS_BONUS_30
            score = imp + bonus + biz_bonus(q)
            gsc_seeds.append(("gsc", q, score, url, imp, round(pos, 2)))

# ── Load trend seeds ──────────────────────────────────────────────────────────
trend_seeds = []
if TRENDS.exists():
    for line in TRENDS.read_text(encoding="utf-8").splitlines():
        t = line.strip()
        if t and not t.startswith("#"):
            trend_seeds.append(("trend", t, TREND_BASE + biz_bonus(t), "", 0, 0.0))

# ── Load manual seeds ─────────────────────────────────────────────────────────
manual_seeds = []
if MANUAL.exists():
    for line in MANUAL.read_text(encoding="utf-8").splitlines():
        t = line.strip()
        if t and not t.startswith("#"):
            manual_seeds.append(("manual", t, MANUAL_BASE + biz_bonus(t), "", 0, 0.0))

all_seeds = gsc_seeds + trend_seeds + manual_seeds

# ── Classify into clusters ────────────────────────────────────────────────────
by_cluster: dict[str, list] = defaultdict(list)
for src, seed, score, url, imp, pos in all_seeds:
    cluster = classify(f"{seed} {url}")
    by_cluster[cluster].append({
        "source": src, "seed": seed, "score": int(score),
        "url": url, "impressions": imp, "position": pos,
    })

# Cluster rollup sorted by total score
cluster_rollup = sorted(
    [
        (c, sum(x["score"] for x in items), len(items))
        for c, items in by_cluster.items()
    ],
    key=lambda x: (-x[1], -x[2]),
)

# ── Write SEED_CANDIDATES.tsv ─────────────────────────────────────────────────
with open(OUT_SEEDS, "w", encoding="utf-8") as f:
    f.write("cluster\tsource\tscore\tseed\turl\timpressions\tposition\n")
    for c, total, n in cluster_rollup:
        for x in sorted(by_cluster[c], key=lambda z: (-z["score"], z["seed"].lower())):
            f.write(f"{c}\t{x['source']}\t{x['score']}\t{x['seed']}\t"
                    f"{x['url']}\t{x['impressions']}\t{x['position']}\n")

# ── Write BUILD_QUEUE.md ──────────────────────────────────────────────────────
lines = [
    "# SideGuy BUILD_QUEUE — Self-Expanding SEO Tree Engine",
    "",
    f"Generated: {NOW}",
    f"Sources: GSC={len(gsc_seeds)}  trends={len(trend_seeds)}  manual={len(manual_seeds)}  total={len(all_seeds)}",
    "",
    "Scoring:",
    "- GSC: impressions + position bonus (≤20 → +200, ≤35 → +80)",
    "- Trend seeds: +120 base",
    "- Manual seeds: +90 base",
    "- Business-intent words: +40 bonus",
    "",
    "## Priority clusters (highest signal first)",
    "",
]

for i, (c, total, n) in enumerate(cluster_rollup[:14], 1):
    top = sorted(by_cluster[c], key=lambda z: (-z["score"], z["seed"].lower()))
    lines += [
        f"### {i}. {c} — total score **{total}** · {n} seeds",
        "",
    ]
    for x in top[:6]:
        extra = ""
        if x["source"] == "gsc":
            extra = f" | imp {x['impressions']} | pos {x['position']} | `{x['url']}`"
        lines.append(f"- **{x['seed']}** _(src: {x['source']}, score: {x['score']}){extra}_")
    lines.append("")

    if top:
        seed = top[0]["seed"]
        lines.append("**5 page title / slug variants for top seed:**")
        for title, slug in title_variants(seed):
            lines.append(f"- {title}")
            lines.append(f"  - `{slug}.html`")
        lines.append("")

    lines.append("---")
    lines.append("")

# ── Write CLAUDE_PROMPT.md ────────────────────────────────────────────────────
prompt_lines = [
    "# Claude Build Prompt — SideGuy Self-Expanding SEO Tree",
    "",
    "You are working in /workspaces/sideguy-solutions.",
    "Goal: expand ONLY the highest-signal clusters from BUILD_QUEUE.md.",
    "",
    "**Rules:**",
    "- SideGuy tone: calm, friendly, clarity-before-cost. No hype.",
    f"- Every page must include Text PJ CTA: {PHONE} / [{SMS}]({SMS})",
    "- Every new leaf links up to its cluster hub and at least 2–3 siblings.",
    "- Prefer tools, checklists, and calculators where the topic warrants it.",
    "- Inline CSS only (no external stylesheets).",
    "- Add canonical, meta description, BreadcrumbList schema, FAQPage schema.",
    "",
    "**Build targets (top clusters):**",
    "",
]
for c, total, n in cluster_rollup[:6]:
    prompt_lines.append(f"## {c}  (score {total})")
    for x in sorted(by_cluster[c], key=lambda z: (-z["score"], z["seed"].lower()))[:8]:
        prompt_lines.append(f"- {x['seed']}")
    prompt_lines.append("")

prompt_lines += [
    "**Deliverables per cluster:**",
    "- 10–25 new leaf pages (scale with score)",
    "- Update cluster hub (add new page links)",
    "- Update category hub (add cluster chip if missing)",
    "- Wire internal links: hub ⇄ leaf ⇄ sibling leaves",
]

# ── Write NEXT_ACTIONS.md ─────────────────────────────────────────────────────
next_lines = [
    "# NEXT ACTIONS — Weekly SideGuy Growth Loop",
    "",
    "1. GSC → Performance → Pages → Last 28 days → Export CSV",
    "2. Paste rows into `docs/traffic-intel/gsc_export_template.csv` (skip original header)",
    "3. Add 5–20 emerging topics to `docs/problem-radar/trends_notes.txt`",
    "4. Add 3–10 priority seeds to `docs/problem-radar/manual_seeds.txt`",
    "5. Run: `python3 scripts/seo-tree-engine.py`",
    "6. Open `expansion/BUILD_QUEUE.md` — work top-down",
    "7. Paste `expansion/CLAUDE_PROMPT.md` into Claude to generate pages",
    "8. Commit + push",
    "",
    "Repeat weekly.",
]

# ── Write all outputs ─────────────────────────────────────────────────────────
OUT_QUEUE.write_text("\n".join(lines),        encoding="utf-8")
OUT_PROMPT.write_text("\n".join(prompt_lines), encoding="utf-8")
OUT_NEXT.write_text("\n".join(next_lines),    encoding="utf-8")

# ── Console summary ───────────────────────────────────────────────────────────
print("SEO Tree Engine complete.")
print(f"  GSC seeds   : {len(gsc_seeds)}")
print(f"  Trend seeds : {len(trend_seeds)}")
print(f"  Manual seeds: {len(manual_seeds)}")
print(f"  Total seeds : {len(all_seeds)}")
print(f"  Clusters    : {len(cluster_rollup)}")
print()
for c, total, n in cluster_rollup[:10]:
    print(f"  {c:<28} score={total:>5}  seeds={n}")
print()
print(f"Wrote: {OUT_QUEUE.relative_to(ROOT)}")
print(f"       {OUT_SEEDS.relative_to(ROOT)}")
print(f"       {OUT_PROMPT.relative_to(ROOT)}")
print(f"       {OUT_NEXT.relative_to(ROOT)}")
