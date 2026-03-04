#!/usr/bin/env python3
"""
SIDEGUY Hub Page Builder
Creates:
  knowledge-hub.html            — central navigation hub
  ai-automation-hub.html        — AI Automation topic hub
  payments-infrastructure-hub.html — Payments topic hub
  prediction-markets-hub.html   — Prediction Markets topic hub
  operator-tools-hub.html       — Operator Tools topic hub

Also updates: sitemap.xml, knowledge/sideguy-knowledge-map.html
Idempotent: add FORCE=True to rebuild existing pages.
"""

from pathlib import Path
from datetime import date

ROOT   = Path(__file__).parent.parent
TODAY  = date.today().isoformat()
DOMAIN = "https://sideguysolutions.com"
PHONE_DISPLAY = "773-544-1231"
PHONE_SMS     = "+17735441231"

FORCE = False   # set True to overwrite existing pages

# ──────────────────────────────────────────────
# SHARED CSS
# ──────────────────────────────────────────────

CSS = """
  :root {
    --bg0:#eefcff; --bg1:#d7f5ff; --ink:#073044; --muted:#3f6173;
    --mint:#21d3a1; --mint2:#00c7ff; --blue2:#1f7cff;
    --r:18px; --pill:999px;
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body {
    font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;
    background:radial-gradient(ellipse at 60% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);
    color:var(--ink);
    min-height:100vh;
  }
  a{color:var(--blue2);text-decoration:none}
  a:hover{text-decoration:underline}

  nav.bc{
    padding:11px 24px;font-size:.8rem;color:var(--muted);
    border-bottom:1px solid rgba(0,0,0,.06);
    background:rgba(255,255,255,.6);backdrop-filter:blur(6px);
    position:sticky;top:0;z-index:10;
  }
  nav.bc a{color:var(--muted)}

  .wrap{max-width:1000px;margin:0 auto;padding:44px 24px 80px}

  /* hero */
  .hub-badge{
    display:inline-block;background:var(--mint);color:#073044;
    font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
    padding:3px 12px;border-radius:var(--pill);margin-bottom:12px;
  }
  h1{font-size:clamp(1.7rem,5vw,2.6rem);font-weight:800;line-height:1.15;margin-bottom:12px}
  .lede{font-size:1rem;color:var(--muted);line-height:1.65;margin-bottom:36px;max-width:680px}

  /* section */
  .hub-section{margin-bottom:50px}
  .hub-section h2{
    font-size:1.1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;
    color:var(--muted);margin-bottom:16px;padding-bottom:8px;
    border-bottom:2px solid var(--bg1);
  }

  /* card grid */
  .card-grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
    gap:12px;
  }
  .card{
    background:rgba(255,255,255,.78);
    border:1px solid rgba(0,0,0,.08);
    border-radius:var(--r);
    padding:18px 20px;
    text-decoration:none;
    color:var(--ink);
    transition:box-shadow .15s,transform .1s;
    display:block;
  }
  .card:hover{box-shadow:0 4px 20px rgba(0,0,0,.1);transform:translateY(-1px);text-decoration:none}
  .card-icon{font-size:1.5rem;margin-bottom:8px}
  .card-title{font-size:.97rem;font-weight:700;margin-bottom:4px}
  .card-desc{font-size:.82rem;color:var(--muted);line-height:1.5}

  /* pill row */
  .pill-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
  .pill{
    background:rgba(255,255,255,.8);border:1px solid rgba(0,0,0,.1);
    border-radius:var(--pill);padding:6px 15px;font-size:.84rem;
    font-weight:500;color:var(--ink);
  }
  .pill:hover{background:var(--mint);color:#073044;text-decoration:none}
  .pill.accent{background:var(--blue2);color:#fff;border-color:var(--blue2)}
  .pill.accent:hover{opacity:.9}

  /* CTA */
  .cta-box{
    background:linear-gradient(135deg,#073044 0%,#0e3d58 100%);
    border-radius:var(--r);padding:30px 34px;color:#fff;
    margin:44px 0 36px;display:flex;align-items:center;gap:24px;flex-wrap:wrap;
  }
  .cta-box h3{font-size:1.15rem;font-weight:700;margin-bottom:5px}
  .cta-box p{font-size:.92rem;opacity:.8;margin:0}
  .cta-btn{
    flex-shrink:0;background:var(--mint);color:#073044;font-weight:700;
    padding:11px 22px;border-radius:var(--pill);white-space:nowrap;
  }
  .cta-btn:hover{opacity:.9;text-decoration:none}

  /* floating */
  .floating{position:fixed;bottom:22px;right:22px;z-index:999}
  .floatBtn{
    display:flex;align-items:center;gap:8px;
    background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;
    padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;
    text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.2);
  }
  .floatBtn:hover{opacity:.92;text-decoration:none}

  footer{
    text-align:center;padding:22px;font-size:.78rem;color:var(--muted);
    border-top:1px solid rgba(0,0,0,.06);margin-top:40px;
  }

  @media(max-width:600px){
    .cta-box{flex-direction:column;gap:16px}
    .floating{bottom:14px;right:14px}
  }
"""

