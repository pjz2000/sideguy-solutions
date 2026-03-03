#!/usr/bin/env python3
"""
SHIP-017: Link Equity Routing + Breadcrumb Schema + Help Hub QR Directory

Phase 1 — Inject trade-specific quote-review CTAs into 9 hub/service pages
           (roofing, hvac, plumbing, electrical, solar hubs + ac-not-cooling,
            ac-repair, roof-repair, general-contractor)
Phase 2 — Add BreadcrumbList JSON-LD to all 46 quote-review pages (16 SD + 30 city)
Phase 3 — Inject full QR directory section into san-diego-help-hub.html
Phase 4 — Fix sitemap.html missing meta description
"""

import os, re, glob

ROOT = "/workspaces/sideguy-solutions"
BASE_URL = "https://sideguysolutions.com"
MESH = "<!-- SIDEGUY_MESH_BLOCK -->"
GUARD = "SHIP-017"

# ---------------------------------------------------------------------------
# PHASE 1 — TRADE HUB / SERVICE PAGE → QUOTE REVIEW CTA INJECTION
# ---------------------------------------------------------------------------

# Map: page filename → (quote_review_slug, trade_label, cta_copy)
HUB_TARGETS = {
    "roofing-hub-san-diego.html": [
        ("roof-repair-quote-review-san-diego.html",
         "Roof Repair Quote Review",
         "Before you sign any roofing contract, use our free quote review checklist. "
         "Learn what's fair pricing, what permits are required, and the red flags that "
         "signal an inflated or incomplete bid."),
        ("roofing-project-quote-review-san-diego.html",
         "Full Roofing Project Quote Review",
         "Planning a full re-roof? Our checklist covers scope verification, material "
         "grades, disposal fees, and how to compare bids on equal footing."),
    ],
    "hvac-problems-hub-san-diego.html": [
        ("hvac-project-quote-review-san-diego.html",
         "HVAC Project Quote Review",
         "Getting quotes for a new system, replacement, or major repair? Our HVAC "
         "quote review checklist walks you through SEER ratings, permit requirements, "
         "what labor should cost, and the line items that inflate bids."),
    ],
    "plumbing-problems-hub-san-diego.html": [
        ("plumbing-project-quote-review-san-diego.html",
         "Plumbing Project Quote Review",
         "Plumbing quotes vary wildly in San Diego. Our checklist helps you verify "
         "scope, check permit requirements, and identify bids that are missing work "
         "or padding margins."),
    ],
    "electrical-problems-hub-san-diego.html": [
        ("electrical-project-quote-review-san-diego.html",
         "Electrical Project Quote Review",
         "Electrical scope can be unclear for homeowners. Use our checklist to "
         "understand panel upgrades, permit requirements, and how to compare quotes "
         "from licensed San Diego electricians."),
    ],
    "solar-hub-san-diego.html": [
        ("solar-project-quote-review-san-diego.html",
         "Solar Project Quote Review",
         "Solar quotes are notoriously hard to compare. Our checklist covers kW sizing, "
         "inverter types, interconnection timelines, and the hidden fees that inflate "
         "the cost of going solar in San Diego."),
    ],
    "ac-not-cooling-san-diego.html": [
        ("hvac-project-quote-review-san-diego.html",
         "HVAC Quote Review Checklist",
         "If your AC diagnosis leads to a repair or replacement quote, don't sign "
         "before reviewing. Our HVAC quote checklist helps you verify the scope and "
         "spot inflated line items."),
    ],
    "ac-repair-san-diego.html": [
        ("hvac-project-quote-review-san-diego.html",
         "Before You Sign an AC Repair Quote",
         "AC repair quotes in San Diego range from fair to $800 over market. "
         "Use our free HVAC quote review checklist to verify what you're being charged "
         "and what should be included."),
    ],
    "roof-repair-san-diego.html": [
        ("roof-repair-quote-review-san-diego.html",
         "Roof Repair Quote Review",
         "Got a roofing quote? Before you approve anything, run it through our "
         "checklist. Know what fair pricing looks like, what permits are required, "
         "and what red flags to watch for in San Diego roofing bids."),
    ],
    "general-contractor-san-diego.html": [
        ("contractor-project-quote-review-san-diego.html",
         "General Contractor Quote Review",
         "General contractor quotes are the hardest to verify. Our checklist covers "
         "scope clarity, subcontractor cost pass-through, markup standards, and the "
         "CSLB license checks every San Diego homeowner should do before signing."),
    ],
}

