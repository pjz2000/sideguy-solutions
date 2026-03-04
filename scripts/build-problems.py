#!/usr/bin/env python3
"""
SIDEGUY Traffic Engine — 500 Problem Pages
- Expands 80 base problems via prefix/suffix patterns to ~500 unique slugs
- Generates each as a styled, schema-tagged problem page
- Builds problems/index.html
- Updates sitemap.xml (batch append, deduped)
- Adds Problems section to knowledge map
- Idempotent: skips pages that already exist
"""

import re, random, csv, os
from pathlib import Path
from datetime import date

ROOT        = Path(__file__).parent.parent
PROBLEMS_DIR = ROOT / "problems"
PROBLEMS_DIR.mkdir(exist_ok=True)

TODAY  = date.today().isoformat()
DOMAIN = "https://sideguysolutions.com"
PHONE_DISPLAY = "773-544-1231"
PHONE_SMS     = "+17735441231"

random.seed(42)   # reproducible shuffle

# ──────────────────────────────────────────────
# 80 BASE PROBLEMS
# ──────────────────────────────────────────────

BASE = [
    "stripe payout pending for days",
    "square instant deposit not showing up",
    "paypal payment on hold how to release",
    "shopify payments account review fix",
    "apple pay not working on checkout",
    "google pay declined troubleshooting",
    "payment gateway error 502",
    "webhook signature verification failed",
    "api key invalid after rotation",
    "oauth redirect uri mismatch fix",
    "dns propagation stuck how long",
    "domain connected but site not loading",
    "ssl certificate pending too long",
    "cloudflare too many redirects fix",
    "email deliverability suddenly dropped",
    "spf dkim dmarc misconfigured fix",
    "zapier task failed webhook timeout",
    "make com scenario errors troubleshooting",
    "openai api rate limit exceeded fix",
    "claude api integration failing",
    "ai agent tool calling not working",
    "csv import errors duplicate headers",
    "quickbooks sync disconnected fix",
    "xero bank feed not updating",
    "merchant account underwriting questions",
    "chargeback received what to do",
    "high decline rate stripe radar tuning",
    "subscription renewal failed recovery",
    "failed payment retry strategy",
    "pos terminal offline fix",
    "wifi drops during transactions fix",
    "restaurant online ordering not syncing",
    "doordash payouts missing",
    "uber eats tax settings wrong",
    "invoice link not opening for customer",
    "payment link expired fix",
    "auth capture mismatch error",
    "3ds authentication failing",
    "apple app store receipt verification failed",
    "google play billing pending fix",
    "subscription proration confusion",
    "crm pipeline stages broken",
    "hubspot forms not submitting",
    "wordpress plugin conflict 500 error",
    "nextjs build failing on deploy",
    "vercel env vars missing",
    "netlify build command failing",
    "github actions secrets not found",
    "docker container exits immediately",
    "server out of memory spike",
    "database connection pool exhausted",
    "postgres slow query sudden",
    "mysql deadlock retry pattern",
    "supabase auth email not sending",
    "firebase rules blocking access",
    "twilio sms not delivering",
    "phone number verification blocked",
    "calendar booking double booked fix",
    "no show reduction automation",
    "local seo page not indexing",
    "sitemap submitted but not discovered",
    "canonical tag wrong fix",
    "duplicate content detected fix",
    "structured data errors faq schema",
    "google search console crawl anomaly",
    "robots txt blocking important pages",
    "lighthouse score dropped suddenly",
    "core web vitals lcp too high",
    "image optimization breaking layout",
    "checkout conversion suddenly down",
    "abandoned cart spike fix",
    "utm tracking broken",
    "ga4 not tracking conversions",
    "google ads disapproved destination mismatch",
    "meta ads pixel not firing",
    "tiktok ads attribution broken",
    "merchant cash flow forecasting setup",
    "how to set pricing for services",
    "how to build a support intake funnel",
    "how to route leads to a human operator",
    "how to use ai safely for business decisions",
]

