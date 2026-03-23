#!/usr/bin/env python3
"""
SIDEGUY GEO EXPANSION — North County
Build 12 unique city-specific decision pages with conversion elements.

4 cities x 3 verticals = 12 pages
Cities: Encinitas, Carlsbad, Oceanside, Escondido
Verticals: HVAC, Payments, AI Automation
"""

import os

PROJECT_ROOT = "/workspaces/sideguy-solutions"
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public", "local")
SMS = "+17735441231"
SMS_PRETTY = "773-544-1231"
DOMAIN = "https://sideguysolutions.com"

# ── City-specific context ───────────────────────────────────────────

CITIES = {
    "encinitas": {
        "name": "Encinitas",
        "vibe": "coastal",
        "detail": "a beach community with older homes near the 101 and newer builds inland toward Olivenhain",
        "hvac": {
            "climate": "coastal humidity and salt air corrode outdoor HVAC units faster than inland San Diego",
            "common_issue": "AC runs but doesn't cool well — salt corrosion on condenser coils is the #1 culprit near the coast",
            "repair_range": "$250–$800 for common repairs; $4,500–$9,000 for full replacement",
            "tip": "If your unit is near the ocean (west of I-5), get a coil inspection yearly — salt damage isn't covered by most warranties",
            "local_note": "Older Encinitas homes (especially near Leucadia and Old Encinitas) often have undersized ductwork from original construction. Before replacing the unit, check if duct sizing is the real problem.",
        },
        "payments": {
            "biz_type": "surf shops, yoga studios, wellness practitioners, and farm-to-table restaurants",
            "pain": "seasonal traffic swings — winter foot traffic drops 30-40% but monthly processing fees don't",
            "tip": "If you're paying a flat monthly fee plus per-transaction costs, you're overpaying in slow months. Ask your processor about seasonal or interchange-plus pricing.",
            "local_note": "Many Encinitas businesses on the 101 corridor still use Square terminals from their startup phase. If you're processing over $8K/month, you've outgrown Square's flat rate.",
        },
        "ai": {
            "biz_type": "wellness practitioners, small studios, and independent professionals",
            "use_case": "automated appointment booking and follow-up texts",
            "tip": "A $50/month scheduling bot can recover 3-5 missed bookings per week. That's $200-500/month in recovered revenue for a yoga studio or massage practice.",
            "local_note": "Encinitas has a high density of solo practitioners who lose clients to no-shows. An automated reminder system pays for itself in the first week.",
        },
    },
    "carlsbad": {
        "name": "Carlsbad",
        "vibe": "suburban-commercial",
        "detail": "a mix of established neighborhoods, the Village, and a growing commercial corridor along Palomar Airport Road",
        "hvac": {
            "climate": "inland Carlsbad (east of El Camino Real) gets 10-15 degrees hotter than the coast in summer",
            "common_issue": "AC runs constantly in July-September — often an oversized or undersized unit for the home's square footage",
            "repair_range": "$300–$900 for diagnostics and repair; $5,000–$11,000 for full system replacement",
            "tip": "Carlsbad has aggressive SDG&E time-of-use rates. A properly sized system with a smart thermostat can cut your summer electric bill by 20-30%",
            "local_note": "The Bressi Ranch and La Costa developments from the early 2000s are hitting the 20-year mark on original HVAC installs. If you're in one of these communities and your system is original, budget for replacement rather than repair.",
        },
        "payments": {
            "biz_type": "restaurants in the Village, retail along Palomar Airport Road, and professional services near the business park",
            "pain": "high tourist-season volume means you're leaving money on the table if your processor charges high rates on card-present transactions",
            "tip": "Carlsbad restaurants processing $20K+ in summer months should negotiate card-present rates separately from card-not-present. The difference is 0.5-1% — that's $100-200/month.",
            "local_note": "The Carlsbad Village restaurant cluster has unique needs — high tip percentages, outdoor POS terminals, and seasonal staff. Make sure your processor handles tip adjustment without extra fees.",
        },
        "ai": {
            "biz_type": "professional services near the Carlsbad business parks and retail in the Village",
            "use_case": "AI-powered lead qualification and automated quote follow-up",
            "tip": "B2B service companies in the Palomar Airport corridor lose 40% of web leads because they respond too slowly. An AI auto-responder that replies in under 2 minutes doubles your close rate.",
            "local_note": "Carlsbad's business park density means you're competing with companies that already have sales automation. If you're still manually following up on form submissions, you're losing to the shop down the street.",
        },
    },
    "oceanside": {
        "name": "Oceanside",
        "vibe": "working-class coastal",
        "detail": "a growing city with military families near Camp Pendleton, a revitalizing downtown, and inland neighborhoods stretching toward Vista",
        "hvac": {
            "climate": "downtown stays mild but inland Oceanside (Mission Mesa, Fire Mountain) gets hot — dual climate zones within one city",
            "common_issue": "military families renting often inherit old or poorly maintained HVAC systems — figure out if it's the landlord's problem or yours before paying",
            "repair_range": "$200–$700 for common repairs; $4,000–$8,500 for replacement",
            "tip": "If you're renting near Camp Pendleton and the AC stops working, California law requires landlords to maintain habitable conditions including heating. Document the problem and notify in writing before paying for repairs yourself.",
            "local_note": "Oceanside has some of the most affordable housing in coastal San Diego, but many homes were built in the 60s-70s with original ductwork. A duct inspection ($150-250) before a unit replacement can save you thousands.",
        },
        "payments": {
            "biz_type": "downtown restaurants, coast highway shops, taco shops, barber shops, and small service businesses",
            "pain": "small transaction sizes ($8-15 average) mean per-transaction fees eat a bigger percentage of revenue",
            "tip": "If your average sale is under $15, per-transaction fees (typically $0.30) matter more than the percentage rate. Look for processors with lower per-transaction costs — it adds up fast at 200+ transactions/day.",
            "local_note": "Oceanside's downtown revitalization is bringing in new food and retail. If you're opening a new spot on Coast Highway or Mission Ave, negotiate your processing rate before you sign — it's easier to get good terms when you're new than to renegotiate later.",
        },
        "ai": {
            "biz_type": "contractors, auto shops, and service businesses",
            "use_case": "automated dispatching, appointment reminders, and review requests",
            "tip": "Oceanside service businesses cover a large geographic area. An AI dispatcher that routes jobs by location can save 30-45 minutes per tech per day in drive time.",
            "local_note": "With Camp Pendleton turnover, Oceanside service businesses get constant new-customer inquiries. An AI chatbot on your website that captures name, address, and service needed — then texts you — converts 3x more than a contact form.",
        },
    },
    "escondido": {
        "name": "Escondido",
        "vibe": "inland suburban",
        "detail": "an inland city with hot summers, a growing downtown, and a mix of residential neighborhoods from older ranch properties to newer developments",
        "hvac": {
            "climate": "Escondido regularly hits 95-105°F in summer — this is real heat, not coastal 80s. Your HVAC works harder here than anywhere else in the county",
            "common_issue": "system can't keep up on triple-digit days — often means the unit is undersized for the heat load or refrigerant is low",
            "repair_range": "$300–$900 for repairs; $5,500–$12,000 for replacement (higher end because of heat load requirements)",
            "tip": "In Escondido heat, a 2-ton unit in a 2,000 sq ft home won't cut it. You likely need 3.5-4 tons. If a contractor quotes replacement, make sure they do a Manual J load calculation — not just matching the old unit's size.",
            "local_note": "Escondido's older homes near downtown often have no insulation in the attic. Adding blown-in insulation ($1,500-2,500) can reduce your cooling costs by 25-40% and extend your HVAC system's life by years.",
        },
        "payments": {
            "biz_type": "auto shops on Auto Park Way, restaurants on Grand Avenue, and agricultural businesses",
            "pain": "high-ticket automotive repairs ($1,000-5,000) mean even small percentage differences in processing fees cost real money",
            "tip": "Auto shops processing $50K+/month should be on interchange-plus pricing, not flat rate. The difference on a $3,000 repair bill is $30-45 per transaction.",
            "local_note": "Escondido's auto repair corridor has unique processing needs — split payments, fleet accounts, and warranty billing. Make sure your processor handles these without surcharges.",
        },
        "ai": {
            "biz_type": "auto repair shops, dental offices, and property management companies",
            "use_case": "automated appointment scheduling, service reminders, and invoice follow-up",
            "tip": "Escondido dental offices lose an average of 8-12 appointments per month to no-shows. A $75/month automated reminder system (text + email 24h and 2h before) cuts no-shows by 60%.",
            "local_note": "Property management companies in Escondido managing 50+ units can automate maintenance request intake, vendor dispatch, and tenant communication. This replaces 15-20 hours/week of admin work.",
        },
    },
}

