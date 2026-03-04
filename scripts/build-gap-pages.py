#!/usr/bin/env python3
# ==============================================================
# SIDEGUY GAP TOPICS BUILDER
# Builds high-priority "gap" pages from reports/gap-topics-to-build.tsv
# Output: generated/<slug>.html
# ==============================================================
# Usage:  python3 scripts/build-gap-pages.py
# Env:    FORCE=true  — rebuild existing pages
# ==============================================================

import os, datetime
from pathlib import Path

ROOT     = Path(__file__).parent.parent
OUT_DIR  = ROOT / "generated"
OUT_DIR.mkdir(exist_ok=True)

TSV      = ROOT / "reports" / "gap-topics-to-build.tsv"
DOMAIN   = "https://sideguysolutions.com"
PHONE_D  = "773-544-1231"
PHONE_S  = "+17735441231"
TODAY    = datetime.date.today().isoformat()
FORCE    = os.getenv("FORCE", "").lower() in ("1","true","yes")

PILLAR_MAP = {
    "payments":           ("/payments.html",            "Payment Processing"),
    "ai-automation":      ("/ai-automation-hub.html",   "AI Automation"),
    "small-business-tech":("/operator-tools-hub.html",  "Operator Tools"),
}

CSS = """  :root{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--blue2:#1f7cff;--r:18px;--pill:999px}
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;background:radial-gradient(ellipse at 60% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);color:var(--ink);min-height:100vh}
  a{color:var(--blue2);text-decoration:none}a:hover{text-decoration:underline}
  nav.bc{padding:11px 24px;font-size:.8rem;color:var(--muted);border-bottom:1px solid rgba(0,0,0,.06);background:rgba(255,255,255,.6);backdrop-filter:blur(6px);position:sticky;top:0;z-index:10}
  nav.bc a{color:var(--muted)}
  .wrap{max-width:860px;margin:0 auto;padding:44px 24px 100px}
  .badge{display:inline-block;background:var(--mint);color:#073044;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 12px;border-radius:var(--pill);margin-bottom:12px}
  h1{font-size:clamp(1.6rem,5vw,2.4rem);font-weight:800;line-height:1.15;margin-bottom:10px}
  .lede{font-size:1rem;color:var(--muted);line-height:1.65;margin-bottom:32px;max-width:680px}
  .section{margin-bottom:38px}
  .section h2{font-size:1.05rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid var(--bg1)}
  .card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
  .card{background:rgba(255,255,255,.78);border:1px solid rgba(0,0,0,.08);border-radius:var(--r);padding:18px 20px;color:var(--ink);display:block;transition:box-shadow .15s,transform .1s}
  .card:hover{box-shadow:0 4px 20px rgba(0,0,0,.1);transform:translateY(-1px);text-decoration:none}
  .card-icon{font-size:1.4rem;margin-bottom:8px}
  .card-title{font-size:.97rem;font-weight:700;margin-bottom:4px}
  .card-desc{font-size:.82rem;color:var(--muted);line-height:1.5}
  .steps{list-style:none;counter-reset:steps;display:flex;flex-direction:column;gap:12px}
  .steps li{counter-increment:steps;padding:14px 18px;padding-left:52px;position:relative;background:rgba(255,255,255,.75);border:1px solid rgba(0,0,0,.07);border-radius:var(--r)}
  .steps li::before{content:counter(steps);position:absolute;left:14px;top:50%;transform:translateY(-50%);width:26px;height:26px;border-radius:50%;background:var(--mint);color:#073044;font-size:.78rem;font-weight:800;display:flex;align-items:center;justify-content:center}
  .steps li strong{display:block;font-size:.93rem;margin-bottom:3px}
  .steps li span{font-size:.85rem;color:var(--muted)}
  .pill-row{display:flex;flex-wrap:wrap;gap:8px}
  .pill{background:rgba(255,255,255,.8);border:1px solid rgba(0,0,0,.1);border-radius:var(--pill);padding:6px 14px;font-size:.84rem;font-weight:500;color:var(--ink)}
  .pill:hover{background:var(--mint);color:#073044;text-decoration:none}
  .pill.ac{background:var(--blue2);color:#fff;border-color:var(--blue2)}
  .cta-box{background:linear-gradient(135deg,#073044 0%,#0e3d58 100%);border-radius:var(--r);padding:26px 30px;color:#fff;display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin:38px 0 28px}
  .cta-box h3{font-size:1.1rem;font-weight:700;margin-bottom:4px}
  .cta-box p{font-size:.9rem;opacity:.8;margin:0}
  .cta-btn{flex-shrink:0;background:var(--mint);color:#073044;font-weight:700;padding:11px 20px;border-radius:var(--pill);white-space:nowrap}
  .cta-btn:hover{opacity:.9;text-decoration:none}
  .floating{position:fixed;bottom:22px;right:22px;z-index:999}
  .floatBtn{display:flex;align-items:center;gap:8px;background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.2)}
  .floatBtn:hover{opacity:.92;text-decoration:none}
  footer{text-align:center;padding:18px;font-size:.76rem;color:var(--muted);border-top:1px solid rgba(0,0,0,.06);margin-top:36px}
  @media(max-width:600px){.cta-box{flex-direction:column;gap:14px}.floating{bottom:14px;right:14px}}"""

