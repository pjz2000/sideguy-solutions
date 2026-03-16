#!/usr/bin/env python3
"""
SideGuy Million Engine — Matrix Page Builder
Generates premium HTML pages from 4-dimension matrix: problem x service x decision x location.
Run: python3 tools/million-engine/matrix-page-builder.py

WARNING: Full matrix = 5,120 pages. Use --dry-run to count without writing.
Use --service=hvac --location="san diego" to generate a subset.
"""
import os
import re
import argparse
from datetime import date

PROBLEMS_FILE  = "data/matrix/problems.txt"
SERVICES_FILE  = "data/matrix/services.txt"
DECISIONS_FILE = "data/matrix/decisions.txt"
LOCATIONS_FILE = "data/matrix/locations.txt"
OUTDIR         = "pages/matrix"
SITEMAP        = "sitemap.xml"
LOG            = "logs/million-engine/build.log"
MONTH          = "March 2026"


# --- cost data per service (used inline in page content) ---
SERVICE_DATA = {
    "hvac": {
        "range": "$3,000–$12,000 replacement / $150–$1,500 repair",
        "permit": "typically required for new installs",
        "license": "C-20 HVAC contractor license (California)",
        "red_flags": "pressure to replace immediately, refusing to itemize parts vs labor, no written estimate",
    },
    "roof repair": {
        "range": "$500–$3,000 repair / $10,000–$30,000 full replacement",
        "permit": "required for full replacement in most cities",
        "license": "C-39 roofing contractor license (California)",
        "red_flags": "door-to-door solicitation after storms, unusually low bids with vague scope",
    },
    "foundation repair": {
        "range": "$2,000–$25,000 depending on method and severity",
        "permit": "almost always required",
        "license": "C-12 earthwork/paving or general engineering (California)",
        "red_flags": "scare tactics about collapse, refusing to show engineering report, unlicensed inspectors",
    },
    "solar installation": {
        "range": "$15,000–$35,000 before incentives / $8,000–$20,000 after ITC",
        "permit": "always required; utility interconnection approval needed",
        "license": "C-46 solar contractor or C-10 electrical (California)",
        "red_flags": "overstated savings projections, locking you into high-rate solar loan, no itemized hardware list",
    },
    "tesla charger install": {
        "range": "$500–$2,500 installed depending on panel upgrade needs",
        "permit": "electrical permit required in most jurisdictions",
        "license": "C-10 electrical contractor (California)",
        "red_flags": "quoting without seeing electrical panel, skipping permit to save time",
    },
    "plumbing repair": {
        "range": "$150–$500 simple repairs / $1,000–$10,000 major work",
        "permit": "required for repiping, water heater replacement, sewer work",
        "license": "C-36 plumbing contractor (California)",
        "red_flags": "pushing camera inspection on every call, inflated parts markup, refusing to show itemized invoice",
    },
    "electrical repair": {
        "range": "$200–$1,500 typical repairs / $3,000–$10,000 panel upgrades",
        "permit": "nearly always required for panel, wiring, or service work",
        "license": "C-10 electrical contractor (California)",
        "red_flags": "working without permits, no load calculation before panel upgrade, cash-only requests",
    },
    "home battery install": {
        "range": "$8,000–$20,000 installed (Powerwall, Enphase)",
        "permit": "electrical permit required; sometimes building permit too",
        "license": "C-10 electrical plus manufacturer certification recommended",
        "red_flags": "oversold capacity, not accounting for your actual usage patterns, unlicensed installers",
    },
    "payment processing": {
        "range": "1.5%–3.5% per transaction; setup $0–$500; monthly $0–$150",
        "permit": "PCI-DSS compliance required; no traditional permit",
        "license": "processor must be registered money transmitter",
        "red_flags": "tiered pricing obfuscation, long-term contracts with early termination fees, leased terminals",
    },
    "ai automation": {
        "range": "$500–$5,000 setup; $100–$2,000/month ongoing depending on scope",
        "permit": "no permit; data privacy compliance (CCPA in California) required",
        "license": "no license required; verify business registration and references",
        "red_flags": "vague ROI promises, no clear scope of work, monthly fees with no deliverables defined",
    },
}