VERTICALS = {
    "hvac": {
        "slug_suffix": "hvac-repair-or-replace",
        "title_template": "HVAC Repair vs Replace in {city} — What to Actually Do",
        "meta_template": "Not sure whether to repair or replace your HVAC in {city}? Real costs, local factors, and a human to text before you decide.",
        "h2_sections": ["The Real Question", "Local Climate Factor", "Cost Reality", "When to Repair", "When to Replace", "What Most People Get Wrong"],
    },
    "payments": {
        "slug_suffix": "payment-processing-fees",
        "title_template": "Payment Processing Fees Too High in {city}? Here's What to Do",
        "meta_template": "If you're a {city} business paying too much in processing fees, here's how to fix it — real numbers, no sales pitch.",
        "h2_sections": ["Are You Actually Overpaying?", "Who This Hits Hardest in {city}", "The Real Cost Breakdown", "What to Ask Your Processor", "When to Switch", "When to Stay"],
    },
    "ai": {
        "slug_suffix": "ai-automation-worth-it",
        "title_template": "Is AI Automation Worth It for {city} Businesses?",
        "meta_template": "Honest breakdown of AI automation costs and ROI for {city} small businesses. No hype, real numbers.",
        "h2_sections": ["The Honest Answer", "Where AI Actually Helps in {city}", "Real Costs", "What to Try First", "What to Skip", "The Bottom Line"],
    },
}


