#!/usr/bin/env python3
"""
SideGuy Authority Builder
Builds hub pages (industry, category, city) and pillar guide pages.
Safe to re-run: only creates pages that don't exist yet.
Run AFTER build-pages.py so root pages already exist.
"""

import json, os, re, datetime, sys

# Add scripts/ to path so we can import the shared module
sys.path.insert(0, os.path.dirname(__file__))
from sideguy_classify import (
    slugify, topic_to_filename, classify_topic,
    CATEGORIES, CATEGORY_HUB_PATH, CATEGORY_HUB_LABELS,
    PILLAR_MAP, PILLAR_LABELS, industry_hub_path, industry_hub_label,
    DOMAIN,
)

MANIFEST    = "seo-reserve/manifest.json"
HUBS_DIR    = "hubs"
PILLARS_DIR = "pillars"
ROOT        = "."
TODAY       = datetime.date.today().isoformat()

# ── Inline CSS shared across all authority pages ──────────────────────────────

SHARED_CSS = """
  :root{
    --bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;
    --ink:#073044;--muted:#3f6173;
    --card:#ffffffcc;--stroke:rgba(7,48,68,.10);
    --shadow:0 18px 50px rgba(7,48,68,.10);
    --mint:#21d3a1;--mint2:#00c7ff;
    --r:22px;--pill:999px;
  }
  *{box-sizing:border-box}
  html,body{height:100%}
  body{
    margin:0;
    font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,Arial,sans-serif;
    color:var(--ink);
    background:radial-gradient(ellipse 120% 80% at 50% -10%,
      var(--bg2) 0%,var(--bg1) 40%,var(--bg0) 100%);
    min-height:100vh;
  }
  header{
    max-width:960px;margin:0 auto;padding:40px 24px 0;
    display:flex;align-items:center;justify-content:space-between;
    flex-wrap:wrap;gap:12px;
  }
  .logo{font-weight:800;font-size:1.25rem;color:var(--ink);
        text-decoration:none;letter-spacing:-.5px;}
  .cta-pill{
    background:linear-gradient(135deg,var(--mint),var(--mint2));
    color:#fff;font-weight:700;font-size:.9rem;
    padding:10px 22px;border-radius:var(--pill);text-decoration:none;
    box-shadow:0 4px 16px rgba(33,211,161,.35);
  }
  nav.breadcrumb{
    max-width:960px;margin:16px auto 0;padding:0 24px;
    font-size:.85rem;color:var(--muted);display:flex;gap:8px;flex-wrap:wrap;
  }
  nav.breadcrumb a{color:var(--muted);font-weight:600;text-decoration:none;}
  nav.breadcrumb a:hover{text-decoration:underline;}
  nav.breadcrumb span{opacity:.5;}
  main{max-width:960px;margin:0 auto;padding:40px 24px 80px;}
  h1{font-size:clamp(1.7rem,4vw,2.6rem);font-weight:900;
     line-height:1.2;margin:0 0 14px;}
  .subtitle{font-size:1.05rem;color:var(--muted);margin:0 0 40px;line-height:1.6;}
  h2{font-size:1.15rem;font-weight:800;margin:30px 0 14px;color:var(--ink);}
  .card{
    background:var(--card);border:1px solid var(--stroke);
    border-radius:var(--r);padding:26px 30px;margin-bottom:22px;
    box-shadow:var(--shadow);
  }
  .card p{margin:0 0 10px;line-height:1.7;color:var(--muted);}
  .card p:last-child{margin-bottom:0;}
  .link-grid{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
    gap:10px;margin-bottom:32px;
  }
  .link-tile{
    background:var(--card);border:1px solid var(--stroke);
    border-radius:14px;padding:14px 18px;
    text-decoration:none;color:var(--ink);font-weight:600;
    font-size:.9rem;line-height:1.4;
    box-shadow:0 2px 8px rgba(7,48,68,.06);
    transition:box-shadow .15s;
  }
  .link-tile:hover{box-shadow:var(--shadow);}
  .hub-links{
    display:flex;flex-wrap:wrap;gap:10px;margin-top:10px;
  }
  .hub-chip{
    background:rgba(33,211,161,.12);border:1px solid rgba(33,211,161,.3);
    border-radius:var(--pill);padding:7px 16px;font-size:.85rem;
    font-weight:700;color:var(--ink);text-decoration:none;
  }
  .hub-chip:hover{background:rgba(33,211,161,.22);}
  .cta-block{
    background:linear-gradient(135deg,var(--mint),var(--mint2));
    border-radius:var(--r);padding:36px 32px;text-align:center;
    margin-top:40px;box-shadow:0 12px 40px rgba(33,211,161,.3);
  }
  .cta-block p{color:#fff;font-size:1.05rem;margin:0 0 20px;font-weight:500;}
  .cta-block a{
    display:inline-block;background:#fff;color:var(--ink);
    font-weight:800;font-size:1rem;padding:14px 32px;
    border-radius:var(--pill);text-decoration:none;
    box-shadow:0 4px 14px rgba(0,0,0,.12);
  }
  footer{
    max-width:960px;margin:0 auto;padding:0 24px 48px;
    color:var(--muted);font-size:.85rem;
  }
  footer a{color:var(--muted);}
"""

