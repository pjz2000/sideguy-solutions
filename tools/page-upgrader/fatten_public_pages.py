#!/usr/bin/env python3
"""
Fatten Public Pages — SideGuy Solutions
========================================
Pass 1: Rebuilds thin stubs (<80 lines) with full SideGuy content template.
Pass 2: Backfills ALL public pages with og:image, accessibility, schema, canonical.
Idempotent — safe to re-run.
"""
from pathlib import Path
import re, json
from datetime import date

ROOT  = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
TODAY  = date.today().isoformat()
DOMAIN = "https://sideguysolutions.com"
PHONE  = "+1-760-454-1860"
OG_IMG = f"{DOMAIN}/og-preview.png"

# ── helpers ──────────────────────────────────────────────────────────────────

def slug_to_title(slug):
    """battery-backup-installation-san-diego → Battery Backup Installation San Diego"""
    return slug.replace(".html","").replace("-"," ").title()

def slug_to_description(slug):
    name = slug.replace("-san-diego.html","").replace("-san-diego","").replace(".html","").replace("-"," ").title()
    return f"{name} — plain-language guidance for San Diego homeowners and small businesses from SideGuy Solutions."

def detect_category(slug):
    slug = slug.lower()
    if any(k in slug for k in ["hvac","ac ","air-cond","heat","cool","furnace","mini-split"]):
        return "HVAC & Cooling"
    if any(k in slug for k in ["plumb","pipe","water","leak","toilet","drain","sewer"]):
        return "Plumbing"
    if any(k in slug for k in ["electric","panel","outlet","wiring","circuit","solar","battery"]):
        return "Electrical & Solar"
    if any(k in slug for k in ["payment","processing","stripe","square","merchant","pos","checkout"]):
        return "Payment Processing"
    if any(k in slug for k in ["ai","automat","software","app","tech","website","wordpress","zapier"]):
        return "Tech & Automation"
    if any(k in slug for k in ["roof","window","door","fence","deck","flooring","tile","paint"]):
        return "Home Improvement"
    if any(k in slug for k in ["account","tax","bookkeep","finance","invoice","payroll"]):
        return "Accounting & Finance"
    if any(k in slug for k in ["marketing","seo","social","brand","ad","email"]):
        return "Marketing"
    return "Home & Business Services"

def faq_for_topic(title, category):
    q1 = f"How much does {title} cost in San Diego?"
    a1 = f"Costs vary by scope and provider. For {title.lower()}, most San Diego residents pay mid-market rates. Always get 2–3 quotes and ask what's included. SideGuy can help you decode a quote — text us at {PHONE}."
    q2 = f"How do I know if I need {title.lower()}?"
    a2 = f"If you're seeing problems related to {title.lower()}, it's worth a quick check before it gets worse. The fastest way to get clarity: text PJ at {PHONE} — no sales pitch, just straight answers."
    q3 = f"Who do I call for {title.lower()} in San Diego?"
    a3 = f"It depends on the root cause. SideGuy helps you figure that out first — so you call the right person, not just the first result on Google. Text {PHONE}."
    return [
        {"q": q1, "a": a1},
        {"q": q2, "a": a2},
        {"q": q3, "a": a3},
    ]