# Per-pillar content packs
CONTENT = {
    "payments": {
        "badge": "Operator Guide · Payments",
        "icon": "💳",
        "lede": "Plain-English explanation with a practical operator checklist — what it is, what it costs you, and what to check first.",
        "wins": [
            ("📋", "What it is", "Clear definition with no jargon — what this actually means for your business."),
            ("💰", "What it costs you", "Where the money goes, what's negotiable, and what's fixed."),
            ("⚡", "Fast checklist", "10-minute check to get signal without overthinking."),
            ("🔀", "Next move", "When to act, when to wait, and when to call someone."),
        ],
        "steps": [
            ("Read your processing statement", "Look for the effective rate line — that's your real cost."),
            ("Identify the fee layers", "Interchange is fixed. Processor markup is negotiable."),
            ("Compare your rate to benchmarks", "Most small businesses should be under 2.7% effective rate."),
            ("Flag any surprises", "PCI fees, batch fees, and monthly minimums are the hidden ones."),
            ("Decide: optimize or switch", "Small tweaks can save hundreds/month before switching makes sense."),
        ],
        "related_pills": [
            ("Payment Processing Fees", "/generated/payment-processing-fees-explained.html"),
            ("Chargebacks Guide", "/generated/reduce-chargebacks.html"),
            ("Switch Processor?", "/decisions/switch-payment-processor.html"),
            ("Payments Hub", "/payments-infrastructure-hub.html"),
        ],
    },
    "ai-automation": {
        "badge": "Operator Guide · AI Automation",
        "icon": "🤖",
        "lede": "Practical implementation guide — what this automation actually does, how to set it up in under an hour, and what to watch for.",
        "wins": [
            ("⚡", "What it does", "Clear explanation of the automation and the problem it solves."),
            ("🔧", "Setup requirements", "What tools you need and what you already have."),
            ("📈", "Expected ROI", "Time saved per week and payback period for most operators."),
            ("⚠️", "Watch out for", "Where this automation breaks and how to catch it early."),
        ],
        "steps": [
            ("Map the current manual process", "Write out each step you do today — this becomes your automation spec."),
            ("Pick your trigger", "Automations start with a trigger: new lead, missed call, form submit, etc."),
            ("Connect your existing tools", "Most automations work with Zapier, Make.com, or a native integration."),
            ("Test with 10 real interactions", "Small batch first — real data reveals edge cases that demos hide."),
            ("Measure and iterate", "Track the metric this automation was supposed to move — check weekly."),
        ],
        "related_pills": [
            ("AI Automation Hub", "/ai-automation-hub.html"),
            ("Workflow Automation", "/clusters/ai-workflow-automation.html"),
            ("Problem Library", "/problems/index.html"),
            ("Should I Use AI?", "/intelligence/decisions/should-i-use-ai.html"),
        ],
    },
    "small-business-tech": {
        "badge": "Operator Guide · Small Business Tech",
        "icon": "🛠️",
        "lede": "Practical operator guide — what to look for, what's overbuilt, and the fastest path to having this working without a consultant.",
        "wins": [
            ("✅", "What to look for", "The 3 things that matter most — everything else is noise."),
            ("⚠️", "Common mistakes", "What operators usually get wrong when setting this up."),
            ("⚡", "Fast setup path", "Shortest path from zero to working with minimal config."),
            ("🔀", "When to get help", "Signs this is complex enough that a 30-minute call saves hours."),
        ],
        "steps": [
            ("Define your one constraint", "What is the single biggest friction point this needs to solve?"),
            ("List your existing tools", "The best solution is usually the one that connects to what you already have."),
            ("Test the free tier or trial", "Never buy a year upfront — test with real data for 2 weeks."),
            ("Confirm the exit path", "Before committing: can you export your data and cancel easily?"),
            ("Document your setup decisions", "Write a one-page SOP before you forget why you configured it that way."),
        ],
        "related_pills": [
            ("Operator Tools Hub", "/operator-tools-hub.html"),
            ("SOPs and Process", "/clusters/sops-and-process.html"),
            ("Customer Ops", "/clusters/customer-ops.html"),
            ("Problem Library", "/problems/index.html"),
        ],
    },
}