# ── HTML template helpers ─────────────────────────────────────────────────────

def header_html(title, canonical, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large"/>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{title} · SideGuy San Diego</title>
<link rel="canonical" href="{canonical}"/>
<meta name="description" content="{desc}"/>
<style>{SHARED_CSS}</style>
</head>
<body>
<header>
  <a class="logo" href="/">SideGuy</a>
  <a class="cta-pill" href="sms:+17604541860">Text PJ</a>
</header>
<nav class="breadcrumb">
  <a href="/">Home</a><span>/</span>
  <a href="/hub.html">Operator Hub</a><span>/</span>
  <span>{title}</span>
</nav>"""

def footer_html():
    return f"""
<footer>
  <p><a href="/">SideGuy Solutions</a> · San Diego · <a href="sms:+17604541860">760-454-1860</a></p>
  <p>Clarity before cost. Updated {TODAY}.</p>
</footer>
</body>
</html>"""

def cta_block():
    return """
  <div class="cta-block">
    <p>Want a real human to look at your situation — no pitch, no pressure?</p>
    <a href="sms:+17604541860">Text PJ · 760-454-1860</a>
  </div>"""

def link_grid(items):
    """items: list of (label, href)"""
    if not items:
        return ""
    tiles = "".join(
        f'    <a class="link-tile" href="{href}">{label}</a>\n'
        for label, href in items
    )
    return f'  <div class="link-grid">\n{tiles}  </div>\n'

def hub_chips(links):
    """links: list of (label, href)"""
    chips = "".join(
        f'    <a class="hub-chip" href="{href}">{label}</a>\n'
        for label, href in links
    )
    return f'  <div class="hub-links">\n{chips}  </div>\n'

# ── Classify all topics ───────────────────────────────────────────────────────

def build_index(topics):
    """
    Returns:
      by_category[cat]   = list of (topic, filename)
      by_industry[slug]  = list of (topic, filename)
      san_diego_topics   = list of (topic, filename)
    """
    by_category  = {c: [] for c in CATEGORIES}
    by_industry  = {}

    for topic in topics:
        fn = topic_to_filename(topic)
        info = classify_topic(topic)
        for cat in info['categories']:
            by_category[cat].append((topic, fn))
        ind = info['industry']
        if ind:
            by_industry.setdefault(ind, []).append((topic, fn))

    return by_category, by_industry

# ── Page builders ─────────────────────────────────────────────────────────────

def build_industry_hub(industry_slug, topic_pairs, all_cats_snippet):
    """Build hubs/industry-<slug>.html"""
    os.makedirs(HUBS_DIR, exist_ok=True)
    path = os.path.join(HUBS_DIR, f"industry-{industry_slug}.html")
    if os.path.exists(path):
        return None

    label  = industry_slug.replace('-', ' ').title()
    canon  = f"{DOMAIN}/hubs/industry-{industry_slug}.html"
    desc   = (f"AI automation guides and resources for {label} in San Diego. "
              "Plain-language help from SideGuy — clarity before cost.")
    title  = f"AI Automation for {label}"

    items = [(t.title(), f"../{fn}") for t, fn in topic_pairs[:200]]
    grid  = link_grid(items)

    html = header_html(title, canon, desc)
    html += f"""
<main>
  <h1>AI Automation for {label} — San Diego Resource Hub</h1>
  <p class="subtitle">
    Everything SideGuy has published about AI automation, tools, and efficiency
    for {label} in San Diego. Calm, operator-first guides with no vendor bias.
  </p>

  <div class="card">
    <p>
      <strong>{label}</strong> are adopting AI faster than most people realize —
      but the honest truth is that most AI tools require real configuration to
      deliver value. SideGuy helps you figure out what's worth it before you spend.
    </p>
    <p>Use the guides below to understand your options. Text PJ when you're ready
    for a real conversation.</p>
  </div>

  <h2>All guides for {label}</h2>
{grid}
  <h2>Related topics</h2>
{all_cats_snippet}
{cta_block()}
</main>"""
    html += footer_html()

    with open(path, "w") as f:
        f.write(html)
    print(f"  Hub: {path}")
    return path


def build_category_hub(cat_key, topic_pairs, related_hub_links):
    """Build hubs/category-<cat>.html"""
    os.makedirs(HUBS_DIR, exist_ok=True)
    path = os.path.join(HUBS_DIR, f"category-{cat_key}.html")
    if os.path.exists(path):
        return None

    label  = CATEGORY_HUB_LABELS[cat_key]
    canon  = f"{DOMAIN}/hubs/category-{cat_key}.html"
    pillar = PILLAR_MAP.get(cat_key, '')

    DESCS = {
        'ai-automation':  'All AI automation guides for San Diego operators — every industry, every use case.',
        'payments':       'Payment processing guides for San Diego small businesses — reduce fees, get paid faster.',
        'crypto-solana':  'Crypto and Solana payment guides for merchants. Plain-language. No hype.',
        'san-diego':      'Local San Diego operator resources — AI consulting, automation, and payment help.',
    }
    INTROS = {
        'ai-automation': (
            "AI automation is moving fast and the vendor noise is overwhelming. "
            "SideGuy cuts through it. Every guide here is written for operators — "
            "not developers, not investors, not VCs. If you run a business and want "
            "to understand what AI can actually do for you, start here."
        ),
        'payments': (
            "Payment processing fees quietly drain thousands of dollars a year from small businesses. "
            "Most operators don't know what their actual effective rate is. "
            "SideGuy explains your options honestly — new rails, crypto alternatives, "
            "and practical ways to reduce what you're giving to processors."
        ),
        'crypto-solana': (
            "Crypto payments are no longer just for tech companies. Solana's low fees and "
            "fast settlement make it genuinely practical for local businesses collecting "
            "payments. SideGuy explains how it works, what the risks are, and when it makes sense."
        ),
        'san-diego': (
            "San Diego operators face specific challenges — high rents, competitive markets, "
            "and a tech ecosystem that's growing fast. These guides are written specifically "
            "for San Diego business owners looking for local AI and automation help."
        ),
    }

    items = [(t.title(), f"../{fn}") for t, fn in topic_pairs[:200]]
    grid  = link_grid(items)
    chips = hub_chips(related_hub_links)

    html = header_html(label, canon, DESCS.get(cat_key, ''))
    html += f"""
<main>
  <h1>{label}</h1>
  <p class="subtitle">{INTROS.get(cat_key, '')}</p>

  <div class="card">
    <p>Browse the guides below — or <a href="sms:+17604541860">text PJ</a> if you'd
    rather just explain your situation and get a straight answer.</p>
  </div>
"""
    if pillar:
        html += f"""
  <div class="card">
    <p>📖 <strong>Start here:</strong>
    <a href="../{pillar}">{PILLAR_LABELS.get(cat_key, 'Master Guide')}</a>
    — the complete overview for this topic.</p>
  </div>
"""
    html += f"""
  <h2>All guides in this category</h2>
{grid}
  <h2>Related hubs</h2>
{chips}
{cta_block()}
</main>"""
    html += footer_html()

    with open(path, "w") as f:
        f.write(html)
    print(f"  Hub: {path}")
    return path


def build_city_hub(san_diego_pairs, all_hub_links):
    """Build hubs/city-san-diego.html"""
    os.makedirs(HUBS_DIR, exist_ok=True)
    path = os.path.join(HUBS_DIR, "city-san-diego.html")
    if os.path.exists(path):
        return None

    canon = f"{DOMAIN}/hubs/city-san-diego.html"
    items = [(t.title(), f"../{fn}") for t, fn in san_diego_pairs[:200]]
    grid  = link_grid(items)
    chips = hub_chips(all_hub_links)

    html = header_html("San Diego Operator Hub", canon,
        "All SideGuy resources for San Diego operators — AI automation, payments, crypto, and local consulting.")
    html += f"""
<main>
  <h1>San Diego Operator Hub</h1>
  <p class="subtitle">
    Every SideGuy guide relevant to San Diego businesses — AI automation,
    payment processing, crypto rails, and local consulting.
    Calm, clarity-first resources for operators making real decisions.
  </p>

  <div class="card">
    <p>SideGuy is based in San Diego. Every guide here is written for local operators —
    not generic "small business" advice, but real guidance for the San Diego market.</p>
  </div>

  <h2>San Diego guides</h2>
{grid}
  <h2>Browse by topic</h2>
{chips}
{cta_block()}
</main>"""
    html += footer_html()

    with open(path, "w") as f:
        f.write(html)
    print(f"  Hub: {path}")
    return path


def build_pillar(cat_key, topic_pairs, related_pillar_links, industry_hub_links):
    """Build pillars/<cat>-master-guide.html"""
    os.makedirs(PILLARS_DIR, exist_ok=True)
    pillar_file = PILLAR_MAP[cat_key]
    path = pillar_file  # already relative path like pillars/ai-automation-master-guide.html
    if os.path.exists(path):
        return None

    label   = PILLAR_LABELS[cat_key]
    canon   = f"{DOMAIN}/{pillar_file}"
    cat_hub = CATEGORY_HUB_PATH.get(cat_key, '')

    PILLAR_INTROS = {
        'ai-automation': (
            "AI automation is one of the most overhyped and underexplained topics in "
            "business today. Vendors promise transformation; reality is messier. "
            "This guide explains what AI automation actually is, which use cases "
            "have proven ROI, which are still experimental, and how to evaluate "
            "vendors without getting burned. Written for operators, not technologists."
        ),
        'payments': (
            "Payment processing is a hidden cost center for most businesses. "
            "The average effective rate after all fees, chargebacks, and processor markups "
            "is often 3–4%. This guide explains how to audit your current costs, "
            "what your real options are, and how emerging payment rails "
            "(crypto, stablecoins, ACH) compare to traditional processing."
        ),
        'crypto-solana': (
            "Crypto payments have crossed from experiment to viable business tool "
            "— especially on Solana, where transaction fees are fractions of a cent "
            "and settlement happens in seconds. This guide explains the options "
            "with real numbers, real risks, and no ideological slant. "
            "Just: here's what it costs, here's what it takes, here's who it makes "
            "sense for."
        ),
        'san-diego': (
            "San Diego has one of the most dynamic small business ecosystems in the US — "
            "high operator density, strong trade industries, and a growing tech adoption curve. "
            "This guide compiles everything SideGuy knows about running, automating, "
            "and optimizing a San Diego business in 2026."
        ),
    }

    PILLAR_SECTIONS = {
        'ai-automation': [
            ("What AI automation actually is",
             "AI automation means using software to handle tasks that previously required human judgment. The key word is 'judgment' — AI has gotten good enough at narrow tasks (scheduling, email drafting, lead scoring, call routing) that the cost of automating them is now within reach of small businesses."),
            ("Which use cases have real ROI",
             "Proven ROI: appointment reminders, review request follow-ups, initial lead screening, invoice generation, and basic customer FAQ responses. Speculative ROI: complex proposal writing, full customer service replacement, and anything requiring brand judgment."),
            ("How to evaluate vendors",
             "Ask every vendor: What's your setup fee? What's the monthly cost? What does success look like at 90 days? Can I cancel month-to-month? Who owns the data? What happens if the AI gets something wrong? Their answers tell you everything."),
            ("Common implementation mistakes",
             "Starting with a complex use case. Not defining what 'done' looks like. Signing 12-month contracts before running a 30-day pilot. Assuming staff will adopt it without training. Picking based on demo quality rather than actual customer case studies."),
        ],
        'payments': [
            ("How to audit your current processing costs",
             "Pull your last 3 months of processor statements. Find your effective rate: total fees ÷ total volume. Most businesses should be at 2.5–2.9%. If you're above 3%, you're leaving money on the table. Look for monthly fees, PCI fees, batch fees, and statement fees — these add up."),
            ("Your actual options",
             "Square and Stripe are the most common. Both charge around 2.9% + 30¢. For high volume, negotiate with your processor — most will reduce rates after $50k/month. ACH/bank transfer is 0.5–1% and works well for repeat customers. Crypto (USDC/Solana) is effectively 0% on rails but requires customer adoption."),
            ("Chargebacks — the hidden cost",
             "Each chargeback costs $15–100 in fees plus you lose the sale. High chargeback rates (above 1%) can get your account terminated. Prevention: clear billing descriptors, easy refund process, delivery confirmation, and customer communication."),
            ("When crypto makes sense",
             "If your customers are comfortable with it (tech-forward, international, or crypto-native), USDC on Solana is genuinely practical. You receive exactly what was sent, settlement is instant, and you can auto-convert to dollars same-day through exchanges like Coinbase or Kraken."),
        ],
        'crypto-solana': [
            ("What Solana is and why it matters for payments",
             "Solana is a blockchain network where transaction fees are fractions of a cent — usually $0.00025. Compared to Ethereum ($1–5 per transaction) or Bitcoin ($1–30), Solana is purpose-built for high-frequency, low-value payments. Settlement is final in ~400 milliseconds."),
            ("USDC: the practical stablecoin",
             "USDC is a dollar-pegged stablecoin on Solana (and other chains). You receive USDC, it's worth $1 per token, and you can convert to actual dollars via Coinbase, Kraken, or similar in minutes. The volatility problem people associate with crypto doesn't apply to USDC."),
            ("How to actually set this up",
             "You need: a business wallet (Phantom or Backpack), a way for customers to pay (QR code or payment link), and a conversion process. Tools like Helio, Sphere Pay, or Coinbase Commerce handle the UX. Setup takes 1–2 hours."),
            ("Tax and accounting",
             "Receiving USDC is taxed as ordinary income at the value received. Converting to dollars is a taxable event but with minimal gain if you convert quickly. Your bookkeeper needs to track each transaction. Tools like Koinly or Crypto.com Tax can help."),
        ],
        'san-diego': [
            ("The San Diego business landscape",
             "San Diego has 150,000+ small businesses. Key sectors: construction/trades, health/wellness, food service, real estate, and defense/tech adjacent. High operator density means competition is real — efficiency and customer experience matter more than average."),
            ("Where AI automation is being adopted",
             "Fastest adoption: medical offices (scheduling, intake), real estate (lead follow-up), restaurants (ordering, reviews), and contractors (quoting, follow-up). Slowest: trades that rely on relationship trust and established referral networks."),
            ("Payment trends locally",
             "San Diego restaurants and food trucks are more crypto-curious than most markets. Several North County businesses accept USDC. Credit card fee pain is real — especially in high-ticket service industries like HVAC, roofing, and solar."),
            ("Finding reliable local help",
             "Most SD 'AI consultants' are generalists or recent converts. Ask: Have you implemented AI for a business like mine? Can you show me before/after metrics? Most can't. SideGuy is honest: we do assessments and referrals, not oversold implementations."),
        ],
    }

    items = [(t.title(), f"../{fn}") for t, fn in topic_pairs[:200]]
    grid  = link_grid(items)
    chips = hub_chips(related_pillar_links)
    ind_chips = hub_chips(industry_hub_links[:20]) if industry_hub_links else ""

    sections_html = ""
    for sec_title, sec_body in PILLAR_SECTIONS.get(cat_key, []):
        sections_html += f"""
  <div class="card">
    <h2>{sec_title}</h2>
    <p>{sec_body}</p>
  </div>"""

    html = header_html(label, canon,
        f"{label} — comprehensive operator guide from SideGuy. Real numbers, real options, no pitch.")
    html += f"""
<main>
  <h1>{label}</h1>
  <p class="subtitle">
    A plain-language master guide for San Diego operators.
    No jargon, no vendor bias, no upsell. Just clarity.
  </p>
{sections_html}
  <h2>All related guides</h2>
{grid}
"""
    if ind_chips:
        html += f"  <h2>Industry hubs</h2>\n{ind_chips}\n"
    html += f"""  <h2>Other master guides</h2>
{chips}
{cta_block()}
</main>"""
    html += footer_html()

    with open(path, "w") as f:
        f.write(html)
    print(f"  Pillar: {path}")
    return path


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    with open(MANIFEST) as f:
        topics = json.load(f)["topics"]

    print(f"Building authority pages for {len(topics)} topics...")

    by_category, by_industry = build_index(topics)

    # All hub/pillar cross-link data
    all_category_hub_links = [
        (CATEGORY_HUB_LABELS[c], f"../hubs/category-{c}.html")
        for c in CATEGORIES
    ]
    all_pillar_links = [
        (PILLAR_LABELS[c], f"../{PILLAR_MAP[c]}")
        for c in PILLAR_MAP
    ]

    created_hubs    = 0
    created_pillars = 0

    # ── Industry hubs ─────────────────────────────────────────────────────────
    print(f"\nBuilding industry hubs ({len(by_industry)} industries)...")
    all_industry_hub_links = [
        (industry_hub_label(slug), f"../hubs/industry-{slug}.html")
        for slug in sorted(by_industry)
    ]
    cat_chips_html = hub_chips(all_category_hub_links)
    for slug, pairs in sorted(by_industry.items()):
        r = build_industry_hub(slug, pairs, cat_chips_html)
        if r:
            created_hubs += 1

    # ── Category hubs ─────────────────────────────────────────────────────────
    print("\nBuilding category hubs...")
    for cat in CATEGORIES:
        related = [(CATEGORY_HUB_LABELS[c], f"../hubs/category-{c}.html")
                   for c in CATEGORIES if c != cat]
        r = build_category_hub(cat, by_category[cat], related)
        if r:
            created_hubs += 1

    # ── City hub ──────────────────────────────────────────────────────────────
    print("\nBuilding city hub...")
    r = build_city_hub(by_category['san-diego'], all_category_hub_links)
    if r:
        created_hubs += 1

    # ── Pillar pages ──────────────────────────────────────────────────────────
    print("\nBuilding pillar pages...")
    for cat in PILLAR_MAP:
        other_pillars = [(PILLAR_LABELS[c], f"../{PILLAR_MAP[c]}")
                         for c in PILLAR_MAP if c != cat]
        r = build_pillar(cat, by_category[cat], other_pillars, all_industry_hub_links)
        if r:
            created_pillars += 1

    print(f"\n✅ Authority build complete.")
    print(f"   Hubs created:    {created_hubs}")
    print(f"   Pillars created: {created_pillars}")
    print(f"   Total industries found: {len(by_industry)}")


if __name__ == "__main__":
    main()