FLOAT_BTN = f"""
<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_SMS}" aria-label="Text PJ">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ · {PHONE_DISPLAY}
  </a>
</div>
"""

CTA_BOX = f"""
  <div class="cta-box">
    <div>
      <h3>Still have questions? Text PJ.</h3>
      <p>Real human, San Diego. Straight answer on what makes sense for your situation — no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_SMS}">💬 Text {PHONE_DISPLAY}</a>
  </div>
"""


def page_shell(title, meta_desc, canonical, bc_trail, badge, h1, lede, body_html,
               jsonld):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title}</title>
  <meta name="description" content="{meta_desc}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{meta_desc}"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:type" content="website"/>
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
  {bc_trail}
</nav>

<main class="wrap">
  <div class="hub-badge">{badge}</div>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>
{body_html}
{CTA_BOX}
  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/knowledge-hub.html">Knowledge Hub</a> ·
    <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a> ·
    <a href="tel:{PHONE_SMS}">{PHONE_DISPLAY}</a>
    <br><small>Updated {TODAY}</small>
  </footer>
</main>

{FLOAT_BTN}
</body>
</html>
"""


# ──────────────────────────────────────────────
# 1. KNOWLEDGE HUB (central nav)
# ──────────────────────────────────────────────

def build_knowledge_hub():
    jsonld = f"""  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"Knowledge Hub","item":"{DOMAIN}/knowledge-hub.html"}}
        ]
      }},
      {{
        "@type": "CollectionPage",
        "name": "SideGuy Knowledge Hub",
        "description": "Central navigation for all SideGuy knowledge layers — intelligence, problems, guides, and concepts.",
        "url": "{DOMAIN}/knowledge-hub.html"
      }}
    ]
  }}"""

    body = """
  <!-- Intelligence Layer -->
  <div class="hub-section">
    <h2>📡 Intelligence Layer</h2>
    <div class="card-grid">
      <a class="card" href="/intelligence/decisions/should-i-use-ai.html">
        <div class="card-icon">🤖</div>
        <div class="card-title">Should I Use AI?</div>
        <div class="card-desc">Decision framework for small business — no hype, honest checklist.</div>
      </a>
      <a class="card" href="/intelligence/ai-reality/ai-vs-human-decisions.html">
        <div class="card-icon">⚖️</div>
        <div class="card-title">AI vs Human Decisions</div>
        <div class="card-desc">Where AI wins, where humans must stay in the loop.</div>
      </a>
      <a class="card" href="/intelligence/operator-guides/ai-for-small-business.html">
        <div class="card-icon">🔧</div>
        <div class="card-title">AI for Small Business</div>
        <div class="card-desc">Operator-first guide to what actually works in real shops.</div>
      </a>
      <a class="card" href="/knowledge/sideguy-knowledge-map.html">
        <div class="card-icon">🗺️</div>
        <div class="card-title">Knowledge Map</div>
        <div class="card-desc">Everything connected — visual index of all SideGuy pages.</div>
      </a>
    </div>
  </div>

  <!-- Topic Hubs -->
  <div class="hub-section">
    <h2>🧭 Topic Hubs</h2>
    <div class="card-grid">
      <a class="card" href="/ai-automation-hub.html">
        <div class="card-icon">⚙️</div>
        <div class="card-title">AI Automation Hub</div>
        <div class="card-desc">Concepts, guides, and problem pages for AI automation.</div>
      </a>
      <a class="card" href="/payments-infrastructure-hub.html">
        <div class="card-icon">💳</div>
        <div class="card-title">Payments Infrastructure Hub</div>
        <div class="card-desc">Fees, settlement, chargebacks, fraud — everything payments.</div>
      </a>
      <a class="card" href="/prediction-markets-hub.html">
        <div class="card-icon">📈</div>
        <div class="card-title">Prediction Markets Hub</div>
        <div class="card-desc">How markets work, Kalshi, Polymarket, and operator use cases.</div>
      </a>
      <a class="card" href="/operator-tools-hub.html">
        <div class="card-icon">🛠️</div>
        <div class="card-title">Operator Tools Hub</div>
        <div class="card-desc">CRM, SOPs, scheduling, invoicing — tools operators actually use.</div>
      </a>
    </div>
  </div>

  <!-- Problem Library -->
  <div class="hub-section">
    <h2>🔧 Problem Library</h2>
    <p style="color:var(--muted);font-size:.95rem;margin-bottom:16px;line-height:1.65">
      500 operator problem guides across payments, automation, infrastructure, and AI.
      Plain-English causes, fast checks, and what usually fixes it.
    </p>
    <div class="pill-row">
      <a class="pill accent" href="/problems/index.html">Browse All 500 Problems →</a>
      <a class="pill" href="/problems/chargeback-received-what-to-do.html">Chargeback Received</a>
      <a class="pill" href="/problems/email-deliverability-suddenly-dropped.html">Email Deliverability Dropped</a>
      <a class="pill" href="/problems/zapier-task-failed-webhook-timeout.html">Zapier Webhook Failed</a>
      <a class="pill" href="/problems/openai-api-rate-limit-exceeded-fix.html">OpenAI Rate Limit</a>
      <a class="pill" href="/problems/checkout-conversion-suddenly-down.html">Checkout Conversion Down</a>
      <a class="pill" href="/problems/google-ads-disapproved-destination-mismatch.html">Google Ads Disapproved</a>
    </div>
  </div>

  <!-- Operator Guides -->
  <div class="hub-section">
    <h2>📋 Operator Guides</h2>
    <div class="card-grid">
      <a class="card" href="/decisions/switch-payment-processor.html">
        <div class="card-icon">🔄</div>
        <div class="card-title">Should I Switch Processors?</div>
        <div class="card-desc">Signal checklist + stay/switch decision framework.</div>
      </a>
      <a class="card" href="/clusters/ai-workflow-automation.html">
        <div class="card-icon">⚙️</div>
        <div class="card-title">Workflow Automation Guide</div>
        <div class="card-desc">Patterns that work in real 5–50 person operations.</div>
      </a>
      <a class="card" href="/clusters/sops-and-process.html">
        <div class="card-icon">📑</div>
        <div class="card-title">SOPs and Process</div>
        <div class="card-desc">How to document operations so they survive staff changes.</div>
      </a>
      <a class="card" href="/clusters/customer-ops.html">
        <div class="card-icon">🤝</div>
        <div class="card-title">Customer Ops</div>
        <div class="card-desc">Intake, routing, follow-up, and missed-call systems.</div>
      </a>
    </div>
  </div>

  <!-- Concepts -->
  <div class="hub-section">
    <h2>📖 Concept Library</h2>
    <div class="card-grid">
      <a class="card" href="/concepts/ai-automation.html">
        <div class="card-icon">🤖</div>
        <div class="card-title">AI Automation</div>
        <div class="card-desc">What it is, how it works, where it wins vs fails.</div>
      </a>
      <a class="card" href="/concepts/payment-processing.html">
        <div class="card-icon">💳</div>
        <div class="card-title">Payment Processing</div>
        <div class="card-desc">Fee layers, interchange, chargebacks — the full picture.</div>
      </a>
      <a class="card" href="/concepts/crypto-payments.html">
        <div class="card-icon">⛓️</div>
        <div class="card-title">Crypto Payments</div>
        <div class="card-desc">Blockchain settlement, stablecoins, and operator considerations.</div>
      </a>
      <a class="card" href="/concepts/prediction-markets.html">
        <div class="card-icon">📊</div>
        <div class="card-title">Prediction Markets</div>
        <div class="card-desc">How Kalshi and Polymarket work — and when to use them.</div>
      </a>
    </div>
    <div class="pill-row" style="margin-top:14px">
      <a class="pill accent" href="/concepts/index.html">All Concepts →</a>
    </div>
  </div>