DEFAULT_DATA = {
    "range": "varies significantly by scope and contractor",
    "permit": "verify with your local city building department",
    "license": "verify contractor license before signing any contract",
    "red_flags": "pressure tactics, no written estimate, large upfront deposits",
}

DECISION_INTRO = {
    "checklist": "Use this checklist before hiring or approving any work.",
    "warning signs": "These warning signs indicate a quote or situation needs closer scrutiny.",
    "cost guide": "Understanding fair cost ranges helps you evaluate any quote more accurately.",
    "second opinion": "Getting a second opinion is almost always worth it for jobs over $500.",
    "common mistakes": "These are the most common and expensive mistakes people make in this situation.",
    "questions to ask": "Ask these questions before signing anything or allowing work to begin.",
    "scam red flags": "These patterns appear in the majority of overcharging and contractor fraud cases.",
    "repair vs replace": "Deciding between repair and replacement involves cost, age, and risk — here is a clear framework.",
}


def slugify(s):
    return re.sub(r"[^a-z0-9-]+", "-", s.lower()).strip("-")


def tc(s):
    return " ".join(w.capitalize() for w in s.split())


def build_page(problem, service, decision, location):
    slug = f"{slugify(service)}-{slugify(problem)}-{slugify(decision)}-{slugify(location)}"
    title = f"{tc(service)} {tc(problem)} — {tc(decision)} · {tc(location)}"
    h1    = f"{tc(service)} {tc(problem)} in {tc(location)}"
    desc  = (f"{tc(decision)} guide for {service} {problem} situations in {tc(location)} — "
             f"plain-language guidance on costs, warning signs, and what to do next.")
    d     = SERVICE_DATA.get(service, DEFAULT_DATA)
    dec_intro = DECISION_INTRO.get(decision, "This guide covers what you need to know.")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <meta name="robots" content="index, follow, max-image-preview:large"/>
  <title>{title} · SideGuy</title>
  <link rel="canonical" href="https://sideguysolutions.com/matrix/{slug}.html"/>
  <meta name="description" content="{desc}"/>
  <meta property="og:title" content="{h1} — {tc(decision)}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:url" content="https://sideguysolutions.com/matrix/{slug}.html"/>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="SideGuy Solutions"/>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "What is a fair cost for {service} in {tc(location)}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Typical range for {service} in {tc(location)}: {d['range']}. Always get at least 2 written quotes and ask for itemized pricing. Text PJ at 773-544-1231 if a quote seems off."
      }}
    }},
    {{
      "@type": "Question",
      "name": "What license should a {service} contractor have in {tc(location)}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{d['license']}. Verify any license before signing a contract."
      }}
    }},
    {{
      "@type": "Question",
      "name": "What are the biggest red flags when dealing with {service} {problem}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "The most common red flags: {d['red_flags']}. If you are seeing any of these, get a second quote before proceeding."
      }}
    }}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"SideGuy","item":"https://sideguysolutions.com"}},
    {{"@type":"ListItem","position":2,"name":"{tc(service)} Guides","item":"https://sideguysolutions.com/matrix/{slugify(service)}-cost-guide-{slugify(location)}.html"}},
    {{"@type":"ListItem","position":3,"name":"{h1}","item":"https://sideguysolutions.com/matrix/{slug}.html"}}
  ]
}}
</script>
<style>
:root{{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--mint2:#00c7ff;--accent:#0a4a6e;--r:22px;--pill:999px;}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;color:var(--ink);background:radial-gradient(1200px 900px at 22% 10%,#ffffff 0%,var(--bg0) 25%,var(--bg1) 60%,#bfeeff 100%);line-height:1.75;-webkit-font-smoothing:antialiased;}}
body:before{{content:"";position:fixed;inset:-20%;background:radial-gradient(closest-side at 18% 20%,rgba(33,211,161,.18),transparent 55%),radial-gradient(closest-side at 78% 28%,rgba(74,169,255,.16),transparent 52%);filter:blur(18px);pointer-events:none;z-index:-2;}}
.topbar{{position:sticky;top:0;z-index:50;padding:12px 14px 8px;display:flex;justify-content:center;pointer-events:none;}}
.homePill{{pointer-events:auto;text-decoration:none;display:inline-flex;align-items:center;gap:10px;padding:10px 16px;border-radius:var(--pill);background:linear-gradient(180deg,rgba(255,255,255,.84),rgba(255,255,255,.62));border:1px solid rgba(7,48,68,.07);box-shadow:0 10px 28px rgba(7,48,68,.08);color:var(--ink);font-weight:700;font-size:12px;backdrop-filter:blur(14px);}}
.dot{{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 0 0 3px rgba(255,255,255,.95);}}
.wrap{{max-width:820px;margin:0 auto;padding:24px 22px 80px;}}
h1{{font-size:2rem;line-height:1.1;margin:8px 0 10px;letter-spacing:-.02em;}}
@media(max-width:520px){{h1{{font-size:1.55rem}}}}
h2{{font-size:1.1rem;color:var(--accent);margin-top:1.8rem;border-bottom:1px solid #c5eef7;padding-bottom:4px;}}
.lede{{font-size:1rem;color:var(--muted);margin-bottom:1.2rem;}}
ul{{padding-left:1.3em;margin:.5rem 0 .9rem;}}li{{margin:.3rem 0;}}
.flag{{background:#fff8e1;border-left:4px solid #f5a623;padding:11px 15px;border-radius:8px;margin:1rem 0;font-size:.93rem;}}
.flag strong{{color:#8a5400;}}
.info{{background:rgba(33,211,161,.09);border-left:4px solid var(--mint);padding:11px 15px;border-radius:8px;margin:1rem 0;font-size:.93rem;}}
table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.88rem;}}
th{{background:rgba(7,48,68,.06);text-align:left;padding:8px 12px;font-weight:700;}}
td{{padding:7px 12px;border-top:1px solid rgba(7,48,68,.07);}}
tr:nth-child(even) td{{background:rgba(255,255,255,.5);}}
.cta-block{{background:linear-gradient(180deg,rgba(33,211,161,.12),rgba(0,199,255,.09));border:1px solid rgba(7,48,68,.09);border-radius:var(--r);padding:18px;margin:1.8rem 0;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;}}
.cta-block .t{{font-weight:800;font-size:.95rem;color:var(--accent);}}
.cta-block .s{{font-size:.83rem;color:var(--muted);margin-top:3px;}}
.btn{{text-decoration:none;display:inline-flex;align-items:center;padding:11px 18px;border-radius:var(--pill);background:linear-gradient(135deg,var(--mint),var(--mint2));color:#fff;font-weight:800;font-size:.84rem;box-shadow:0 12px 30px rgba(0,199,255,.22);white-space:nowrap;}}
nav.bc{{max-width:820px;margin:0 auto;padding:8px 22px;font-size:.8rem;color:var(--muted);display:flex;flex-wrap:wrap;gap:4px;align-items:center;}}
nav.bc a{{color:var(--muted);text-decoration:none;}}nav.bc span{{opacity:.4;margin:0 3px;}}
.related{{display:flex;flex-wrap:wrap;gap:8px;margin:1rem 0;}}
.related a{{display:inline-block;padding:7px 13px;border-radius:var(--pill);border:1px solid rgba(7,48,68,.12);background:rgba(255,255,255,.65);font-size:.81rem;color:var(--ink);text-decoration:none;}}
.floating{{position:fixed;right:18px;bottom:16px;z-index:999;display:flex;align-items:center;gap:10px;}}
.fpill{{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.68);border:1px solid rgba(7,48,68,.08);box-shadow:0 18px 55px rgba(7,48,68,.14);backdrop-filter:blur(14px);min-width:190px;}}
.fpill .t1{{font-weight:900;font-size:12px;color:rgba(7,48,68,.88);display:flex;align-items:center;gap:8px;}}
.cdot{{width:9px;height:9px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));}}
.fpill .t2{{font-size:11px;color:rgba(7,48,68,.62);}}
.forb{{width:54px;height:54px;border-radius:999px;background:radial-gradient(circle at 30% 20%,#ffffff,rgba(33,211,161,.95) 52%,rgba(0,199,255,.95) 100%);border:1px solid rgba(255,255,255,.8);box-shadow:0 0 0 4px rgba(255,255,255,.92),0 22px 60px rgba(0,199,255,.22);text-decoration:none;display:flex;align-items:center;justify-content:center;color:var(--ink);font-weight:900;font-size:11px;animation:pulse 2.2s ease-in-out infinite;}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 4px rgba(255,255,255,.92),0 14px 40px rgba(0,199,255,.22)}}50%{{box-shadow:0 0 0 4px rgba(255,255,255,.92),0 22px 60px rgba(0,199,255,.45)}}}}
footer{{opacity:.6;font-size:.82rem;border-top:1px solid #c5eef7;padding-top:1rem;text-align:center;margin-top:2rem;}}
</style>
</head>
<body>
<a href="#main" style="position:absolute;left:0;top:0;background:#fff;color:#073044;padding:8px 16px;border-radius:8px;z-index:1000;font-size:.8rem;">Skip to content</a>
<div class="topbar"><a class="homePill" href="/index.html"><span class="dot"></span>Back to home</a></div>
<nav class="bc" aria-label="Breadcrumb">
  <a href="/index.html">SideGuy</a><span>/</span>
  <a href="/matrix/{slugify(service)}-cost-guide-{slugify(location)}.html">{tc(service)}</a><span>/</span>
  {tc(problem)} — {tc(decision)}
</nav>
<div class="wrap"><main id="main">
<p style="font-size:.8rem;opacity:.6;margin-bottom:4px;">SideGuy · {tc(location)} · Updated {MONTH}</p>
<h1>{h1}</h1>
<p class="lede">{dec_intro} This guide covers what is fair, what to watch for, and who to call for {service} situations in {tc(location)}.</p>

<h2>The Situation</h2>
<p>When dealing with a {service} {problem} in {tc(location)}, most costly mistakes come from two places: not knowing what fair pricing looks like, and not knowing which questions to ask before work begins. This page exists to fix both of those gaps.</p>
<p>{tc(location)} has a competitive market for {service} contractors, but that range in competition also means a wide range in quality, transparency, and pricing practices. The steps below apply whether you are evaluating a first quote or trying to decide if a current situation is normal.</p>

<h2>Cost Reference ({tc(location)})</h2>
<div class="info">Typical range for {service} in {tc(location)}: <strong>{d['range']}</strong></div>
<table>
  <thead><tr><th>Factor</th><th>What to Know</th></tr></thead>
  <tbody>
    <tr><td>Permit requirements</td><td>{d['permit']}</td></tr>
    <tr><td>Contractor license</td><td>{d['license']}</td></tr>
    <tr><td>Quote minimum</td><td>Get at least 2 written, itemized quotes for any job over $500</td></tr>
    <tr><td>Deposit limits</td><td>10–30% is standard; never pay more than 50% before work begins</td></tr>
  </tbody>
</table>

<h2>{tc(decision)} — Key Points</h2>
<ul>
  <li>Verify the contractor license at the state licensing board before signing</li>
  <li>Ask for a written scope of work with itemized parts and labor</li>
  <li>Confirm permit status — work done without required permits creates liability at resale</li>
  <li>Ask what the warranty covers and get it in writing</li>
  <li>Ask what happens if additional problems are found once work begins</li>
  <li>Compare at least 2 quotes — the spread tells you a lot about what is and isn't included</li>
  <li>Ask for references from similar jobs completed in the last 6 months</li>
  <li>Never let urgency be used as a sales tactic — a legitimate contractor will give you time to decide</li>
</ul>

<div class="cta-block">
  <div>
    <p class="t">Does the quote look right?</p>
    <p class="s">Text PJ — quick read on whether the numbers make sense for {tc(location)}.</p>
  </div>
  <a class="btn" href="sms:+17735441231">📱 Text PJ</a>
</div>

<h2>Red Flags to Watch For</h2>
<div class="flag"><strong>These patterns appear in most overcharging and fraud cases for {service} in {tc(location)}:</strong></div>
<ul>
  <li>{tc(d['red_flags'].split(',')[0].strip())} — this is a common tactic; get a second quote before proceeding</li>
  <li>Quoting over the phone without a site visit or inspection — legitimate contractors inspect first</li>
  <li>No written estimate or contract — never allow work to begin without a signed document</li>
  <li>Request for full or very large deposit before work begins — standard is 10–30% maximum</li>
  <li>Pressure to decide immediately or claims the price increases tomorrow — this is a sales tactic, not reality</li>
  <li>Reluctance to pull required permits — this protects them, not you; insist on permits</li>
</ul>

<h2>Before You Decide — Checklist</h2>
<ul>
  <li>✓ Verified contractor license with the state licensing board</li>
  <li>✓ Confirmed they carry general liability and workers compensation insurance</li>
  <li>✓ Received at least 2 written, itemized quotes</li>
  <li>✓ Confirmed permit requirements with the local building department</li>
  <li>✓ Understood the full scope of work and what is excluded</li>
  <li>✓ Confirmed payment schedule — no more than 30% upfront for most jobs</li>
  <li>✓ Got the warranty terms in writing</li>
</ul>

<h2>Related Guides</h2>
<div class="related">
  <a href="/matrix/{slugify(service)}-quote-too-high-cost-guide-{slugify(location)}.html">{tc(service)} Cost Guide — {tc(location)}</a>
  <a href="/matrix/{slugify(service)}-quote-too-high-scam-red-flags-{slugify(location)}.html">Scam Red Flags</a>
  <a href="/matrix/{slugify(service)}-quote-too-high-questions-to-ask-{slugify(location)}.html">Questions to Ask</a>
  <a href="/matrix/{slugify(service)}-repair-cost-too-high-second-opinion-{slugify(location)}.html">Getting a Second Opinion</a>
  <a href="/index.html">SideGuy Home</a>
</div>

</main></div>
<footer><p>SideGuy Solutions · {tc(location)} · Clarity before cost · Updated {MONTH}</p></footer>
<div class="floating">
  <div class="fpill">
    <span class="t1"><span class="cdot"></span>Text PJ — real answers</span>
    <span class="t2">773-544-1231 · No pressure</span>
  </div>
  <a class="forb" href="sms:+17735441231" aria-label="Text PJ" rel="nofollow">PJ</a>
</div>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Count pages without writing")
    parser.add_argument("--service",  default=None, help="Filter to one service")
    parser.add_argument("--location", default=None, help="Filter to one location")
    args = parser.parse_args()

    problems  = [l.strip() for l in open(PROBLEMS_FILE)  if l.strip()]
    services  = [l.strip() for l in open(SERVICES_FILE)  if l.strip()]
    decisions = [l.strip() for l in open(DECISIONS_FILE) if l.strip()]
    locations = [l.strip() for l in open(LOCATIONS_FILE) if l.strip()]

    if args.service:
        services = [s for s in services if args.service.lower() in s.lower()]
    if args.location:
        locations = [l for l in locations if args.location.lower() in l.lower()]

    total = len(problems) * len(services) * len(decisions) * len(locations)
    print(f"Matrix: {len(problems)} problems × {len(services)} services × "
          f"{len(decisions)} decisions × {len(locations)} locations = {total:,} pages")

    if args.dry_run:
        print("Dry run — no pages written.")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG), exist_ok=True)

    new_urls = []
    count = 0
    for problem in problems:
        for service in services:
            for decision in decisions:
                for location in locations:
                    slug = (f"{slugify(service)}-{slugify(problem)}"
                            f"-{slugify(decision)}-{slugify(location)}")
                    html = build_page(problem, service, decision, location)
                    open(os.path.join(OUTDIR, f"{slug}.html"), "w").write(html)
                    new_urls.append(
                        f"https://sideguysolutions.com/matrix/{slug}.html"
                    )
                    count += 1
                    if count % 500 == 0:
                        print(f"  {count:,}/{total:,} pages written…")

    if os.path.exists(SITEMAP) and new_urls:
        content = open(SITEMAP).read()
        blocks = "\n".join(
            f'<url><loc>{u}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>'
            for u in new_urls
        )
        open(SITEMAP, "w").write(content.replace("</urlset>", blocks + "\n</urlset>", 1))
        print(f"Sitemap updated: +{len(new_urls):,} URLs")

    with open(LOG, "a") as f:
        f.write(f"Build {date.today()}: {count} pages\n")

    print(f"\nPages generated: {count:,}")
    print(f"Output: {OUTDIR}/")


if __name__ == "__main__":
    main()
