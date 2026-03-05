#!/usr/bin/env python3
"""
SideGuy Traffic Radar — Problem Radar AI
-----------------------------------------
Detects + prioritizes new problem clusters BEFORE competitors using:
  - Google Search Console export (real demand signal)
  - docs/problem-radar/trends_notes.txt  (emerging topics you paste in)
  - docs/problem-radar/manual_seeds.txt  (things you personally want to own)

Outputs:
  docs/problem-radar/generated/RADAR_QUEUE.md    — prioritized build plan
  docs/problem-radar/generated/CLAUDE_PROMPT.md  — paste to Claude to generate pages
  docs/problem-radar/generated/NEXT_ACTIONS.md   — weekly workflow reminder
  docs/problem-radar/generated/seeds_classified.tsv

Usage:
  python3 scripts/traffic-radar.py
"""

import csv, json, os, re
from collections import defaultdict
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ROOT = "."

GSC_CSV    = "docs/traffic-intel/gsc_export_template.csv"
TRENDS_TXT = "docs/problem-radar/trends_notes.txt"
MANUAL_TXT = "docs/problem-radar/manual_seeds.txt"
RULES_FILE = "docs/auto-cluster/rules.tsv"
OUT_DIR    = "docs/problem-radar/generated"

MIN_IMPRESSIONS = 50
MAX_POSITION    = 35
FINAL_TOP_SEEDS = 250
PAGES_PER_SEED  = 12

PHONE     = "773-544-1231"
PHONE_SMS = "sms:+17735441231"