"""

    return page_shell(
        title="SideGuy Knowledge Hub — Central Navigation",
        meta_desc="Central navigation for all SideGuy knowledge layers: intelligence, topic hubs, 500 problem guides, operator guides, and concept library.",
        canonical=f"{DOMAIN}/knowledge-hub.html",
        bc_trail=f'<a href="/">SideGuy</a> › Knowledge Hub',
        badge="Knowledge Hub",
        h1="SideGuy Knowledge Hub",
        lede="One place to navigate all SideGuy knowledge layers — intelligence decisions, topic hubs, problem guides, operator playbooks, and concept deep-dives.",
        body_html=body,
        jsonld=jsonld,
    )


# ──────────────────────────────────────────────
# 2–5.  TOPIC HUB BUILDER
# ──────────────────────────────────────────────

def build_topic_hub(slug, title, meta_desc, badge, lede, icon,
                    concepts, guides, problems, pillar_url=None):
    canonical = f"{DOMAIN}/{slug}.html"

    jsonld = f"""  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"Knowledge Hub","item":"{DOMAIN}/knowledge-hub.html"}},
          {{"@type":"ListItem","position":3,"name":"{title}","item":"{canonical}"}}
        ]
      }},
      {{
        "@type": "CollectionPage",
        "name": "{title}",
        "description": "{meta_desc}",
        "url": "{canonical}"
      }}
    ]
  }}"""

    def card_grid(items):
        html = '  <div class="card-grid">\n'
        for ic, ttl, desc, href in items:
            html += f"""    <a class="card" href="{href}">
      <div class="card-icon">{ic}</div>
      <div class="card-title">{ttl}</div>
      <div class="card-desc">{desc}</div>
    </a>
