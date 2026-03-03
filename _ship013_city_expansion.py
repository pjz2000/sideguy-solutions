#!/usr/bin/env python3
"""SHIP-013: North County Quote Review City Expansion
Creates 5 × 6 = 30 city-variant pages from SD originals.
"""
import os, glob, json

ROOT = "/workspaces/sideguy-solutions"

CITIES = {
    "carlsbad": {
        "name": "Carlsbad",
        "permit_authority": "City of Carlsbad Building Division (760-602-2700)",
        "permit_url": "https://www.carlsbadca.gov/business/permits-licenses/building-permits",
        "intro_flavor": "coastal climate with marine exposure that accelerates wear on exterior materials",
        "price_adj": 1.04,  # +4%
        "note": "Carlsbad's Coastal Zone designation adds an additional layer of permit review for exterior and structural work — projects within the Coastal Zone require a Coastal Development Permit in addition to standard building permits. Your contractor should flag this at the proposal stage.",
    },
    "encinitas": {
        "name": "Encinitas",
        "permit_authority": "City of Encinitas Development Services Division (760-633-2600)",
        "permit_url": "https://www.encinitasca.gov/government/departments/development-services",
        "intro_flavor": "bluff-top and canyon-adjacent properties with soil stability considerations",
        "price_adj": 1.05,  # +5%
        "note": "Encinitas has significant hillside and bluff-top inventory. Projects involving grading, retaining walls, or work near slopes require a geotechnical report and may trigger additional review from the Encinitas Grading and Drainage Division.",
    },
    "oceanside": {
        "name": "Oceanside",
        "permit_authority": "City of Oceanside Development Services — Building Division (760-435-3920)",
        "permit_url": "https://www.ci.oceanside.ca.us/gov/dev/building/default.asp",
        "intro_flavor": "diverse mix of post-war inventory and newer coastal development",
        "price_adj": 0.97,  # -3%
        "note": "Oceanside's Building Division processes permits through a standard counter-permit and plan-check pathway. Many residential trade permits (mechanical, electrical, plumbing) can be issued over the counter. Structural and remodel permits require plan check, which typically runs 6–15 business days.",
    },
    "la-jolla": {
        "name": "La Jolla",
        "permit_authority": "City of San Diego DSD — La Jolla permit area (619-446-5000)",
        "permit_url": "https://www.sandiegoca.gov/dsd",
        "intro_flavor": "high-value coastal properties with premium contractor demand and corresponding pricing pressure",
        "price_adj": 1.08,  # +8%
        "note": "La Jolla falls within the City of San Diego jurisdiction and uses the San Diego DSD permit process. However, many properties have HOA overlay requirements, historical review for homes in designated historical areas, and coastal zone permit requirements that add review time and cost above standard San Diego permits.",
    },
    "chula-vista": {
        "name": "Chula Vista",
        "permit_authority": "City of Chula Vista Development Services Department — Building Division (619-476-5370)",
        "permit_url": "https://www.chulavistaca.gov/departments/development-services/building-division",
        "intro_flavor": "rapidly growing south county market with newer master-planned communities and aging Otay Ranch inventory",
        "price_adj": 0.96,  # -4%
        "note": "Chula Vista's Building Division handles permits for both the western, older neighborhoods and the newer Eastlake and Otay Ranch developments. Newer tract homes often have HOA architectural approval requirements that run parallel to the city permit process — confirm with your HOA before signing a contract.",
    },
}

