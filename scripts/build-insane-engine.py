#!/usr/bin/env python3
"""
SIDEGUY INSANE ENGINE v1 — Python build script
Generates: 2 pillar pages, 1 decision page, 8 cluster pages, 12 longtail pages
All styled to match existing SideGuy conventions.
"""

import os
from datetime import datetime, timezone

STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
BASE = "/workspaces/sideguy-solutions"
DOMAIN = "https://sideguysolutions.com"
PHONE_DISPLAY = "773-544-1231"
PHONE_E164 = "+17735441231"

# ─── Shared CSS ────────────────────────────────────────────────────────────────

LIGHT_CSS = """:root{
  --bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;
  --ink:#073044;--muted:#3f6173;--muted2:#5e7d8e;
  --card:#ffffffcc;--card2:#ffffffb8;
  --stroke:rgba(7,48,68,.10);--stroke2:rgba(7,48,68,.07);
  --shadow:0 18px 50px rgba(7,48,68,.10);
  --mint:#21d3a1;--mint2:#00c7ff;--blue:#4aa9ff;--blue2:#1f7cff;
  --r:22px;--pill:999px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;
  background:radial-gradient(ellipse 130% 60% at 60% -10%,var(--bg1),var(--bg0) 55%),var(--bg0);
  color:var(--ink);line-height:1.65;min-height:100vh}
a{color:var(--blue2);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:880px;margin:0 auto;padding:28px 18px 90px}
.bc{font-size:.78rem;color:var(--muted2);margin-bottom:20px}
.bc a{color:var(--muted2)}
h1{font-size:clamp(1.5rem,4vw,2rem);font-weight:900;line-height:1.15;margin-bottom:10px}
.sub{font-size:1rem;color:var(--muted);margin-bottom:24px}
h2{font-size:1.1rem;font-weight:800;margin:26px 0 10px;color:var(--ink)}
h3{font-size:.95rem;font-weight:700;color:var(--muted2);margin:16px 0 6px}
p{color:var(--muted);font-size:.95rem;margin-bottom:12px}
ul{margin-left:20px;color:var(--muted);font-size:.95rem}
li{margin-bottom:5px}
li a{color:var(--blue2)}
.card{background:var(--card);border:1px solid var(--stroke);border-radius:16px;padding:20px;margin-bottom:14px}
.pill-grid{display:flex;flex-wrap:wrap;gap:7px;margin-top:8px}
.pill-grid a{padding:6px 12px;border-radius:var(--pill);border:1px solid var(--stroke);
  background:rgba(255,255,255,.8);font-size:.82rem;font-weight:700;color:var(--ink);text-decoration:none}
.pill-grid a:hover{background:#fff;border-color:var(--mint)}
.related{background:rgba(0,199,255,.07);border:1px solid rgba(0,199,255,.18);border-radius:16px;padding:18px;margin-top:28px}
.related .label{font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted2);margin-bottom:10px}
.cta-box{background:linear-gradient(135deg,rgba(33,211,161,.12),rgba(0,199,255,.08));
  border:1px solid rgba(33,211,161,.25);border-radius:18px;padding:22px;margin-top:28px;text-align:center}
.cta-box p{color:var(--ink);font-weight:600;margin-bottom:10px}
.cta-box a.btn{display:inline-block;padding:11px 22px;background:var(--mint);color:#fff;
  font-weight:800;border-radius:var(--pill);font-size:.9rem}
.floating{position:fixed;bottom:20px;right:20px;z-index:999}
.floating a{display:flex;align-items:center;gap:8px;padding:11px 18px;
  background:linear-gradient(135deg,var(--mint),var(--mint2));
  color:#fff;font-weight:800;border-radius:var(--pill);
  box-shadow:0 8px 28px rgba(33,211,161,.35);text-decoration:none;font-size:.88rem}
.stamp{font-size:.7rem;color:var(--muted2);margin-top:28px;opacity:.7}"""

DARK_CSS = """:root{
  --bg:#07121a;--card:#0b1b25;--text:#e9f2ff;--muted:#a9c0d6;
  --line:#123041;--accent:#68f0c6;--accent2:#7ab6ff;
  --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Courier New",monospace;
  --sans:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
}
*{box-sizing:border-box}
body{margin:0;font-family:var(--sans);
  background:radial-gradient(1200px 700px at 20% 0%,#0b2331 0%,var(--bg) 55%),var(--bg);
  color:var(--text);line-height:1.6}
a{color:var(--accent2);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1040px;margin:0 auto;padding:28px 18px 80px}
.topbar{display:flex;gap:12px;align-items:center;justify-content:space-between;margin-bottom:18px;flex-wrap:wrap}
.badge{font-family:var(--mono);font-size:12px;color:var(--muted);
  border:1px solid var(--line);padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.03)}
h1{font-size:clamp(1.6rem,4vw,2.1rem);line-height:1.15;margin:10px 0 8px;font-weight:900;color:var(--text)}
.sub{color:var(--muted);margin:0 0 22px;font-size:1rem}
.k{color:var(--accent);font-family:var(--mono);font-size:12px}
.layout{display:grid;grid-template-columns:1.25fr .75fr;gap:16px}
@media(max-width:820px){.layout{grid-template-columns:1fr}}
.card{background:rgba(255,255,255,0.03);border:1px solid var(--line);border-radius:14px;padding:20px}
.card h2{margin:22px 0 10px;font-size:1.1rem;font-weight:800;color:var(--text)}
.card h2:first-child{margin-top:0}
.card h3{margin:14px 0 8px;font-size:.95rem;color:var(--accent);font-weight:700}
.card ul{margin:8px 0 0 20px;padding:0}
.card li{margin-bottom:5px;font-size:.95rem;color:var(--muted)}
.card li a{color:var(--accent2)}
.card p{color:var(--muted);font-size:.95rem;margin:8px 0}
.footer{margin-top:30px;color:var(--muted);font-size:.8rem;border-top:1px solid var(--line);padding-top:16px}
.orb{position:fixed;right:18px;bottom:18px;width:72px;height:72px;border-radius:999px;
  background:radial-gradient(circle at 30% 30%,rgba(104,240,198,.95),rgba(122,182,255,.25) 60%,rgba(0,0,0,.25) 100%);
  box-shadow:0 0 0 1px rgba(104,240,198,.25),0 10px 40px rgba(0,0,0,.4);
  display:flex;align-items:center;justify-content:center;text-align:center;animation:pulse 2.2s ease-in-out infinite}
.orb a{color:#001018;font-weight:800;font-size:12px;text-decoration:none}
@keyframes pulse{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-2px) scale(1.03)}}"""

FLOAT_LIGHT = f"""<div class="floating"><a href="sms:{PHONE_E164}">💬 Text PJ · {PHONE_DISPLAY}</a></div>"""

FLOAT_DARK = f"""<div class="orb"><a href="sms:{PHONE_E164}" title="Text PJ">Text<br>PJ</a></div>"""

def schema_breadcrumb(crumbs):
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        items.append(f'{{"@type":"ListItem","position":{i},"name":"{name}","item":"{url}"}}')
    return ('{\n  "@context":"https://schema.org",\n  "@type":"BreadcrumbList",\n  '
            '"itemListElement":[\n    ' + ',\n    '.join(items) + '\n  ]\n}')

def schema_faq(items):
    entities = []
    for q, a in items:
        entities.append(
            f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        )
    return ('{\n  "@context":"https://schema.org",\n  "@type":"FAQPage",\n  '
            '"mainEntity":[\n    ' + ',\n    '.join(entities) + '\n  ]\n}')