PREFIXES = [
    "how to fix",
    "why is",
    "troubleshooting",
    "best way to solve",
    "what causes",
    "quick fix for",
    "step by step fix for",
    "how to diagnose",
]

SUFFIXES = [
    "in 2026",
    "for small business",
    "for ecommerce",
    "for service business",
    "without hiring devs",
    "fast",
    "without downtime",
    "root cause",
]


# ──────────────────────────────────────────────
# EXPAND TITLES TO 500
# ──────────────────────────────────────────────

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s[:80].strip("-")

def titlecase(s: str) -> str:
    stop = {"and","or","the","a","an","to","for","of","in","on","at","with"}
    words = s.split()
    out = []
    for i, w in enumerate(words):
        if i == 0 or w.lower() not in stop:
            out.append(w.capitalize())
        else:
            out.append(w.lower())
    result = " ".join(out)
    # fix common acronyms
    for old, new in [("Ai","AI"),("Api","API"),("Ga4","GA4"),("Dns","DNS"),
                     ("Ssl","SSL"),("Ssh","SSH"),("Pos","POS"),("Seo","SEO"),
                     ("Utm","UTM"),("Crm","CRM"),("Spf","SPF"),("Dkim","DKIM"),
                     ("Dmarc","DMARC"),("3ds","3DS"),("Csv","CSV"),("Sms","SMS"),
                     ("Lcp","LCP"),("Ach","ACH"),("Oauth","OAuth"),("Urls","URLs")]:
        result = result.replace(old, new)
    return result

def expand_titles(base, target=500):
    titles = list(base)
    seen = set(t.lower() for t in titles)

    for b in base:
        for p in PREFIXES:
            cand = f"{p} {b}"
            if cand.lower() not in seen:
                titles.append(cand)
                seen.add(cand.lower())
        for s in SUFFIXES:
            cand = f"{b} {s}"
            if cand.lower() not in seen:
                titles.append(cand)
                seen.add(cand.lower())

    random.shuffle(titles)

    # pad if needed with random combos
    while len(titles) < target:
        b = random.choice(base)
        p = random.choice(PREFIXES)
        s = random.choice(SUFFIXES)
        cand = f"{p} {b} {s}"
        if cand.lower() not in seen:
            titles.append(cand)
            seen.add(cand.lower())

    return titles[:target]


# ──────────────────────────────────────────────
# CSS  (light ocean — matching site conventions)
# ──────────────────────────────────────────────