TRADES = {
    "garage-door": {
        "label": "Garage Door",
        "title_tag": "Spring, Opener &amp; Door Bids Reviewed",
        "lede_sd": "review the bid, flag upsell patterns, and check if the spring, opener, or door price is realistic",
        "cslb": "C-61/D28 (Doors, Gates and Activating Devices)",
        "checklist": [
            "Contractor's CSLB C-61/D28 license verified at cslb.ca.gov",
            "General Liability and Workers' Compensation insurance certificates",
            "Labor costs broken out from parts",
            "Spring type specified: torsion vs. extension — pricing differs substantially",
            "Spring count specified: single vs. two torsion springs",
            "Opener make and model (LiftMaster, Chamberlain, Genie) — not 'standard opener'",
            "Drive type: belt, chain, or wall-mount/jackshaft",
            "Door material, gauge, and insulation R-value specified if replacing",
            "Debris removal and haul-away included or explicitly excluded",
            "Warranty on springs, opener, and labor stated separately",
        ],
        "red_flags": [
            "No CSLB C-61/D28 license number provided",
            "Same-day upsell from spring replacement to full opener replacement",
            "Off-brand opener installed without disclosure (lock-in tactic)",
            "'Lifetime warranty' from a company with no fixed address",
            "Quote valid 'today only' — high-pressure urgency is a reliable red flag",
            "Spring type not specified in the quote",
            "Full payment required before any work begins",
            "No written quote — verbal pricing is not a contract",
        ],
        "permit_note_generic": "No permit required for like-for-like garage door or opener replacement. If a new electrical circuit is needed for the opener, that work requires a permit from the local building department.",
        "price_low_sd": 150, "price_high_sd": 4500,
        "faq_q1": "How much does garage door spring replacement cost in {city}?",
        "faq_a1": "Single torsion spring: ${spring_low}–${spring_high} installed. Two torsion springs: ${two_low}–${two_high}. Expect a modest premium vs. national averages due to local labor rates in {city}.",
        "faq_q2": "Do I need a permit for garage door replacement in {city}?",
        "faq_a2": "Typically no permit for like-for-like door or spring work. If a new electrical circuit is needed, a permit from {permit_authority} is required. Confirm with your contractor.",
        "faq_q3": "How do I know if a garage door quote in {city} is fair?",
        "faq_a3": "Ask for itemized parts and labor. Compare opener model against manufacturer retail. Labor for a standard spring job should be $120–$280. Total spring-only job: ${spring_low}–${two_high}.",
        "cta_note": "Garage door calls are where same-day upsell pressure runs highest. A 10-minute review before you agree can save you $500–$1,500.",
    },
    "roof-repair": {
        "label": "Roof Repair",
        "title_tag": "Check Your Roof Bid Before You Sign",
        "lede_sd": "review the bid, flag storm-chaser pricing, and tell you what repair vs. replacement actually makes sense",
        "cslb": "C-39 (Roofing Contractor)",
        "checklist": [
            "Contractor's CSLB C-39 license verified at cslb.ca.gov",
            "General Liability and Workers' Compensation insurance certificates",
            "Scope: exact number of squares or sq ft being repaired or replaced",
            "Material specification: product brand, type, and weight/class",
            "Underlayment specification — not just 'standard felt'",
            "Flashing: scope of all flashing work described explicitly",
            "Deck inspection scope — agreement to report deck damage discovered during tear-off",
            "Permit status — full re-roofs require a permit from the local building department",
            "Debris haul-away and disposal included",
            "Warranty: separate manufacturer and labor warranties stated",
        ],
        "red_flags": [
            "No C-39 license — California requires it for any roofing work over $500",
            "Quote arrived unsolicited after a weather event (storm-chasing)",
            "Scope says 'roof repair' with no square footage or material specification",
            "Permit not mentioned for a re-roof — this is a compliance violation",
            "Same-day pressure to sign before getting a second opinion",
            "No mention of deck inspection or hidden damage provision",
            "Haul-away not listed — budget $300–$600 if excluded",
            "Verbal pricing only — no written scope",
        ],
        "permit_note_generic": "Full re-roofs require a permit from the local building department. Spot repairs under a certain threshold may not, but confirm with your contractor.",
        "price_low_sd": 300, "price_high_sd": 28000,
        "faq_q1": "How much does roof repair cost in {city} in 2026?",
        "faq_a1": "Minor patching: ${patch_low}–${patch_high}. Section repair (1–2 squares): ${section_low}–${section_high}. Full re-roof on a 2,000 sq ft home: ${reroof_low}–${reroof_high}.",
        "faq_q2": "Do I need a permit for roof work in {city}?",
        "faq_a2": "Full re-roofs require a permit from {permit_authority}. Spot repairs typically do not, but verify before work begins. Contractors who say no permit is needed for a re-roof are incorrect.",
        "faq_q3": "How do I evaluate a roof repair quote in {city}?",
        "faq_a3": "Ask for: material spec with brand, underlayment spec, all flashing work itemized, and haul-away scope. A quote missing these items is incomplete.",
        "cta_note": "Roof bids vary widely in {city} — especially after storms. A quick review before you sign can catch missing scope, unlicensed contractors, and inflated storm-chaser pricing.",
    },
    "kitchen-remodel": {
        "label": "Kitchen Remodel",
        "title_tag": "Check Your Remodel Bid Before You Sign",
        "lede_sd": "review the bid, map the allowance traps, and tell you what the real project cost should be",
        "cslb": "Class B (General Building Contractor)",
        "checklist": [
            "Contractor's Class B CSLB license verified at cslb.ca.gov",
            "Subcontractor list: who is doing electrical, plumbing, and tile?",
            "Cabinet specification — brand, door style, box material, stock/semi-custom/custom",
            "Countertop material and edge profile specified or a realistic stated allowance",
            "Appliance package with model numbers, or per-appliance allowance clearly stated",
            "Plumbing scope — relocations, new rough-in, drain and supply work described",
            "Electrical scope — new circuits, outlet locations, panel evaluation",
            "Permit fees itemized — City permits required for electrical and plumbing changes",
            "Demolition and haul-away included and scoped",
            "Timeline with milestones and payment schedule tied to milestones",
            "General Liability and Workers' Comp insurance certificates",
            "Warranty on labor and finishes clearly stated",
        ],
        "red_flags": [
            "Allowances without stated dollar amounts — these reliably inflate",
            "No subcontractor disclosure — who holds the C-10 and C-36 licenses?",
            "No permit line item for electrical or plumbing changes",
            "Payment schedule based on calendar dates, not project milestones",
            "No structural engineering noted if a load-bearing wall is being removed",
            "Lump-sum quote with no line-item breakdown",
            "Contract does not include a lien release provision",
            "Same-day pressure to sign before reviewing with another party",
        ],
        "permit_note_generic": "Permits required for electrical changes, plumbing relocations, and structural wall removal. All issued by the local building department.",
        "price_low_sd": 25000, "price_high_sd": 160000,
        "faq_q1": "How much does a kitchen remodel cost in {city} in 2026?",
        "faq_a1": "Budget refresh: ${budget_low}–${budget_high}. Mid-range: ${mid_low}–${mid_high}. High-end: ${high_low}+. {city} remodel costs reflect local labor rates.",
        "faq_q2": "Do I need permits for a kitchen remodel in {city}?",
        "faq_a2": "Yes. Electrical, plumbing, and structural work require permits from {permit_authority}. Skipping permits creates insurance and resale problems.",
        "faq_q3": "How do I evaluate a kitchen remodel quote in {city}?",
        "faq_a3": "Request a fully specified quote with no open allowances. Verify Class B license at cslb.ca.gov. Ask for a subcontractor list. Confirm permit fees are itemized.",
        "cta_note": "Kitchen remodel quotes in {city} routinely contain allowances that inflate by $15,000–$40,000 once real product selections are made. Review before you sign.",
    },
    "window-replacement": {
        "label": "Window Replacement",
        "title_tag": "Check Your Window Bid Before You Sign",
        "lede_sd": "review the bid, verify the glass specs, and check if the price is competitive",
        "cslb": "C-17 (Glazing Contractor) or Class B General",
        "checklist": [
            "Contractor's CSLB C-17 or Class B license verified at cslb.ca.gov",
            "Window count and sizes listed for each unit",
            "Frame material specified: vinyl, fiberglass, aluminum, or wood-clad",
            "Glass package: dual-pane, Low-E coating, tempering requirements",
            "U-factor and SHGC (Solar Heat Gain Coefficient) listed",
            "Window brand and product line named",
            "Installation method specified: insert/retrofit vs. full-frame replacement",
            "Stucco or siding repair scope for full-frame jobs",
            "Permit status — many window replacements require a permit",
            "Lead paint testing scope for pre-1978 homes",
            "Manufacturer warranty and separate installer labor warranty",
        ],
        "red_flags": [
            "No frame material, glass package, or brand specified",
            "No distinction between insert and full-frame installation",
            "Stucco repair not mentioned on a full-frame job — common $500–$3,000 hidden cost",
            "No permit mentioned where required",
            "Lead paint disclosure absent on pre-1978 homes (EPA RRP violation risk)",
            "Deposit over 10% before work begins (California contractor deposit law)",
            "Lifetime warranty with no manufacturer documentation",
            "Same-day-only pricing pressure",
        ],
        "permit_note_generic": "Like-for-like window replacements in the same opening typically do not require a permit. Enlarging openings or structural changes do. Confirm with the local building department.",
        "price_low_sd": 300, "price_high_sd": 35000,
        "faq_q1": "How much does window replacement cost in {city} in 2026?",
        "faq_a1": "Single vinyl insert: ${single_low}–${single_high} installed. Full-frame replacement: ${ff_low}–${ff_high} per window. Whole-home (20 windows, mid-grade vinyl): ${home_low}–${home_high}.",
        "faq_q2": "Do I need permits for window replacement in {city}?",
        "faq_a2": "Like-for-like replacement in the same opening typically does not require a permit. Enlarging openings or adding windows requires a permit from {permit_authority}.",
        "faq_q3": "How do I evaluate a window replacement quote in {city}?",
        "faq_a3": "Ask for the window model number, U-factor, SHGC. Verify the C-17 license. Confirm whether install is insert or full-frame — the cost difference is substantial.",
        "cta_note": "Window quotes in {city} vary widely between big-box installers, dealer networks, and independent glaziers. A 15-minute review can save you thousands.",
    },
    "stucco-repair": {
        "label": "Stucco Repair",
        "title_tag": "Check Your Stucco Bid Before You Sign",
        "lede_sd": "review the scope, verify material layers, and tell you if the price reflects what's actually needed",
        "cslb": "C-35 (Lathing and Plastering Contractor)",
        "checklist": [
            "Contractor's CSLB C-35 license verified at cslb.ca.gov",
            "Scope: exact square footage being repaired or replaced",
            "System type specified: traditional 3-coat stucco vs. EIFS/synthetic stucco",
            "Layers described: scratch coat, brown coat, finish coat — all included?",
            "Water barrier (WRB) inspection and replacement scope if moisture damage exists",
            "Substrate damage assessment: sheathing inspection included?",
            "Color matching process described — number of samples, approval step",
            "Permit status if applicable",
            "Debris removal and haul-away included",
            "Warranty on materials and labor duration stated",
        ],
        "red_flags": [
            "Quote covers only the finish coat — scratch and brown coat damage ignored",
            "No water barrier (WRB) inspection where moisture intrusion exists",
            "System type not specified — EIFS vs. traditional drives price significantly",
            "No mention of sheathing inspection where rot or damage is visible",
            "Color match guarantee without a documented sample approval process",
            "No C-35 license number provided",
            "Lump-sum price with no square footage or layer specification",
            "Same-day pressure to authorize work",
        ],
        "permit_note_generic": "Small patch repairs typically do not require a permit. Full re-coats and EIFS system replacement often do. Water damage repair involving sheathing replacement may also require a permit.",
        "price_low_sd": 400, "price_high_sd": 28000,
        "faq_q1": "How much does stucco repair cost in {city} in 2026?",
        "faq_a1": "Small patch under 10 sq ft: ${patch_low}–${patch_high}. Medium repair (10–100 sq ft): ${med_low}–${med_high}. Full re-coat on a 2,000 sq ft home: ${full_low}–${full_high}.",
        "faq_q2": "Do I need a permit for stucco repair in {city}?",
        "faq_a2": "Small patches typically do not. Full re-coats and EIFS systems often do require a permit from {permit_authority}. If water damage exists, sheathing replacement triggers permit requirements.",
        "faq_q3": "How do I evaluate a stucco repair quote in {city}?",
        "faq_a3": "Ask whether the scope covers all three coats or just the finish layer. Confirm water barrier inspection is included if moisture was present. Verify C-35 license at cslb.ca.gov.",
        "cta_note": "Stucco quotes in {city} frequently miss the underlying water barrier and sheathing work — the hidden costs that appear mid-project. Review before you sign.",
    },
    "pool-installation": {
        "label": "Pool Installation",
        "title_tag": "Check Your Pool Bid Before You Sign",
        "lede_sd": "review the scope, verify equipment specs, and flag allowances that inflate after you sign",
        "cslb": "C-53 (Swimming Pool Contractor)",
        "checklist": [
            "Contractor's CSLB C-53 license verified at cslb.ca.gov",
            "Permit from local building department included in scope (required)",
            "California-compliant pool barrier (fencing/cover) included in scope",
            "Pool shape, dimensions, and depth fully specified",
            "Gunite/shotcrete shell specification — contractor's psi rating and application method",
            "Plumbing: pipe sizing, pump brand and model, filter brand and model",
            "Electrical: C-10 subcontractor identified, panel capacity confirmed",
            "Plaster: brand, type, and color specified or allowance stated with dollar amount",
            "Coping: material, width, and color specified",
            "Decking: square footage, material, and any drainage scope",
            "Fencing/barrier: height, material, and self-latching gate included",
            "Soil export: estimated cubic yards, disposal cost included",
        ],
        "red_flags": [
            "No C-53 license number provided",
            "No permit fee in the quote — pool permits are required in all California jurisdictions",
            "Pool barrier (fencing) not mentioned — California law requires compliant enclosure",
            "Equipment brand and model not specified — 'standard pump and filter' is not a spec",
            "Plaster allowance without a stated dollar amount",
            "Excavation/soil export cost not itemized",
            "Same design-build company handling the full project with no subcontractor list",
            "No lien release provision in the contract",
        ],
        "permit_note_generic": "All pool installations require a permit from the local building department. California law requires a compliant pool barrier (fence/cover) inspected at permit final.",
        "price_low_sd": 50000, "price_high_sd": 200000,
        "faq_q1": "How much does pool installation cost in {city} in 2026?",
        "faq_a1": "Basic gunite pool installed: ${basic_low}–${basic_high}. Mid-range with spa and decking: ${mid_low}–${mid_high}. Full custom build: ${full_low}+.",
        "faq_q2": "Do I need permits for a pool in {city}?",
        "faq_a2": "Yes. All pool installations require a building permit from {permit_authority}. California also requires a compliant pool barrier at permit final inspection.",
        "faq_q3": "How do I evaluate a pool installation quote in {city}?",
        "faq_a3": "Ask for itemized pricing by phase: excavation, gunite, plumbing, electrical, plaster, coping, decking, equipment, and fencing. Equipment specs must include brand and model.",
        "cta_note": "Pool quotes in {city} frequently understate excavation costs and over-rely on allowances. A review before you sign protects a $90k–$200k decision.",
    },
}