def build_page(city_key, vertical_key):
    city = CITIES[city_key]
    vert = VERTICALS[vertical_key]
    data = city[vertical_key]

    slug = f"{city_key}-{vert['slug_suffix']}"
    title = vert["title_template"].format(city=city["name"])
    meta_desc = vert["meta_template"].format(city=city["name"])
    canonical = f"{DOMAIN}/public/local/{slug}.html"

    # Build the page content based on vertical
    if vertical_key == "hvac":
        body_content = _build_hvac_content(city, data)
    elif vertical_key == "payments":
        body_content = _build_payments_content(city, data)
    else:
        body_content = _build_ai_content(city, data)

    # Related pages for interlinks
    other_cities = [c for c in CITIES if c != city_key]
    related_links = []
    for oc in other_cities:
        oc_name = CITIES[oc]["name"]
        related_links.append(f'<li><a href="/public/local/{oc}-{vert["slug_suffix"]}.html">{vert["title_template"].format(city=oc_name)}</a></li>')

    # Cross-vertical links for this city
    other_verts = [v for v in VERTICALS if v != vertical_key]
    for ov in other_verts:
        ov_title = VERTICALS[ov]["title_template"].format(city=city["name"])
        related_links.append(f'<li><a href="/public/local/{city_key}-{VERTICALS[ov]["slug_suffix"]}.html">{ov_title}</a></li>')

    # San Diego hub links
    if vertical_key == "hvac":
        related_links.append('<li><a href="/public/authority/hvac.html">HVAC Authority Hub</a></li>')
        related_links.append('<li><a href="/public/money-pages/hvac-repair-or-replace.html">HVAC Repair or Replace (San Diego)</a></li>')
    elif vertical_key == "payments":
        related_links.append('<li><a href="/public/authority/payments.html">Payments Authority Hub</a></li>')
        related_links.append('<li><a href="/public/money-pages/should-i-switch-payment-processor.html">Should I Switch Processor?</a></li>')
    else:
        related_links.append('<li><a href="/public/authority/ai.html">AI Authority Hub</a></li>')
        related_links.append('<li><a href="/public/auto-pages/ai-receptionist-cost-comparison.html">AI Receptionist Cost Comparison</a></li>')

    interlinks_html = "\n    ".join(related_links)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} · SideGuy Solutions</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{canonical}">

  <style>
    :root {{
      --bg0: #eefcff;
      --ink: #073044;
      --mint: #21d3a1;
      --muted: #3f6173;
    }}
    body {{
      font-family: -apple-system, system-ui, Inter, sans-serif;
      background: radial-gradient(ellipse at 20% 40%, #b8f4f0 0%, #d6f5ff 35%, #eefcff 70%, #fff8f0 100%);
      color: var(--ink);
      min-height: 100vh;
      margin: 0;
      padding: 0;
    }}
    main {{
      max-width: 780px;
      margin: 0 auto;
      padding: 0 20px 60px;
    }}
    h1 {{
      font-size: clamp(1.6rem, 4vw, 2.2rem);
      line-height: 1.25;
      margin: 0 0 8px;
    }}
    h2 {{
      font-size: 1.25rem;
      margin: 32px 0 8px;
      color: var(--ink);
    }}
    p, li {{
      line-height: 1.65;
      color: var(--muted);
      font-size: 1.05rem;
    }}
    .cost-callout {{
      background: #fff;
      border-left: 4px solid var(--mint);
      padding: 16px 20px;
      border-radius: 0 10px 10px 0;
      margin: 16px 0;
      font-size: 1.05rem;
    }}
    .local-tip {{
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 10px;
      padding: 16px 20px;
      margin: 16px 0;
    }}
    .local-tip strong {{
      color: #92400e;
    }}
  </style>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "SideGuy Solutions",
    "url": "https://sideguysolutions.com",
    "telephone": "+1-773-544-1231",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{city['name']}",
      "addressRegion": "CA",
      "addressCountry": "US"
    }},
    "areaServed": "{city['name']}, CA"
  }}
  </script>

  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="SideGuy Solutions"/>
  <meta property="og:title" content="{title} · SideGuy Solutions"/>
  <meta property="og:description" content="{meta_desc}"/>
  <meta property="og:url" content="{canonical}"/>
  <meta name="twitter:card" content="summary"/>
  <meta name="twitter:title" content="{title} · SideGuy Solutions"/>
  <meta name="twitter:description" content="{meta_desc}"/>
