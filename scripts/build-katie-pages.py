#!/usr/bin/env python3
"""
SideGuy — Katie Pages Builder
Generates 50+ app-development & custom-software landing pages for web searchers
who want to build apps, targeting Katie's four specialties across 18 industries.
Output: katie/*.html  (flat inside katie/ subdirectory)
"""
import os, json, datetime
from pathlib import Path

ROOT     = Path(".").resolve()
OUT      = ROOT / "katie"
OUT.mkdir(parents=True, exist_ok=True)

DOMAIN     = "https://sideguysolutions.com"
PHONE_SMS  = "sms:+17735441231"
PHONE_DISP = "773-544-1231"
TODAY      = datetime.date.today().isoformat()

# ── Katie's four service areas ────────────────────────────────────────────────
SERVICES = [
    {
        "key":   "custom-software",
        "label": "Custom Software Development",
        "icon":  "⚙️",
        "tagline": "Purpose-built tools for how you actually work — not shelf software jammed into your process.",
        "bullets": [
            "Scoped to your workflow, not a generic SaaS template",
            "Integrates with your existing tools (CRM, accounting, scheduling)",
            "You own the code — no vendor lock-in",
            "Iterative builds: working software fast, then refined",
        ],
        "questions": [
            ("What does it cost?", "Most projects start with a scoping call — no surprise invoices. Custom software ranges widely; clearly defined scope = clearly defined cost."),
            ("How long does it take?", "A focused MVP typically lands in 4–12 weeks. Full custom platforms vary. Timeline depends on scope, integrations, and how quickly feedback comes back."),
            ("Do you do maintenance after launch?", "Yes. Katie can own ongoing support, or hand off clean documented code to your internal team — whichever serves you better."),
            ("What if I just have an idea and no spec?", "That's normal. Start with a text. PJ will get Katie on it and you'll get a plain-language scope draft, no commitment needed."),
        ],
    },
    {
        "key":   "mobile-app",
        "label": "Mobile App Development",
        "icon":  "📱",
        "tagline": "iOS and Android apps built for real-world operator use — not App-Store theater.",
        "bullets": [
            "Native iOS + Android or cross-platform (React Native / Flutter)",
            "Field-ready UX: works on gloves, bright sun, one hand",
            "Offline-first options for crews without reliable data signal",
            "App Store submission + CDN distribution handled",
        ],
        "questions": [
            ("Do I need both iOS and Android?", "Depends on your crew and customers. Katie will ask that first. Cross-platform saves budget when both are needed."),
            ("Can it work without internet?", "Yes. Offline-first architecture is a real option — syncs when connectivity returns. Common for field crews."),
            ("What about push notifications?", "Included by default for anything requiring customer or crew updates."),
            ("What's the App Store review process?", "Katie handles submission and manages any reviewer feedback. Typically 24–72 hours for approval."),
        ],
    },
    {
        "key":   "web-app",
        "label": "Web App & Full-Stack Development",
        "icon":  "🌐",
        "tagline": "Dashboards, portals, booking systems, internal tools — if it runs in a browser, it belongs here.",
        "bullets": [
            "Customer-facing portals, booking/scheduling, quoting tools",
            "Internal dashboards: job tracking, inventory, team ops",
            "API design + integrations (Stripe, QuickBooks, CRMs, webhooks)",
            "Scalable cloud deployment — AWS, GCP, Vercel, or your host",
        ],
        "questions": [
            ("What's the difference between a website and a web app?", "A website is mostly read-only. A web app has user accounts, live data, forms that do things, and logic behind the scenes."),
            ("Can it connect to my existing software?", "Most common SaaS tools have APIs. Katie will map the integration surface in the scoping call."),
            ("Who hosts it?", "Your choice. Katie can deploy to your infrastructure or set up managed cloud hosting with transparent costs."),
            ("Do I need a database?", "Almost certainly yes. Katie selects the right one (SQL vs NoSQL) based on your data shape and query patterns."),
        ],
    },
    {
        "key":   "ai-automation",
        "label": "AI Automation & Smart App Development",
        "icon":  "🤖",
        "tagline": "AI that actually runs your workflows — not a chatbot bolted onto a slow process.",
        "bullets": [
            "LLM-powered workflows: intake, triage, draft, route, escalate",
            "Document extraction + classification (invoices, contracts, forms)",
            "Custom AI agents wired into your existing tools",
            "Model selection matched to your budget and data sensitivity",
        ],
        "questions": [
            ("Do I need to understand AI to get value from it?", "No. Katie translates your workflow into the right AI stack. You describe the problem; she designs the system."),
            ("Is my data safe?", "Yes. Data residency, model selection, and privacy controls are part of every AI project scoping."),
            ("What's the difference between an AI agent and a chatbot?", "A chatbot answers questions. An AI agent takes actions — reads your inbox, files a ticket, sends a follow-up, flags anomalies."),
            ("Can AI integrate with my current tools?", "Usually yes. Zapier, Make, native APIs, or custom middleware — Katie will find the right connection layer."),
        ],
    },
]