"""
        html += "  </div>\n"
        return html

    def pill_list(items):
        html = '  <div class="pill-row">\n'
        for label, href in items:
            html += f'    <a class="pill" href="{href}">{label}</a>\n'
        html += "  </div>\n"
        return html

    pillar_link = f'\n  <div class="pill-row" style="margin-bottom:24px"><a class="pill accent" href="{pillar_url}">📌 View Full Pillar →</a></div>' if pillar_url else ""

    body = f"""
{pillar_link}

  <!-- Concepts -->
  <div class="hub-section">
    <h2>📖 Concepts</h2>
{card_grid(concepts)}  </div>

  <!-- Guides -->
  <div class="hub-section">
    <h2>📋 Guides &amp; Clusters</h2>
{card_grid(guides)}  </div>

  <!-- Problems -->
  <div class="hub-section">
    <h2>🔧 Problem Guides</h2>
    <p style="color:var(--muted);font-size:.93rem;margin-bottom:14px;line-height:1.6">
      Common operator issues related to {title.lower()} — causes, fast checks, and what usually fixes it.
    </p>
{pill_list(problems)}
    <div style="margin-top:12px">
      <a class="pill accent" href="/problems/index.html">Browse All 500 Problems →</a>
    </div>
  </div>

  <!-- Back to hub -->
  <div style="margin-bottom:40px">
    <a class="pill" href="/knowledge-hub.html">← Knowledge Hub</a>
    &nbsp;
    <a class="pill" href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a>
  </div>