def adjust_price(price, adj):
    """Round price to nearest $50"""
    return round(price * adj / 50) * 50


def make_faq_answers(trade_key, city_key):
    t = TRADES[trade_key]
    c = CITIES[city_key]
    a = c["price_adj"]
    city = c["name"]
    pa = c["permit_authority"]

    faq = {}
    if trade_key == "garage-door":
        faq["spring_low"] = adjust_price(150, a)
        faq["spring_high"] = adjust_price(280, a)
        faq["two_low"] = adjust_price(220, a)
        faq["two_high"] = adjust_price(380, a)
    elif trade_key == "roof-repair":
        faq["patch_low"] = adjust_price(300, a)
        faq["patch_high"] = adjust_price(800, a)
        faq["section_low"] = adjust_price(800, a)
        faq["section_high"] = adjust_price(2500, a)
        faq["reroof_low"] = adjust_price(14000, a)
        faq["reroof_high"] = adjust_price(28000, a)
    elif trade_key == "kitchen-remodel":
        faq["budget_low"] = adjust_price(25000, a)
        faq["budget_high"] = adjust_price(45000, a)
        faq["mid_low"] = adjust_price(50000, a)
        faq["mid_high"] = adjust_price(90000, a)
        faq["high_low"] = adjust_price(110000, a)
    elif trade_key == "window-replacement":
        faq["single_low"] = adjust_price(350, a)
        faq["single_high"] = adjust_price(750, a)
        faq["ff_low"] = adjust_price(650, a)
        faq["ff_high"] = adjust_price(1300, a)
        faq["home_low"] = adjust_price(7000, a)
        faq["home_high"] = adjust_price(24000, a)
    elif trade_key == "stucco-repair":
        faq["patch_low"] = adjust_price(400, a)
        faq["patch_high"] = adjust_price(950, a)
        faq["med_low"] = adjust_price(1500, a)
        faq["med_high"] = adjust_price(5500, a)
        faq["full_low"] = adjust_price(8500, a)
        faq["full_high"] = adjust_price(28000, a)
    elif trade_key == "pool-installation":
        faq["basic_low"] = adjust_price(55000, a)
        faq["basic_high"] = adjust_price(90000, a)
        faq["mid_low"] = adjust_price(95000, a)
        faq["mid_high"] = adjust_price(130000, a)
        faq["full_low"] = adjust_price(140000, a)

    faq["city"] = city
    faq["permit_authority"] = pa

    q1 = t["faq_q1"].format(**faq)
    a1 = t["faq_a1"].format(**faq)
    q2 = t["faq_q2"].format(**faq)
    a2 = t["faq_a2"].format(**faq)
    q3 = t["faq_q3"].format(**faq)
    a3 = t["faq_a3"].format(**faq)
    return q1, a1, q2, a2, q3, a3


