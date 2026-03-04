#!/usr/bin/env python3
# ==============================================================
# SIDEGUY CONCEPT STUBS BUILDER
# Generates the 30 new concept pages from data/concepts.tsv
# + the 17-concept backlog (Phase 4).
# Output: concepts/<slug>.html + updates concepts/index.html
# ==============================================================
# Usage:  python3 scripts/build-concepts-stubs.py
# Env:    FORCE=true — rebuild existing pages
# ==============================================================

import os, datetime, re
from pathlib import Path

ROOT     = Path(__file__).parent.parent
OUT_DIR  = ROOT / "concepts"
OUT_DIR.mkdir(exist_ok=True)

DOMAIN   = "https://sideguysolutions.com"
PHONE_D  = "773-544-1231"
PHONE_S  = "+17735441231"
TODAY    = datetime.date.today().isoformat()
FORCE    = os.getenv("FORCE", "").lower() in ("1","true","yes")

# ── New concepts to build ─────────────────────────────────────
# (slug, title, category, short_def)

NEW_CONCEPTS = [
    # Phase-4 backlog
    ("blockchain-payments",    "Blockchain Payments",           "Payments",       "Using distributed ledger technology to settle transactions directly between parties without a traditional intermediary."),
    ("ai-agents",              "AI Agents",                     "AI Automation",  "Software programs that perceive their environment, make decisions, and take actions autonomously to complete multi-step tasks."),
    ("stablecoins",            "Stablecoins",                   "Payments",       "Cryptocurrencies pegged to a stable asset (usually USD) to eliminate price volatility while keeping crypto-rail settlement speed."),
    ("payment-settlement",     "Payment Settlement",            "Payments",       "The process of transferring funds between a buyer's bank and a merchant's bank after a transaction is authorized."),
    ("api-infrastructure",     "API Infrastructure",            "Technology",     "The systems, protocols, and tooling that allow software services to communicate and share data reliably at scale."),
    ("automation-workflows",   "Automation Workflows",          "AI Automation",  "Sequences of automated steps that move data and trigger actions across tools without manual intervention."),
    ("machine-learning",       "Machine Learning",              "AI Automation",  "A branch of AI where systems learn patterns from data and improve performance on tasks without being explicitly programmed."),
    ("programmatic-seo",       "Programmatic SEO",              "Marketing",      "Creating large volumes of search-optimized web pages using templates and structured data rather than manual writing."),
    ("knowledge-graphs",       "Knowledge Graphs",              "Technology",     "Structured representations of entities and their relationships, used to power smarter search and AI reasoning."),
    ("search-intent",          "Search Intent",                 "Marketing",      "The underlying goal behind a user's search query — informational, navigational, commercial, or transactional."),
    ("ai-decision-engines",    "AI Decision Engines",           "AI Automation",  "Systems that use AI to evaluate inputs and output a recommended action, automating decisions that once required human judgment."),
    ("payment-orchestration",  "Payment Orchestration",         "Payments",       "Routing payments across multiple processors, gateways, and methods to maximize approval rates and minimize costs."),
    ("ai-assistants",          "AI Assistants",                 "AI Automation",  "Conversational AI tools that help users complete tasks, answer questions, or retrieve information through natural language."),
    ("distributed-computing",  "Distributed Computing",         "Technology",     "Systems where computation is spread across multiple networked machines to improve performance, resilience, and scale."),
    ("data-pipelines",         "Data Pipelines",                "Technology",     "Automated sequences that extract, transform, and load data from source systems into destinations for analysis or action."),
    ("autonomous-agents",      "Autonomous Agents",             "AI Automation",  "AI systems that operate independently over time, planning and executing multi-step tasks without human prompting for each step."),
    ("future-of-search",       "Future of Search",              "Marketing",      "How AI, voice, and intent-based discovery are changing where people find information and how businesses must respond."),
    # From data/concepts.tsv (new only)
    ("ai-workflows",           "AI Workflows",                  "AI Automation",  "End-to-end automated processes powered by AI that handle input classification, action routing, and output generation."),
    ("ai-call-agents",         "AI Call Agents",                "AI Automation",  "AI-powered phone or voice agents that handle inbound and outbound calls, qualify leads, and schedule appointments."),
    ("ai-scheduling-agents",   "AI Scheduling Agents",          "AI Automation",  "AI systems that manage appointment booking, rescheduling, and reminder flows without human dispatcher involvement."),
    ("kalshi-trading",         "Kalshi Prediction Trading",     "Finance",        "Regulated event contracts on Kalshi where traders take positions on real-world outcomes like economic data and elections."),
    ("polymarket-trading",     "Polymarket Trading",            "Finance",        "Crypto-based prediction market platform where participants trade outcome contracts using stablecoins."),
    ("stablecoin-payments",    "Stablecoin Payments",           "Payments",       "Using USD-pegged cryptocurrencies (USDC, USDT) to settle business payments with blockchain speed and no exchange-rate risk."),
    ("solana-payments",        "Solana Payments",               "Payments",       "Using the Solana blockchain for payment settlement — sub-second finality, near-zero fees, no chargebacks."),
    ("merchant-fees",          "Merchant Fees",                 "Payments",       "All the costs a business incurs to accept card payments — interchange, processor markup, gateway fees, and monthly minimums."),
    ("interchange-fees",       "Interchange Fees",              "Payments",       "The fee paid to the card-issuing bank on every transaction — set by Visa/Mastercard, non-negotiable, typically 1.5–2.1%."),
    ("chargebacks",            "Chargebacks",                   "Payments",       "A forced transaction reversal initiated by a cardholder through their bank — the primary dispute mechanism in card payments."),
    ("small-business-automation","Small Business Automation",   "AI Automation",  "Using software and AI to automate repetitive tasks in small operations — scheduling, invoicing, follow-up, and customer comms."),
    ("crm-automation",         "CRM Automation",                "Technology",     "Using workflow rules and AI to automatically update CRM records, assign leads, send follow-ups, and track pipeline stages."),
    ("invoice-automation",     "Invoice Automation",            "Technology",     "Software-driven creation, delivery, and tracking of invoices — reducing manual entry and accelerating cash collection."),
]