"""

    return page_shell(
        title=f"{title} | SideGuy",
        meta_desc=meta_desc,
        canonical=canonical,
        bc_trail=f'<a href="/">SideGuy</a> › <a href="/knowledge-hub.html">Knowledge Hub</a> › {title}',
        badge=badge,
        h1=title,
        lede=lede,
        body_html=body,
        jsonld=jsonld,
    )


# ──────────────────────────────────────────────
# HUB DEFINITIONS
# ──────────────────────────────────────────────

HUBS = [

    ("ai-automation-hub", "AI Automation Hub",
     "Everything on AI automation for operators — concepts, workflow guides, scheduling, customer service, and 100+ problem pages.",
     "Topic Hub · AI", "⚙️",
     "Concepts, guides, clusters, and problem pages focused on AI automation for real businesses. No hype — practical clarity on what works and what doesn't.",
     # concepts
     [
         ("🤖", "AI Automation", "What it is, types, where it wins vs fails.", "/concepts/ai-automation.html"),
         ("⚙️", "Workflow Automation", "Patterns: intake → routing → summary → action.", "/clusters/ai-workflow-automation.html"),
         ("💬", "AI Customer Service", "What to automate and what to keep human.", "/clusters/ai-customer-service.html"),
         ("📅", "AI Scheduling", "Reminder flows, intake questions, reschedule handling.", "/clusters/ai-scheduling.html"),
     ],
     # guides
     [
         ("📣", "Marketing Automation", "Content, email, review replies — systems that keep your voice.", "/clusters/ai-marketing-automation.html"),
         ("📈", "Sales Automation", "Lead follow-up, pipeline tracking, and CRM sync.", "/clusters/ai-sales-automation.html"),
         ("✉️", "Email Automation", "Sequences that feel personal because they're context-aware.", "/clusters/ai-email-automation.html"),
         ("⚡", "Productivity Tools", "The tools operators actually keep using after month one.", "/clusters/ai-productivity-tools.html"),
     ],
     # problems
     [
         ("AI agent tool calling not working", "/problems/ai-agent-tool-calling-not-working.html"),
         ("OpenAI API rate limit exceeded", "/problems/openai-api-rate-limit-exceeded-fix.html"),
         ("Claude API integration failing", "/problems/claude-api-integration-failing.html"),
         ("Zapier webhook timeout", "/problems/zapier-task-failed-webhook-timeout.html"),
         ("Make.com scenario errors", "/problems/make-com-scenario-errors-troubleshooting.html"),
         ("Calendar double-booked fix", "/problems/calendar-booking-double-booked-fix.html"),
         ("No-show reduction automation", "/problems/no-show-reduction-automation.html"),
         ("CSV import errors", "/problems/csv-import-errors-duplicate-headers.html"),
     ],
     "/pillars/ai-automation.html"),

    ("payments-infrastructure-hub", "Payments Infrastructure Hub",
     "Complete reference for payment processing — fees, interchange, chargebacks, instant settlement, fraud, and crypto rails.",
     "Topic Hub · Payments", "💳",
     "Everything operators need to understand about how money moves — fee layers, settlement mechanics, chargeback systems, and the alternatives to traditional card processing.",
     # concepts
     [
         ("💳", "Payment Processing", "Fee layers, interchange, processor markup, money flow.", "/concepts/payment-processing.html"),
         ("⛓️", "Crypto Payments", "Blockchain settlement, stablecoins, Solana for operators.", "/concepts/crypto-payments.html"),
         ("📊", "Payment Fees", "What you're actually paying and what's negotiable.", "/clusters/payment-fees.html"),
         ("⚡", "Instant Settlement", "Why speed matters and where it helps most.", "/clusters/instant-settlement.html"),
     ],
     # guides
     [
         ("🔄", "Chargebacks", "Prevention systems and response templates.", "/clusters/chargebacks.html"),
         ("🔒", "Payment Security", "PCI, fraud controls, verification layers.", "/clusters/payment-security.html"),
         ("🔀", "Should I Switch Processors?", "Signal checklist + stay/switch framework.", "/decisions/switch-payment-processor.html"),
         ("🏦", "Payments Pillar", "Full Wikipedia-style reference on payments.", "/pillars/payments.html"),
     ],
     # problems
     [
         ("Stripe payout pending for days", "/problems/stripe-payout-pending-for-days.html"),
         ("Chargeback received", "/problems/chargeback-received-what-to-do.html"),
         ("High decline rate — Stripe Radar", "/problems/high-decline-rate-stripe-radar-tuning.html"),
         ("Payment gateway error 502", "/problems/payment-gateway-error-502.html"),
         ("Subscription renewal failed", "/problems/subscription-renewal-failed-recovery.html"),
         ("Auth capture mismatch", "/problems/auth-capture-mismatch-error.html"),
         ("3DS authentication failing", "/problems/3ds-authentication-failing.html"),
         ("POS terminal offline", "/problems/pos-terminal-offline-fix.html"),
     ],
     "/pillars/payments.html"),

    ("prediction-markets-hub", "Prediction Markets Hub",
     "Prediction markets explained — how Kalshi and Polymarket work, use cases for operators, accuracy research, and risk considerations.",
     "Topic Hub · Prediction Markets", "📈",
     "A complete reference for prediction markets — how they work, which platforms matter, where they're accurate, and how operators can use them for business intelligence.",
     # concepts
     [
         ("📊", "Prediction Markets", "How contracts work, pricing, platforms, accuracy.", "/concepts/prediction-markets.html"),
         ("⛓️", "Crypto Payments", "Related: blockchain-based settlement and contract platforms.", "/concepts/crypto-payments.html"),
         ("💱", "Payment Settlement", "How value settlement works in financial markets.", "/concepts/payment-processing.html"),
         ("🤖", "AI Decision Tools", "Where AI and prediction markets overlap in decision support.", "/concepts/ai-automation.html"),
     ],
     # guides
     [
         ("📈", "Payments Pillar", "Broader context on financial infrastructure for operators.", "/pillars/payments.html"),
         ("🔒", "Payment Security", "Risk management basics relevant to market participants.", "/clusters/payment-security.html"),
         ("💳", "Crypto Payments", "The blockchain rails underlying many prediction market platforms.", "/concepts/crypto-payments.html"),
         ("🗺️", "Knowledge Map", "Navigate all connected SideGuy pages.", "/knowledge/sideguy-knowledge-map.html"),
     ],
     # problems
     [
         ("Webhook verification failed", "/problems/webhook-signature-verification-failed.html"),
         ("API key invalid after rotation", "/problems/api-key-invalid-after-rotation.html"),
         ("OAuth redirect URI mismatch", "/problems/oauth-redirect-uri-mismatch-fix.html"),
         ("3DS authentication failing", "/problems/3ds-authentication-failing.html"),
         ("Payment gateway error 502", "/problems/payment-gateway-error-502.html"),
         ("Failed payment retry strategy", "/problems/failed-payment-retry-strategy.html"),
         ("Google Play billing pending", "/problems/google-play-billing-pending-fix.html"),
         ("Subscription proration confusion", "/problems/subscription-proration-confusion.html"),
     ],
     None),

    ("operator-tools-hub", "Operator Tools Hub",
     "CRM selection, SOPs, scheduling, invoicing, and time-saving systems for small business operators — practical guides and problem pages.",
     "Topic Hub · Operator Tools", "🛠️",
     "The practical side of running a small operation — picking the right software, documenting processes, handling customer ops, and building systems that save time without needing a dev.",
     # concepts
     [
         ("🤖", "AI Automation", "Which AI tools are worth adding to your stack.", "/concepts/ai-automation.html"),
         ("⚙️", "Workflow Automation", "Connecting tools to eliminate manual hand-offs.", "/clusters/ai-workflow-automation.html"),
         ("📱", "Software Selection", "Questions to avoid buying the wrong system.", "/clusters/software-selection.html"),
         ("⏱️", "Time-Saving Systems", "The 5 automations most operators should have by month 3.", "/clusters/time-saving-systems.html"),
     ],
     # guides
     [
         ("📑", "SOPs and Process", "Document operations so they survive staff changes.", "/clusters/sops-and-process.html"),
         ("🤝", "Customer Ops", "Intake, routing, follow-up, missed-call capture.", "/clusters/customer-ops.html"),
         ("📱", "CRM for Contractors", "Trade-specific CRM selection framework.", "/generated/best-crm-for-contractors.html"),
         ("📞", "Missed Call Systems", "Auto-text, routing, and lead capture for contractors.", "/generated/how-to-stop-missed-calls-for-contractors.html"),
     ],
     # problems
     [
         ("CRM pipeline stages broken", "/problems/crm-pipeline-stages-broken.html"),
         ("HubSpot forms not submitting", "/problems/hubspot-forms-not-submitting.html"),
         ("QuickBooks sync disconnected", "/problems/quickbooks-sync-disconnected-fix.html"),
         ("Xero bank feed not updating", "/problems/xero-bank-feed-not-updating.html"),
         ("Invoice link not opening", "/problems/invoice-link-not-opening-for-customer.html"),
         ("No-show reduction automation", "/problems/no-show-reduction-automation.html"),
         ("Calendar double-booked fix", "/problems/calendar-booking-double-booked-fix.html"),
         ("Twilio SMS not delivering", "/problems/twilio-sms-not-delivering.html"),
     ],
     "/pillars/small-business-tech.html"),
]


# ──────────────────────────────────────────────
# SITEMAP UPDATE
# ──────────────────────────────────────────────

def update_sitemap(slugs):
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        print("  sitemap.xml not found — skipping")
        return
    content = sitemap_path.read_text()
    new_urls = ""
    added = 0
    for slug in slugs:
        url = f"{DOMAIN}/{slug}.html"
        if url not in content:
            new_urls += f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>0.8</priority></url>\n"
            added += 1
    if new_urls:
        content = content.replace("</urlset>", new_urls + "</urlset>")
        sitemap_path.write_text(content)
    print(f"  Sitemap: {added} URLs added")


# ──────────────────────────────────────────────
# KNOWLEDGE MAP UPDATE
# ──────────────────────────────────────────────

def update_knowledge_map(hub_slugs):
    km_path = ROOT / "knowledge" / "sideguy-knowledge-map.html"
    if not km_path.exists():
        print("  Knowledge map not found")
        return
    content = km_path.read_text()
    if "SIDEGUY_HUBS_SECTION" in content:
        print("  Knowledge map already has Hubs section — skipping")
        return

    node_cards = ""
    entries = [
        ("knowledge-hub", "🗺️", "Knowledge Hub", "Central navigation for all SideGuy knowledge layers."),
        ("ai-automation-hub", "⚙️", "AI Automation Hub", "Concepts, guides, and problems for AI automation."),
        ("payments-infrastructure-hub", "💳", "Payments Infrastructure Hub", "Fees, settlement, chargebacks, fraud — everything payments."),
        ("prediction-markets-hub", "📈", "Prediction Markets Hub", "How Kalshi and Polymarket work and operator use cases."),
        ("operator-tools-hub", "🛠️", "Operator Tools Hub", "CRM, SOPs, scheduling, invoicing — what operators actually use."),
    ]
    for slug, icon, title, desc in entries:
        node_cards += f"""      <a class="node" href="/{slug}.html">
        <span class="node-type type-guide">Hub</span>
        <div class="node-icon">{icon}</div>
        <div class="node-title">{title}</div>
        <div class="node-desc">{desc}</div>
      </a>