CSS = """
  :root {
    --bg0:#eefcff; --bg1:#d7f5ff; --ink:#073044; --muted:#3f6173;
    --mint:#21d3a1; --mint2:#00c7ff; --blue2:#1f7cff;
    --r:16px; --pill:999px;
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
    padding:11px 22px;font-size:.8rem;color:var(--muted);
    border-bottom:1px solid rgba(0,0,0,.06);
    background:rgba(255,255,255,.55);backdrop-filter:blur(6px);
  }
  nav.bc a{color:var(--muted)}
  .wrap{max-width:800px;margin:0 auto;padding:40px 22px 80px}
  .prob-badge{
    display:inline-block;background:rgba(31,124,255,.12);color:var(--blue2);
    font-size:.72rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
    padding:3px 11px;border-radius:var(--pill);margin-bottom:12px;
  }
  h1{font-size:clamp(1.6rem,5vw,2.4rem);font-weight:800;line-height:1.2;margin-bottom:12px}
  .lede{font-size:1rem;color:var(--muted);margin-bottom:30px;line-height:1.65}
  .card{
    background:rgba(255,255,255,.75);border:1px solid rgba(0,0,0,.08);
    border-radius:var(--r);padding:20px 22px;margin-bottom:14px;
  }
  .card h2{font-size:1.05rem;font-weight:700;margin-bottom:10px;color:var(--ink)}
  .card ul{padding-left:20px}
  .card li{margin-bottom:6px;font-size:.93rem;line-height:1.6;color:#2a4555}
  .card p{font-size:.93rem;line-height:1.65;color:#2a4555}
  .cta-box{
    background:linear-gradient(135deg,#073044 0%,#0e3d58 100%);
    border-radius:var(--r);padding:26px 28px;color:#fff;
    margin:34px 0 28px;display:flex;align-items:center;gap:22px;flex-wrap:wrap;
  }
  .cta-box h3{font-size:1.1rem;font-weight:700;margin-bottom:5px}
  .cta-box p{font-size:.9rem;opacity:.8;margin:0}
  .cta-btn{
    flex-shrink:0;background:var(--mint);color:#073044;font-weight:700;
    padding:11px 22px;border-radius:var(--pill);white-space:nowrap;
  }
  .cta-btn:hover{opacity:.9;text-decoration:none}
  .pills{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
  .pill{
    background:rgba(255,255,255,.8);border:1px solid rgba(0,0,0,.1);
    border-radius:var(--pill);padding:5px 14px;font-size:.83rem;
    font-weight:500;color:var(--ink);
  }
  .pill:hover{background:var(--mint);color:#073044;text-decoration:none}
  footer{text-align:center;padding:22px;font-size:.78rem;color:var(--muted);border-top:1px solid rgba(0,0,0,.06)}
  .floating{position:fixed;bottom:22px;right:22px;z-index:999}
  .floatBtn{
    display:flex;align-items:center;gap:8px;
    background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;
    padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;
    text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.2);
  }
  .floatBtn:hover{opacity:.92;text-decoration:none}
  @media(max-width:580px){.cta-box{flex-direction:column;gap:14px}}
"""


# ──────────────────────────────────────────────
# PROBLEM PAGE BUILDER
# ──────────────────────────────────────────────

def build_problem_page(title: str, slug: str) -> str:
    t = titlecase(title)
    canonical = f"{DOMAIN}/problems/{slug}.html"

    faq_q1 = f"What is — {t}?"
    faq_a1 = (f"{t} is a common operator or business issue that surfaces when systems, "
              "tools, or settings drift out of alignment. This page explains it in plain English "
              "and gives you the fastest path to a resolution.")
    faq_q2 = f"What usually causes {t}?"
    faq_a2 = ("Most causes fall into a few buckets: a recent change (update, integration flip, "
              "or settings drift), permissions mismatch, vendor policy change, stale API credentials, "
              "or a hidden dependency that silently broke. The checklist below covers the most common triggers.")
    faq_q3 = "What should I do first?"
    faq_a3 = ("Start with the fastest checks: confirm the exact error message and timestamp, "
              "verify you&apos;re in the right account/workspace, reproduce with a minimal test, "
              "check vendor status pages, and isolate your last change. "
              "If it's still unclear after 15 minutes, a second set of eyes saves time.")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{t} | SideGuy Solutions</title>
  <meta name="description" content="Practical clarity on {t}: what causes it, the fastest checks, and what usually fixes it. SideGuy = clarity before cost."/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:title" content="{t} | SideGuy"/>
  <meta property="og:description" content="Clear, operator-first breakdown of {t.lower()}. Causes, checks, and fixes."/>
  <meta property="og:url" content="{canonical}"/>
  <meta name="robots" content="index,follow"/>
  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@graph":[
      {{
        "@type":"BreadcrumbList",
        "itemListElement":[
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"Problems","item":"{DOMAIN}/problems/index.html"}},
          {{"@type":"ListItem","position":3,"name":"{t}","item":"{canonical}"}}
        ]
      }},
      {{
        "@type":"FAQPage",
        "mainEntity":[
          {{
            "@type":"Question","name":"{faq_q1}",
            "acceptedAnswer":{{"@type":"Answer","text":"{faq_a1}"}}
          }},
          {{
            "@type":"Question","name":"{faq_q2}",
            "acceptedAnswer":{{"@type":"Answer","text":"{faq_a2}"}}
          }},
          {{
            "@type":"Question","name":"{faq_q3}",
            "acceptedAnswer":{{"@type":"Answer","text":"{faq_a3}"}}
          }}
        ]
      }}
    ]
  }}
  </script>
  <style>
{CSS}
  </style>