# ── Per-category content packs ────────────────────────────────

CATEGORY_PACKS = {
    "Payments": {
        "icon": "💳",
        "pillar_href": "/payments-infrastructure-hub.html",
        "pillar_name": "Payments Infrastructure",
        "related": [
            ("Payment Processing", "/concepts/payment-processing.html"),
            ("Crypto Payments",    "/concepts/crypto-payments.html"),
            ("Payments Hub",       "/payments-infrastructure-hub.html"),
            ("Knowledge Hub",      "/knowledge-hub.html"),
        ],
        "sections": [
            ("Why operators care", "This is a foundational concept that directly affects your costs, cash flow, or risk exposure. Understanding it prevents expensive surprises."),
            ("How it works in practice", "The mechanics are simpler than they look. Once you understand the core flow, most related problems become obvious."),
            ("What operators get wrong", "The most common misunderstanding is treating this as a \"set and forget\" system. It requires periodic review as your volume and mix change."),
            ("When to act", "If this is costing you money you didn't know about, or creating friction for customers, act now. Otherwise, build it into your quarterly review."),
        ],
    },
    "AI Automation": {
        "icon": "🤖",
        "pillar_href": "/ai-automation-hub.html",
        "pillar_name": "AI Automation",
        "related": [
            ("AI Automation",      "/concepts/ai-automation.html"),
            ("AI Automation Hub",  "/ai-automation-hub.html"),
            ("Problem Library",    "/problems/index.html"),
            ("Knowledge Hub",      "/knowledge-hub.html"),
        ],
        "sections": [
            ("What makes it useful", "The practical value is in handling high-volume, repetitive inputs that follow a predictable pattern. Anything unpredictable still needs human oversight."),
            ("Where operators use it", "Most operators start with one automation (missed call text-back, appointment reminders, or invoice delivery) and expand from there once they trust the system."),
            ("Where it breaks", "It fails when inputs vary too much, when the stakes of a wrong output are high, or when the \"data\" it needs is locked in someone's head rather than a system."),
            ("Getting started", "Map the manual process first. Write it as if you're training someone on the job. That document becomes your automation spec."),
        ],
    },
    "Technology": {
        "icon": "⚙️",
        "pillar_href": "/operator-tools-hub.html",
        "pillar_name": "Operator Tools",
        "related": [
            ("Operator Tools Hub",  "/operator-tools-hub.html"),
            ("AI Automation Hub",   "/ai-automation-hub.html"),
            ("Problem Library",     "/problems/index.html"),
            ("Knowledge Hub",       "/knowledge-hub.html"),
        ],
        "sections": [
            ("What it is in plain English", "Strip away the jargon and this is a system that moves data or executes logic in a predictable way. The implementation details matter less than the outcomes."),
            ("Why small businesses need to understand it", "You don't need to build it — but you need to ask the right questions when a vendor or employee proposes it, and know when something is broken."),
            ("Common operator traps", "The most expensive mistake is buying or building something without confirming it connects to your existing tools and that there's a real exit path if it doesn't work."),
            ("Practical next step", "If you're evaluating a tool or service that involves this concept, ask: what does the data flow look like, who owns the data, and what happens when we want to switch?"),
        ],
    },
    "Marketing": {
        "icon": "📣",
        "pillar_href": "/ai-automation-hub.html",
        "pillar_name": "AI & Marketing",
        "related": [
            ("AI Automation Hub",    "/ai-automation-hub.html"),
            ("AI Marketing Cluster", "/clusters/ai-marketing-automation.html"),
            ("Problem Library",      "/problems/index.html"),
            ("Knowledge Hub",        "/knowledge-hub.html"),
        ],
        "sections": [
            ("Why this matters for operators", "Most small businesses leave significant organic traffic on the table by not understanding how search and content systems actually work."),
            ("What changed recently", "AI has changed both how content is created and how users find it. The rules from 2022 no longer apply completely."),
            ("What still works", "Specificity, trust signals, and relevance to clear operator intent are still the foundation. Tactics change; those fundamentals don't."),
            ("Practical starting point", "Start with the question your best customers ask most before they hire you. That's your first page. Build from there."),
        ],
    },
    "Finance": {
        "icon": "📈",
        "pillar_href": "/prediction-markets-hub.html",
        "pillar_name": "Prediction Markets",
        "related": [
            ("Prediction Markets",     "/concepts/prediction-markets.html"),
            ("Prediction Markets Hub", "/prediction-markets-hub.html"),
            ("Crypto Payments",        "/concepts/crypto-payments.html"),
            ("Knowledge Hub",          "/knowledge-hub.html"),
        ],
        "sections": [
            ("What this is and why it matters", "Financial instruments and market structures are increasingly accessible to non-professionals. Understanding the basics prevents costly misuse."),
            ("How it works mechanically", "The underlying mechanics are simpler than they appear. Pricing reflects collective probability estimates, not guaranteed outcomes."),
            ("Operator use cases", "For small businesses, the value is usually in macro intelligence — using public market prices as a signal, not as a direct investment product."),
            ("Risks and limitations", "Markets are efficient but not perfect. Use them as one signal among several, especially for decisions with material consequences."),
        ],
    },
}

