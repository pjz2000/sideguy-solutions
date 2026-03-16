#!/usr/bin/env python3
"""
SideGuy Topic Expansion Engine
Generates premium HTML pages from topic seeds.
Run: python3 tools/expansion/topic-expansion-engine.py
"""

import os
import re
from string import Template
from datetime import date

SEEDS_FILE = "data/topic-seeds/service-topics.txt"
OUTDIR = "pages/expansion"
SITEMAP = "sitemap.xml"
LOG_FILE = "logs/expansion/expansion.log"
MONTH = "March 2026"

TAG_VARIANTS = [
    ("cost-guide",        "Cost Guide"),
    ("repair-vs-replace", "Repair vs Replace"),
    ("warning-signs",     "Warning Signs"),
    ("checklist",         "Checklist"),
    ("common-mistakes",   "Common Mistakes"),
    ("questions-to-ask",  "Questions to Ask"),
    ("scam-red-flags",    "Scam Red Flags"),
    ("inspection-cost",   "Inspection Cost"),
    ("upgrade-options",   "Upgrade Options"),
    ("future-tech",       "Future Tech"),
]


def slugify(text):
    return re.sub(r"[^a-z0-9-]", "", text.lower().replace(" ", "-"))


def title_case(text):
    return " ".join(w.capitalize() for w in text.split())