# ── Industries ────────────────────────────────────────────────────────────────
INDUSTRIES = [
    ("restaurants",         "Restaurants & Food Service"),
    ("contractors",         "General Contractors"),
    ("hvac",                "HVAC Companies"),
    ("plumbers",            "Plumbing Companies"),
    ("electricians",        "Electrical Contractors"),
    ("realtors",            "Real Estate & Realtors"),
    ("dentists",            "Dental Practices"),
    ("law-firms",           "Law Firms"),
    ("landscapers",         "Landscaping Companies"),
    ("accountants",         "Accounting Firms"),
    ("insurance-agents",    "Insurance Agencies"),
    ("chiropractors",       "Chiropractic Clinics"),
    ("pest-control",        "Pest Control Companies"),
    ("roofers",             "Roofing Contractors"),
    ("physical-therapy",    "Physical Therapy Clinics"),
    ("medical-offices",     "Medical Offices"),
    ("ecommerce",           "E-Commerce Businesses"),
    ("saas",                "SaaS & Software Companies"),
]

# Industry-specific pain lines surfaced in industry pages
INDUSTRY_PAINS = {
    "restaurants":       ["job-costing spreadsheets that break mid-service", "reservation and waitlist chaos", "staff scheduling across locations"],
    "contractors":       ["bid sheets in 12 formats", "job-site photo management", "subcontractor coordination without a paper trail"],
    "hvac":              ["dispatch and routing done by phone", "maintenance contract reminders sent manually", "parts inventory tracked in a notebook"],
    "plumbers":          ["job status updates called in from the field", "invoicing delayed until the truck returns", "recurring maintenance missed"],
    "electricians":      ["permit documents scattered across email", "punch-list management on paper", "customer follow-up falling through the cracks"],
    "realtors":          ["lead follow-up still manual", "offer tracking in spreadsheets", "client portals that don't reflect real-time status"],
    "dentists":          ["appointment reminders sent one at a time", "insurance pre-auth tracked manually", "patient intake forms on paper"],
    "law-firms":         ["intake questionnaires emailed back and forth", "deadline and calendar management split across tools", "client portal that's just a shared folder"],
    "landscapers":       ["route optimization done by memory", "crew task assignments via group text", "seasonal contract renewals tracked manually"],
    "accountants":       ["document collection still via email attachment", "client portal security concerns", "recurring billing that requires manual work each month"],
    "insurance-agents":  ["lead routing from multiple sources", "renewal tracking in a spreadsheet", "policy doc delivery still manual"],
    "chiropractors":     ["intake and SOAP notes on paper", "rebooking reminders sent manually", "insurance eligibility checked one patient at a time"],
    "pest-control":      ["route sheets printed every morning", "customer notification of arrival time still a phone call", "annual contract renewal tracking"],
    "roofers":           ["estimates built in Excel, versioned through email", "job photo uploads from the field", "materials ordering without a system"],
    "physical-therapy":  ["home exercise program delivery by printout", "outcome tracking in a spreadsheet", "insurance auth management across patients"],
    "medical-offices":   ["prior auth tracking across payers", "patient follow-up after procedures", "referral coordination between providers"],
    "ecommerce":         ["order status page that's just Shopify default", "return and exchange workflow", "customer LTV tracking outside the cart platform"],
    "saas":              ["onboarding flows that don't adapt to user behavior", "internal admin tools still built in spreadsheets", "customer health scoring done manually"],
}