"""

    section = f"""
  <!-- SIDEGUY_HUBS_SECTION -->
  <div class="cluster-group">
    <div class="cluster-header">
      <div class="cluster-icon">🧭</div>
      <div>
        <div class="cluster-title">Topic Navigation Hubs</div>
        <div class="cluster-sub">Central knowledge hub + 4 topic hubs — AI, Payments, Prediction Markets, Operator Tools</div>
      </div>
      <a class="cluster-cta" href="/knowledge-hub.html">Knowledge Hub →</a>
    </div>
    <div class="node-grid">
{node_cards}    </div>
  </div>
  <!-- END SIDEGUY_HUBS_SECTION -->
"""

    # Insert before Concepts section if it exists
    if "<!-- SIDEGUY_CONCEPTS_SECTION -->" in content:
        content = content.replace(
            "<!-- SIDEGUY_CONCEPTS_SECTION -->",
            section + "<!-- SIDEGUY_CONCEPTS_SECTION -->",
            1
        )
    elif "<!-- SIDEGUY_PROBLEMS_SECTION -->" in content:
        content = content.replace(
            "<!-- SIDEGUY_PROBLEMS_SECTION -->",
            section + "<!-- SIDEGUY_PROBLEMS_SECTION -->",
            1
        )
    else:
        content = content.replace(
            '<div class="microFooter"',
            section + '<div class="microFooter"',
            1
        )
    km_path.write_text(content)
    print("  Knowledge map updated with Topic Hubs section")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SideGuy Hub Page Builder ===\n")

    built_slugs = []

    # 1. knowledge-hub
    path = ROOT / "knowledge-hub.html"
    if not path.exists() or FORCE:
        html = build_knowledge_hub()
        path.write_text(html)
        print(f"  BUILT: knowledge-hub.html  ({len(html):,} chars)")
    else:
        print("  SKIP: knowledge-hub.html")
    built_slugs.append("knowledge-hub")

    # 2–5. topic hubs
    for slug, title, meta_desc, badge, icon, lede, concepts, guides, problems, pillar in HUBS:
        path = ROOT / f"{slug}.html"
        if not path.exists() or FORCE:
            html = build_topic_hub(slug, title, meta_desc, badge, lede, icon,
                                   concepts, guides, problems, pillar)
            path.write_text(html)
            print(f"  BUILT: {slug}.html  ({len(html):,} chars)")
        else:
            print(f"  SKIP: {slug}.html")
        built_slugs.append(slug)

    print()
    update_sitemap(built_slugs)
    update_knowledge_map(built_slugs)

    print(f"\n=== Done — 5 hub pages ===")
    for s in built_slugs:
        print(f"  {DOMAIN}/{s}.html")