# string.Template uses $identifier substitution.
# CSS uses var(--name) — no $ signs, safe.
# JSON-LD uses {} braces — not Template placeholders, safe.
PAGE_TEMPLATE = Template("""\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <meta name="robots" content="index, follow, max-image-preview:large"/>
  <title>$page_title · San Diego · SideGuy</title>
  <link rel="canonical" href="https://sideguysolutions.com/expansion/$page_slug.html"/>
  <meta name="description" content="$page_title in San Diego — plain-language guidance on $topic including costs, red flags, and what to check before spending money."/>
  <meta property="og:title" content="$page_title · San Diego"/>
  <meta property="og:description" content="SideGuy guide to $topic — clarity before cost."/>
  <meta property="og:url" content="https://sideguysolutions.com/expansion/$page_slug.html"/>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="SideGuy Solutions"/>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does $topic cost in San Diego?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Costs for $topic in San Diego vary by scope, contractor, and timing. Getting 2-3 quotes helps establish what is fair for your specific situation. Text PJ at 773-544-1231 for a quick read on whether a quote seems reasonable."
      }
    },
    {
      "@type": "Question",
      "name": "What are the warning signs I need $topic service?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Common warning signs include unusual performance issues, visible damage, increased operating costs, and declining reliability. Catching problems early usually reduces the total cost of repair or replacement."
      }
    },
    {
      "@type": "Question",
      "name": "How do I avoid getting overcharged for $topic in San Diego?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Get at least 2 written quotes, ask for itemized pricing, and verify contractor licensing through the California CSLB. Unusually low or high quotes both warrant questions. SideGuy can help you read a quote — text PJ at 773-544-1231."
      }
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "SideGuy", "item": "https://sideguysolutions.com"},
    {"@type": "ListItem", "position": 2, "name": "$topic_tc", "item": "https://sideguysolutions.com/expansion/$slug-cost-guide.html"},
    {"@type": "ListItem", "position": 3, "name": "$page_title", "item": "https://sideguysolutions.com/expansion/$page_slug.html"}
  ]
}
</script>
<style>
:root{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--mint2:#00c7ff;--accent:#0a4a6e;--r:22px;--pill:999px;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;color:var(--ink);background:radial-gradient(1200px 900px at 22% 10%,#ffffff 0%,var(--bg0) 25%,var(--bg1) 60%,#bfeeff 100%);line-height:1.75;-webkit-font-smoothing:antialiased;}
body:before{content:"";position:fixed;inset:-20%;background:radial-gradient(closest-side at 18% 20%,rgba(33,211,161,.18),transparent 55%),radial-gradient(closest-side at 78% 28%,rgba(74,169,255,.16),transparent 52%);filter:blur(18px);pointer-events:none;z-index:-2;}
.topbar{position:sticky;top:0;z-index:50;padding:12px 14px 8px;display:flex;justify-content:center;pointer-events:none;}
.homePill{pointer-events:auto;text-decoration:none;display:inline-flex;align-items:center;gap:10px;padding:10px 16px;border-radius:var(--pill);background:linear-gradient(180deg,rgba(255,255,255,.84),rgba(255,255,255,.62));border:1px solid rgba(7,48,68,.07);box-shadow:0 10px 28px rgba(7,48,68,.08);color:var(--ink);font-weight:700;font-size:12px;backdrop-filter:blur(14px);}
.dot{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 0 0 3px rgba(255,255,255,.95);}
.wrap{max-width:820px;margin:0 auto;padding:24px 22px 80px;}
h1{font-size:2.1rem;line-height:1.1;margin:8px 0 10px;letter-spacing:-.02em;}
@media(max-width:520px){h1{font-size:1.6rem}}
h2{font-size:1.15rem;color:var(--accent);margin-top:2rem;border-bottom:1px solid #c5eef7;padding-bottom:4px;}
.lede{font-size:1.05rem;color:var(--muted);margin-bottom:1.4rem;max-width:680px;}
ul{padding-left:1.3em;margin:.6rem 0 1rem;}
li{margin:.35rem 0;line-height:1.65;}
details{background:rgba(255,255,255,.6);border:1px solid rgba(7,48,68,.08);border-radius:10px;padding:12px 16px;margin:.6rem 0;}
details summary{cursor:pointer;font-size:.95rem;}
details p{margin:.6rem 0 0;font-size:.93rem;color:var(--muted);}
.flag{background:#fff8e1;border-left:4px solid #f5a623;padding:12px 16px;border-radius:8px;margin:1.2rem 0;font-size:.93rem;}
.flag strong{color:#8a5400;}
.cta-block{background:linear-gradient(180deg,rgba(33,211,161,.12),rgba(0,199,255,.09));border:1px solid rgba(7,48,68,.09);border-radius:var(--r);padding:20px;margin:2rem 0;display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;}
.cta-block .t{font-weight:800;font-size:1rem;color:var(--accent);}
.cta-block .s{font-size:.85rem;color:var(--muted);margin-top:3px;}
.btn{text-decoration:none;display:inline-flex;align-items:center;padding:12px 20px;border-radius:var(--pill);background:linear-gradient(135deg,var(--mint),var(--mint2));color:#fff;font-weight:800;font-size:.85rem;box-shadow:0 14px 36px rgba(0,199,255,.22);white-space:nowrap;}
.related{display:flex;flex-wrap:wrap;gap:8px;margin:1.2rem 0;}
.related a{display:inline-block;padding:8px 14px;border-radius:var(--pill);border:1px solid rgba(7,48,68,.12);background:rgba(255,255,255,.65);font-size:.82rem;color:var(--ink);text-decoration:none;}
nav.bc{max-width:820px;margin:0 auto;padding:8px 22px;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;gap:4px;align-items:center;}
nav.bc a{color:var(--muted);text-decoration:none;}
nav.bc span{opacity:.4;margin:0 3px;}
.floating{position:fixed;right:18px;bottom:16px;z-index:999;display:flex;align-items:center;gap:10px;}
.fpill{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.68);border:1px solid rgba(7,48,68,.08);box-shadow:0 18px 55px rgba(7,48,68,.14);backdrop-filter:blur(14px);min-width:190px;}
.fpill .t1{font-weight:900;font-size:12px;color:rgba(7,48,68,.88);display:flex;align-items:center;gap:8px;}
.cdot{width:9px;height:9px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));}
.fpill .t2{font-size:11px;color:rgba(7,48,68,.62);}
.forb{width:54px;height:54px;border-radius:999px;background:radial-gradient(circle at 30% 20%,#ffffff,rgba(33,211,161,.95) 52%,rgba(0,199,255,.95) 100%);border:1px solid rgba(255,255,255,.8);box-shadow:0 0 0 4px rgba(255,255,255,.92),0 22px 60px rgba(0,199,255,.22);text-decoration:none;display:flex;align-items:center;justify-content:center;color:var(--ink);font-weight:900;font-size:11px;animation:pulse 2.2s ease-in-out infinite;}
@keyframes pulse{0%,100%{box-shadow:0 0 0 4px rgba(255,255,255,.92),0 14px 40px rgba(0,199,255,.22)}50%{box-shadow:0 0 0 4px rgba(255,255,255,.92),0 22px 60px rgba(0,199,255,.45)}}
footer{opacity:.6;font-size:.82rem;border-top:1px solid #c5eef7;padding-top:1rem;text-align:center;margin-top:2rem;}
</style>
</head>
<body>
<a href="#main" style="position:absolute;left:0;top:0;background:#fff;color:#073044;padding:8px 16px;border-radius:8px;z-index:1000;font-size:.8rem;">Skip to content</a>
<div class="topbar"><a class="homePill" href="/index.html"><span class="dot"></span>Back to home</a></div>
<nav class="bc" aria-label="Breadcrumb">
  <a href="/index.html">SideGuy</a><span>/</span>
  <a href="/expansion/$slug-cost-guide.html">$topic_tc</a><span>/</span>
  $page_title
</nav>
<div class="wrap"><main id="main">
<p style="font-size:.8rem;opacity:.6;margin-bottom:4px;">SideGuy Solutions · San Diego · Updated $month</p>
<h1>$page_title in San Diego</h1>
<p class="lede">Plain-language guidance on $topic — so you know what to expect, what is fair, and what to watch out for before spending money.</p>

<h2>What You Need to Know</h2>
<p>When it comes to $topic in San Diego, most problems operators and homeowners face come down to three things: not knowing what fair pricing looks like, not knowing what questions to ask, and not having a reference point when a quote seems off. This guide exists to fix all three.</p>
<p>San Diego has a competitive market for $topic services, which is good for consumers — but it also means there is a wide range of quality and pricing. The cheapest option is rarely the best, and the most expensive rarely necessary. The goal is to be informed enough to ask the right questions and recognize a fair deal when you see one.</p>
<p>Whether you are dealing with a new installation, an unexpected repair, or simply researching your options, the same principles apply: get it in writing, verify credentials, and never let urgency be used as a sales tactic against you.</p>

<h2>Key Questions to Ask Any Contractor</h2>
<ul>
  <li>Are you licensed and insured for this specific type of work in California?</li>
  <li>Can you provide a written, itemized quote before starting?</li>
  <li>What is included in this price — and what is not?</li>
  <li>How long will the work take, and what could cause delays?</li>
  <li>Do you pull permits when required by the City of San Diego?</li>
  <li>What warranty do you provide on parts and labor?</li>
  <li>Can you provide references from similar jobs completed in the last 6 months?</li>
</ul>

<h2>Warning Signs to Watch For</h2>
<div class="flag"><strong>Red flags that warrant a second quote or a call to PJ:</strong></div>
<ul>
  <li>Pressure to decide immediately or claims that the price goes up tomorrow</li>
  <li>Quote given over the phone without a site visit or inspection</li>
  <li>No written contract or itemized breakdown offered</li>
  <li>Request for full payment upfront before any work begins</li>
  <li>No license number provided when asked — verify at cslb.ca.gov</li>
  <li>Unusually low bid with no clear explanation for the discount</li>
  <li>Reluctance to pull permits for work that legally requires them</li>
  <li>Vague answers about scope, timeline, or what happens if something goes wrong</li>
</ul>

<h2>Typical Cost Drivers in San Diego</h2>
<p>For $topic, cost in San Diego is typically influenced by the scope and complexity of the job, the age and condition of existing systems or structures, local labor rates (which tend to run 10 to 20 percent above national averages), materials availability, and whether permits or inspections are required by the city.</p>
<p>Always get at least two written quotes for any job over five hundred dollars. For jobs over two thousand dollars, three quotes is the standard. The comparison will give you useful data points about what is included and what different contractors prioritize — revealing who is thorough and who is cutting corners.</p>

<div class="cta-block">
  <div>
    <p class="t">Not sure if a quote is fair?</p>
    <p class="s">Text PJ — quick read on whether the numbers make sense. No pitch.</p>
  </div>
  <a class="btn" href="sms:+17735441231">📱 Text PJ</a>
</div>

<h2>Before You Hire — Checklist</h2>
<ul>
  <li>Verified contractor license on the California CSLB website (cslb.ca.gov)</li>
  <li>Confirmed they carry general liability and workers compensation insurance</li>
  <li>Received at least 2 written quotes with itemized line items</li>
  <li>Understood what is and is not included in the scope of work</li>
  <li>Confirmed permit requirements with the City of San Diego if applicable</li>
  <li>Checked reviews on Google, Yelp, or BBB from within the last 12 months</li>
  <li>Got a clear timeline with start and estimated completion dates in writing</li>
  <li>Confirmed payment terms — a reasonable deposit is 10 to 30 percent for larger jobs</li>
</ul>

<h2>Common Mistakes to Avoid</h2>
<ul>
  <li>Choosing based on price alone without verifying credentials or reviews</li>
  <li>Skipping the permit process to save money — this creates liability and resale issues later</li>
  <li>Not getting the full scope of work in writing before work begins</li>
  <li>Paying more than 30 to 40 percent upfront for large projects</li>
  <li>Ignoring early warning signs until a minor issue becomes a major repair</li>
  <li>Assuming all contractors carry insurance — always ask for a certificate of insurance</li>
</ul>

<h2>Frequently Asked Questions</h2>
<details>
  <summary><strong>How much does $topic cost in San Diego?</strong></summary>
  <p>Costs vary by scope, contractor, and timing. Getting 2 to 3 written quotes is the best way to establish what is fair for your specific situation. Text PJ at 773-544-1231 for a quick read on whether a quote seems reasonable.</p>
</details>
<details>
  <summary><strong>What are the warning signs I need $topic service?</strong></summary>
  <p>Common warning signs include unusual performance issues, visible damage, increased operating costs, and declining reliability. Catching problems early usually reduces the total cost of repair or replacement significantly.</p>
</details>
<details>
  <summary><strong>How do I avoid getting overcharged for $topic in San Diego?</strong></summary>
  <p>Get at least 2 written quotes, ask for itemized pricing, and verify the contractor license through the California CSLB. Unusually low or high quotes both warrant follow-up questions. Text PJ at 773-544-1231 if you want a second opinion.</p>
</details>

<h2>Related Guides</h2>
<div class="related">
  <a href="/expansion/$slug-cost-guide.html">$topic_tc Cost Guide</a>
  <a href="/expansion/$slug-warning-signs.html">$topic_tc Warning Signs</a>
  <a href="/expansion/$slug-checklist.html">$topic_tc Checklist</a>
  <a href="/expansion/$slug-questions-to-ask.html">Questions to Ask</a>
  <a href="/expansion/$slug-scam-red-flags.html">Scam Red Flags</a>
  <a href="/expansion/$slug-repair-vs-replace.html">Repair vs Replace</a>
  <a href="/index.html">SideGuy Home</a>
</div>

</main></div>
<footer><p>SideGuy Solutions · San Diego · Clarity before cost · Updated $month</p></footer>
<div class="floating">
  <div class="fpill">
    <span class="t1"><span class="cdot"></span>Text PJ — real answers</span>
    <span class="t2">773-544-1231 · No pressure</span>
  </div>
  <a class="forb" href="sms:+17735441231" aria-label="Text PJ" rel="nofollow">PJ</a>
</div>
</body>
</html>""")


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    with open(LOG_FILE, "a") as log:
        log.write(f"Expansion run {date.today()}\n")

    topics = []
    with open(SEEDS_FILE) as f:
        for line in f:
            t = line.strip()
            if t:
                topics.append(t)

    new_urls = []
    count = 0

    for topic in topics:
        slug = slugify(topic)
        topic_tc = title_case(topic)
        for variant_slug, variant_label in TAG_VARIANTS:
            page_slug = f"{slug}-{variant_slug}"
            page_title = f"{topic_tc} {variant_label}"
            html = PAGE_TEMPLATE.safe_substitute(
                page_title=page_title,
                page_slug=page_slug,
                topic=topic,
                topic_tc=topic_tc,
                slug=slug,
                month=MONTH,
            )
            filepath = os.path.join(OUTDIR, f"{page_slug}.html")
            with open(filepath, "w") as fh:
                fh.write(html)
            new_urls.append(
                f"https://sideguysolutions.com/expansion/{page_slug}.html"
            )
            count += 1

    # Update sitemap in a single pass
    if os.path.exists(SITEMAP) and new_urls:
        content = open(SITEMAP).read()
        url_blocks = "\n".join(
            f'<url><loc>{u}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>'
            for u in new_urls
        )
        updated = content.replace("</urlset>", url_blocks + "\n</urlset>", 1)
        open(SITEMAP, "w").write(updated)
        print(f"Sitemap updated: +{len(new_urls)} URLs")

    with open(LOG_FILE, "a") as log:
        log.write(f"Expansion complete: {count} pages\n")

    print(f"\nPages generated: {count}")
    print(f"Output: {OUTDIR}/")
    print(f"Log: {LOG_FILE}")


if __name__ == "__main__":
    main()