def build_cta_block(entries):
    """Build a quote-review CTA section with one or more trade links."""
    items_html = []
    for slug, label, description in entries:
        items_html.append(f"""    <div style="background:#fff;border:1px solid #c8eee7;border-radius:8px;padding:1.2rem 1.4rem;margin-bottom:0.8rem;">
      <p style="margin:0 0 0.4rem;font-weight:600;color:var(--ink);">
        <a href="/{slug}" style="color:var(--ink);text-decoration:none;">→ {label}</a>
      </p>
      <p style="margin:0;font-size:0.92rem;color:var(--muted);">{description}</p>
    </div>""")
    items_joined = "\n".join(items_html)
    return f"""
  <!-- {GUARD}: QR CTA block — injected 2026-03-03 -->
  <section style="margin:2.5rem 0;padding:1.5rem;background:#eefcff;border-left:5px solid #21d3a1;border-radius:0 8px 8px 0;">
    <h2 style="font-size:1.1rem;margin:0 0 1rem;color:var(--ink);">Before You Hire — Free Quote Review</h2>
{items_joined}
  </section>
  <!-- /{GUARD} -->

  {MESH}"""

phase1_updated = 0
phase1_skip = 0

for fname, entries in HUB_TARGETS.items():
    fp = os.path.join(ROOT, fname)
    if not os.path.isfile(fp):
        print(f"  [WARN] missing {fname}")
        continue

    with open(fp) as f:
        content = f.read()

    if GUARD in content:
        phase1_skip += 1
        continue

    if MESH not in content:
        print(f"  [WARN] no MESH_BLOCK in {fname}")
        continue

    block = build_cta_block(entries)
    content = content.replace(f"  {MESH}", block, 1)
    if MESH in content and f"  {MESH}" not in content:
        content = content.replace(MESH, block.replace(f"  {MESH}", MESH), 1)

    with open(fp, "w") as f:
        f.write(content)
    labels = ", ".join(e[1] for e in entries)
    print(f"  [qr-cta] {fname} → {labels}")
    phase1_updated += 1

print(f"\nPhase 1 done — {phase1_updated} pages updated, {phase1_skip} already done\n")

# ---------------------------------------------------------------------------
# PHASE 2 — BREADCRUMB JSON-LD ON ALL 46 QUOTE-REVIEW PAGES
# ---------------------------------------------------------------------------

QR_HUB_URL = f"{BASE_URL}/contractor-services-hub-san-diego.html"
QR_HUB_NAME = "San Diego Contractor Quote Reviews"

def get_qr_pages():
    """Return list of (filepath, is_city_variant, trade_key, city_key_or_None)"""
    pages = []
    # SD pages
    for fp in glob.glob(os.path.join(ROOT, "*-quote-review-san-diego.html")):
        fname = os.path.basename(fp)
        trade_key = fname.replace("-quote-review-san-diego.html", "")
        pages.append((fp, False, trade_key, None))
    # City pages (pattern: *-quote-review-{city}.html but NOT -san-diego)
    for fp in glob.glob(os.path.join(ROOT, "*-quote-review-*.html")):
        fname = os.path.basename(fp)
        if fname.endswith("-quote-review-san-diego.html"):
            continue
        # Extract trade and city
        m = re.match(r"^(.+)-quote-review-(.+)\.html$", fname)
        if m:
            trade_key = m.group(1)
            city_key = m.group(2)
            pages.append((fp, True, trade_key, city_key))
    return pages