# ── CSS ───────────────────────────────────────────────────────────────────────
def css():
    return """
:root{
  --bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;
  --ink:#073044;--muted:#3f6173;--muted2:#5e7d8e;
  --card:#ffffffcc;--stroke:rgba(7,48,68,.10);--shadow:0 18px 50px rgba(7,48,68,.10);
  --mint:#21d3a1;--blue2:#1f7cff;--r:22px;--pill:999px;
}
*{box-sizing:border-box}
html,body{margin:0;font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,Arial,sans-serif;
  color:var(--ink);background:radial-gradient(1200px 900px at 22% 10%,#fff 0%,var(--bg0) 25%,var(--bg1) 60%,var(--bg2) 100%);
  -webkit-font-smoothing:antialiased;overflow-x:hidden;}
a{color:var(--blue2);text-decoration:none;}a:hover{text-decoration:underline;}
.wrap{max-width:960px;margin:0 auto;padding:32px 20px 120px;}
.crumb{font-size:13px;color:var(--muted);margin-bottom:16px;}
h1{font-size:clamp(24px,4.5vw,40px);line-height:1.1;margin:0 0 10px;letter-spacing:-.02em;}
h2{font-size:20px;margin:28px 0 10px;}
.tag{display:inline-block;border:1px solid var(--stroke);border-radius:var(--pill);
  padding:5px 14px;font-size:13px;color:var(--muted);margin-bottom:14px;}
.lead{font-size:17px;color:var(--muted);line-height:1.6;margin:0 0 24px;max-width:680px;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0 24px;}
@media(max-width:640px){.grid2{grid-template-columns:1fr;}}
.card{border:1px solid var(--stroke);border-radius:var(--r);background:var(--card);
  padding:20px 22px;box-shadow:var(--shadow);}
.card h3{margin:0 0 10px;font-size:16px;}
.card ul{margin:0;padding-left:18px;}
.card li{margin:6px 0;font-size:14px;color:var(--muted);}
.bullets li{color:var(--ink);}
.faq-item{margin:16px 0;}
.faq-item strong{display:block;margin-bottom:4px;}
.faq-item p{margin:0;font-size:14px;color:var(--muted);line-height:1.6;}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 24px;}
.pill-link{border:1px solid var(--stroke);border-radius:var(--pill);padding:8px 14px;
  font-size:13px;color:var(--ink);background:var(--card);}
.cta-block{background:linear-gradient(135deg,#073044,#0a4a68);color:#fff;
  border-radius:var(--r);padding:28px;text-align:center;margin:28px 0;}
.cta-block h2{color:#fff;margin:0 0 8px;}
.cta-block p{opacity:.85;margin:0 0 18px;font-size:15px;}
.cta-btn{display:inline-block;background:var(--mint);color:#073044;font-weight:800;
  border-radius:var(--pill);padding:14px 28px;font-size:16px;text-decoration:none;}
.cta-btn:hover{opacity:.9;text-decoration:none;}
.floatBtn{position:fixed;right:16px;bottom:16px;z-index:9999;background:#073044;
  color:#fff;border-radius:var(--pill);padding:14px 20px;font-weight:700;
  text-decoration:none;font-size:14px;box-shadow:0 8px 24px rgba(7,48,68,.25);}
.floatBtn:hover{transform:translateY(-2px);text-decoration:none;}
"""


# ── Shell ────────────────────────────────────────────────────────────────────
def shell(title, desc, slug, body, noindex=False):
    robots = '<meta name="robots" content="noindex,follow"/>' if noindex else \
             '<meta name="robots" content="index,follow,max-image-preview:large"/>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
{robots}
<title>{title} · SideGuy</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="{DOMAIN}/katie/{slug}.html"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:type" content="website"/>
<style>{css()}</style>
</head>
<body>
<a class="floatBtn" href="{PHONE_SMS}">Text PJ · {PHONE_DISP}</a>
<div class="wrap">
{body}
<p style="font-size:12px;color:var(--muted);margin-top:32px;">Last updated: {TODAY} · SideGuy Solutions · Clarity before cost.</p>
</div>
</body>
</html>
"""


# ── Index hub ────────────────────────────────────────────────────────────────
def build_index():
    service_cards = "\n".join(
        f"""<a href="/katie/{s['key']}.html" style="text-decoration:none;">