</head>
<body>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> › <a href="/problems/index.html">Problems</a> › {t}
</nav>

<main class="wrap">

  <div class="prob-badge">Problem Guide</div>
  <h1>{t}</h1>
  <p class="lede">Operator-first breakdown: what causes this, the fastest checks, and what usually fixes it — in plain English.</p>

  <div class="card">
    <h2>What this is</h2>
    <p>
      {t} is one of those issues that feels chaotic until you break it into
      3–5 checks. Most operators hit it after a setting change, integration update,
      or vendor policy shift they didn't notice at the time. This page gives you the
      checks, the causes, and the "what to do next."
    </p>
  </div>

  <div class="card">
    <h2>Most likely causes</h2>
    <ul>
      <li>Recent change — update, integration flip, or settings drift</li>
      <li>Account or permissions mismatch</li>
      <li>Vendor policy or rate-limit change (often undocumented)</li>
      <li>Stale API key, webhook secret, or auth token</li>
      <li>Hidden dependency — DNS, auth, environment variable, billing limit</li>
      <li>Gap between documentation and current platform behavior</li>
    </ul>
  </div>

  <div class="card">
    <h2>Fast checks (10–15 minutes)</h2>
    <ul>
      <li>Capture the exact error message and timestamp</li>
      <li>Reproduce with the smallest possible test case</li>
      <li>Confirm you're in the right account/workspace/environment</li>
      <li>Check vendor status pages and recent changelogs</li>
      <li>Roll back your last change (if safe) to isolate the trigger</li>
      <li>Test with a fresh credential or minimal config</li>
    </ul>
  </div>

  <div class="card">
    <h2>What usually fixes it</h2>
    <ul>
      <li>Re-authenticate or regenerate credentials (keys, tokens, secrets)</li>
      <li>Rebuild from the minimal config that worked most recently</li>
      <li>Move one change at a time — avoid "big bang" configuration changes</li>
      <li>Contact vendor support with timestamps and the exact error string</li>
      <li>Document the fix so it never costs you the same time twice</li>
    </ul>
  </div>

  <div class="card">
    <h2>Related concepts</h2>
    <div class="pills">
      <a class="pill" href="/concepts/ai-automation.html">AI Automation</a>
      <a class="pill" href="/concepts/payment-processing.html">Payment Processing</a>
      <a class="pill" href="/concepts/crypto-payments.html">Crypto Payments</a>
      <a class="pill" href="/clusters/ai-workflow-automation.html">Workflow Automation</a>
      <a class="pill" href="/clusters/payment-fees.html">Payment Fees</a>
      <a class="pill" href="/pillars/ai-automation.html">AI Automation Pillar</a>
      <a class="pill" href="/pillars/payments.html">Payments Pillar</a>
      <a class="pill" href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a>
    </div>
  </div>

  <div class="cta-box">
    <div>
      <h3>Still stuck? Text PJ.</h3>
      <p>Real human, San Diego. Straight answer on what actually makes sense for your situation — no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_SMS}">💬 Text {PHONE_DISPLAY}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/problems/index.html">Problems Index</a> ·
    <a href="/concepts/index.html">Concepts</a> ·
    <a href="tel:{PHONE_SMS}">{PHONE_DISPLAY}</a>
    <br><small>Page updated {TODAY}</small>
  </footer>

</main>

<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_SMS}" aria-label="Text PJ">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ
  </a>
</div>