def trade_label(trade_key):
    labels = {
        "garage-door": "Garage Door",
        "kitchen-remodel": "Kitchen Remodel",
        "roof-repair": "Roof Repair",
        "window-replacement": "Window Replacement",
        "stucco-repair": "Stucco Repair",
        "pool-installation": "Pool Installation",
        "adu-project": "ADU Project",
        "roofing-project": "Roofing Project",
        "solar-project": "Solar Project",
        "hvac-project": "HVAC Project",
        "plumbing-project": "Plumbing Project",
        "electrical-project": "Electrical Project",
        "painting-project": "Painting Project",
        "landscaping": "Landscaping",
        "foundation": "Foundation",
        "contractor-project": "Contractor Project",
    }
    return labels.get(trade_key, trade_key.replace("-", " ").title())

def city_label(city_key):
    labels = {
        "carlsbad": "Carlsbad",
        "encinitas": "Encinitas",
        "oceanside": "Oceanside",
        "la-jolla": "La Jolla",
        "chula-vista": "Chula Vista",
    }
    return labels.get(city_key, city_key.replace("-", " ").title())

def build_breadcrumb_sd(trade_key):
    fname = f"{trade_key}-quote-review-san-diego.html"
    tl = trade_label(trade_key)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": QR_HUB_NAME, "item": QR_HUB_URL},
            {"@type": "ListItem", "position": 3, "name": f"{tl} Quote Review — San Diego",
             "item": f"{BASE_URL}/{fname}"}
        ]
    }

def build_breadcrumb_city(trade_key, city_key):
    sd_fname = f"{trade_key}-quote-review-san-diego.html"
    city_fname = f"{trade_key}-quote-review-{city_key}.html"
    tl = trade_label(trade_key)
    cl = city_label(city_key)
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": QR_HUB_NAME, "item": QR_HUB_URL},
            {"@type": "ListItem", "position": 3, "name": f"{tl} Quote Review — San Diego",
             "item": f"{BASE_URL}/{sd_fname}"},
            {"@type": "ListItem", "position": 4, "name": f"{tl} Quote Review — {cl}",
             "item": f"{BASE_URL}/{city_fname}"}
        ]
    }

import json

qr_pages = get_qr_pages()
phase2_updated = 0
phase2_skip = 0

for fp, is_city, trade_key, city_key in qr_pages:
    with open(fp) as f:
        content = f.read()

    if '"BreadcrumbList"' in content:
        phase2_skip += 1
        continue

    # Build schema
    if is_city:
        schema = build_breadcrumb_city(trade_key, city_key)
    else:
        schema = build_breadcrumb_sd(trade_key)

    schema_block = '\n<script type="application/ld+json">\n' + json.dumps(schema, indent=2) + '\n</script>'

    # Inject before </body>
    if "</body>" in content:
        content = content.replace("</body>", schema_block + "\n</body>", 1)
        with open(fp, "w") as f:
            f.write(content)
        phase2_updated += 1
    else:
        print(f"  [WARN] no </body> in {os.path.basename(fp)}")

print(f"Phase 2 done — {phase2_updated} BreadcrumbList schemas added, {phase2_skip} already had breadcrumbs\n")

# ---------------------------------------------------------------------------
# PHASE 3 — SAN DIEGO HELP HUB: FULL QR DIRECTORY SECTION
# ---------------------------------------------------------------------------

help_hub = os.path.join(ROOT, "san-diego-help-hub.html")
with open(help_hub) as f:
    hub_content = f.read()

if GUARD in hub_content:
    print("Phase 3 skipped — QR directory already in san-diego-help-hub.html\n")