<div class="card">
<h3>{s['icon']} {s['label']}</h3>
<p style="font-size:14px;color:var(--muted);margin:0;">{s['tagline']}</p>
</div></a>"""
        for s in SERVICES
    )

    industry_links = " ".join(
        f'<a class="pill-link" href="/katie/{ikey}-apps.html">{iname}</a>'
        for ikey, iname in INDUSTRIES
    )

    body = f"""
<div class="crumb"><a href="/">SideGuy</a> › Build with Katie</div>
<div class="tag">Custom Development · San Diego</div>
<h1>Build Something Real<br/>with Katie</h1>
<p class="lead">Katie builds custom software, mobile apps, web apps, and AI-powered tools for operators who've outgrown off-the-shelf solutions. Not a dev shop — a single expert who owns the full stack.</p>

<h2>What Katie builds</h2>
<div class="grid2">
{service_cards}
</div>

<h2>By industry</h2>
<div class="pills">{industry_links}</div>

<div class="cta-block">
<h2>Ready to scope it?</h2>
<p>Text PJ with a one-line description of what you want to build. Katie will respond with a plain-language scoping draft — no pitch deck, no sales call.</p>
<a class="cta-btn" href="{PHONE_SMS}">Text PJ · {PHONE_DISP}</a>
</div>

<div class="pills">
<a class="pill-link" href="/custom-software-development-san-diego.html">Custom Software San Diego</a>
<a class="pill-link" href="/app-development-san-diego.html">App Development San Diego</a>
<a class="pill-link" href="/ai-automation-consulting-san-diego.html">AI Automation Consulting</a>
<a class="pill-link" href="/decisions/index.html">Tool Comparisons</a>
<a class="pill-link" href="/">SideGuy Home</a>
</div>
"""
    return shell(
        title="Build Apps & Custom Software — Work with Katie",
        desc="Katie builds custom software, mobile apps, web apps, and AI automation tools. Text PJ to scope your project.",
        slug="index",
        body=body,
    )


# ── Service hub pages ─────────────────────────────────────────────────────────
def build_service_page(s):
    faq_html = "\n".join(
        f"""<div class="faq-item"><strong>{q}</strong><p>{a}</p></div>"""
        for q, a in s["questions"]
    )
    bullet_li = "\n".join(f"<li>{b}</li>" for b in s["bullets"])

    industry_links = " ".join(
        f'<a class="pill-link" href="/katie/{ikey}-apps.html">{iname}</a>'
        for ikey, iname in INDUSTRIES
    )

    body = f"""
<div class="crumb"><a href="/">SideGuy</a> › <a href="/katie/index.html">Build with Katie</a> › {s['label']}</div>
<div class="tag">{s['icon']} {s['label']}</div>
<h1>{s['label']}</h1>
<p class="lead">{s['tagline']}</p>

<div class="grid2">
<div class="card bullets">
<h3>What you get</h3>
<ul>{bullet_li}</ul>
</div>
<div class="card">
<h3>How to start</h3>
<ol style="padding-left:18px;margin:0;">
<li style="margin:6px 0;font-size:14px;">Text PJ one sentence about what you want to build.</li>
<li style="margin:6px 0;font-size:14px;">Katie sends a plain-language scope draft (no commitment).</li>
<li style="margin:6px 0;font-size:14px;">You review, adjust, and greenlight when it feels right.</li>
<li style="margin:6px 0;font-size:14px;">Iterative builds — working software fast, then refined.</li>
</ol>
</div>
</div>

<h2>Frequently asked questions</h2>
{faq_html}

<div class="cta-block">
<h2>Start with a text</h2>
<p>One sentence about what you need. PJ gets it to Katie. You get a scope draft — no pitch, no pressure.</p>
<a class="cta-btn" href="{PHONE_SMS}">Text PJ · {PHONE_DISP}</a>
</div>

<h2>Build for your industry</h2>
<div class="pills">{industry_links}</div>

<div class="pills">
<a class="pill-link" href="/katie/index.html">← All Katie's Services</a>
<a class="pill-link" href="/decisions/index.html">Tool Comparisons</a>
<a class="pill-link" href="/">SideGuy Home</a>
</div>
"""
    return shell(
        title=f"{s['label']} — Work with Katie",
        desc=f"Katie builds {s['label'].lower()} for operators. {s['tagline']} Text PJ to scope your project.",
        slug=s["key"],
        body=body,
    )


# ── Industry × service pages ──────────────────────────────────────────────────
def build_industry_page(ikey: str, iname: str):
    pains = INDUSTRY_PAIN = INDUSTRY_PAINS.get(ikey, [
        "manual processes that should be automated",
        "disconnected tools that don't talk to each other",
        "reporting done by hand at month-end",
    ])
    pain_li = "\n".join(f"<li>{p}</li>" for p in pains)

    service_cards = "\n".join(
        f"""<div class="card" style="grid-column:span 1;">