CSS = """  :root{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--blue2:#1f7cff;--r:18px;--pill:999px}
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;background:radial-gradient(ellipse at 60% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);color:var(--ink);min-height:100vh}
  a{color:var(--blue2);text-decoration:none}a:hover{text-decoration:underline}
  nav.bc{padding:11px 24px;font-size:.8rem;color:var(--muted);border-bottom:1px solid rgba(0,0,0,.06);background:rgba(255,255,255,.6);backdrop-filter:blur(6px);position:sticky;top:0;z-index:10}
  nav.bc a{color:var(--muted)}
  .wrap{max-width:860px;margin:0 auto;padding:44px 24px 100px}
  .badge{display:inline-block;background:var(--mint);color:#073044;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 12px;border-radius:var(--pill);margin-bottom:12px}
  h1{font-size:clamp(1.6rem,5vw,2.5rem);font-weight:800;line-height:1.15;margin-bottom:10px}
  .defbox{background:linear-gradient(135deg,rgba(33,211,161,.12),rgba(74,169,255,.10));border:1px solid rgba(33,211,161,.25);border-radius:var(--r);padding:20px 24px;margin-bottom:32px}
  .defbox strong{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);margin-bottom:8px}
  .defbox p{font-size:.97rem;line-height:1.65;color:var(--ink)}
  .section{margin-bottom:36px}
  .section h2{font-size:1.4rem;font-weight:800;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid var(--bg1)}
  .section p{line-height:1.7;color:var(--ink);margin-bottom:12px}
  .pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
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

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_concept(slug, title, category, short_def):
    pack     = CATEGORY_PACKS.get(category, CATEGORY_PACKS["Technology"])
    icon     = pack["icon"]
    canonical= f"{DOMAIN}/concepts/{slug}.html"

    secs_html = ""
    for s_title, s_body in pack["sections"]:
        secs_html += f"""  <div class="section">
    <h2>{esc(s_title)}</h2>
    <p>{esc(s_body)}</p>
  </div>
"""

    pills_related = "".join(
        f'    <a class="pill" href="{href}">{label}</a>\n'
        for label, href in pack["related"]
    )

    jsonld = f"""  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"Concept Library","item":"{DOMAIN}/concepts/index.html"}},
          {{"@type":"ListItem","position":3,"name":"{esc(title)}","item":"{canonical}"}}
        ]
      }},
      {{
        "@type": "DefinedTerm",
        "name": "{esc(title)}",
        "description": "{esc(short_def)}",
        "url": "{canonical}",
        "inDefinedTermSet": {{
          "@type": "DefinedTermSet",
          "name": "SideGuy Concept Library",
          "url": "{DOMAIN}/concepts/index.html"
        }}
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
          {{"@type":"Question","name":"What is {esc(title)}?","acceptedAnswer":{{"@type":"Answer","text":"{esc(short_def)}"}}}},
          {{"@type":"Question","name":"Why does {esc(title)} matter for operators?","acceptedAnswer":{{"@type":"Answer","text":"Understanding this concept helps operators make better decisions about costs, tools, and risk — without needing a specialist to translate it."}}}},
          {{"@type":"Question","name":"Where can I learn more about {esc(title)}?","acceptedAnswer":{{"@type":"Answer","text":"Start with the related pages below, then text PJ if your situation has specific constraints that the guides don\u2019t cover."}}}}
        ]
      }}
    ]
  }}"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{esc(title)} Explained — Operator Guide | SideGuy Solutions</title>
  <meta name="description" content="{esc(short_def)} Practical operator guide from SideGuy — clarity before cost."/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:title" content="{esc(title)} Explained | SideGuy Solutions"/>
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
  <a href="/concepts/index.html">Concept Library</a> ›
  {esc(title)}