def light_head(title, desc, canonical, bc_schema, faq_schema=None):
    schemas = f'<script type="application/ld+json">\n{bc_schema}\n</script>\n'
    if faq_schema:
        schemas += f'<script type="application/ld+json">\n{faq_schema}\n</script>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title}</title>
<link rel="canonical" href="{canonical}"/>
<meta name="description" content="{desc}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="SideGuy Solutions"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary"/>
{schemas}<style>
{LIGHT_CSS}
</style>
</head>"""

def dark_head(title, desc, canonical, bc_schema):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title}</title>
  <meta name="description" content="{desc}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:site_name" content="SideGuy Solutions"/>
  <script type="application/ld+json">
{bc_schema}
</script>
  <style>
{DARK_CSS}
  </style>
</head>"""

# ─── PILLAR PAGES (dark theme) ─────────────────────────────────────────────────

PILLARS = [
    {
        "slug": "payments",
        "title": "Payments & Processing — SideGuy Pillar Guide",
        "h1": "Payments & Processing",
        "desc": "Payment processing explained for operators: fees, settlement speed, chargebacks, and modern payment rails. Clarity before cost.",
        "sub": "Understand your payment stack before you change anything.",
        "clusters": [
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/clusters/instant-settlement.html", "Instant Settlement"),
            ("/clusters/chargebacks.html", "Chargebacks"),
            ("/clusters/payment-security.html", "Payment Security"),
        ],
        "decisions": [
            ("/decisions/switch-payment-processor.html", "Should I Switch Payment Processors?"),
        ],
        "longtail": [
            ("/longtail/why-payment-fees-are-so-high.html", "Why payment processing fees are so high"),
            ("/longtail/how-to-reduce-payment-processing-fees.html", "How to reduce payment processing fees"),
            ("/longtail/what-is-instant-settlement.html", "What is instant settlement?"),
            ("/longtail/how-to-handle-chargebacks.html", "How to handle chargebacks"),
        ],
    },
    {
        "slug": "small-business-tech",
        "title": "Small Business Tech — SideGuy Pillar Guide",
        "h1": "Small Business Tech",
        "desc": "Technology clarity for operators: software selection, SOPs, customer operations, and time-saving systems. No vendor hype.",
        "sub": "Systems that reduce friction without creating complexity.",
        "clusters": [
            ("/clusters/software-selection.html", "Software Selection"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/clusters/time-saving-systems.html", "Time-Saving Systems"),
        ],
        "decisions": [
            ("/decisions/should-i-use-ai.html", "Should I Use AI in My Business?"),
        ],
        "longtail": [
            ("/longtail/best-crm-for-small-business.html", "Best CRM for small business (how to choose)"),
            ("/longtail/how-to-build-sops.html", "How to build SOPs"),
            ("/longtail/how-to-stop-missed-calls.html", "How to stop missed calls"),
            ("/longtail/how-to-automate-invoices.html", "How to automate invoices"),
        ],
    },
]

def build_pillar(p):
    slug = p["slug"]
    canonical = f"{DOMAIN}/pillars/{slug}.html"
    bc = schema_breadcrumb([
        ("SideGuy Solutions", DOMAIN),
        (p["h1"], canonical),
    ])
    head = dark_head(p["title"], p["desc"], canonical, bc)

    cluster_li = "\n".join(f'      <li><a href="{u}">{n}</a></li>' for u, n in p["clusters"])
    decision_li = "\n".join(f'      <li><a href="{u}">{n}</a></li>' for u, n in p["decisions"])
    longtail_li = "\n".join(f'      <li><a href="{u}">{n}</a></li>' for u, n in p["longtail"])

    return f"""{head}
<body>
<div class="wrap">
  <div class="topbar">
    <div class="badge">SideGuy Pillar · <span class="k">Updated</span> {STAMP}</div>
    <div class="badge"><a href="/">Home</a> · <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a></div>
  </div>

  <h1>{p["h1"]}</h1>
  <p class="sub">{p["sub"]}</p>

  <div class="layout">
    <div>
      <div class="card">
        <h2>Topic Clusters</h2>
        <ul>
{cluster_li}
        </ul>
      </div>
      <div class="card">
        <h2>Decision Nodes</h2>
        <ul>
{decision_li}
        </ul>
      </div>
      <div class="card">
        <h2>Long-Tail Pages</h2>
        <ul>
{longtail_li}
        </ul>
      </div>
    </div>
    <div>
      <div class="card">
        <h2>Operator Rule</h2>
        <p>Understand before you change. Know your current state, then decide.</p>
        <h3>Text PJ</h3>
        <p>Want a fast sanity-check? <a href="sms:{PHONE_E164}">{PHONE_DISPLAY}</a></p>
      </div>
      <div class="card">
        <h2>Navigation</h2>
        <ul>
          <li><a href="/">← SideGuy Home</a></li>
          <li><a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a></li>
          <li><a href="/intelligence/problem-index.html">Problem Index</a></li>
          <li><a href="/pillars/ai-automation.html">AI Automation Pillar</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div class="footer">Updated: {STAMP} · SideGuy Solutions · Clarity before cost.</div>
</div>
{FLOAT_DARK}
</body>
</html>"""

# ─── DECISION PAGE (light theme) ──────────────────────────────────────────────

def build_decision():
    canonical = f"{DOMAIN}/decisions/switch-payment-processor.html"
    bc = schema_breadcrumb([
        ("SideGuy Solutions", DOMAIN),
        ("Decisions", f"{DOMAIN}/intelligence/problem-index.html"),
        ("Switch Payment Processors?", canonical),
    ])
    faq = schema_faq([
        ("When should I switch payment processors?",
         "Switch when fees are eating meaningful margin, payouts are delaying cash flow, or your current processor can't support your volume or business type."),
        ("How long does it take to switch payment processors?",
         "A basic switch takes 1–2 weeks. Complex integrations (POS, custom billing, subscriptions) can take 3–6 weeks. Plan for parallel testing before cutting over."),
        ("Will switching payment processors affect my customers?",
         "If done correctly, no. Customers see a checkout experience — not your backend processor. The risk window is the cutover period, so test thoroughly first."),
    ])
    head = light_head(
        "Should I Switch Payment Processors? | SideGuy",
        "A calm decision framework for evaluating payment processor fees, payout speed, reliability, and switching costs. Clarity before cost.",
        canonical, bc, faq
    )
    return f"""{head}
<body>
<div class="wrap">
  <nav class="bc"><a href="/">SideGuy</a> › <a href="/intelligence/problem-index.html">Decisions</a> › Switch Payment Processors?</nav>

  <h1>Should I Switch Payment Processors?</h1>
  <p class="sub">A calm signal checklist — not a vendor pitch.</p>

  <div class="card">
    <h2>Switch Signals</h2>
    <ul>
      <li>Effective rate feels high vs your margins (benchmark: 2–3% total for most businesses)</li>
      <li>Payout delays (net-2, net-7) are hurting cash flow</li>
      <li>Chargebacks are consuming team time with poor dispute tooling</li>
      <li>Poor integration with your POS, invoicing, or accounting stack</li>
      <li>Account holds or freezes without clear explanation</li>
      <li>You want more control over customer data and transaction history</li>
    </ul>
  </div>

  <div class="card">
    <h2>Stay Signals</h2>
    <ul>
      <li>Switching cost (dev time, retraining, downtime) exceeds 6 months of savings</li>
      <li>Your card volume doesn't justify the switch overhead</li>
      <li>You're mid-contract with early termination fees</li>
      <li>Current processor handles high-risk category well and alternatives don't</li>
    </ul>
  </div>

  <div class="card">
    <h2>Operator Rule</h2>
    <p>Run the math: projected monthly savings vs realistic switching cost + 6-week test period. If payback is under 60 days, it's usually worth it. If it's over 6 months, be skeptical of the pitch.</p>
  </div>

  <div class="card">
    <h2>Frequently Asked Questions</h2>
    <h3>When should I switch payment processors?</h3>
    <p>Switch when fees are eating meaningful margin, payouts are delaying cash flow, or your current processor can't support your volume or business type.</p>
    <h3>How long does it take to switch payment processors?</h3>
    <p>A basic switch takes 1–2 weeks. Complex integrations (POS, custom billing, subscriptions) can take 3–6 weeks. Plan for parallel testing before cutting over.</p>
    <h3>Will switching payment processors affect my customers?</h3>
    <p>If done correctly, no. Customers see a checkout experience — not your backend processor. The risk window is the cutover period, so test thoroughly first.</p>
  </div>

  <div class="related">
    <div class="label">Related Knowledge</div>
    <div class="pill-grid">
      <a href="/pillars/payments.html">Payments Pillar</a>
      <a href="/clusters/payment-fees.html">Payment Fees</a>
      <a href="/clusters/chargebacks.html">Chargebacks</a>
      <a href="/longtail/why-payment-fees-are-so-high.html">Why Fees Are High</a>
      <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a>
    </div>
  </div>

  <div class="cta-box">
    <p>Want a fast sanity-check on your current processor before you decide?</p>
    <a href="sms:{PHONE_E164}" class="btn">💬 Text PJ · {PHONE_DISPLAY}</a>
  </div>

  <p class="stamp">Updated: {STAMP} · SideGuy Solutions</p>
</div>
{FLOAT_LIGHT}
</body>
</html>"""

# ─── CLUSTER PAGES (light theme) ──────────────────────────────────────────────

CLUSTERS = [
    {
        "slug": "payment-fees",
        "title": "Payment Processing Fees Explained | SideGuy",
        "h1": "Payment Processing Fees",
        "desc": "Why fees happen, how to read a processor statement, and how operators reduce costs without breaking their payment flow.",
        "intro": "Most operators overpay — not because they're getting cheated, but because they haven't read a statement since they signed up.",
        "what_works": [
            "Understand your effective rate (total fees ÷ total volume)",
            "Negotiate interchange-plus pricing vs flat-rate when volume justifies it",
            "Batch transactions daily to avoid authorization-only holds",
            "Reduce card-not-present (CNP) transactions where possible — they cost more",
        ],
        "warnings": [
            "Flat-rate processors (Stripe, Square at 2.9%) are simple but expensive at scale",
            "Contract processors often hide downgrades — read the interchange table",
            "Monthly minimums and PCI compliance fees add up quietly",
        ],
        "faqs": [
            ("What is an effective payment processing rate?",
             "Your effective rate is total fees paid divided by total card volume. For most businesses it ranges 1.8–3.2%. Above 3% is worth investigating."),
            ("What is interchange-plus pricing?",
             "Interchange-plus separates the card network cost (interchange) from the processor markup. It's more transparent than flat-rate and usually cheaper at volume above $10k/month."),
            ("How do I reduce payment processing fees?",
             "Accept more in-person (card-present) payments, negotiate your markup rate, reduce keyed-in transactions, and audit your statement for unnecessary monthly fees."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/chargebacks.html", "Chargebacks Cluster"),
            ("/longtail/how-to-reduce-payment-processing-fees.html", "How to Reduce Fees"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Payments", f"{DOMAIN}/pillars/payments.html"), ("Payment Fees", "")],
    },
    {
        "slug": "instant-settlement",
        "title": "Instant Settlement for Business | SideGuy",
        "h1": "Instant Settlement",
        "desc": "Settlement speed impacts cash flow, vendor payments, and operational calm. What it is, who offers it, and when it matters.",
        "intro": "Waiting 2–7 days for money you've already earned is a system design choice by your processor — not a law of physics.",
        "what_works": [
            "Same-day or instant settlement processors: Stripe Instant (1% fee), PayPal Instant, Square Instant Deposits",
            "For volume businesses, negotiate next-day standard settlement instead of net-2",
            "ACH push to business account — faster than card pull flows",
            "Crypto settlement (USDC/stablecoins) for contractors and B2B who accept it",
        ],
        "warnings": [
            "Instant settlement often costs 0.5–1.5% extra — run the math on when it's worth it",
            "High-risk merchant categories may not qualify for instant settlement",
            "Instant ≠ irrevocable — chargebacks can still reclaim settled funds",
        ],
        "faqs": [
            ("What is instant settlement in payment processing?",
             "Instant settlement means funds from card transactions appear in your bank account within minutes or hours instead of 2–7 business days."),
            ("Is instant settlement worth the extra fee?",
             "If cash flow timing causes you to delay vendor payments or incur overdraft fees, yes. If you have healthy reserves, probably not worth the premium."),
            ("Which payment processors offer instant settlement?",
             "Stripe (Instant Payouts), Square (Instant Deposit), PayPal, and several bank-integrated processors. Most charge 0.5–1.5% per instant payout."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/longtail/what-is-instant-settlement.html", "What Is Instant Settlement?"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Payments", f"{DOMAIN}/pillars/payments.html"), ("Instant Settlement", "")],
    },
    {
        "slug": "chargebacks",
        "title": "Chargebacks Explained for Operators | SideGuy",
        "h1": "Chargebacks",
        "desc": "Why chargebacks happen, how to respond in time, and the documentation habits that prevent most disputes from escalating.",
        "intro": "A chargeback isn't a fraud claim — it's a dispute. Most are winnable with the right documentation sent within the deadline.",
        "what_works": [
            "Document fulfillment at the time of service: photos, signatures, delivery confirmation",
            "Use clear business names on statements (customers dispute what they don't recognize)",
            "Send dispute responses before the deadline — usually 7–20 days depending on processor",
            "Build a fast-response template: order ID, delivery proof, customer communication log",
        ],
        "warnings": [
            "Chargeback ratio above 1% triggers processor reviews and potential account termination",
            "Friendly fraud (buyer's remorse filed as fraud) is common — fight it with documentation",
            "Never ignore a chargeback — no response = automatic loss",
        ],
        "faqs": [
            ("What is a chargeback?",
             "A chargeback is when a cardholder asks their bank to reverse a charge. The bank pulls the funds from you while the dispute is reviewed. You can win by submitting evidence."),
            ("How do I respond to a chargeback?",
             "Log into your processor dashboard, find the dispute, gather your evidence (order confirmation, delivery proof, communication), and submit before the response deadline."),
            ("How do I prevent chargebacks?",
             "Clear refund policies, recognizable billing descriptors, prompt customer service responses, and documented delivery reduce chargeback rates significantly."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/longtail/how-to-handle-chargebacks.html", "How to Handle Chargebacks"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Payments", f"{DOMAIN}/pillars/payments.html"), ("Chargebacks", "")],
    },
    {
        "slug": "payment-security",
        "title": "Payment Security for Small Business | SideGuy",
        "h1": "Payment Security",
        "desc": "Payment security explained for operators: fraud basics, PCI compliance in plain language, and controls that don't slow down sales.",
        "intro": "Security is a system. The goal isn't zero risk — it's risk that's proportional to the cost of the controls.",
        "what_works": [
            "Use hosted payment pages (Stripe, Square) — you never touch raw card data",
            "Enable AVS (address verification) and CVV checks for card-not-present transactions",
            "Review transaction reports weekly for anomalies — catches fraud before it scales",
            "3DS2 (3D Secure) for high-ticket transactions adds friction but stops most fraud",
        ],
        "warnings": [
            "PCI compliance isn't a one-time checkbox — it's an annual audit + ongoing SAQ",
            "Self-hosted checkout forms create PCI scope — hosted iFrames remove it",
            "Password-reused accounts are the #1 merchant portal compromise vector",
        ],
        "faqs": [
            ("What is PCI compliance?",
             "PCI DSS is the Payment Card Industry Data Security Standard — a set of requirements for any business that stores, processes, or transmits cardholder data. For most small businesses, using a hosted payment page keeps you in the simplest compliance tier."),
            ("Do I need to be PCI compliant?",
             "Yes, if you accept cards. But most small businesses qualify for SAQ-A (the simplest tier) if they use hosted payment pages and never touch card data directly."),
            ("How do I protect against payment fraud?",
             "Enable CVV and AVS checks, review your transaction report weekly, use 3D Secure on high-value orders, and keep your processor credentials in a password manager with 2FA."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/chargebacks.html", "Chargebacks"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Payments", f"{DOMAIN}/pillars/payments.html"), ("Payment Security", "")],
    },
    {
        "slug": "software-selection",
        "title": "How to Choose Business Software | SideGuy",
        "h1": "Software Selection",
        "desc": "How operators choose software without getting oversold: requirements, tradeoffs, and the test-before-commit checklist.",
        "intro": "Most operators regret software purchases made in demos, not in production. Slow down the decision, speed up the test.",
        "what_works": [
            "Define the one problem you're buying the software to solve",
            "Try the free trial on your actual workflow — not a demo scenario",
            "Check integration with your existing stack (accounting, calendar, POS)",
            "Talk to one customer who isn't on their reference list",
        ],
        "warnings": [
            "Annual contracts remove leverage after month 3 — negotiate monthly or quarterly first",
            "Feature count is a distraction — time-saved is the real metric",
            "Data portability: ask how you export everything before you sign",
        ],
        "faqs": [
            ("How do I choose the right software for my business?",
             "Start with the problem, not the features. Define what you're trying to fix, test the top 2–3 options on a real task, and pick the one your team will actually use."),
            ("Should I sign an annual software contract?",
             "Only after running it for 30–60 days and confirming it solves the problem. Annual discounts average 15–20% but cost you leverage if the product disappoints."),
            ("What questions should I ask a software vendor?",
             "Ask: How do I export my data? What's the uptime SLA? Who handles support — chat bot or human? What does the cancellation process look like?"),
        ],
        "related": [
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/longtail/best-crm-for-small-business.html", "Best CRM for Small Business"),
            ("/intelligence/decisions/should-i-use-ai.html", "Should I Use AI?"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Small Business Tech", f"{DOMAIN}/pillars/small-business-tech.html"), ("Software Selection", "")],
    },
    {
        "slug": "sops-and-process",
        "title": "SOPs & Process for Small Business | SideGuy",
        "h1": "SOPs & Process",
        "desc": "Standard operating procedures explained for operators: simple, readable, and actually used. Document once, run calmly forever.",
        "intro": "An SOP doesn't need to be a manual. It needs to answer: who does what, when, and what does 'done' look like.",
        "what_works": [
            "Write SOPs right after doing the task — while it's fresh",
            "Use a 3-part format: Trigger | Steps | Done Criteria",
            "Store them where the work happens (Notion, Google Docs, shared drive — anywhere your team actually opens)",
            "Review quarterly — stale SOPs are worse than none",
        ],
        "warnings": [
            "Overly long SOPs aren't read — 1 page max per process",
            "Don't write SOPs for things you do once a year — write them for weekly/daily work",
            "Version control matters: date every update and archive old versions",
        ],
        "faqs": [
            ("What is an SOP?",
             "A Standard Operating Procedure (SOP) is a documented way of completing a task consistently. For operators, the goal is: anyone on your team can do this right without asking you."),
            ("How long should an SOP be?",
             "One page or less for most tasks. If it's longer, it's either two processes or it needs a checklist format instead of paragraphs."),
            ("What format should I use for SOPs?",
             "Trigger → Steps → Done Criteria. Add screenshots or a short video for visual tasks. Text-only is fine for most things. Stored wherever your team already works."),
        ],
        "related": [
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/longtail/how-to-build-sops.html", "How to Build SOPs"),
            ("/clusters/time-saving-systems.html", "Time-Saving Systems"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Small Business Tech", f"{DOMAIN}/pillars/small-business-tech.html"), ("SOPs & Process", "")],
    },
    {
        "slug": "customer-ops",
        "title": "Customer Operations for Small Business | SideGuy",
        "h1": "Customer Operations",
        "desc": "Customer ops explained: intake, follow-up, missed call handling, and service delivery systems that reduce friction for both sides.",
        "intro": "Customer ops is the gap between your service and their experience. Close the gap with systems, not heroics.",
        "what_works": [
            "Intake form that captures name, problem, timeline, and budget before first call",
            "Auto-confirmation via text/email within 5 minutes of booking",
            "Follow-up sequence 24h after service: satisfaction + referral ask",
            "Missed call text-back within 2 minutes (easily automated)",
        ],
        "warnings": [
            "Generic CRM pipelines don't fit service businesses — customise stages to your actual workflow",
            "Over-automated follow-up feels impersonal — use automation for triggers, human tone for messages",
            "Tracking response time matters more than tracking NPS — fast replies prevent most problems",
        ],
        "faqs": [
            ("What is a customer ops system?",
             "Customer ops is the set of processes that manage how customers interact with your business from first contact to follow-up. The goal is consistent, low-friction experiences that don't depend on who's having a good day."),
            ("How do I handle missed calls automatically?",
             "Most phone systems (OpenPhone, Dialpad, Google Voice Business) support auto-text on missed call. The message should offer to help and give a callback option within 2 minutes."),
            ("What CRM is best for small service businesses?",
             "HubSpot Free, Zoho, or a simple spreadsheet for < 50 customers/month. The tool matters less than whether your team uses it. Start simple."),
        ],
        "related": [
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/longtail/how-to-stop-missed-calls.html", "Stop Missed Calls"),
            ("/longtail/best-crm-for-small-business.html", "Best CRM"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Small Business Tech", f"{DOMAIN}/pillars/small-business-tech.html"), ("Customer Ops", "")],
    },
    {
        "slug": "time-saving-systems",
        "title": "Time-Saving Systems for Operators | SideGuy",
        "h1": "Time-Saving Systems",
        "desc": "Practical time-saving systems for small business operators: automations that remove friction without introducing fragility.",
        "intro": "The best time-saving system is the one that runs without you noticing it. Start with your most repeated task.",
        "what_works": [
            "Text/email auto-responder for new inquiries (immediate response, 24/7)",
            "Recurring invoice automation (Stripe, QuickBooks, Wave)",
            "Calendar booking link instead of back-and-forth scheduling",
            "Weekly report automation instead of manual dashboard pulls",
        ],
        "warnings": [
            "Automating a broken process makes it faster and worse",
            "Over-automating customer touchpoints removes the human warmth that wins loyalty",
            "Track what breaks when you're sick — that's your automation priority list",
        ],
        "faqs": [
            ("What's the best time-saving automation for small business?",
             "Appointment booking automation saves an average of 3–5 hours/week for service businesses. Automated invoice follow-up is second. Both have fast, measurable payback."),
            ("How do I know which processes to automate?",
             "Track what you repeat most. If a task runs weekly and follows the same steps each time, it's automatable. If it requires judgment each time, keep it human."),
            ("Is automation expensive for small businesses?",
             "Entry-level tools cost $0–$50/month and handle most common automations. Zapier, Make.com, and your existing tools (Stripe, Google Calendar, Gmail) cover 80% of needs."),
        ],
        "related": [
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/longtail/how-to-automate-invoices.html", "Automate Invoices"),
            ("/clusters/customer-ops.html", "Customer Ops"),
        ],
        "breadcrumb": [("SideGuy Solutions", DOMAIN), ("Small Business Tech", f"{DOMAIN}/pillars/small-business-tech.html"), ("Time-Saving Systems", "")],
    },
]

def build_cluster(c):
    slug = c["slug"]
    canonical = f"{DOMAIN}/clusters/{slug}.html"
    bc_crumbs = [(n, u if u else canonical) for n, u in c["breadcrumb"]]
    bc_schema = schema_breadcrumb(bc_crumbs)
    faq_schema = schema_faq(c["faqs"])
    head = light_head(c["title"], c["desc"], canonical, bc_schema, faq_schema)

    works_li = "\n".join(f"      <li>{w}</li>" for w in c["what_works"])
    warn_li = "\n".join(f"      <li>{w}</li>" for w in c["warnings"])
    faq_html = ""
    for q, a in c["faqs"]:
        faq_html += f"    <h3>{q}</h3>\n    <p>{a}</p>\n"
    related_pills = "\n".join(f'      <a href="{u}">{n}</a>' for u, n in c["related"])

    bc_parts = " › ".join(
        f'<a href="{u if u else canonical}">{n}</a>' if u else n
        for n, u in c["breadcrumb"]
    )

    return f"""{head}
<body>
<div class="wrap">
  <nav class="bc">{bc_parts}</nav>

  <h1>{c["h1"]}</h1>
  <p class="sub">{c["intro"]}</p>

  <div class="card">
    <h2>What Works</h2>
    <ul>
{works_li}
    </ul>
  </div>

  <div class="card">
    <h2>Watch Out For</h2>
    <ul>
{warn_li}
    </ul>
  </div>

  <div class="card">
    <h2>Frequently Asked Questions</h2>
{faq_html}  </div>

  <div class="related">
    <div class="label">Related Knowledge</div>
    <div class="pill-grid">
{related_pills}
      <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a>
    </div>
  </div>

  <div class="cta-box">
    <p>Want a quick operator take on your specific situation?</p>
    <a href="sms:{PHONE_E164}" class="btn">💬 Text PJ · {PHONE_DISPLAY}</a>
  </div>

  <p class="stamp">Updated: {STAMP} · SideGuy Solutions</p>
</div>
{FLOAT_LIGHT}
</body>
</html>"""

# ─── LONGTAIL PAGES (light theme) ─────────────────────────────────────────────

LONGTAIL = [
    {
        "slug": "ai-automation-for-contractors",
        "title": "AI Automation for Contractors | SideGuy",
        "h1": "AI Automation for Contractors",
        "desc": "How contractors use AI to reduce admin, scheduling friction, and missed calls — without buying enterprise software.",
        "answer": "Contractors lose the most time to three things: scheduling back-and-forth, following up on estimates, and paperwork between jobs. AI handles all three.",
        "points": [
            ("Booking & Scheduling", "Auto-booking links sent after every estimate. Customers pick from real-time availability."),
            ("Estimate Follow-Up", "AI drafts follow-up texts/emails 2 days and 5 days after estimates are sent — you approve, it sends."),
            ("Job Notes & SOPs", "AI summarizes voice notes from the job site into client-ready summaries or invoice line items."),
            ("After-Hours Inquiries", "SMS auto-responder handles new lead contact instantly — before they call the next contractor."),
        ],
        "what_not": "Don't automate the estimate itself or scope-of-work decisions. Clients hire contractors for judgment — keep that human.",
        "faqs": [
            ("Does AI really save time for contractors?", "For admin-heavy contractors, yes — typically 3–6 hours/week. Scheduling, follow-up, and paperwork automation have clear, measurable ROI."),
            ("What AI tools work best for contractors?", "ServiceTitan, Jobber, and Housecall Pro have built-in automation. For lighter needs, Calendly + a simple SMS auto-responder covers most cases."),
            ("Is AI automation expensive for a small contracting business?", "Entry-level tools run $30–$100/month. For a solo operator, even 2 hours/week saved at your billing rate pays for most tools."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-scheduling.html", "AI Scheduling"),
            ("/clusters/ai-customer-service.html", "AI Customer Service"),
            ("/intelligence/decisions/should-i-use-ai.html", "Should I Use AI?"),
        ],
        "pillar": "AI Automation",
        "pillar_url": "/pillars/ai-automation.html",
    },
    {
        "slug": "ai-automation-for-restaurants",
        "title": "AI Automation for Restaurants | SideGuy",
        "h1": "AI Automation for Restaurants",
        "desc": "How restaurants use AI to reduce order errors, automate reservations, and handle guest communications without adding staff.",
        "answer": "Restaurants win with AI on repetitive, rule-based tasks: reservations, FAQ replies, and order routing. The kitchen and hospitality stay human.",
        "points": [
            ("Reservation Automation", "AI-powered reservation systems (OpenTable, Resy) handle booking, reminders, and waitlist — instantly."),
            ("FAQ & Menu Inquiries", "Chatbot or SMS autoresponder answers hours, allergies, parking, and specials without staff time."),
            ("Review Response Drafting", "AI drafts responses to Google and Yelp reviews — you review, approve, post."),
            ("Inventory Alerts", "Threshold-based alerts for low stock tied to POS data — reduces last-minute sourcing scrambles."),
        ],
        "what_not": "Don't automate guest complaint resolution or anything involving a dissatisfied table. Human response is the only acceptable path there.",
        "faqs": [
            ("What AI tools do restaurants use?", "Toast, Square for Restaurants, and Olo have built-in automation. Resy and OpenTable handle reservations. ChatGPT is used by many operators to draft menu descriptions and review responses."),
            ("Can AI help reduce food waste in restaurants?", "Indirectly — demand forecasting tools like Winnow or simple POS trend analysis help predict prep needs and reduce over-ordering."),
            ("Is AI customer service good for restaurants?", "For FAQs and reservations, yes. For complaints or anything requiring hospitality judgment, no. Keep humans on the floor."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-scheduling.html", "AI Scheduling"),
            ("/clusters/ai-customer-service.html", "AI Customer Service"),
            ("/clusters/ai-marketing-automation.html", "AI Marketing Automation"),
        ],
        "pillar": "AI Automation",
        "pillar_url": "/pillars/ai-automation.html",
    },
    {
        "slug": "ai-automation-for-real-estate",
        "title": "AI Automation for Real Estate | SideGuy",
        "h1": "AI Automation for Real Estate",
        "desc": "How real estate agents and brokerages use AI to handle lead follow-up, listing content, and client communication without losing the human relationship.",
        "answer": "Real estate AI wins on speed: instant lead response, automated follow-up sequences, and listing content drafts. It loses on judgment: pricing, negotiation, relationship trust.",
        "points": [
            ("Lead Response Speed", "AI auto-responds to new inquiries within 60 seconds — dramatically higher contact rates than next-day replies."),
            ("Follow-Up Sequences", "Automated drip campaigns for buyer/seller leads with conditional logic based on engagement."),
            ("Listing Content Drafts", "AI generates first-draft MLS descriptions from your property notes — you refine and publish."),
            ("CRM Automation", "Trigger-based task creation: new lead → create follow-up task → assign to agent → track to close."),
        ],
        "what_not": "Don't automate pricing conversations, offer negotiations, or any conversation where trust and judgment are the actual product.",
        "faqs": [
            ("What CRM is best for real estate AI automation?", "Follow Up Boss, HubSpot, and kvCORE have strong automation tooling. Salesforce works but is overkill for most independent agents."),
            ("Does AI replace real estate agents?", "No. AI handles speed and repetition. Real estate is a trust and judgment business at the point of purchase. The human relationship is the product."),
            ("How fast should AI respond to real estate leads?", "Under 5 minutes dramatically improves conversion. Under 60 seconds is ideal. Every hour of delay loses meaningful contact rate."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-customer-service.html", "AI Customer Service"),
            ("/clusters/ai-marketing-automation.html", "AI Marketing Automation"),
            ("/clusters/ai-email-automation.html", "AI Email Automation"),
        ],
        "pillar": "AI Automation",
        "pillar_url": "/pillars/ai-automation.html",
    },
    {
        "slug": "ai-automation-for-medical-offices",
        "title": "AI Automation for Medical Offices | SideGuy",
        "h1": "AI Automation for Medical Offices",
        "desc": "How medical practices use AI for scheduling, intake, and patient communications — without creating HIPAA exposure.",
        "answer": "Medical office AI wins on front-desk friction: appointment booking, intake forms, and insurance verification. It runs into HIPAA walls when clinical data enters the loop.",
        "points": [
            ("Appointment Scheduling", "AI booking systems reduce phone volume by 40–60% for most practices. Reminders cut no-shows."),
            ("Intake Forms", "Digital intake before the appointment speeds check-in and reduces front-desk burden."),
            ("Insurance Verification", "Automated eligibility checks via Availity or similar before appointments — flags issues in advance."),
            ("After-Visit Summaries", "AI-assisted note summarization (Ambient AI, Nuance DAX) reduces documentation time per visit."),
        ],
        "what_not": "Any AI system handling PHI must be covered by a BAA (Business Associate Agreement). Don't use general-purpose AI tools with patient data unless HIPAA compliance is confirmed.",
        "faqs": [
            ("Is AI HIPAA compliant?", "General AI tools (ChatGPT, etc.) are not HIPAA compliant by default. Purpose-built medical AI tools with BAA agreements are. Verify before any use with patient data."),
            ("What AI tools are approved for medical offices?", "Nuance DAX, Ambient Clinical Intelligence (ACI), and several EHR-native AI features have HIPAA compliance. Your EHR vendor is usually the safest starting point."),
            ("How do I reduce no-shows with AI?", "Automated appointment reminders via text and email (24h and 2h before) consistently reduce no-shows 20–40%. Most modern scheduling systems include this."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-scheduling.html", "AI Scheduling"),
            ("/clusters/ai-customer-service.html", "AI Customer Service"),
            ("/intelligence/decisions/should-i-use-ai.html", "Should I Use AI?"),
        ],
        "pillar": "AI Automation",
        "pillar_url": "/pillars/ai-automation.html",
    },
    {
        "slug": "why-payment-fees-are-so-high",
        "title": "Why Are Payment Processing Fees So High? | SideGuy",
        "h1": "Why Payment Processing Fees Are So High",
        "desc": "A plain-language breakdown of why you pay 2–3% per swipe and who actually gets that money.",
        "answer": "Every card transaction passes through 4 parties who each take a cut: the card network, the card-issuing bank, your acquiring bank, and your payment processor. You see one rate — it's actually 4 separate fees bundled.",
        "points": [
            ("Card Network Fee", "Visa/Mastercard/Amex charge between 0.13–0.15% per transaction. Small, but unavoidable."),
            ("Interchange Fee", "The issuing bank (your customer's bank) takes the largest cut — typically 1.5–2.2% for rewards cards, lower for debit."),
            ("Processor Markup", "Your payment processor (Stripe, Square, etc.) adds 0.2–0.5% on top plus a per-transaction fee ($0.10–$0.30)."),
            ("Rewards Cards Cost More", "Premium travel and cashback cards have higher interchange rates — the rewards come from merchant fees."),
        ],
        "what_not": "Don't try to surcharge customers without understanding your state laws and card network rules — illegal or policy-violating surcharges create chargebacks and account risk.",
        "faqs": [
            ("Who gets the money from payment processing fees?", "Roughly 70–80% goes to the card-issuing bank (interchange), 10–15% to the card network, and 10–15% to your processor."),
            ("Why do rewards cards cost merchants more?", "Reward programs are funded by interchange. The higher the cardholder reward, the higher the interchange rate charged to the merchant."),
            ("Can I pass payment processing fees to customers?", "In most US states, yes — with required disclosures and network compliance. Some states restrict it. Cash discount programs are an alternative."),
        ],
        "related": [
            ("/clusters/payment-fees.html", "Payment Fees Cluster"),
            ("/pillars/payments.html", "Payments Pillar"),
            ("/longtail/how-to-reduce-payment-processing-fees.html", "Reduce Payment Fees"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "pillar": "Payments",
        "pillar_url": "/pillars/payments.html",
    },
    {
        "slug": "how-to-reduce-payment-processing-fees",
        "title": "How to Reduce Payment Processing Fees | SideGuy",
        "h1": "How to Reduce Payment Processing Fees",
        "desc": "Practical steps operators take to lower effective rate, negotiate markup, and reduce the cost of accepting cards.",
        "answer": "You can't eliminate interchange, but you can reduce it by accepting lower-cost card types, negotiating processor markup, and eliminating unnecessary add-on fees.",
        "points": [
            ("Calculate Your Effective Rate First", "Total monthly fees ÷ total card volume = effective rate. Know this before any negotiation."),
            ("Negotiate Processor Markup", "Once you're over $10k/month in card volume, processors will negotiate. Ask for interchange-plus pricing."),
            ("Reduce Card-Not-Present Transactions", "Keyed-in and e-commerce transactions cost more than swiped/tapped. Move recurring customers to in-person ACH or direct bank transfer where possible."),
            ("Audit Monthly Fees", "Most processors pile on: PCI non-compliance fee, statement fee, monthly minimum, gateway fee. Review your monthly statement line by line."),
        ],
        "what_not": "Don't switch processors just for the base rate — always calculate total cost including monthly fees, batch fees, and the cost of your team's time to manage disputes.",
        "faqs": [
            ("What is a good payment processing rate?", "1.8–2.5% effective rate for in-person businesses. 2.5–3.2% for online-heavy. Above 3% is worth reviewing. Below 1.7% usually means high debit mix or large volume negotiation."),
            ("Can I negotiate payment processing fees?", "Yes, for monthly volume above $5–10k most processors will negotiate markup. Flat-rate processors (Stripe basic, Square) don't negotiate — but other cost levers exist."),
            ("Is ACH cheaper than credit card processing?", "Yes — ACH costs $0.20–$1.50 flat per transaction regardless of amount. For invoices over $500, ACH is almost always cheaper than card."),
        ],
        "related": [
            ("/clusters/payment-fees.html", "Payment Fees Cluster"),
            ("/longtail/why-payment-fees-are-so-high.html", "Why Fees Are High"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
            ("/pillars/payments.html", "Payments Pillar"),
        ],
        "pillar": "Payments",
        "pillar_url": "/pillars/payments.html",
    },
    {
        "slug": "what-is-instant-settlement",
        "title": "What Is Instant Settlement? | SideGuy",
        "h1": "What Is Instant Settlement?",
        "desc": "Instant settlement explained: what it means, which processors offer it, what it costs, and when it's worth paying for.",
        "answer": "Instant settlement means your card revenue is deposited within minutes or hours instead of 1–7 business days. It usually costs an additional 0.5–1.5% per deposit but can eliminate cash flow gaps.",
        "points": [
            ("Standard Settlement Timeline", "Most processors settle in T+1 to T+2 (next or day-after business day). Some older setups run T+3 to T+7."),
            ("Instant Payout Cost", "Stripe charges 1% for Instant Payouts. Square charges 1.5%. PayPal charges 1%. These fees are per payout, not per transaction."),
            ("When It Pays Off", "If delayed settlement forces you to use a credit line, the interest cost usually exceeds the instant payout fee. Calculate the actual cost comparison."),
            ("ACH as Alternative", "If same-day isn't critical, ACH to your bank account is typically next-day and low-cost — no instant payout premium required."),
        ],
        "what_not": "Instant settlement isn't automatically better. If you have healthy operating cash, you're paying a premium for speed you don't need.",
        "faqs": [
            ("What is instant settlement in payment processing?", "Instant settlement deposits funds from card transactions into your bank account within minutes instead of 1–7 days. It's an optional feature most processors charge a premium for."),
            ("Is instant settlement safe?", "Yes — the funds are real and immediately accessible. The caveat: chargebacks can still reverse settled funds weeks later, so it's not 'irrevocable.'"),
            ("Which payment processors offer instant settlement?", "Stripe (Instant Payouts), Square (Instant Deposits), PayPal (Instant Transfer), and several integrated bank processors. Most charge 1–1.5% per payout."),
        ],
        "related": [
            ("/clusters/instant-settlement.html", "Instant Settlement Cluster"),
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "pillar": "Payments",
        "pillar_url": "/pillars/payments.html",
    },
    {
        "slug": "how-to-handle-chargebacks",
        "title": "How to Handle Chargebacks | SideGuy",
        "h1": "How to Handle Chargebacks",
        "desc": "Step-by-step guide to responding to chargebacks, gathering the right evidence, and building habits that prevent most disputes from starting.",
        "answer": "Most chargebacks are winnable with the right documentation submitted before the deadline. The operators who lose are usually the ones who don't respond.",
        "points": [
            ("Step 1 — Respond Immediately", "Log in to your processor dashboard. Find the dispute. Note the response deadline — usually 7–20 days. Don't miss it."),
            ("Step 2 — Gather Evidence", "Collect: order confirmation, delivery proof, customer communication, signed terms, refund policy. Photos if applicable."),
            ("Step 3 — Write a Response", "One paragraph: what was ordered, when it was delivered, what proof you have. Include your refund policy."),
            ("Step 4 — Send Everything", "Upload all documents to the processor portal. Keep a copy. The evidence bundle wins or loses the case."),
        ],
        "what_not": "Don't contact the customer directly during an open dispute unless your processor explicitly allows it — it can be used against you.",
        "faqs": [
            ("Can I win a chargeback?", "Yes. Win rates depend on documentation quality and chargeback reason code. Merchants with strong evidence win 40–60% of disputes they respond to. Non-response is automatic loss."),
            ("How long do I have to respond to a chargeback?", "Usually 7–20 days from the notification date depending on processor and card network. Stripe and Square typically give 7–10 days. Check your processor portal immediately."),
            ("How do I prevent chargebacks?", "Clear billing descriptors (use your business name), documented delivery, easy return/refund policies, and fast first response to complaints prevent the majority of chargebacks before they start."),
        ],
        "related": [
            ("/clusters/chargebacks.html", "Chargebacks Cluster"),
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-security.html", "Payment Security"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
        "pillar": "Payments",
        "pillar_url": "/pillars/payments.html",
    },
    {
        "slug": "best-crm-for-small-business",
        "title": "Best CRM for Small Business (How to Choose) | SideGuy",
        "h1": "Best CRM for Small Business",
        "desc": "How to choose the right CRM for your small business without paying for features you'll never use. Honest comparison, no affiliate links.",
        "answer": "The best CRM is the one your team actually uses. A spreadsheet that's current beats a Salesforce nobody opens.",
        "points": [
            ("Under 50 Customers/Month", "Google Sheets or Airtable is fine. Free, fast, and no training needed."),
            ("50–200 Customers/Month", "HubSpot Free or Zoho Free tier. Both handle contacts, deals, and basic follow-up automation."),
            ("Service Businesses (Appointments)", "Jobber, ServiceM8, or HouseCall Pro are built for service workflow — CRM + scheduling + invoicing in one."),
            ("B2B Sales Motion", "HubSpot Starter or Pipedrive if you have a pipeline with multiple stages and sales reps."),
        ],
        "what_not": "Don't pay for Salesforce at under $1M revenue unless you have a dedicated admin and integration requirements that justify it.",
        "faqs": [
            ("What CRM do small businesses use most?", "HubSpot Free and Zoho CRM are the most common for small businesses under $1M revenue. Jobber and ServiceM8 dominate service businesses. Pipedrive for B2B sales."),
            ("Is a free CRM enough for small business?", "For most businesses under 200 customers/month, yes. HubSpot Free, Zoho Free, and even Notion templates handle core contact management and follow-up tracking without cost."),
            ("How do I migrate from spreadsheets to a CRM?", "Export your spreadsheet to CSV, import to the CRM, map your columns, and spend one hour cleaning up duplicates. Most modern CRMs have a CSV import wizard."),
        ],
        "related": [
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/software-selection.html", "Software Selection"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/clusters/time-saving-systems.html", "Time-Saving Systems"),
        ],
        "pillar": "Small Business Tech",
        "pillar_url": "/pillars/small-business-tech.html",
    },
    {
        "slug": "how-to-build-sops",
        "title": "How to Build SOPs for Small Business | SideGuy",
        "h1": "How to Build SOPs",
        "desc": "A practical guide to writing standard operating procedures that your team will actually read and follow.",
        "answer": "Write the SOP right after doing the task. Use a 3-part format. Keep it under one page. Store it where the work happens.",
        "points": [
            ("Format: Trigger → Steps → Done Criteria", "Every SOP answers: what starts this? what are the exact steps? how do I know it's complete?"),
            ("Write it Fresh", "Document the task the day you do it, not a month later. Accuracy drops fast from memory."),
            ("One Page Maximum", "If it's longer, split into two SOPs or use a checklist. Unread SOPs are worse than no SOPs."),
            ("Store Where Work Happens", "Google Docs, Notion, or even a shared drive folder. The tool doesn't matter — proximity to the workflow does."),
        ],
        "what_not": "Don't write SOPs for tasks you do once a year or tasks that require judgment each time. SOPs are for repeatable, rule-based tasks.",
        "faqs": [
            ("What does SOP stand for?", "Standard Operating Procedure — a documented method for completing a repeatable task consistently, regardless of who does it."),
            ("How long should an SOP be?", "One page or less for most tasks. If your SOP needs 3 pages, it's either two processes or it needs to be condensed into a checklist."),
            ("What tools do businesses use to store SOPs?", "Notion, Google Docs, Confluence, and simple shared drives are all common. The most important factor is that it's where your team naturally looks — not a separate 'documentation system' nobody opens."),
        ],
        "related": [
            ("/clusters/sops-and-process.html", "SOPs & Process Cluster"),
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/time-saving-systems.html", "Time-Saving Systems"),
            ("/clusters/customer-ops.html", "Customer Ops"),
        ],
        "pillar": "Small Business Tech",
        "pillar_url": "/pillars/small-business-tech.html",
    },
    {
        "slug": "how-to-stop-missed-calls",
        "title": "How to Stop Missed Calls Losing Business | SideGuy",
        "h1": "How to Stop Missed Calls",
        "desc": "Practical systems for service businesses to capture missed call leads before they call the next number on Google.",
        "answer": "You have 2 minutes before a missed call becomes a lost lead. Auto-text-back is the single highest-ROI response system most small businesses don't have.",
        "points": [
            ("Auto Text-Back on Missed Call", "Most business phone systems (OpenPhone, Dialpad, Google Voice Business) support this out of the box. Message: 'Hey, we missed your call — we'll be back within [X]. Or reply here.'"),
            ("Voicemail That Prompts Action", "Replace generic voicemail with: 'We're unavailable — text this number for faster response.' Deflects to SMS where response is easier."),
            ("Call Routing Logic", "Ring primary → ring backup → route to voicemail + auto-text. One setup prevents 90% of dropped lead situations."),
            ("Track the Metric", "Know your missed call rate weekly. If it's above 15%, you have a capacity or system problem — not just a phone problem."),
        ],
        "what_not": "Don't use a general AI phone agent for service intake unless you've tested it with real customers. Poorly handled calls lose trust faster than a missed call.",
        "faqs": [
            ("What is the best auto-text-back system for missed calls?", "OpenPhone, Dialpad, and Google Voice Business all include missed-call auto-text. For service businesses with field staff, OpenPhone has the clearest UX."),
            ("How quickly should I respond to a missed call?", "Under 2 minutes for a text response. Under 30 minutes for a callback. Every hour of delay reduces contact rate by roughly 10%."),
            ("Does auto text-back work for all business types?", "Yes for inquiry-based businesses. Less useful for inbound customer support lines where issues require immediate phone resolution."),
        ],
        "related": [
            ("/clusters/customer-ops.html", "Customer Ops Cluster"),
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/time-saving-systems.html", "Time-Saving Systems"),
            ("/clusters/ai-scheduling.html", "AI Scheduling"),
        ],
        "pillar": "Small Business Tech",
        "pillar_url": "/pillars/small-business-tech.html",
    },
    {
        "slug": "how-to-automate-invoices",
        "title": "How to Automate Invoices for Small Business | SideGuy",
        "h1": "How to Automate Invoices",
        "desc": "Practical invoice automation for small businesses: recurring billing, auto-send on job completion, and follow-up sequences that get paid faster.",
        "answer": "Manual invoicing costs 15–45 minutes per invoice in admin time. Automation brings that to under 2 minutes while improving payment speed.",
        "points": [
            ("Recurring Billing Setup", "For regular clients: create a recurring invoice in Stripe, QuickBooks, or Wave. It sends and charges automatically on your schedule."),
            ("Trigger-Based Invoice Send", "Configure your job management tool to auto-send an invoice when a job is marked complete. Jobber, ServiceM8, and HouseCall Pro all support this."),
            ("Payment Reminder Sequence", "Auto-send: reminder 3 days before due → reminder on due date → overdue notice 3 days after. Reduces manual follow-up by 70%+."),
            ("ACH/Bank Transfer Option", "Add ACH payment option to invoices over $500. Faster for clients with AP approval workflows, and cheaper for you."),
        ],
        "what_not": "Don't fully automate invoice disputes or unusual charges. When a client questions a line item, human response maintains the relationship.",
        "faqs": [
            ("What's the best invoice automation software for small business?", "QuickBooks Online for accounting-integrated businesses. Stripe Invoicing for tech-forward operators. Jobber/ServiceM8 for field service. Wave for bootstrapped teams (free)."),
            ("How does invoice automation improve cash flow?", "Automated sending eliminates delay between job completion and invoice delivery. Automated reminders cut average payment time by 30–50% according to most SMB studies."),
            ("Can I automate invoice follow-ups?", "Yes — QuickBooks, FreshBooks, and Stripe all support configurable automatic payment reminder sequences. Set it once, let it run."),
        ],
        "related": [
            ("/clusters/time-saving-systems.html", "Time-Saving Systems Cluster"),
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/clusters/customer-ops.html", "Customer Ops"),
        ],
        "pillar": "Small Business Tech",
        "pillar_url": "/pillars/small-business-tech.html",
    },
]

def build_longtail(lt):
    slug = lt["slug"]
    canonical = f"{DOMAIN}/longtail/{slug}.html"
    pillar = lt["pillar"]
    pillar_url = lt["pillar_url"]
    bc_schema = schema_breadcrumb([
        ("SideGuy Solutions", DOMAIN),
        (pillar, f"{DOMAIN}{pillar_url}"),
        (lt["h1"], canonical),
    ])
    faq_schema = schema_faq(lt["faqs"])
    head = light_head(lt["title"], lt["desc"], canonical, bc_schema, faq_schema)

    points_html = ""
    for label, detail in lt["points"]:
        points_html += f'  <div class="card">\n    <h3>{label}</h3>\n    <p>{detail}</p>\n  </div>\n'

    faq_html = ""
    for q, a in lt["faqs"]:
        faq_html += f"    <h3>{q}</h3>\n    <p>{a}</p>\n"

    related_pills = "\n".join(f'      <a href="{u}">{n}</a>' for u, n in lt["related"])

    return f"""{head}
<body>
<div class="wrap">
  <nav class="bc"><a href="/">SideGuy</a> › <a href="{pillar_url}">{pillar}</a> › {lt["h1"]}</nav>

  <h1>{lt["h1"]}</h1>
  <p class="sub">{lt["answer"]}</p>

{points_html}
  <div class="card">
    <h2>Watch Out For</h2>
    <p>{lt["what_not"]}</p>
  </div>

  <div class="card">
    <h2>Frequently Asked Questions</h2>
{faq_html}  </div>

  <div class="related">
    <div class="label">Related Knowledge</div>
    <div class="pill-grid">
{related_pills}
      <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a>
    </div>
  </div>

  <div class="cta-box">
    <p>Want a quick operator take on your situation?</p>
    <a href="sms:{PHONE_E164}" class="btn">💬 Text PJ · {PHONE_DISPLAY}</a>
  </div>

  <p class="stamp">Updated: {STAMP} · SideGuy Solutions</p>
</div>
{FLOAT_LIGHT}
</body>
</html>"""

# ─── WRITE ALL FILES ───────────────────────────────────────────────────────────

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created: {path.replace(BASE + '/', '')}")

if __name__ == "__main__":
    # Pillars
    for p in PILLARS:
        write(f"{BASE}/pillars/{p['slug']}.html", build_pillar(p))

    # Decision page
    write(f"{BASE}/decisions/switch-payment-processor.html", build_decision())

    # New clusters
    for c in CLUSTERS:
        write(f"{BASE}/clusters/{c['slug']}.html", build_cluster(c))

    # Longtail pages
    for lt in LONGTAIL:
        write(f"{BASE}/longtail/{lt['slug']}.html", build_longtail(lt))

    print(f"\nDone: {len(PILLARS)} pillars, 1 decision, {len(CLUSTERS)} clusters, {len(LONGTAIL)} longtail pages")