<h3>{s['icon']} <a href="/katie/{s['key']}.html">{s['label']}</a></h3>
<p style="font-size:14px;color:var(--muted);margin:0;">{s['tagline']}</p>
</div>"""
        for s in SERVICES
    )

    body = f"""
<div class="crumb"><a href="/">SideGuy</a> › <a href="/katie/index.html">Build with Katie</a> › {iname}</div>
<div class="tag">Custom Apps for {iname}</div>
<h1>Custom Software &amp; Apps<br/>for {iname}</h1>
<p class="lead">Most {iname.lower()} still run critical operations in spreadsheets, group texts, and disconnected SaaS tools. Katie builds the custom layer that makes everything work together — owned by you, built for how you actually work.</p>

<div class="card" style="margin-bottom:20px;">
<h3>What {iname.lower()} typically need solved</h3>
<ul class="bullets">
{pain_li}
</ul>
</div>

<h2>What Katie can build for you</h2>
<div class="grid2">
{service_cards}
</div>

<h2>How it works</h2>
<div class="grid2">
<div class="card">
<h3>1. Describe the problem</h3>
<p style="font-size:14px;color:var(--muted);margin:0;">Text PJ one sentence about what's broken or missing. No spec required — just the pain point.</p>
</div>
<div class="card">
<h3>2. Get a scope draft</h3>
<p style="font-size:14px;color:var(--muted);margin:0;">Katie turns it into a plain-language scope: what gets built, in what order, for what cost range. No surprises.</p>
</div>
<div class="card">
<h3>3. Greenlight when ready</h3>
<p style="font-size:14px;color:var(--muted);margin:0;">No commitment until you say go. Adjust scope as needed — you control the budget.</p>
</div>
<div class="card">
<h3>4. Iterative delivery</h3>
<p style="font-size:14px;color:var(--muted);margin:0;">Working software fast, then refined. You see progress before the final invoice.</p>
</div>
</div>

<div class="cta-block">
<h2>Tell Katie what you need</h2>
<p>Text PJ with your {iname.lower()} problem. One sentence is enough to start.</p>
<a class="cta-btn" href="{PHONE_SMS}">Text PJ · {PHONE_DISP}</a>
</div>

<div class="pills">
<a class="pill-link" href="/katie/index.html">← All Katie's Services</a>
<a class="pill-link" href="/katie/custom-software.html">Custom Software</a>
<a class="pill-link" href="/katie/web-app.html">Web Apps</a>
<a class="pill-link" href="/katie/mobile-app.html">Mobile Apps</a>
<a class="pill-link" href="/katie/ai-automation.html">AI Automation</a>
<a class="pill-link" href="/decisions/index.html">Tool Comparisons</a>
</div>
"""
    return shell(
        title=f"Custom Apps &amp; Software for {iname} — Work with Katie",
        desc=f"Katie builds custom software and apps for {iname.lower()}. Scheduling, dispatch, portals, AI workflows — owned by you. Text PJ to start.",
        slug=f"{ikey}-apps",
        body=body,
    )


def main():
    built = []

    # Index hub
    (OUT / "index.html").write_text(build_index(), encoding="utf-8")
    built.append("index.html")

    # 4 service hub pages
    for s in SERVICES:
        fname = f"{s['key']}.html"
        (OUT / fname).write_text(build_service_page(s), encoding="utf-8")
        built.append(fname)

    # 18 industry pages
    for ikey, iname in INDUSTRIES:
        fname = f"{ikey}-apps.html"
        (OUT / fname).write_text(build_industry_page(ikey, iname), encoding="utf-8")
        built.append(fname)

    print(f"=== Katie Pages Built ===")
    print(f"  Pages : {len(built)}")
    print(f"  Output: {OUT}")
    for f in built:
        print(f"    katie/{f}")


if __name__ == "__main__":
    main()