</head>
<body>

<!-- sideguy-conversion-upgrade: top-banner -->
<div id="sg-top-banner" style="
  background: linear-gradient(90deg, #073044, #0f4c63);
  color: #eaf6ff;
  padding: 12px 16px;
  text-align: center;
  font-family: -apple-system, system-ui, Inter, sans-serif;
  font-size: 0.95rem;
">
  Not sure what to do? A real human answers in minutes&nbsp;&rarr;&nbsp;
  <a href="sms:{SMS}" style="color: #21d3a1; font-weight: 600; text-decoration: none; border-bottom: 1px solid #21d3a180;">Text PJ ({SMS_PRETTY})</a>
</div>

<main>
  <p style="margin: 24px 0 8px;"><a href="/index.html" style="color: var(--muted); text-decoration: none;">&larr; Back to Home</a></p>
  <h1>{title}</h1>

{body_content}

  <!-- sideguy-conversion-upgrade: trust-block -->
  <div id="sg-trust-block" style="
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 24px 20px;
    margin: 32px 0;
    line-height: 1.6;
  ">
    <p style="font-size: 1.1rem; font-weight: 600; margin: 0 0 8px; color: var(--ink);">
      Still not sure?
    </p>
    <p style="margin: 0 0 12px; color: var(--muted);">
      Text PJ your situation &mdash; get a straight answer in minutes.
      No sales pitch. Just clarity.
    </p>
    <a href="sms:{SMS}" style="
      display: inline-block;
      padding: 10px 18px;
      background: #10b981;
      color: white;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
    ">Text PJ Now</a>
  </div>

  <!-- sideguy-interlinks -->
  <div style="margin: 32px 0; padding: 16px 20px; border-radius: 12px; background: #f1f5f9; border: 1px solid #e2e8f0;">
    <h3 style="margin: 0 0 12px; font-size: 1.1rem; color: var(--ink);">Related Decisions</h3>
    <ul style="margin: 0; padding: 0 0 0 20px; line-height: 1.8;">
      {interlinks_html}
    </ul>
  </div>

</main>

<!-- sideguy-conversion-upgrade: sticky-button -->
<div id="sg-sticky-cta" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
  <a href="sms:{SMS}" style="
    display: flex; align-items: center; gap: 8px;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white; padding: 14px 20px; border-radius: 999px;
    font-weight: 700; font-size: 0.95rem; text-decoration: none;
    box-shadow: 0 4px 24px rgba(16, 185, 129, 0.5);
    font-family: -apple-system, system-ui, Inter, sans-serif;
  ">&#x1F4AC; Text PJ</a>
</div>

</body>
</html>"""

    return slug, html


def _build_hvac_content(city, data):
    return f"""
  <p>{city['name']} is {city['detail']}. When your HVAC stops working here, the decision matters.</p>

  <h2>The Real Question</h2>
  <p>You're not really asking "should I repair or replace?" You're asking "am I about to waste money?" That's the right question.</p>

  <h2>Why {city['name']} Is Different</h2>
  <p>{data['climate']}.</p>
  <p><strong>Most common issue:</strong> {data['common_issue']}.</p>

  <div class="cost-callout">
    <strong>Cost reality in {city['name']}:</strong> {data['repair_range']}.
  </div>

  <h2>When to Repair</h2>
  <ul>
    <li>System is under 10 years old</li>
    <li>Problem is isolated (one component, not systemic)</li>
    <li>Repair cost is less than 40% of replacement cost</li>
    <li>No strange smells, no refrigerant leaks, no electrical issues</li>
  </ul>

  <h2>When to Replace</h2>
  <ul>
    <li>System is 15+ years old</li>
    <li>You've had 2+ repairs in the past 12 months</li>
    <li>Energy bills keep climbing despite maintenance</li>
    <li>System uses R-22 refrigerant (phased out — refills are expensive)</li>
  </ul>

  <h2>Pro Tip for {city['name']}</h2>
  <p>{data['tip']}.</p>

  <div class="local-tip">
    <strong>{city['name']} local note:</strong> {data['local_note']}
  </div>

  <h2>What Most People Get Wrong</h2>
  <p>They get one quote and panic. Get two opinions minimum. A good HVAC company will explain what's wrong without pressuring you to replace. If someone shows up and immediately says "you need a whole new system" without running diagnostics, get a second opinion.</p>
"""


def _build_payments_content(city, data):
    return f"""
  <p>If you run a business in {city['name']}, you're probably paying more in credit card processing fees than you need to. Most business owners don't realize it because the statements are designed to be confusing.</p>

  <h2>Are You Actually Overpaying?</h2>
  <p>Quick test: look at your last monthly statement. Divide total fees by total volume. If you're above 3.0% effective rate, you're almost certainly overpaying. Above 3.5%, you're definitely overpaying.</p>

  <h2>Who This Hits Hardest in {city['name']}</h2>
  <p>{city['name']} has a concentration of {data['biz_type']}. The common pain point: {data['pain']}.</p>

  <div class="cost-callout">
    <strong>Quick math:</strong> On $15,000/month in processing, a 0.5% reduction saves you $75/month — $900/year. On $50,000/month, that's $3,000/year.
  </div>

  <h2>What to Do About It</h2>
  <p>{data['tip']}</p>

  <h2>When to Switch Processors</h2>
  <ul>
    <li>Your effective rate is above 3.2% on card-present transactions</li>
    <li>You're in a multi-year contract with early termination fees</li>
    <li>Your processor doesn't offer interchange-plus pricing</li>
    <li>You're paying monthly minimums that exceed your actual fees</li>
  </ul>

  <h2>When to Stay</h2>
  <ul>
    <li>Your effective rate is under 2.8%</li>
    <li>You're month-to-month with no contract</li>
    <li>The processor integrates well with your POS and accounting</li>
    <li>Support actually answers your calls</li>
  </ul>

  <div class="local-tip">
    <strong>{city['name']} local note:</strong> {data['local_note']}
  </div>

  <h2>What Most People Get Wrong</h2>
  <p>They switch processors for a lower advertised rate without reading the fee schedule. The "1.5%" rate doesn't include interchange, assessments, PCI fees, batch fees, or statement fees. Always compare total effective rate, not the headline number.</p>
"""


def _build_ai_content(city, data):
    return f"""
  <p>If you run a small business in {city['name']}, you've probably seen AI tools advertised everywhere. The honest answer: some of it is genuinely useful, and a lot of it is premature hype. Here's how to tell the difference.</p>

  <h2>The Honest Answer</h2>
  <p>AI automation is worth it when it solves a specific, repeated problem that's costing you time or money right now. It's not worth it when you're buying a solution for a problem you don't actually have.</p>

  <h2>Where AI Actually Helps in {city['name']}</h2>
  <p>{city['name']} has a lot of {data['biz_type']}. The highest-ROI use case: {data['use_case']}.</p>

  <div class="cost-callout">
    <strong>Real numbers:</strong> {data['tip']}
  </div>

  <h2>What to Try First (Low Risk)</h2>
  <ul>
    <li>Automated appointment reminders — $30-75/month, works immediately</li>
    <li>AI-powered review request follow-ups — $20-50/month</li>
    <li>Basic chatbot for FAQ on your website — $0-50/month</li>
    <li>Automated invoice reminders — most accounting software includes this free</li>
  </ul>

  <h2>What to Skip (For Now)</h2>
  <ul>
    <li>"Full AI transformation" packages ($5K+ setup) — you don't need this yet</li>
    <li>Custom-built AI agents — unless you're processing 500+ interactions/month</li>
    <li>AI-generated content for your website — Google's getting better at detecting it</li>
    <li>Any vendor who won't let you try before you buy</li>
  </ul>

  <div class="local-tip">
    <strong>{city['name']} local note:</strong> {data['local_note']}
  </div>

  <h2>The Bottom Line</h2>
  <p>Start with one automation that solves your biggest time drain. Run it for 30 days. Measure the result. If it works, add another. If it doesn't, cancel and try something else. The right approach is incremental, not transformational.</p>
"""


def main():
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    print("━" * 50)
    print("⚡ SIDEGUY GEO EXPANSION — North County")
    print("━" * 50)
    print()

    created = 0
    skipped = 0

    for city_key in CITIES:
        for vert_key in VERTICALS:
            slug, html = build_page(city_key, vert_key)
            filepath = os.path.join(PUBLIC_DIR, f"{slug}.html")

            if os.path.exists(filepath):
                # Check if it's a stub (under 500 bytes = placeholder)
                size = os.path.getsize(filepath)
                if size > 500:
                    print(f"  ⏭  Exists (real content): {slug}.html ({size}b)")
                    skipped += 1
                    continue
                else:
                    print(f"  ↻  Replacing stub: {slug}.html ({size}b → full page)")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"  ✅ Created: {slug}.html")
            created += 1

    print()
    print("━" * 50)
    print(f"  ✅ Created: {created}")
    print(f"  ⏭  Skipped: {skipped}")
    print("━" * 50)
    print()
    print("Pages include:")
    print("  • City-specific content (not templates)")
    print("  • Local tips and cost ranges")
    print("  • Conversion elements (banner + trust + sticky)")
    print("  • Cross-city and cross-vertical interlinks")
    print("  • Schema.org + OG metadata")


if __name__ == "__main__":
    main()