</body>
</html>
"""


# ──────────────────────────────────────────────
# PROBLEMS INDEX
# ──────────────────────────────────────────────

def build_index(items: list) -> str:
    """items = list of (title, slug) tuples"""
    cards = ""
    for title, slug in items:
        t = titlecase(title)
        cards += f'      <a class="pcard" href="/problems/{slug}.html">{t}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>SideGuy Problems Index — 500 Operator Problem Guides</title>
  <meta name="description" content="SideGuy Problems Index: practical clarity on 500 real operator and business problems across payments, automation, infrastructure, and modern tech."/>
  <link rel="canonical" href="{DOMAIN}/problems/index.html"/>
  <meta name="robots" content="index,follow"/>
  <style>
{CSS}
    .wrap{{max-width:1100px}}
    .pgrid{{
      display:grid;
      grid-template-columns:repeat(auto-fill,minmax(240px,1fr));
      gap:10px;
      margin:24px 0;
    }}
    .pcard{{
      background:rgba(255,255,255,.75);
      border:1px solid rgba(0,0,0,.08);
      border-radius:12px;
      padding:13px 16px;
      font-size:.88rem;
      font-weight:500;
      color:var(--ink);
      line-height:1.4;
    }}
    .pcard:hover{{background:var(--mint);color:#073044;text-decoration:none}}
    .filter-row{{
      display:flex;flex-wrap:wrap;gap:8px;margin:18px 0;
    }}
    .ftag{{
      background:rgba(255,255,255,.7);border:1px solid rgba(0,0,0,.1);
      border-radius:var(--pill);padding:5px 14px;font-size:.82rem;
      font-weight:600;color:var(--muted);cursor:pointer;
    }}
    .ftag:hover{{background:var(--mint);color:#073044}}
  </style>
</head>
<body>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> › Problems
</nav>

<main class="wrap">

  <div class="prob-badge">Problem Library</div>
  <h1>SideGuy Problems Index</h1>
  <p class="lede" style="max-width:700px">
    {len(items)} operator problem guides across payments, automation, infrastructure, AI, and modern business systems.
    Clarity before cost — plain English, no hype.
  </p>

  <div class="filter-row">
    <span class="ftag">Payments</span>
    <span class="ftag">Automation</span>
    <span class="ftag">Infrastructure</span>
    <span class="ftag">AI</span>
    <span class="ftag">SEO</span>
    <span class="ftag">CRM</span>
    <span class="ftag">APIs</span>
  </div>

  <div class="pgrid">
{cards}  </div>

  <div class="cta-box">
    <div>
      <h3>Don't see your problem?</h3>
      <p>Text PJ. Real human, San Diego. Straight answer — no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_SMS}">💬 Text {PHONE_DISPLAY}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/concepts/index.html">Concepts</a> ·
    <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a> ·
    <a href="tel:{PHONE_SMS}">{PHONE_DISPLAY}</a>
  </footer>

</main>

<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_SMS}" aria-label="Text PJ">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ
  </a>
</div>

</body>
</html>
"""


# ──────────────────────────────────────────────
# SITEMAP UPDATE
# ──────────────────────────────────────────────

def update_sitemap(slugs: list):
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        print("  sitemap.xml not found — skipping")
        return
    content = sitemap_path.read_text()
    new_urls = ""
    added = 0
    for slug in slugs + ["index"]:
        url = f"{DOMAIN}/problems/{slug}.html"
        if url not in content:
            new_urls += f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>\n"
            added += 1
    if new_urls:
        content = content.replace("</urlset>", new_urls + "</urlset>")
        sitemap_path.write_text(content)
    print(f"  Sitemap: {added} new URLs added")


# ──────────────────────────────────────────────
# KNOWLEDGE MAP UPDATE
# ──────────────────────────────────────────────