os.makedirs("docs/problem-radar", exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────
# Create input templates if missing
# ─────────────────────────────────────────────────────
if not os.path.exists(TRENDS_TXT):
    with open(TRENDS_TXT, "w") as f:
        f.write("# Paste emerging topics here (one per line).\n"
                "# Examples:\n"
                "# ai receptionist for plumbers\n"
                "# stripe chargebacks rising\n"
                "# tesla charging slow after update\n"
                "# heat pump freezing at night\n"
                "# solana payments instant settlement\n")
    print(f"Created: {TRENDS_TXT}")

if not os.path.exists(MANUAL_TXT):
    with open(MANUAL_TXT, "w") as f:
        f.write("# Manual seeds — things you want SideGuy to own (one per line).\n"
                "# Examples:\n"
                "# ai automation for restaurants\n"
                "# payment processing savings calculator\n"
                "# hvac troubleshooting decision tree\n"
                "# crypto wallet safety checklist\n")
    print(f"Created: {MANUAL_TXT}")

# ─────────────────────────────────────────────────────
# Load classification rules from rules.tsv
# ─────────────────────────────────────────────────────
rules = []
if os.path.exists(RULES_FILE):
    with open(RULES_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            pat, pillar, cluster, ctitle = parts[0], parts[1], parts[2], parts[3]
            try:
                rules.append((re.compile(pat, re.IGNORECASE), pillar, cluster, ctitle))
            except re.error:
                pass

# Fallback rules (always appended last)
for pat, p, c, ct in [
    (r"ai.{0,25}cost|automation.{0,25}cost|ai.{0,25}roi",     "ai-automation", "ai-cost",             "AI Automation Cost & ROI"),
    (r"schedul|booking.{0,25}ai|appointment.{0,25}automat",   "ai-automation", "ai-scheduling",        "AI Scheduling & Booking"),
    (r"customer.service.{0,25}ai|chatbot",                     "ai-automation", "ai-customer-service",  "AI Customer Service"),
    (r"zapier|make\.com|n8n|workflow.automat",                 "ai-automation", "ai-tools",             "AI Automation Tools"),
    (r"ai.automat",                                            "ai-automation", "ai-overview",          "AI Automation (Overview)"),
    (r"chargeback|dispute.{0,25}payment",                      "payments",      "chargebacks",          "Chargebacks & Disputes"),
    (r"stripe",                                                "payments",      "stripe",               "Stripe Troubleshooting"),
    (r"payment|credit.card.{0,25}process|merchant",           "payments",      "payments-overview",    "Payment Processing (Overview)"),
    (r"hvac|heat.pump|furnace|air.handler",                   "home-systems",  "hvac",                 "HVAC Troubleshooting"),
    (r"air.condition|ac.not|ac.cool",                         "home-systems",  "ac-problems",          "AC Problems"),
    (r"tesla|ev.charg|supercharger|level.2.charg",            "energy-ev",     "ev-charging",          "EV Charging & Tesla Charging"),
    (r"bitcoin|crypto|solana|usdc|stablecoin|wallet|web3",    "crypto-web3",   "wallets",              "Crypto Wallets & Safety"),
    (r"kalshi|polymarket|prediction.market",                  "prediction-markets", "overview",        "Prediction Markets (Overview)"),
    (r"calculator|checklist|worksheet",                       "operator-tools","tools",                "Operator Tools"),
]:
    rules.append((re.compile(pat, re.IGNORECASE), p, c, ct))

def classify(seed):
    for rgx, pillar, cluster, ctitle in rules:
        if rgx.search(seed):
            return pillar, cluster, ctitle
    return "problem-intelligence", "general", "General Problems"

def normalize(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

# ─────────────────────────────────────────────────────
# Ingest seeds
# ─────────────────────────────────────────────────────
seed_map = {}

def upsert(src, raw, impressions=0, position=0.0, url=""):
    key = normalize(raw)
    if not key:
        return
    ex = seed_map.get(key)
    if ex is None or impressions > ex["impressions"] or \
       (impressions == ex["impressions"] and 0 < position < ex.get("position", 99)):
        seed_map[key] = {"src": src, "raw": raw, "impressions": impressions,
                         "position": position, "url": url}

gsc_count = 0
if os.path.exists(GSC_CSV):
    with open(GSC_CSV, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = next(csv.reader([line]))
            if len(parts) < 6:
                continue
            try:
                imp  = float(parts[2].replace(",", ""))
                pos  = float(parts[5].replace(",", ""))
                url  = parts[6].strip() if len(parts) > 6 else ""
                qry  = parts[7].strip() if len(parts) > 7 else ""
            except (ValueError, IndexError):
                continue
            seed = qry or url
            if imp >= MIN_IMPRESSIONS and 0 < pos <= MAX_POSITION and seed:
                upsert("gsc", seed, int(imp), pos, url)
                gsc_count += 1

trend_count = 0
if os.path.exists(TRENDS_TXT):
    with open(TRENDS_TXT) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                upsert("trend", line)
                trend_count += 1

manual_count = 0
if os.path.exists(MANUAL_TXT):
    with open(MANUAL_TXT) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                upsert("manual", line)
                manual_count += 1

print(f"Seeds — GSC:{gsc_count}  trends:{trend_count}  manual:{manual_count}  unique:{len(seed_map)}")

# ─────────────────────────────────────────────────────
# Score + classify
# ─────────────────────────────────────────────────────
INTENT_RE = re.compile(r"cost|price|calculator|best|near me|service|company|fees|chargeback|repair|install|compare|vs\b|review", re.I)

def score(src, impressions, position, seed):
    s = 0
    if src == "gsc":
        s += impressions
        s += 200 if position <= 20 else 80 if position <= 30 else 20
    elif src == "trend":
        s += 120
    elif src == "manual":
        s += 90
    else:
        s += 50
    if INTENT_RE.search(seed):
        s += 40
    return s

scored = []
for norm_seed, meta in seed_map.items():
    pillar, cluster, ctitle = classify(norm_seed)
    s = score(meta["src"], meta["impressions"], meta["position"], norm_seed)
    scored.append({
        "score": s, "src": meta["src"], "seed": norm_seed, "raw": meta["raw"],
        "impressions": meta["impressions"], "position": meta["position"],
        "pillar": pillar, "cluster": cluster, "cluster_title": ctitle, "url": meta["url"],
    })

scored.sort(key=lambda x: -x["score"])
top = scored[:FINAL_TOP_SEEDS]

# ─────────────────────────────────────────────────────
# seeds_classified.tsv
# ─────────────────────────────────────────────────────
with open(f"{OUT_DIR}/seeds_classified.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["score","src","seed","impressions","position","pillar","cluster","cluster_title","url"])
    for r in top:
        w.writerow([r["score"],r["src"],r["seed"],r["impressions"],r["position"],
                    r["pillar"],r["cluster"],r["cluster_title"],r["url"]])
print(f"  seeds_classified.tsv ({len(top)} seeds)")

cluster_buckets = defaultdict(list)
for r in top:
    cluster_buckets[(r["pillar"], r["cluster"], r["cluster_title"])].append(r)

# ─────────────────────────────────────────────────────
# RADAR_QUEUE.md
# ─────────────────────────────────────────────────────
def write_radar_queue():
    lines = [
        "# SideGuy Problem Radar Queue",
        "",
        f"Generated: {TIMESTAMP}",
        "",
        "Prioritized by: GSC impressions + near-ranking position + trend signal + business intent.",
        "",
        "## Signal summary",
        "",
        "| Source | Seeds |",
        "|--------|-------|",
        f"| GSC export | {gsc_count} |",
        f"| Trends/notes | {trend_count} |",
        f"| Manual seeds | {manual_count} |",
        f"| **Total unique** | **{len(seed_map)}** |",
        f"| Top seeds in queue | {len(top)} |",
        "",
    ]
    if not gsc_count:
        lines += [
            "> **Demo mode** — GSC file has no data rows yet.",
            "> Add rows to `docs/traffic-intel/gsc_export_template.csv` and re-run.",
            "> Column order: `date_range,type,impressions,clicks,ctr,position,url,top_query`",
            "",
        ]
    lines += ["---", "", "## Build queue — by cluster", ""]

    for (pillar, cluster, ctitle), seeds in sorted(cluster_buckets.items(),
            key=lambda x: -sum(s["score"] for s in x[1])):
        total_score = sum(s["score"] for s in seeds)
        total_imp   = sum(s["impressions"] for s in seeds)
        pos_vals    = [s["position"] for s in seeds if s["position"] > 0]
        avg_pos     = round(sum(pos_vals)/len(pos_vals), 1) if pos_vals else "—"

        lines += [
            f"### {ctitle}",
            f"**Pillar:** `{pillar}`  **Cluster:** `{cluster}`  "
            f"**Score:** {total_score}  **Impr:** {total_imp:,}  "
            f"**Avg pos:** {avg_pos}  **Seeds:** {len(seeds)}",
            "",
            f"**Hub:** `auto-hubs/clusters/{pillar}--{cluster}.html`",
            f"**New leaf targets:** {max(4, len(seeds)*2)}–{len(seeds)*PAGES_PER_SEED//3}",
            "",
            "**Seeds:**",
        ]
        for s in sorted(seeds, key=lambda x: -x["score"])[:15]:
            tag = f'{s["impressions"]:,} imp @ pos {s["position"]}' if s["impressions"] else s["src"]
            lines.append(f'- `{s["seed"]}` — {tag}')
        if len(seeds) > 15:
            lines.append(f"- *(+{len(seeds)-15} more in seeds_classified.tsv)*")
        lines += ["", "---", ""]

    with open(f"{OUT_DIR}/RADAR_QUEUE.md", "w") as f:
        f.write("\n".join(lines) + "\n")

write_radar_queue()
print(f"  RADAR_QUEUE.md  ({len(cluster_buckets)} clusters)")

# ─────────────────────────────────────────────────────
# CLAUDE_PROMPT.md
# ─────────────────────────────────────────────────────
def page_variants(seed):
    slug = re.sub(r"[^a-z0-9]+", "-", seed.lower()).strip("-")
    s = seed.strip()
    return [
        (f"{s.title()} — What to Know First",        f"{slug}-san-diego.html"),
        (f"{s.title()} Cost in San Diego",           f"{slug}-cost-san-diego.html"),
        (f"Best Tools for {s.title()}",              f"best-{slug}-san-diego.html"),
        (f"Common {s.title()} Mistakes",             f"{slug}-mistakes-san-diego.html"),
        (f"{s.title()} Checklist (San Diego)",       f"{slug}-checklist-san-diego.html"),
        (f"How to Handle {s.title()} in San Diego",  f"how-to-{slug}-san-diego.html"),
    ]

def write_claude_prompt():
    lines = [
        "# Claude Prompt — SideGuy Problem Radar Expansion",
        "",
        f"Generated: {TIMESTAMP}",
        "",
        "---",
        "",
        "You are operating inside the SideGuy repo.",
        "Goal: build the most friendly, intelligent SEO knowledge platform in San Diego.",
        "",
        "## Operating principles (non-negotiable)",
        "",
        "- **Pyramid structure:** Pillar → Category → Cluster → Leaf",
        "- **Dense internal linking:** leaf→cluster→pillar + cluster↔cluster See Also",
        "- **No orphan pages** — every new page links up and sideways",
        "- **Friendly clarity blocks on every leaf:**",
        "  1. Quick answer (2–3 sentences)",
        "  2. Why this happens",
        "  3. What people misunderstand",
        "  4. Simple next steps (numbered)",
        f"  5. Text PJ CTA: [{PHONE}]({PHONE_SMS})",
        "- **Voice:** calm smart friend, non-jargony",
        "- **Inline CSS only** — no external stylesheets",
        f"- **Phone:** {PHONE} / {PHONE_SMS}  ← use this, NOT 773-544-1231",
        "",
        "## Page template",
        "",
        "```html",
        "<!doctype html><html lang='en'><head>",
        "  <title>[Problem] in San Diego — SideGuy Solutions</title>",
        "  <meta name='description' content='[~150 char calm actionable]'/>",
        "  <!-- BreadcrumbList JSON-LD -->",
        "  <!-- inline CSS :root vars --></head>",
        "<body>",
        "  <h1>[Problem] — What to Check First</h1>",
        "  <section>Quick Answer</section>",
        "  <section>Why This Happens</section>",
        "  <section>Common Misunderstandings</section>",
        "  <section>Next Steps</section>",
        "  <!-- sideguy-related-problems nav (5 same-cluster links) -->",
        "  <!-- Text PJ CTA -->",
        "</body></html>",
        "```",
        "",
        f"## Build {PAGES_PER_SEED} leaf pages per seed, using these variants:",
        "explained / cost / tools / mistakes / checklist / comparison / how-to / what-to-do-next",
        "",
        "---",
        "",
        "## Top radar seeds — build these first",
        "",
    ]

    for (pillar, cluster, ctitle), seeds in sorted(cluster_buckets.items(),
            key=lambda x: -sum(s["score"] for s in x[1]))[:20]:
        lines += [f"### {ctitle}  (`{pillar}/{cluster}`)", ""]
        for s in sorted(seeds, key=lambda x: -x["score"])[:5]:
            lines.append(f"**Seed:** `{s['seed']}`")
            for title, slug in page_variants(s["seed"])[:4]:
                lines.append(f"- {title} → `{slug}`")
            lines.append("")
        lines += ["---", ""]

    with open(f"{OUT_DIR}/CLAUDE_PROMPT.md", "w") as f:
        f.write("\n".join(lines) + "\n")

write_claude_prompt()
print(f"  CLAUDE_PROMPT.md")

# ─────────────────────────────────────────────────────
# NEXT_ACTIONS.md
# ─────────────────────────────────────────────────────
with open(f"{OUT_DIR}/NEXT_ACTIONS.md", "w") as f:
    f.write(f"""# Next Actions — Problem Radar AI

Generated: {TIMESTAMP}

## Weekly workflow

### Step 1 — Paste new signals
- Emerging topics → `{TRENDS_TXT}`
- Things you want to own → `{MANUAL_TXT}`
- GSC export → `{GSC_CSV}`
  - GSC: Performance → Pages → Last 28 days → Export CSV
  - Column order: `date_range,type,impressions,clicks,ctr,position,url,top_query`

### Step 2 — Re-run
```bash
python3 scripts/traffic-radar.py
```

### Step 3 — Feed Claude
Copy `docs/problem-radar/generated/CLAUDE_PROMPT.md` into a new Claude conversation.

### Step 4 — Build top cluster targets
Work top-to-bottom in `docs/problem-radar/generated/RADAR_QUEUE.md`.

### Step 5 — Improve rules over time
Better classification accuracy → edit `{RULES_FILE}`
- Add more specific patterns ABOVE general ones
- Re-run after editing

---

## Next engine: Cluster Gap Finder
Detects clusters with GSC traffic but weak hub pages → auto-prioritizes hub upgrades.
""")
print(f"  NEXT_ACTIONS.md")

print()
print("─" * 50)
print("SIDEGUY PROBLEM RADAR AI COMPLETE")
print(f"  Queue:         {OUT_DIR}/RADAR_QUEUE.md")
print(f"  Claude prompt: {OUT_DIR}/CLAUDE_PROMPT.md")
print(f"  Next actions:  {OUT_DIR}/NEXT_ACTIONS.md")
print(f"  TSV:           {OUT_DIR}/seeds_classified.tsv")
print("─" * 50)