def build_faq_schema(faqs):
    entities = [{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in faqs]
    return json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":entities}, indent=2)

def build_full_page(slug, title, category, faqs, description):
    faq_schema = build_faq_schema(faqs)
    faq_html = "\n".join([
        f"""<details style="margin-bottom:12px;border-radius:8px;border:1px solid #d0ecf7;overflow:hidden;">
  <summary style="padding:14px 18px;cursor:pointer;font-weight:600;background:#f0faff;color:#073044;">{f['q']}</summary>
  <div style="padding:14px 18px;font-size:.97rem;color:#073044;line-height:1.65;">{f['a']}</div>
</details>"""
        for f in faqs
    ])
    url = f"{DOMAIN}/public/{slug}"
    page_topic = title.replace(" San Diego","").replace(" — What to Know","").strip()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} · SideGuy Solutions (San Diego)</title>
  <meta name="description" content="{description}"/>
  <link rel="canonical" href="{url}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="SideGuy Solutions"/>
  <meta property="og:title" content="{title} · SideGuy Solutions"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:image" content="{OG_IMG}"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{title} · SideGuy Solutions"/>
  <meta name="twitter:description" content="{description}"/>
  <meta name="twitter:image" content="{OG_IMG}"/>
  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"LocalBusiness",
    "name":"SideGuy Solutions",
    "url":"{DOMAIN}",
    "telephone":"{PHONE}",
    "address":{{"@type":"PostalAddress","addressLocality":"San Diego","addressRegion":"CA","addressCountry":"US"}},
    "areaServed":"San Diego, CA"
  }}
  </script>
  <script type="application/ld+json">
  {faq_schema}
  </script>
  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"BreadcrumbList",
    "itemListElement":[
      {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}"}},
      {{"@type":"ListItem","position":2,"name":"{category}","item":"{DOMAIN}"}},
      {{"@type":"ListItem","position":3,"name":"{title}","item":"{url}"}}
    ]
  }}
  </script>
  <style>
    :root{{--bg0:#eefcff;--ink:#073044;--mint:#21d3a1;--mint2:#00c7ff;--card:#fff;--r:14px}}
    *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
    body{{font-family:-apple-system,system-ui,"Segoe UI",Roboto,Inter,sans-serif;background:radial-gradient(ellipse at 20% 40%,#b8f4f0 0%,#d6f5ff 35%,#eefcff 70%,#fff8f0 100%);color:var(--ink);min-height:100vh}}
    .skip-link{{position:absolute;left:0;top:0;background:#fff;color:var(--ink);padding:8px 16px;border-radius:8px;z-index:1000;transform:translateY(-100%);transition:.2s}}
    .skip-link:focus{{transform:translateY(0)}}
    header{{display:flex;align-items:center;justify-content:space-between;padding:14px 24px;background:rgba(255,255,255,.7);backdrop-filter:blur(8px);border-bottom:1px solid rgba(33,211,161,.25)}}
    .brand{{font-weight:800;font-size:1.15rem;color:var(--ink);text-decoration:none}}
    .cta-pill{{background:var(--mint);color:#fff;font-size:.85rem;font-weight:700;padding:8px 18px;border-radius:99px;text-decoration:none;white-space:nowrap}}
    nav[aria-label="Breadcrumb navigation"]{{max-width:820px;margin:12px auto 0;padding:0 24px;font-size:.82rem;color:#3f6173;display:flex;flex-wrap:wrap;align-items:center;gap:4px}}
    nav a{{color:#3f6173;text-decoration:none}}nav a:hover{{color:var(--mint)}}
    main{{max-width:820px;margin:0 auto;padding:40px 20px 80px}}
    h1{{font-size:clamp(1.5rem,4vw,2.2rem);font-weight:900;line-height:1.2;margin-bottom:18px;color:var(--ink)}}
    .lead{{font-size:1.12rem;line-height:1.7;color:#1a4d62;margin-bottom:28px}}
    .card{{background:#fff;border-radius:var(--r);box-shadow:0 4px 20px rgba(7,48,68,.08);padding:28px 32px;margin-bottom:28px}}
    .card h2{{font-size:1.15rem;font-weight:800;color:var(--ink);margin-bottom:14px}}
    ul.checklist{{list-style:none;padding:0}}
    ul.checklist li{{padding:8px 0 8px 28px;position:relative;border-bottom:1px solid #e8f4f8;font-size:.97rem;line-height:1.55}}
    ul.checklist li:last-child{{border-bottom:none}}
    ul.checklist li::before{{content:"✓";position:absolute;left:0;color:var(--mint);font-weight:700}}
    .cta-block{{background:linear-gradient(135deg,var(--mint),var(--mint2));border-radius:var(--r);padding:32px;text-align:center;color:#fff;margin:32px 0}}
    .cta-block h2{{font-size:1.3rem;font-weight:800;margin-bottom:10px}}
    .cta-block p{{font-size:1rem;opacity:.92;margin-bottom:20px}}
    .cta-block a{{background:#fff;color:var(--ink);font-weight:700;padding:12px 28px;border-radius:99px;text-decoration:none;font-size:1rem}}
    .faq-section h2{{font-size:1.1rem;font-weight:800;margin-bottom:16px;color:var(--ink)}}
    footer{{max-width:820px;margin:0 auto;padding:32px 20px;border-top:1px solid #d0ecf7;font-size:.85rem;color:#5a7b8a;text-align:center}}
    footer a{{color:var(--mint);text-decoration:none}}
    @media(max-width:600px){{.card{{padding:20px 16px}}header{{padding:12px 16px}}}}
  </style>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to content</a>
  <header>
    <a href="/" class="brand">SideGuy Solutions</a>
    <a href="sms:+17604541860" class="cta-pill">Text PJ Now</a>
  </header>
  <nav aria-label="Breadcrumb navigation">
    <a href="/">Home</a>&nbsp;›&nbsp;<span>{category}</span>&nbsp;›&nbsp;<span>{page_topic}</span>
  </nav>
  <main id="main-content">
    <h1>{title}</h1>
    <p class="lead">{description}</p>

    <div class="card">
      <h2>What to check first</h2>
      <ul class="checklist">
        <li>Define the actual problem before calling anyone — symptoms vs. root cause matter</li>
        <li>Get 2–3 quotes and ask each provider to explain what they're actually fixing</li>
        <li>Check if your situation is a DIY fix, a licensed contractor job, or a warranty issue</li>
        <li>Ask what happens if the first fix doesn't work — is there a follow-up plan?</li>
        <li>Avoid paying in full upfront — 50% deposit is standard, remainder on completion</li>
      </ul>
    </div>

    <div class="card">
      <h2>Common mistakes people make with {page_topic.lower()}</h2>
      <ul class="checklist">
        <li>Hiring based on price alone without checking reviews or licensing</li>
        <li>Not getting the scope of work in writing before work starts</li>
        <li>Delaying action — small problems become expensive ones fast</li>
        <li>Assuming the first diagnosis is always correct — a second opinion is often worth it</li>
      </ul>
    </div>

    <div class="cta-block">
      <h2>Not sure where to start?</h2>
      <p>Text PJ — real human, straight answer, no sales pitch. San Diego based.</p>
      <a href="sms:+17604541860">Text +1-760-454-1860</a>
    </div>

    <section class="faq-section">
      <h2>Common questions about {page_topic.lower()}</h2>
      {faq_html}
    </section>

    <!-- SideGuy Meme Block -->
    <div class="sideguy-meme" style="background:#f0faff;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;text-align:center;">
      <strong>Real talk:</strong> The best time to research {page_topic.lower()} was before it became urgent. The second best time is right now.
    </div>

  </main>
  <footer>
    <p>SideGuy Solutions · San Diego, CA · <a href="sms:+17604541860">{PHONE}</a> · <a href="/">Home</a> · <a href="/public/sitemap.xml">Sitemap</a></p>
    <p style="margin-top:8px;font-size:.78rem;color:#8aabb8">Clarity before cost. Human guidance layer. Last updated {TODAY}.</p>
  </footer>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# PASS 1: Rebuild thin stubs
# ─────────────────────────────────────────────────────────────────────────────
rebuilt = 0
for page in sorted(PUBLIC.rglob("*.html")):
    lines = page.read_text(errors="ignore").splitlines()
    if len(lines) >= 80:
        continue
    slug   = page.name
    title  = slug_to_title(slug)
    cat    = detect_category(slug)
    desc   = slug_to_description(slug)
    faqs   = faq_for_topic(title.replace(" San Diego","").strip(), cat)
    html   = build_full_page(slug, title, cat, faqs, desc)
    page.write_text(html)
    rebuilt += 1

print(f"Pass 1 — stubs rebuilt: {rebuilt}")

# ─────────────────────────────────────────────────────────────────────────────
# PASS 2: Backfill ALL pages with missing signals
# ─────────────────────────────────────────────────────────────────────────────
og_added = 0
a11y_added = 0
schema_added = 0
canonical_added = 0
viewport_added = 0

for page in sorted(PUBLIC.rglob("*.html")):
    text = page.read_text(errors="ignore")
    changed = False

    # --- viewport ---
    if 'name="viewport"' not in text and '</head>' in text:
        text = text.replace('<head>', '<head>\n  <meta name="viewport" content="width=device-width, initial-scale=1"/>', 1)
        changed = True
        viewport_added += 1

    # --- og:image + twitter:image ---
    if 'og:image' not in text and '</head>' in text:
        img_tags = f'  <meta property="og:image" content="{OG_IMG}"/>\n  <meta name="twitter:image" content="{OG_IMG}"/>\n'
        text = text.replace('</head>', img_tags + '</head>', 1)
        changed = True
        og_added += 1

    # --- canonical ---
    if 'rel="canonical"' not in text and '</head>' in text:
        url = f"{DOMAIN}/public/{page.name}"
        can = f'  <link rel="canonical" href="{url}"/>\n'
        text = text.replace('</head>', can + '</head>', 1)
        changed = True
        canonical_added += 1

    # --- LocalBusiness schema ---
    if 'application/ld+json' not in text and '</head>' in text:
        schema = f"""  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"LocalBusiness",
    "name":"SideGuy Solutions",
    "url":"{DOMAIN}",
    "telephone":"{PHONE}",
    "address":{{"@type":"PostalAddress","addressLocality":"San Diego","addressRegion":"CA","addressCountry":"US"}},
    "areaServed":"San Diego, CA"
  }}
  </script>\n"""
        text = text.replace('</head>', schema + '</head>', 1)
        changed = True
        schema_added += 1

    # --- accessibility: skip-link + main id ---
    if 'skip-link' not in text and '<body>' in text:
        text = text.replace('<body>', '<body>\n  <a href="#main-content" class="skip-link" style="position:absolute;left:0;top:0;background:#fff;color:#073044;padding:8px 16px;border-radius:8px;z-index:1000;">Skip to content</a>', 1)
        changed = True
        a11y_added += 1
    if 'id="main-content"' not in text:
        if '<main>' in text:
            text = text.replace('<main>', '<main id="main-content">', 1)
            changed = True
        elif '<main ' in text and 'id="main-content"' not in text:
            text = re.sub(r'<main(?! id=)', '<main id="main-content"', text, count=1)
            changed = True

    if changed:
        page.write_text(text)

print(f"Pass 2 — og:image added: {og_added}, a11y: {a11y_added}, schema: {schema_added}, canonical: {canonical_added}, viewport: {viewport_added}")
print(f"Total pages in /public/: {len(list(PUBLIC.rglob('*.html')))}")
