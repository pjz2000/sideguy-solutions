#!/usr/bin/env python3
"""
SideGuy Tools + Intelligence Engine
-------------------------------------
1. Creates tools/ directory with 8 styled decision-tool pages + index
2. Injects Tools block into auto-hubs/categories/ hubs
3. Builds problem-radar signals TSV from seed problems
4. Builds knowledge-graph site inventory
5. Writes authority-flow report and expansion queue
"""

import os, re, csv, json, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
NOW  = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

PHONE     = "773-544-1231"
SMS_LINK  = "sms:+17735441231"
SITE      = "https://sideguysolutions.com"
MINT      = "#21d3a1"

# ── Tool definitions ──────────────────────────────────────────────────────────
TOOLS = [
    {
        "slug":  "payments-fee-calculator",
        "title": "Payments Fee Calculator",
        "desc":  "Estimate what you're actually paying in merchant fees—and whether switching processors makes sense.",
        "cluster": "payments",
        "cluster_hub": "/auto-hubs/categories/payments.html",
        "fields": [
            ("Monthly volume ($)", "volume", "number", "10000"),
            ("Current rate (%)", "rate", "number", "2.9"),
            ("Monthly flat fees ($)", "fees", "number", "10"),
        ],
        "formula": "Total cost = volume × (rate/100) + fees",
        "why": "Most operators don't know their effective rate. This gets you to a real number before calling anyone.",
    },
    {
        "slug":  "chargeback-cost-estimator",
        "title": "Chargeback Cost Estimator",
        "desc":  "See the true cost of chargebacks—fee, merchandise, and time—before deciding whether to fight them.",
        "cluster": "payments",
        "cluster_hub": "/auto-hubs/categories/payments.html",
        "fields": [
            ("Chargebacks per month", "count", "number", "3"),
            ("Average transaction ($)", "avg", "number", "120"),
            ("Chargeback fee per dispute ($)", "cbfee", "number", "25"),
        ],
        "formula": "Monthly loss = count × (avg + cbfee)",
        "why": "Understanding your true chargeback cost is the first step to deciding what's worth fighting.",
    },
    {
        "slug":  "ai-automation-roi",
        "title": "AI Automation ROI Calculator",
        "desc":  "Estimate time savings and payback period before committing to an AI workflow tool.",
        "cluster": "ai-automation",
        "cluster_hub": "/auto-hubs/categories/ai-automation.html",
        "fields": [
            ("Hours saved per week", "hours", "number", "5"),
            ("Your hourly rate ($)", "rate", "number", "75"),
            ("Tool monthly cost ($)", "cost", "number", "99"),
        ],
        "formula": "Monthly value = hours × 4.33 × rate",
        "why": "AI tools are only worth buying if they save more than they cost. Start here.",
    },
    {
        "slug":  "ev-charger-cost-estimator",
        "title": "EV Charger Install Estimator",
        "desc":  "Rough-out Level 2 home or business charger costs before calling an electrician.",
        "cluster": "energy-ev",
        "cluster_hub": "/auto-hubs/categories/ev-charging.html",
        "fields": [
            ("Panel distance to garage (ft)", "dist", "number", "30"),
            ("Panel upgrade needed?", "panel", "select", "no|yes"),
            ("Number of charging stations", "stations", "number", "1"),
        ],
        "formula": "Est. cost = $800 base + $10/ft + panel upgrade ($1,500) if needed",
        "why": "Electricians vary wildly on EV quotes. This gives you a reality check before calls.",
    },
    {
        "slug":  "hvac-repair-vs-replace",
        "title": "HVAC Repair vs Replace",
        "desc":  "Use the 5,000-rule and system age to decide whether repair or replacement pencils out.",
        "cluster": "home-systems",
        "cluster_hub": "/auto-hubs/categories/hvac.html",
        "fields": [
            ("System age (years)", "age", "number", "12"),
            ("Repair quote ($)", "repair", "number", "800"),
            ("New system estimate ($)", "newcost", "number", "6000"),
        ],
        "formula": "Rule: if age × repair > new_cost, lean toward replace",
        "why": "The 5,000-rule is contractor shorthand most homeowners don't know. Now you do.",
    },
    {
        "slug":  "business-software-selector",
        "title": "Business Software Selector",
        "desc":  "Answer 5 questions and get a plain-language recommendation before evaluating vendors.",
        "cluster": "business-software",
        "cluster_hub": "/auto-hubs/categories/business-software.html",
        "fields": [
            ("Business type", "type", "text", "Restaurant"),
            ("Team size", "size", "number", "4"),
            ("Max monthly budget ($)", "budget", "number", "200"),
        ],
        "formula": "Matches against common operator profiles",
        "why": "Most software decisions are made after too many demos. This narrows it first.",
    },
    {
        "slug":  "crypto-wallet-safety-checklist",
        "title": "Crypto Wallet Safety Checklist",
        "desc":  "12-point checklist before you store or accept crypto—hardware wallet, seed phrase, and exchange risk.",
        "cluster": "crypto-web3",
        "cluster_hub": "/auto-hubs/categories/crypto-wallets.html",
        "fields": [
            ("Wallet type", "wtype", "text", "Hardware"),
            ("Stablecoin usage?", "stable", "select", "yes|no"),
            ("Holding or accepting payments?", "mode", "select", "holding|accepting"),
        ],
        "formula": "Checklist: hardware wallet, offline seed, exchange withdrawal, 2FA, test transaction",
        "why": "Most crypto losses are self-inflicted. This checklist catches the obvious ones.",
    },
    {
        "slug":  "prediction-market-hedge-matrix",
        "title": "Prediction Market Hedge Matrix",
        "desc":  "Map out correlated outcomes to find natural hedge pairs before placing positions.",
        "cluster": "prediction-markets",
        "cluster_hub": "/auto-hubs/categories/prediction-markets.html",
        "fields": [
            ("Market / event", "event", "text", "Fed rate decision"),
            ("Position size ($)", "pos", "number", "500"),
            ("Confidence (%)", "conf", "number", "65"),
        ],
        "formula": "Expected value = (confidence/100 × payout) − ((1−confidence/100) × stake)",
        "why": "Knowing your EV and natural hedges before entering is basic risk hygiene.",
    },
]