else:
    # All 16 SD QR pages with labels
    SD_QR_PAGES = [
        ("garage-door-quote-review-san-diego.html", "Garage Door Quote Review"),
        ("kitchen-remodel-quote-review-san-diego.html", "Kitchen Remodel Quote Review"),
        ("roof-repair-quote-review-san-diego.html", "Roof Repair Quote Review"),
        ("window-replacement-quote-review-san-diego.html", "Window Replacement Quote Review"),
        ("stucco-repair-quote-review-san-diego.html", "Stucco Repair Quote Review"),
        ("pool-installation-quote-review-san-diego.html", "Pool Installation Quote Review"),
        ("adu-project-quote-review-san-diego.html", "ADU Project Quote Review"),
        ("roofing-project-quote-review-san-diego.html", "Full Roofing Project Quote Review"),
        ("solar-project-quote-review-san-diego.html", "Solar Project Quote Review"),
        ("hvac-project-quote-review-san-diego.html", "HVAC Project Quote Review"),
        ("plumbing-project-quote-review-san-diego.html", "Plumbing Project Quote Review"),
        ("electrical-project-quote-review-san-diego.html", "Electrical Project Quote Review"),
        ("painting-project-quote-review-san-diego.html", "Painting Project Quote Review"),
        ("landscaping-quote-review-san-diego.html", "Landscaping Quote Review"),
        ("foundation-quote-review-san-diego.html", "Foundation Work Quote Review"),
        ("contractor-project-quote-review-san-diego.html", "General Contractor Quote Review"),
    ]

    link_items = "\n".join(
        f'      <li><a href="/{slug}">{label}</a></li>'
        for slug, label in SD_QR_PAGES
    )

    qr_section = f"""
  <!-- {GUARD}: QR Directory — injected 2026-03-03 -->
  <section style="margin:2.5rem 0;padding:1.8rem;background:#eefcff;border-left:5px solid #21d3a1;border-radius:0 8px 8px 0;">
    <h2 style="font-size:1.15rem;margin:0 0 0.6rem;color:var(--ink);">Free Quote Review Checklists — San Diego</h2>
    <p style="font-size:0.93rem;color:var(--muted);margin:0 0 1rem;">
      Getting a contractor quote? These free checklists cover fair pricing, red flags,
      permit requirements, and CSLB license verification for every major home project.
    </p>
    <ul style="list-style:none;padding:0;margin:0;columns:2;column-gap:2rem;line-height:2;">
{link_items}
    </ul>
  </section>
  <!-- /{GUARD} -->

  {MESH}"""

    hub_content = hub_content.replace(f"  {MESH}", qr_section, 1)
    if MESH in hub_content and f"  {MESH}" not in hub_content:
        hub_content = hub_content.replace(MESH, qr_section.replace(f"  {MESH}", MESH), 1)

    with open(help_hub, "w") as f:
        f.write(hub_content)
    print(f"Phase 3 done — san-diego-help-hub.html → 16 QR links injected\n")

# ---------------------------------------------------------------------------
# PHASE 4 — FIX sitemap.html MISSING META DESCRIPTION
# ---------------------------------------------------------------------------

sitemap_html = os.path.join(ROOT, "sitemap.html")
with open(sitemap_html) as f:
    sm_content = f.read()

META_DESC = '<meta name="description" content="Complete index of all SideGuy Solutions pages — HVAC, plumbing, electrical, roofing, payments, AI automation, and contractor quote reviews for San Diego.">'

if 'name="description"' in sm_content:
    print("Phase 4 skipped — sitemap.html already has meta description\n")
else:
    if "</head>" in sm_content:
        sm_content = sm_content.replace("</head>", f"  {META_DESC}\n</head>", 1)
        with open(sitemap_html, "w") as f:
            f.write(sm_content)
        print("Phase 4 done — sitemap.html meta description added\n")
    else:
        print("Phase 4 WARN — no </head> in sitemap.html\n")

# ---------------------------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------------------------
print("=" * 60)
print("SHIP-017 COMPLETE")
print(f"  Phase 1: {phase1_updated} hub/service pages → QR CTAs injected")
print(f"  Phase 2: {phase2_updated} quote-review pages → BreadcrumbList schema")
print(f"  Phase 3: san-diego-help-hub.html → 16-link QR directory")
print(f"  Phase 4: sitemap.html → meta description fixed")
print("=" * 60)