def generate_page(trade_key, city_key):
    t = TRADES[trade_key]
    c = CITIES[city_key]
    city = c["name"]
    a = c["price_adj"]
    sd_slug = f"{trade_key}-quote-review-san-diego.html"
    city_slug = f"{trade_key}-quote-review-{city_key}.html"

    # Price range for lede
    if t["price_low_sd"] >= 1000:
        price_low = f"${adjust_price(t['price_low_sd'], a):,}"
        price_high = f"${adjust_price(t['price_high_sd'], a):,}+"
    else:
        price_low = f"${adjust_price(t['price_low_sd'], a)}"
        price_high = f"${adjust_price(t['price_high_sd'], a):,}"

    q1, a1, q2, a2, q3, a3 = make_faq_answers(trade_key, city_key)

    checklist_items = "".join(
        f"        <li>{item}</li>\n" for item in t["checklist"]
    )
    redflag_items = "".join(
        f"        <li>{item}</li>\n" for item in t["red_flags"]
    )

    cta_note = t["cta_note"].format(city=city)

    schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q1,
             "acceptedAnswer": {"@type": "Answer", "text": a1}},
            {"@type": "Question", "name": q2,
             "acceptedAnswer": {"@type": "Answer", "text": a2}},
            {"@type": "Question", "name": q3,
             "acceptedAnswer": {"@type": "Answer", "text": a3}},
        ]
    }, ensure_ascii=False, separators=(',', ':'))

    lb_schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "SideGuy Solutions",
        "description": f"Human-first guidance for home and business owners in {city}",
        "url": "https://sideguysolutions.com",
        "telephone": "+1-773-544-1231",
        "address": {"@type": "PostalAddress",
                     "addressLocality": city,
                     "addressRegion": "CA",
                     "addressCountry": "US"},
        "areaServed": {"@type": "City", "name": city},
        "priceRange": "Free"
    }, ensure_ascii=False, separators=(',', ':'))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<!-- SHIP010_ROBOTS -->
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{t["label"]} Quote Review {city} — {t["title_tag"]} | SideGuy Solutions</title>
<link rel="canonical" href="https://sideguysolutions.com/{city_slug}"/>
<meta name="description" content="Got a {t["label"].lower()} quote in {city}? Send it to SideGuy. We {t["lede_sd"]}. Free, no contractor affiliations."/>
<script defer data-domain="sideguysolutions.com" src="https://plausible.io/js/script.js"></script>
<style>
:root{{--bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;--ink:#073044;--muted:#3f6173;--muted2:#5e7d8e;--card:#ffffffcc;--card2:#ffffffb8;--stroke:rgba(7,48,68,.10);--shadow:0 18px 50px rgba(7,48,68,.10);--mint:#21d3a1;--blue:#4aa9ff;--red:#ff4d4d;--r:22px;--pill:999px}}
*{{box-sizing:border-box}}html,body{{height:100%;margin:0}}
body{{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;color:var(--ink);background:radial-gradient(1200px 900px at 22% 10%,#ffffff 0%,var(--bg0) 25%,var(--bg1) 60%,var(--bg2) 100%);-webkit-font-smoothing:antialiased}}
.wrap{{max-width:860px;margin:0 auto;padding:40px 24px 100px}}
h1{{font-size:44px;letter-spacing:-.03em;line-height:1.1;margin:0 0 18px}}
.lede{{font-size:20px;line-height:1.6;color:var(--muted);margin-bottom:36px;max-width:700px}}
.hub-back{{font-size:14px;color:var(--muted2);margin-bottom:32px}}
.hub-back a{{color:var(--muted);text-decoration:underline}}
.section{{margin:44px 0}}
.section h2{{font-size:28px;margin:0 0 20px;color:var(--ink)}}
.card{{background:var(--card);padding:22px 26px;border-radius:var(--r);border:1px solid var(--stroke);box-shadow:var(--shadow);backdrop-filter:blur(12px);margin-bottom:14px}}
.card h3{{font-size:17px;margin:0 0 8px;color:var(--ink)}}
.card p{{margin:0;font-size:15px;color:var(--muted2);line-height:1.6}}
.checklist{{list-style:none;padding:0;margin:0}}
.checklist li{{padding:10px 0 10px 32px;position:relative;border-bottom:1px solid var(--stroke);font-size:16px;color:var(--muted);line-height:1.5}}
.checklist li:last-child{{border-bottom:none}}
.checklist li::before{{content:"✓";position:absolute;left:0;color:var(--mint);font-weight:700;font-size:18px}}
.redflag{{list-style:none;padding:0;margin:0}}
.redflag li{{padding:10px 0 10px 32px;position:relative;border-bottom:1px solid var(--stroke);font-size:16px;color:var(--muted);line-height:1.5}}
.redflag li:last-child{{border-bottom:none}}
.redflag li::before{{content:"⚠";position:absolute;left:0;font-size:16px}}
.cta-box{{background:linear-gradient(135deg,var(--mint),var(--blue));color:#fff;padding:40px 36px;border-radius:var(--r);text-align:center;margin:48px 0}}
.cta-box h2{{margin:0 0 12px;font-size:28px}}
.cta-box p{{margin:0 0 24px;font-size:17px;opacity:.95;line-height:1.6}}
.cta-box a{{display:inline-block;background:#fff;color:var(--ink);padding:16px 32px;border-radius:var(--pill);text-decoration:none;font-weight:700;font-size:17px;box-shadow:0 8px 24px rgba(0,0,0,.15)}}
details{{border:1px solid var(--stroke);border-radius:16px;padding:18px 22px;margin-bottom:12px;background:var(--card)}}
summary{{font-weight:700;font-size:17px;cursor:pointer;color:var(--ink)}}
details p{{margin:12px 0 0;color:var(--muted);line-height:1.7;font-size:15px}}
.floating{{position:fixed;bottom:24px;right:24px;display:flex;align-items:center;gap:10px;z-index:999}}
.floatBtn{{background:var(--mint);color:#fff;padding:14px 20px;border-radius:var(--pill);text-decoration:none;font-weight:700;font-size:15px;box-shadow:0 8px 28px rgba(33,211,161,.35)}}
@media(max-width:640px){{h1{{font-size:32px}}.cta-box{{padding:28px 20px}}}}
</style>
</head>
<body>
<div class="wrap">

  <div class="hub-back">&#x2190; <a href="contractor-services-hub-san-diego.html">Contractor Services Hub</a> &mdash; San Diego County home improvement guidance</div>

  <h1>Got a {t["label"]} Quote in {city}? Send It Before You Sign.</h1>
  <div class="lede">{t["label"]} projects in {city} run {price_low}–{price_high} depending on scope — and the {c["intro_flavor"]} means there are local pricing variables that differ from broader San Diego County norms. We'll {t["lede_sd"]} before you commit to anything.</div>

  <div class="section">
    <h2>&#x1F4CB; What a Complete {t["label"]} Quote Should Include in {city}</h2>
    <div class="card">
      <ul class="checklist">
{checklist_items}      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x26A0;&#xFE0F; Common Red Flags in {city} {t["label"]} Quotes</h2>
    <div class="card" style="border-left:4px solid var(--red)">
      <ul class="redflag">
{redflag_items}      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4C4; {city} Permit Context</h2>
    <div class="card">
      <p>{t["permit_note_generic"]}</p>
      <p style="margin-top:12px">{c["note"]}</p>
      <p style="margin-top:12px">Permit authority: <strong>{c["permit_authority"]}</strong>. Always confirm permit requirements before signing a contract — your contractor should be able to tell you exactly which permits they will pull and what the inspection schedule looks like.</p>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4C4; CSLB License Verification</h2>
    <div class="card">
      <p>For {t["label"].lower()} work in {city}, the relevant CSLB classification is <strong>{t["cslb"]}</strong>. Verify any contractor's license at <a href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" rel="nofollow noopener" target="_blank" style="color:var(--mint)">cslb.ca.gov</a> before signing. The lookup shows current license status, bond, workers' compensation coverage, and any disciplinary history. It takes 60 seconds and costs nothing.</p>
    </div>
  </div>

  <div class="cta-box">
    <h2>&#x1F4AC; Send Us Your {t["label"]} Quote from {city}</h2>
    <p>{cta_note}</p>
    <a href="sms:+17735441231" rel="nofollow" aria-label="Text PJ for {city} quote review">Text 773-544-1231</a>
  </div>

  <div class="section">
    <h2>&#x2753; {city} {t["label"]} FAQ</h2>
    <details>
      <summary>{q1}</summary>
      <p>{a1}</p>
    </details>
    <details>
      <summary>{q2}</summary>
      <p>{a2}</p>
    </details>
    <details>
      <summary>{q3}</summary>
      <p>{a3}</p>
    </details>
  </div>

  <div style="background:rgba(33,211,161,.06);border:1px solid rgba(33,211,161,.18);border-radius:14px;padding:18px 22px;margin:32px 0">
    <p style="font-size:14px;color:var(--muted2);margin:0;line-height:1.7">Reviewed with 20+ years of local contractor pricing exposure across San Diego County including {city}. SideGuy does not sell construction services or accept referral fees. Clarity before cost. &#x2192; <a href="{sd_slug}" style="color:var(--muted2)">See the full {t["label"]} quote review guide for San Diego</a></p>
  </div>

  <div style="margin-top:32px;padding:16px;text-align:center;font-size:13px;color:var(--muted2)">Updated March 2026</div>
</div>

<div class="floating">
  <a class="floatBtn" href="sms:+17735441231" rel="nofollow" aria-label="Text PJ for {city} quote review">Text PJ</a>
</div>

<script type="application/ld+json">
{lb_schema}
</script>
<script type="application/ld+json">
{schema_json}
</script>
<!-- SIDEGUY_MESH_BLOCK -->
<section style="margin-top:60px;padding:30px;background:#f4fdfb;border-left:6px solid #1fc7a6;">
<h3>{city} &amp; San Diego County Quote Reviews</h3>
<ul style="line-height:1.8;">
<li><a href="{sd_slug}">San Diego {t["label"]} Quote Review</a></li>
<li><a href="contractor-services-hub-san-diego.html">Contractor Services Hub — San Diego</a></li>
<li><a href="html-sitemap.html">All San Diego Homeowner Guides</a></li>
</ul>
</section>
<!-- SHIP010_FRESHNESS -->
<div style="display:none">Updated: 2026-03-03</div>
</body>
</html>
"""
    return html, city_slug


def main():
    created = []
    for city_key in CITIES:
        for trade_key in TRADES:
            html, slug = generate_page(trade_key, city_key)
            filepath = os.path.join(ROOT, slug)
            if os.path.exists(filepath):
                print(f"  SKIP {slug} — already exists")
                continue
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            created.append(slug)
            print(f"  OK   {slug}")

    print(f"\nDone — {len(created)} pages created")

    # Output list for sitemap
    with open(os.path.join(ROOT, "_ship013_new_pages.txt"), "w") as f:
        for slug in created:
            f.write(slug + "\n")
    print(f"Slug list written to _ship013_new_pages.txt")


if __name__ == "__main__":
    main()