# ── HTML template ─────────────────────────────────────────────────────────────
def tool_page(t: dict) -> str:
    slug        = t["slug"]
    title_text  = t["title"]
    desc        = t["desc"]
    cluster_hub = t["cluster_hub"]
    formula     = t["formula"]
    why         = t["why"]
    canonical   = f"{SITE}/tools/{slug}.html"

    fields_html = ""
    for label, name, ftype, default in t["fields"]:
        if ftype == "select":
            opts = "".join(f'<option value="{o}">{o.title()}</option>' for o in default.split("|"))
            fields_html += f'<div class="field"><label>{label}<select name="{name}">{opts}</select></label></div>\n'
        else:
            placeholder = default
            fields_html += (
                f'<div class="field"><label>{label}'
                f'<input type="{ftype}" name="{name}" value="{placeholder}" /></label></div>\n'
            )

    schema_faq = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What does the {title_text} tool do?",
                "acceptedAnswer": {"@type": "Answer", "text": desc}
            },
            {
                "@type": "Question",
                "name": "How do I get help interpreting results?",
                "acceptedAnswer": {"@type": "Answer", "text": f"Text PJ at {PHONE} for a plain honest answer. No pitch, no contracts pressure."}
            }
        ]
    })

    schema_bc = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",          "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Tools",         "item": f"{SITE}/tools/"},
            {"@type": "ListItem", "position": 3, "name": title_text,      "item": canonical},
        ]
    })

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title_text} | SideGuy Tools · San Diego</title>
  <meta name="description" content="{desc}"/>
  <link rel="canonical" href="{canonical}"/>
  <script type="application/ld+json">{schema_bc}</script>
  <script type="application/ld+json">{schema_faq}</script>
  <style>
    :root{{--bg0:#eefcff;--ink:#073044;--mint:#21d3a1;--muted:#3f6173;--border:rgba(7,48,68,.12)}}
    *{{box-sizing:border-box}}
    body{{font-family:-apple-system,system-ui,Segoe UI,Roboto,sans-serif;
      background:radial-gradient(900px 500px at 30% 10%,rgba(33,211,161,.12),transparent 60%),
                 linear-gradient(170deg,#eefcff 0%,#d9f5f0 100%);
      color:var(--ink);margin:0;padding:0 0 60px}}
    .wrap{{max-width:720px;margin:0 auto;padding:28px 20px}}
    .bc{{font-size:.82rem;color:var(--muted);margin-bottom:18px}}
    .bc a{{color:var(--ink);text-decoration:underline}}
    .badge{{display:inline-block;padding:5px 14px;border-radius:999px;
      background:rgba(33,211,161,.15);font-size:.78rem;font-weight:700;color:var(--ink);margin-bottom:14px}}
    h1{{font-size:1.75rem;margin:0 0 8px;line-height:1.2}}
    .desc{{font-size:.96rem;color:var(--muted);margin:0 0 28px}}
    .tool-card{{background:#fff;border:1px solid var(--border);border-radius:16px;padding:24px 28px;margin-bottom:24px}}
    .field{{margin-bottom:16px}}
    label{{display:flex;flex-direction:column;gap:6px;font-size:.88rem;font-weight:600;color:var(--ink)}}
    input,select{{padding:10px 14px;border:1px solid var(--border);border-radius:10px;
      font-size:.95rem;background:#fafcfd;color:var(--ink);font-family:inherit}}
    input:focus,select:focus{{outline:2px solid var(--mint);border-color:var(--mint)}}
    .formula{{background:rgba(33,211,161,.08);border-left:3px solid var(--mint);
      padding:12px 16px;border-radius:0 8px 8px 0;font-size:.85rem;margin:20px 0 0;color:var(--muted)}}
    .why{{margin-top:24px}}
    .why-label{{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
      color:var(--muted);margin-bottom:6px}}
    .why p{{font-size:.9rem;margin:0;color:var(--ink)}}
    .cta{{margin-top:32px;background:linear-gradient(135deg,#21d3a1,#1ab88b);
      color:#073044;padding:20px 24px;border-radius:16px;font-weight:700;font-size:1rem}}
    .cta a{{color:#073044;font-weight:800}}
    .back{{font-size:.83rem;margin-top:18px}}
    .back a{{color:var(--muted);text-decoration:underline}}
  </style>
</head>
<body>
  <div class="wrap">
    <nav class="bc">
      <a href="/">Home</a> /
      <a href="{cluster_hub}">{t["cluster"].replace("-"," ").title()}</a> /
      <a href="/tools/">Tools</a> /
      {title_text}
    </nav>
    <div class="badge">SideGuy Tool</div>
    <h1>{title_text}</h1>
    <p class="desc">{desc}</p>

    <div class="tool-card">
      <form onsubmit="return false;">
        {fields_html}
        <div class="formula"><strong>How it works:</strong> {formula}</div>
      </form>
    </div>

    <div class="why">
      <div class="why-label">Why this matters</div>
      <p>{why}</p>
    </div>

    <div class="cta">
      Results confusing? <a href="{SMS_LINK}">Text PJ: {PHONE}</a> — real human, fast answer.
    </div>

    <p class="back"><a href="/tools/">← All SideGuy Tools</a></p>
  </div>
</body>
</html>
"""


def tools_index(tools: list) -> str:
    canonical = f"{SITE}/tools/"
    items_html = "\n".join(
        f'      <a class="tool-row" href="/tools/{t["slug"]}.html">\n'
        f'        <div class="tr-title">{t["title"]}</div>\n'
        f'        <div class="tr-desc">{t["desc"][:90]}…</div>\n'
        f'      </a>'
        for t in tools
    )
    schema_bc = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",  "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Tools", "item": canonical},
        ]
    })
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>SideGuy Decision Tools · San Diego</title>
  <meta name="description" content="Simple calculators and checklists that help San Diego operators make better decisions before spending money."/>
  <link rel="canonical" href="{canonical}"/>
  <script type="application/ld+json">{schema_bc}</script>
  <style>
    :root{{--bg0:#eefcff;--ink:#073044;--mint:#21d3a1;--muted:#3f6173;--border:rgba(7,48,68,.12)}}
    *{{box-sizing:border-box}}
    body{{font-family:-apple-system,system-ui,Segoe UI,Roboto,sans-serif;
      background:radial-gradient(900px 500px at 30% 10%,rgba(33,211,161,.12),transparent 60%),
                 linear-gradient(170deg,#eefcff 0%,#d9f5f0 100%);
      color:var(--ink);margin:0;padding:0 0 60px}}
    .wrap{{max-width:800px;margin:0 auto;padding:28px 20px}}
    .bc{{font-size:.82rem;color:var(--muted);margin-bottom:18px}}
    .bc a{{color:var(--ink);text-decoration:underline}}
    .badge{{display:inline-block;padding:5px 14px;border-radius:999px;
      background:rgba(33,211,161,.15);font-size:.78rem;font-weight:700;color:var(--ink);margin-bottom:14px}}
    h1{{font-size:1.85rem;margin:0 0 8px}}
    .sub{{font-size:.95rem;color:var(--muted);margin:0 0 28px}}
    .tool-list{{display:flex;flex-direction:column;gap:10px}}
    .tool-row{{display:block;background:#fff;border:1px solid var(--border);border-radius:12px;
      padding:16px 20px;text-decoration:none;color:var(--ink);transition:border-color .15s,box-shadow .15s}}
    .tool-row:hover{{border-color:var(--mint);box-shadow:0 0 0 3px rgba(33,211,161,.15)}}
    .tr-title{{font-weight:700;font-size:.97rem;margin-bottom:4px}}
    .tr-desc{{font-size:.84rem;color:var(--muted)}}
    .cta{{margin-top:36px;background:linear-gradient(135deg,#21d3a1,#1ab88b);
      color:#073044;padding:22px 26px;border-radius:16px;font-weight:700;font-size:1rem}}
    .cta a{{color:#073044;font-weight:800}}
  </style>
</head>
<body>
  <div class="wrap">
    <nav class="bc"><a href="/">Home</a> / Tools</nav>
    <div class="badge">SideGuy Tools</div>
    <h1>Decision Tools</h1>
    <p class="sub">Simple calculators and checklists. Figure things out before spending money.</p>

    <div class="tool-list">
{items_html}
    </div>

    <div class="cta">
      Not sure which tool to use? <a href="{SMS_LINK}">Text PJ: {PHONE}</a> — real human, fast answer.
    </div>
  </div>
</body>
</html>
"""


# ── Write tool pages ──────────────────────────────────────────────────────────
tools_dir = ROOT / "tools"
tools_dir.mkdir(exist_ok=True)

(tools_dir / "index.html").write_text(tools_index(TOOLS), encoding="utf-8")
print("✓ tools/index.html")

for t in TOOLS:
    (tools_dir / f"{t['slug']}.html").write_text(tool_page(t), encoding="utf-8")
    print(f"✓ tools/{t['slug']}.html")


# ── Inject tools block into auto-hubs/categories/ ───────────────────────────
TOOLS_BLOCK = """
<section style="margin-top:36px;padding:24px;background:#fff;border:1px solid rgba(7,48,68,.12);border-radius:16px;">
  <div style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#3f6173;margin-bottom:12px;">SideGuy Tools</div>
  <p style="margin:0 0 12px;font-size:.9rem;">Calculators and checklists — figure things out before spending money.</p>
  <ul style="margin:0 0 14px;padding-left:18px;font-size:.87rem;display:flex;flex-wrap:wrap;gap:4px 20px;list-style:none;padding:0;">
    <li><a href="/tools/payments-fee-calculator.html" style="color:#073044;">Payments Fee Calculator</a></li>
    <li><a href="/tools/chargeback-cost-estimator.html" style="color:#073044;">Chargeback Estimator</a></li>
    <li><a href="/tools/ai-automation-roi.html" style="color:#073044;">AI Automation ROI</a></li>
    <li><a href="/tools/hvac-repair-vs-replace.html" style="color:#073044;">HVAC Repair vs Replace</a></li>
    <li><a href="/tools/" style="color:#21d3a1;font-weight:700;">All tools →</a></li>
  </ul>
</section>"""

cats_dir = ROOT / "auto-hubs" / "categories"
injected = 0
skipped  = 0
for f in sorted(cats_dir.glob("*.html")):
    html = f.read_text(encoding="utf-8", errors="replace")
    if "SideGuy Tools" in html:
        skipped += 1
        continue
    new_html = html.replace("</body>", TOOLS_BLOCK + "\n</body>", 1)
    if new_html != html:
        f.write_text(new_html, encoding="utf-8")
        injected += 1

print(f"\n✓ Tools block injected into {injected} category hubs ({skipped} already had it)")


# ── Problem radar signals ─────────────────────────────────────────────────────
(ROOT / "docs" / "problem-radar").mkdir(parents=True, exist_ok=True)
(ROOT / "data" / "problem-signals").mkdir(parents=True, exist_ok=True)

SEED_PROBLEMS = {
    "hvac":          ["hvac noise", "hvac not cooling", "hvac leaking water", "hvac compressor not starting",
                      "hvac repair vs replace cost", "hvac blowing warm air", "hvac short cycling"],
    "payments":      ["payment processing fees too high", "stripe alternatives san diego",
                      "payment gateway problems", "chargeback prevention", "mobile payment terminal",
                      "ach vs credit card fees"],
    "ai-automation": ["ai automation for small business", "automate business tasks",
                      "ai workflow automation", "ai scheduling tools", "ai customer service bot"],
    "energy":        ["ev charging cost", "home ev charger install", "ev battery lifespan",
                      "level 2 charger cost", "tesla home charger install"],
    "business-software": ["crm for small business", "accounting software comparison",
                          "quickbooks alternatives", "invoice software san diego"],
    "crypto-web3":   ["crypto wallet security risks", "accept bitcoin payments",
                      "stablecoin for business", "best hardware wallet"],
    "prediction-markets": ["kalshi san diego", "prediction market legality", "polymarket guide",
                           "hedge with prediction markets"],
}

radar_rows = []
for pillar, problems in SEED_PROBLEMS.items():
    for p in problems:
        radar_rows.append({"source": "seed", "pillar": pillar, "topic": p, "timestamp": NOW})

# Write signals TSV
radar_tsv = ROOT / "docs" / "problem-radar" / "radar-signals.tsv"
with open(radar_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["source","pillar","topic","timestamp"], delimiter="\t")
    w.writeheader()
    w.writerows(radar_rows)
print(f"\n✓ docs/problem-radar/radar-signals.tsv ({len(radar_rows)} signals)")

# Write common-problems.json for data/problem-signals/
(ROOT / "data" / "problem-signals" / "common-problems.json").write_text(
    json.dumps(SEED_PROBLEMS, indent=2), encoding="utf-8"
)
print("✓ data/problem-signals/common-problems.json")

# Expansion queue
queue_lines = []
for row in radar_rows:
    slug = re.sub(r"[^a-z0-9]+", "-", row["topic"].lower()).strip("-")
    queue_lines.append(f"- {slug}  ← {row['pillar']}")

queue_md = ROOT / "docs" / "problem-radar" / "radar-expansion-queue.md"
queue_md.write_text(
    f"# Radar Expansion Queue\n\nGenerated: {NOW}\n\n"
    + "\n".join(queue_lines) + "\n",
    encoding="utf-8"
)
print(f"✓ docs/problem-radar/radar-expansion-queue.md ({len(queue_lines)} entries)")


# ── Knowledge graph inventory ─────────────────────────────────────────────────
(ROOT / "docs" / "knowledge-graph").mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "intelligence").mkdir(parents=True, exist_ok=True)

html_pages = sorted(ROOT.rglob("*.html"))
# Exclude quarantine, git, node_modules
html_pages = [p for p in html_pages if not any(x in str(p) for x in
              ["_quarantine_backups", ".git/", "node_modules"])]

graph_tsv = ROOT / "docs" / "knowledge-graph" / "site-graph.tsv"
with open(graph_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["rel_path", "dir"])
    for p in html_pages:
        rel = str(p.relative_to(ROOT))
        d   = str(p.parent.relative_to(ROOT)) if p.parent != ROOT else "(root)"
        w.writerow([rel, d])
print(f"\n✓ docs/knowledge-graph/site-graph.tsv ({len(html_pages)} pages)")

# Directory breakdown
from collections import Counter
dirs = Counter(str(p.parent.relative_to(ROOT)) if p.parent != ROOT else "(root)" for p in html_pages)
top_dirs = dirs.most_common(15)

auth_md = ROOT / "docs" / "intelligence" / "authority-flow.md"
dir_rows = "\n".join(f"| `{d}` | {c} |" for d, c in top_dirs)
auth_md.write_text(
    f"# SideGuy Authority Flow Report\n\n"
    f"Generated: {NOW}\n\n"
    f"**Total pages:** {len(html_pages)}\n\n"
    f"## Architecture\n\n"
    f"```\nHome → Pillar → Category → Cluster → Leaf\n```\n\n"
    f"## Top directories by page count\n\n"
    f"| Directory | Pages |\n|---|---|\n{dir_rows}\n",
    encoding="utf-8"
)
print("✓ docs/intelligence/authority-flow.md")


# ── Summary ───────────────────────────────────────────────────────────────────
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SideGuy Tools + Intelligence Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Tool pages created : {len(TOOLS) + 1}  (tools/index.html + 8 pages)
  Category hubs updated : {injected}
  Radar signals : {len(radar_rows)}
  Expansion queue entries : {len(queue_lines)}
  Site inventory : {len(html_pages)} pages
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