def read_tsv(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        headers = f.readline().strip().split("\t")
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            rows.append(dict(zip(headers, parts)))
    return rows

def esc(s: str) -> str:
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_page(slug: str, title: str, pillar: str) -> str:
    pillar_href, pillar_name = PILLAR_MAP.get(pillar, ("/knowledge-hub.html", "Knowledge Hub"))
    pack = CONTENT.get(pillar, CONTENT["ai-automation"])
    canonical = f"{DOMAIN}/generated/{slug}.html"

    jsonld = f"""  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"{esc(pillar_name)}","item":"{DOMAIN}{pillar_href}"}},
          {{"@type":"ListItem","position":3,"name":"{esc(title)}","item":"{canonical}"}}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{"@type":"Question","name":"What is {esc(title)}?","acceptedAnswer":{{"@type":"Answer","text":"{esc(title)} is an operator-relevant topic. This guide explains it in plain English with a practical checklist — no jargon, no hype."}}}},
          {{"@type":"Question","name":"What should I do first?","acceptedAnswer":{{"@type":"Answer","text":"Start by confirming what you\u2019re actually dealing with using the fast checklist, then act on the clearest signal before making bigger changes."}}}},
          {{"@type":"Question","name":"When should I ask a human for help?","acceptedAnswer":{{"@type":"Answer","text":"When money, compliance, or customer impact is involved \u2014 a 10-minute sanity check can prevent expensive mistakes."}}}}
        ]
      }}
    ]
  }}"""

    wins_html = ""
    for w_icon, w_title, w_desc in pack["wins"]:
        wins_html += f"""    <a class="card" href="{pillar_href}">
      <div class="card-icon">{w_icon}</div>
      <div class="card-title">{w_title}</div>
      <div class="card-desc">{w_desc}</div>
    </a>
"""

    steps_html = "".join(
        f"    <li><strong>{s}</strong><span>{d}</span></li>\n"
        for s, d in pack["steps"]
    )

    pills_html = "".join(
        f'    <a class="pill" href="{href}">{label}</a>\n'
        for label, href in pack["related_pills"]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{esc(title)} | SideGuy Solutions</title>
  <meta name="description" content="Practical guide to {title.lower()}: what it is, what it costs you, and the fast operator checklist. Clarity before cost."/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:title" content="{esc(title)} | SideGuy Solutions"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:type" content="article"/>
  <meta name="robots" content="index,follow"/>
  <script type="application/ld+json">
{jsonld}
  </script>
  <style>
{CSS}
  </style>
</head>
<body>
<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> ›
  <a href="{pillar_href}">{esc(pillar_name)}</a> ›
  {esc(title)}
</nav>
<main class="wrap">
  <div class="badge">{pack['badge']}</div>
  <h1>{pack['icon']} {esc(title)}</h1>
  <p class="lede">{pack['lede']}</p>

  <div class="section">
    <h2>📋 What to Know</h2>
    <div class="card-grid">
{wins_html}    </div>
  </div>

  <div class="section">
    <h2>🚀 Fast Checklist</h2>
    <ol class="steps">
{steps_html}    </ol>
  </div>

  <div class="section">
    <h2>📖 Related Guides</h2>
    <div class="pill-row">
{pills_html}      <a class="pill ac" href="/knowledge-hub.html">Knowledge Hub →</a>
    </div>
  </div>

  <div class="cta-box">
    <div>
      <h3>Want a quick sanity check?</h3>
      <p>Text PJ — real human, San Diego. Straight answer, no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_S}">💬 Text {PHONE_D}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="{pillar_href}">{esc(pillar_name)}</a> ·
    <a href="/knowledge-hub.html">Knowledge Hub</a> ·
    <a href="tel:{PHONE_S}">{PHONE_D}</a>
    <br><small>Updated {TODAY}</small>
  </footer>
</main>
<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_S}">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ · {PHONE_D}
  </a>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    print("=== SideGuy Gap Topics Builder ===\n")
    rows  = read_tsv(TSV)
    built = skipped = 0
    for row in rows:
        slug   = row["slug"].strip()
        title  = row["title"].strip()
        pillar = row["pillar"].strip()
        path   = OUT_DIR / f"{slug}.html"
        if path.exists() and not FORCE:
            skipped += 1
            continue
        path.write_text(build_page(slug, title, pillar))
        print(f"  BUILT {slug}.html")
        built += 1
    print(f"\n  Built: {built}   Skipped: {skipped}")
    print(f"  Run python3 scripts/generate-sitemap.py to update the sitemap.")