def update_knowledge_map(sample_items: list):
    km_path = ROOT / "knowledge" / "sideguy-knowledge-map.html"
    if not km_path.exists():
        print("  Knowledge map not found — skipping")
        return
    content = km_path.read_text()
    if "SIDEGUY_PROBLEMS_SECTION" in content:
        print("  Knowledge map already has Problems section — skipping")
        return

    node_cards = ""
    for title, slug in sample_items[:8]:
        t = titlecase(title)
        node_cards += f"""      <a class="node" href="/problems/{slug}.html">
        <span class="node-type type-guide">Problem</span>
        <div class="node-title">{t}</div>
        <div class="node-desc">Causes, fast checks, and what usually fixes it.</div>
      </a>
"""

    section = f"""
  <!-- SIDEGUY_PROBLEMS_SECTION -->
  <div class="cluster-group">
    <div class="cluster-header">
      <div class="cluster-icon">🔧</div>
      <div>
        <div class="cluster-title">Operator Problem Guides</div>
        <div class="cluster-sub">500 real problems — payments, automation, infrastructure, AI — plain English + fast fixes</div>
      </div>
      <a class="cluster-cta" href="/problems/index.html">All 500 Problems →</a>
    </div>
    <div class="node-grid">
{node_cards}    </div>
  </div>
  <!-- END SIDEGUY_PROBLEMS_SECTION -->
"""

    # Insert before Concept Authority section if it exists, else before Topic Gap Link, else microFooter
    if "<!-- SIDEGUY_CONCEPTS_SECTION -->" in content:
        content = content.replace(
            "<!-- SIDEGUY_CONCEPTS_SECTION -->",
            section + "<!-- SIDEGUY_CONCEPTS_SECTION -->",
            1
        )
    elif "<!-- SIDEGUY_TOPIC_GAP_LINK -->" in content:
        content = content.replace(
            "<!-- SIDEGUY_TOPIC_GAP_LINK -->",
            section + "<!-- SIDEGUY_TOPIC_GAP_LINK -->",
            1
        )
    else:
        content = content.replace(
            '<div class="microFooter"',
            section + '<div class="microFooter"',
            1
        )

    km_path.write_text(content)
    print("  Knowledge map updated with Problems section (8 sample nodes)")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SideGuy Traffic Engine — 500 Problem Pages ===\n")

    # 1. Expand titles
    titles = expand_titles(BASE, target=500)
    print(f"Titles after expansion: {len(titles)}")

    # 2. Deduplicate slugs (keep first occurrence)
    items = []          # (title, slug)
    seen_slugs = set()
    for t in titles:
        s = slugify(t)
        if s and s not in seen_slugs:
            seen_slugs.add(s)
            items.append((t, s))

    print(f"Unique slugs: {len(items)}")

    # 3. Build pages (skip existing)
    built = 0
    skipped = 0
    for title, slug in items:
        path = PROBLEMS_DIR / f"{slug}.html"
        if path.exists():
            skipped += 1
            continue
        html = build_problem_page(title, slug)
        path.write_text(html)
        built += 1

    print(f"  Built: {built}  Skipped (existing): {skipped}")

    # 4. Build/rebuild index
    idx_html = build_index(items)
    (PROBLEMS_DIR / "index.html").write_text(idx_html)
    print(f"  Index rebuilt: problems/index.html  ({len(items)} entries)")

    # 5. Sitemap
    print()
    update_sitemap([s for _, s in items])

    # 6. Knowledge map — use a stable sample of real-sounding problems
    sample = [(t, s) for t, s in items
              if any(k in s for k in ["stripe","chargeback","checkout","email-deliver",
                                       "webhook","calendar","pos-terminal","crm"])][:8]
    if len(sample) < 8:
        sample += [(t, s) for t, s in items if (t, s) not in sample]
    sample = sample[:8]
    update_knowledge_map(sample)

    # 7. Write slug CSV for reference
    csv_path = ROOT / "problems" / "problem-slugs.csv"
    with open(csv_path, "w") as f:
        f.write("title,slug\n")
        for title, slug in items:
            f.write(f'"{title}",{slug}\n')
    print(f"  Slug CSV: problems/problem-slugs.csv")

    print(f"\n=== Done — {built} new pages, {skipped} skipped, {len(items)} total ===")
    print(f"Index: {DOMAIN}/problems/index.html")