</nav>
<main class="wrap">
  <div class="badge">Concept Guide · {category}</div>
  <h1>{icon} {esc(title)}</h1>

  <div class="defbox">
    <strong>Definition</strong>
    <p>{esc(short_def)}</p>
  </div>

{secs_html}
  <div class="section">
    <h2>📖 Related Concepts &amp; Guides</h2>
    <div class="pill-row">
{pills_related}      <a class="pill ac" href="/concepts/index.html">Concept Library →</a>
    </div>
  </div>

  <div class="cta-box">
    <div>
      <h3>Have a specific question about {esc(title)}?</h3>
      <p>Text PJ — real human, San Diego. Straight answer, no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_S}">💬 Text {PHONE_D}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/concepts/index.html">Concept Library</a> ·
    <a href="{pack['pillar_href']}">{esc(pack['pillar_name'])}</a> ·
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

# ── Update concepts/index.html ────────────────────────────────

def rebuild_index_additions(new_slugs: list):
    idx = OUT_DIR / "index.html"
    if not idx.exists():
        return
    content = idx.read_text()
    marker_s = "<!-- SIDEGUY_CONCEPTS_STUBS_START -->"
    marker_e = "<!-- SIDEGUY_CONCEPTS_STUBS_END -->"

    cards = ""
    for slug, title, category, short_def in NEW_CONCEPTS:
        if slug not in new_slugs:
            continue
        icon = CATEGORY_PACKS.get(category, CATEGORY_PACKS["Technology"])["icon"]
        cards += f"""      <a href="/concepts/{slug}.html" style="display:block;background:rgba(255,255,255,.78);border:1px solid rgba(0,0,0,.08);border-radius:18px;padding:18px 20px;color:#073044;text-decoration:none;transition:box-shadow .15s,transform .1s">
        <div style="font-size:1.4rem;margin-bottom:8px">{icon}</div>
        <div style="font-size:.97rem;font-weight:700;margin-bottom:4px">{title}</div>
        <div style="font-size:.82rem;color:#3f6173;line-height:1.45">{short_def[:80]}…</div>
      </a>
"""

    section = f"""
  <div style="margin-top:40px">
    <h2 style="font-size:1.05rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:#3f6173;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #d7f5ff">New Concept Guides</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px">
{marker_s}
{cards}
{marker_e}
    </div>
  </div>
"""

    if marker_s in content and marker_e in content:
        content = re.sub(
            re.escape(marker_s) + r".*?" + re.escape(marker_e),
            f"{marker_s}\n{cards}\n{marker_e}",
            content, flags=re.S
        )
    elif "</main>" in content:
        content = content.replace("</main>", section + "\n</main>", 1)
    else:
        content = content.replace("</body>", section + "\n</body>", 1)

    idx.write_text(content)
    print(f"  concepts/index.html updated ({len(new_slugs)} new entries)")


# ── Update sitemap ────────────────────────────────────────────

def update_sitemap(new_slugs: list):
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        return
    content = sm.read_text()
    added = 0
    inserts = ""
    for slug in new_slugs:
        url = f"{DOMAIN}/concepts/{slug}.html"
        if url not in content:
            inserts += f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n"
            added += 1
    if inserts:
        content = content.replace("</urlset>", inserts + "</urlset>")
        sm.write_text(content)
    print(f"  sitemap.xml: {added} concept URLs added")


# ── Main ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SideGuy Concept Stubs Builder ===\n")
    built_slugs = []
    skipped = 0

    for slug, title, category, short_def in NEW_CONCEPTS:
        path = OUT_DIR / f"{slug}.html"
        if path.exists() and not FORCE:
            skipped += 1
            continue
        html = build_concept(slug, title, category, short_def)
        path.write_text(html)
        print(f"  BUILT concepts/{slug}.html")
        built_slugs.append(slug)

    print(f"\n  Built: {len(built_slugs)}   Skipped: {skipped}")

    if built_slugs:
        rebuild_index_additions(built_slugs)
        update_sitemap(built_slugs)

    print(f"\n✅  Run python3 scripts/generate-sitemap.py to fully refresh sitemaps.")
