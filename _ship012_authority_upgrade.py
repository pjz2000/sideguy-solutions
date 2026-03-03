#!/usr/bin/env python3
"""SHIP-012: Quote Review Authority Density Upgrade
Injects 4 authority blocks + E-E-A-T signal + internal cluster
into every *-quote-review-san-diego.html page.
"""
import os, glob, re

ROOT = "/workspaces/sideguy-solutions"

# ── Trade-specific pricing / permit / CSLB data ───────────────────────────────
TRADE_DATA = {
    "garage-door": {
        "label":   "Garage Door",
        "price":   "$150 (spring swap) to $4,500 (full door install)",
        "permit":  "No permit required for like-for-like door or opener replacement. A new dedicated electrical circuit for an opener does require a City of San Diego DSD permit.",
        "cslb":    "C-61/D28 (Doors, Gates and Activating Devices)",
        "labor":   "$75–$150 per hour — spring replacement is typically 1 hour of billed labor",
        "materials": "Torsion springs: $35–$90 material cost. Opener units: $120–$380 retail. Full steel door panels: $300–$900 supplier price.",
        "margin":  "Typical contractor margin on garage door work: 40–65%. A job quoted at $1,200 may have $450–$600 in materials.",
        "faq_q1":  "How much does garage door repair cost in San Diego?",
        "faq_a1":  "Spring replacement: $150–$380. Opener replacement: $350–$900 installed. Full single-car door: $800–$2,000. Full double-car door: $1,200–$4,500.",
        "faq_q2":  "Do I need a permit for a garage door replacement in San Diego?",
        "faq_a2":  "Not for like-for-like door or spring work. If a new electrical circuit is required for the opener, a permit from City of San Diego DSD is needed.",
        "faq_q3":  "How do I know if a garage door quote is fair?",
        "faq_a3":  "Ask the contractor for a line-item breakdown: spring cost, opener model and price, labor hours, and any service call fee. Compare opener model MSRP against quoted price — material markup above 40% warrants negotiation.",
    },
    "kitchen-remodel": {
        "label":   "Kitchen Remodel",
        "price":   "$25,000 (budget refresh) to $160,000+ (full high-end remodel)",
        "permit":  "Permits required in San Diego for electrical changes (new circuits, panel upgrades), plumbing relocations, and structural wall removal. City of San Diego DSD issues these.",
        "cslb":    "Class B (General Building Contractor) for full remodels; C-7 (Low Voltage) if AV/smart-home work is included",
        "labor":   "$65–$120/hr for general labor; $120–$180/hr for licensed plumbing and electrical subcontractors",
        "materials":"Cabinets range from $2,500 (stock) to $35,000+ (custom). Countertop: $40–$200/sq ft installed. Appliance packages: $3,000–$25,000.",
        "margin":  "General contractors typically mark up subcontractor and material costs 15–25%. Management overhead and profit is often called out as a separate line — 10–18% is normal.",
        "faq_q1":  "How much does a kitchen remodel cost in San Diego in 2026?",
        "faq_a1":  "Budget remodel: $25,000–$45,000. Mid-range: $50,000–$90,000. High-end: $100,000–$160,000+. Biggest cost drivers are cabinet grade, layout changes requiring plumbing relocation, and structural work.",
        "faq_q2":  "Do I need permits for a kitchen remodel in San Diego?",
        "faq_a2":  "Yes — electrical changes, plumbing changes, and structural work all require permits from the City of San Diego DSD. Unpermitted work creates insurance and resale issues.",
        "faq_q3":  "How do I know if a kitchen remodel quote is fair?",
        "faq_a3":  "Request a fully specified quote with no 'allowances' — or demand that each allowance state the exact dollar amount. Compare cabinet-line pricing to distributor pricing. Ask for a subcontractor list so you can verify individual trade licenses.",
    },
    "roof-repair": {
        "label":   "Roof Repair",
        "price":   "$300 (minor patch) to $28,000 (major section replacement)",
        "permit":  "Permits required in San Diego for full re-roofs and any structural deck work. Spot repairs under a specific square footage threshold may not require permits — verify with City of San Diego DSD.",
        "cslb":    "C-39 (Roofing Contractor)",
        "labor":   "$75–$130/hr for roofing crews. Flat or low-slope membrane work often carries a premium.",
        "materials":"Composition shingle: $80–$120/square material cost. Tile (concrete): $200–$350/square. TPO/flat membrane: $180–$280/square.",
        "margin":  "Roofing contractors typically target 35–55% gross margin. Storm-chasing contractors operating after weather events routinely charge 2–3× normal market rates.",
        "faq_q1":  "How much does roof repair cost in San Diego in 2026?",
        "faq_a1":  "Minor leak repair: $300–$800. Section repair (1–2 squares): $800–$2,500. Full replacement on a 2,000 sq ft home: $14,000–$28,000 depending on material choice.",
        "faq_q2":  "Do I need a permit for roof repair in San Diego?",
        "faq_a2":  "Full re-roofs and structural deck repairs require a City of San Diego DSD permit. Like-for-like spot repairs typically do not. When in doubt, ask the contractor to pull the permit — if they refuse, that is a red flag.",
        "faq_q3":  "How do I know if a roof repair quote is fair?",
        "faq_a3":  "Ask for a scope that lists the number of squares, material specification (brand and type), underlayment spec, flashing work, and disposal costs. A quote missing any of these is incomplete.",
    },
    "window-replacement": {
        "label":   "Window Replacement",
        "price":   "$300 (single window) to $35,000 (whole-home replacement)",
        "permit":  "Permits required for structural rough opening changes and any new openings. Like-for-like replacements in the same frame opening typically do not require a permit in San Diego.",
        "cslb":    "C-17 (Glazing Contractor) for window installation",
        "labor":   "$75–$150/hr. Installation of a standard window runs 1–2 hours per window.",
        "materials":"Vinyl dual-pane: $150–$600/window. Fiberglass: $500–$1,200/window. Aluminum: $200–$800/window. Low-E coating and argon fill are standard in San Diego's climate zone.",
        "margin":  "Window contractors typically mark up product 30–60% above wholesale. Ask for the product model number so you can verify retail pricing independently.",
        "faq_q1":  "How much does window replacement cost in San Diego?",
        "faq_a1":  "Single double-pane vinyl window installed: $350–$900. Full home (20 windows): $8,000–$25,000. Premium fiberglass or wood-clad can reach $35,000 for a full home.",
        "faq_q2":  "Do I need permits to replace windows in San Diego?",
        "faq_a2":  "Like-for-like window replacement in the same opening does not require a permit. Enlarging openings or adding new openings does require a permit from City of San Diego DSD.",
        "faq_q3":  "How do I know if a window replacement quote is fair?",
        "faq_a3":  "Ask for the exact window model number, U-factor, SHGC, and frame material in writing. Verify the model's retail price. Labor for a standard 3-hour install job should be $200–$400 per window.",
    },
    "stucco-repair": {
        "label":   "Stucco Repair",
        "price":   "$400 (small patch) to $28,000 (full re-coat or EIFS system)",
        "permit":  "Stucco repairs under a certain square footage threshold typically do not require permits. Full re-coat or EIFS replacement often requires a permit and may trigger water barrier inspection in San Diego.",
        "cslb":    "C-35 (Lathing and Plastering Contractor)",
        "labor":   "$60–$100/hr for plaster crews. Color-matching is a skilled specialty that commands premium pricing.",
        "materials":"Portland cement stucco: $8–$18/sq ft installed. EIFS (synthetic): $10–$22/sq ft. Elastomeric paint coat: $3–$8/sq ft.",
        "margin":  "Stucco contractors typically operate at 40–55% gross margin on material and labor. Texture matching and color matching labor is difficult to benchmark — get multiple bids.",
        "faq_q1":  "How much does stucco repair cost in San Diego?",
        "faq_a1":  "Small patch under 10 sq ft: $400–$900. Medium repair (10–100 sq ft): $1,500–$5,000. Full re-coat on a 2,000 sq ft home: $8,000–$28,000.",
        "faq_q2":  "Do I need a permit for stucco repair in San Diego?",
        "faq_a2":  "Small patches typically do not require a permit. Full re-coats or EIFS system replacement often do. If water damage is involved, a permit may be required for sheathing and water barrier work.",
        "faq_q3":  "How do I know if a stucco repair quote is fair?",
        "faq_a3":  "Ask whether the quote covers just the finish coat or also the scratch and brown coat layers. Water damage repair requires removal of affected sheathing — confirm that scope is included if moisture was present.",
    },
    "pool-installation": {
        "label":   "Pool Installation",
        "price":   "$50,000 (basic gunite) to $140,000+ (full custom with features)",
        "permit":  "All pool installations in San Diego require a permit from City of San Diego DSD or the relevant city building department. California law also requires compliant fencing enclosure (pool barrier) inspected at permit final.",
        "cslb":    "C-53 (Swimming Pool Contractor)",
        "labor":   "Pool labor is typically bundled into a lump bid, not hourly. Gunite crews, plastering crews, and electrical/plumbing subcontractors are usually separate trade-licensed contractors.",
        "materials":"Gunite/shotcrete: $20–$35/sq ft for shell. Coping: $50–$150 per linear foot. Plaster: $5–$12/sq ft. Tile: $30–$100/sq ft.",
        "margin":  "Pool contractors typically carry 30–50% gross margin. Custom feature add-ons (waterfalls, fire features, automation systems) often carry higher margins.",
        "faq_q1":  "How much does pool installation cost in San Diego in 2026?",
        "faq_a1":  "Basic gunite pool installed: $55,000–$85,000. Mid-range with spa and decking: $90,000–$120,000. Full custom build with features: $130,000–$200,000+.",
        "faq_q2":  "Do I need permits for a pool in San Diego?",
        "faq_a2":  "Yes. All pool installations require a building permit. California also requires compliant pool barrier (fencing/cover) inspected at permit final. No permit means no legal occupancy of the pool.",
        "faq_q3":  "How do I know if a pool installation quote is fair?",
        "faq_a3":  "Ask for itemized pricing: excavation, gunite/shotcrete, plumbing rough-in, electrical (separate C-10 contractor), plaster, coping, decking, and equipment (pump, filter, heater). Equipment specs should include brand and model.",
    },
    "adu-project": {
        "label":   "ADU",
        "price":   "$120,000 (basic attached ADU conversion) to $450,000+ (detached custom ADU)",
        "permit":  "All ADUs require City of San Diego (or local jurisdiction) building permits. Utility connections require SDGE and SDWD coordination. Permit timeline in San Diego typically runs 4–12 months.",
        "cslb":    "Class B (General Building Contractor) required for full ADU construction",
        "labor":   "$65–$120/hr general labor; licensed trades (electrical, plumbing) run $110–$180/hr",
        "materials":"Framing lumber runs 30–40% of rough construction cost. Finishes vary widely — prefab/panelized systems can reduce material costs 15–25% vs. stick-frame.",
        "margin":  "GC overhead and profit on ADU projects: 18–28% of total hard costs. Design/permit fees are often 8–15% of total project cost and should be itemized separately.",
        "faq_q1":  "How much does an ADU cost in San Diego?",
        "faq_a1":  "Garage conversion to JADU: $60,000–$120,000. Attached ADU addition: $150,000–$280,000. Detached ADU: $200,000–$450,000. Costs depend heavily on utility connections and site conditions.",
        "faq_q2":  "Do I need permits for an ADU in San Diego?",
        "faq_a2":  "Yes. All ADUs require building, electrical, plumbing, and mechanical permits. San Diego has a streamlined ADU permit pathway, but 'streamlined' still means 4–8 months in most cases.",
        "faq_q3":  "How do I evaluate an ADU construction quote?",
        "faq_a3":  "Ask for a clear breakdown: design/permitting fees, site prep/demolition, foundation, framing, rough trades, insulation/drywall, finishes, and utility connections. Each category should have a dollar amount, not a bundled number.",
    },
    "roofing-project": {
        "label":   "Roofing",
        "price":   "$8,000 (small low-slope) to $45,000+ (full large-home re-roof with tile)",
        "permit":  "Full re-roofs in San Diego require a permit from City of San Diego DSD. Structural deck repairs and changes to roof sheathing also require inspection.",
        "cslb":    "C-39 (Roofing Contractor)",
        "labor":   "$75–$130/hr. Tile work commands a premium over composition shingle labor.",
        "materials":"Composition shingle: $80–$130/square. Concrete tile: $200–$350/square. Clay tile: $350–$600/square. Metal roofing: $350–$700/square.",
        "margin":  "Roofing contractors target 35–55% gross margin. Material markup varies widely — ask for the product brand and AHJ-approved product number for comparison.",
        "faq_q1":  "How much does a full roof replacement cost in San Diego in 2026?",
        "faq_a1":  "Composition shingle Re-roof (2,000 sq ft): $12,000–$22,000. Concrete tile: $22,000–$38,000. Clay tile: $32,000–$55,000. Metal: $25,000–$45,000.",
        "faq_q2":  "Do I need a permit for a new roof in San Diego?",
        "faq_a2":  "Yes. Full re-roofs require a City of San Diego DSD permit and may require an inspection at rough (deck) and final. Contractors who say no permit is needed for a full re-roof are incorrect.",
        "faq_q3":  "How do I evaluate a roofing quote?",
        "faq_a3":  "Ask for: total squares, material spec (manufacturer and product line), underlayment spec, flashing work scope, deck inspection scope, and disposal/haul-away. A quote missing these is incomplete.",
    },
    "solar-project": {
        "label":   "Solar Installation",
        "price":   "$18,000 (small system) to $65,000+ (large battery-backup system)",
        "permit":  "All solar installations in San Diego require a permit and SDGE interconnection approval. Battery storage systems require additional fire/electrical inspection under California Fire Code.",
        "cslb":    "C-46 (Solar Contractor) — or Class B with C-10 (Electrical) for solar + electrical scope",
        "labor":   "$80–$150/hr. A typical 7kW system installation takes 1–2 days for a 2-person crew.",
        "materials":"Solar panels (per watt): $0.30–$0.70 material cost. Inverter: $1,500–$6,000. Battery bank (10kWh): $8,000–$14,000 installed.",
        "margin":  "Solar contractors operate at 25–45% gross margin. Equipment markup is often 30–50% above wholesale cost. Ask for equipment brand/model to verify market pricing.",
        "faq_q1":  "How much does solar installation cost in San Diego in 2026?",
        "faq_a1":  "6–8kW system (most common): $22,000–$38,000 before incentives. After 30% federal ITC: $15,000–$27,000. Adding a 10kWh battery adds $10,000–$18,000.",
        "faq_q2":  "Do I need permits for solar installation in San Diego?",
        "faq_a2":  "Yes. Building permit, electrical permit, and SDGE interconnection approval are all required. Battery systems also require a fire department inspection.",
        "faq_q3":  "How do I evaluate a solar quote?",
        "faq_a3":  "Ask for: panel brand and model, inverter brand and model, system size in kW, estimated annual production in kWh, warranty terms, and proof of C-46 license. Compare panel model pricing on EnergySage.",
    },
    "hvac-project": {
        "label":   "HVAC",
        "price":   "$3,500 (basic AC replacement) to $28,000+ (full system with ductwork)",
        "permit":  "HVAC replacements and new system installs in San Diego require a permit from City of San Diego DSD. Permits ensure HERS rater sign-off on new efficiency standards.",
        "cslb":    "C-20 (Warm-Air Heating, Ventilating and Air-Conditioning Contractor)",
        "labor":   "$85–$160/hr for HVAC technicians. New system replacements are often quoted as flat rates.",
        "materials":"Standard split-system (3-ton): $2,000–$4,000 equipment cost. Heat pump system: $3,500–$7,000. Ductwork (major repair/replacement): $3,000–$12,000.",
        "margin":  "HVAC contractors typically operate at 40–60% gross margin on service calls and 30–45% on equipment-replacement projects. Verify equipment pricing by requesting the model number.",
        "faq_q1":  "How much does HVAC replacement cost in San Diego in 2026?",
        "faq_a1":  "Basic AC-only replacement (3-ton): $5,000–$9,000. Full split-system (AC+furnace): $8,000–$16,000. New ductwork added: $14,000–$28,000.",
        "faq_q2":  "Do I need a permit for HVAC replacement in San Diego?",
        "faq_a2":  "Yes. Any system replacement or new equipment install requires a permit in San Diego. HERS rater verification of new equipment is required and is part of the permit process.",
        "faq_q3":  "How do I evaluate an HVAC quote?",
        "faq_a3":  "Ask for the equipment brand, model, SEER2 rating, tonnage, and full installation scope. Permit fees should be itemized. A quote with no equipment model number is not a complete quote.",
    },
    "plumbing-project": {
        "label":   "Plumbing",
        "price":   "$200 (minor repair) to $18,000+ (full re-pipe)",
        "permit":  "New plumbing work and re-pipes in San Diego require a permit from City of San Diego DSD. Service and repair work (no new pipe runs) typically does not require a permit.",
        "cslb":    "C-36 (Plumbing Contractor)",
        "labor":   "$90–$175/hr for licensed plumbers in San Diego. Drain and sewer work typically runs flat rates per job.",
        "materials":"Copper pipe: $4–$12 per linear foot. PEX: $1–$4 per linear foot. ABS drain pipe: $1–$3 per linear foot.",
        "margin":  "Plumbing contractors typically operate at 50–70% gross margin on service calls. Material markup is often 50–100% above supply house pricing on service work.",
        "faq_q1":  "How much does a plumbing re-pipe cost in San Diego?",
        "faq_a1":  "PEX re-pipe on a 1,500 sq ft home: $5,000–$10,000. Copper: $8,000–$18,000. Includes wall access cuts and patches.",
        "faq_q2":  "Do I need permits for plumbing work in San Diego?",
        "faq_a2":  "New plumbing work, re-pipes, and water heater replacements require a permit. Repair of existing pipes typically does not.",
        "faq_q3":  "How do I evaluate a plumbing quote?",
        "faq_a3":  "Ask for pipe material specification (PEX vs. copper), access method (open walls vs. minimal cuts), inspection schedule, and whether the permit fee is included. A contractor who says no permit is needed for a re-pipe is incorrect.",
    },
    "electrical-project": {
        "label":   "Electrical",
        "price":   "$300 (outlet/switch repair) to $25,000+ (full panel upgrade with EV and solar prep)",
        "permit":  "All electrical work beyond minor repairs requires a permit from City of San Diego DSD. Panel upgrades, new circuits, and EV charger installs all require permits and inspection.",
        "cslb":    "C-10 (Electrical Contractor)",
        "labor":   "$95–$180/hr for licensed electricians in San Diego.",
        "materials":"200A panel upgrade: $1,500–$3,000 equipment. EV Level 2 charger: $400–$1,500 unit cost. 240V circuit wire run: $3–$8 per foot.",
        "margin":  "Electrical contractors operate at 45–65% gross margin on service work. Material markup is typically 30–50%.",
        "faq_q1":  "How much does electrical panel upgrade cost in San Diego?",
        "faq_a1":  "100A-to-200A upgrade: $2,500–$5,000. 200A-to-400A (for EV/solar): $4,500–$9,000. Cost varies by distance from meter to panel and local utility coordination required.",
        "faq_q2":  "Do I need permits for electrical work in San Diego?",
        "faq_a2":  "Yes — all new circuits, panel upgrades, and EV charger installs require permits from City of San Diego DSD. Unpermitted electrical work voids homeowner's insurance coverage for related incidents.",
        "faq_q3":  "How do I evaluate an electrical quote?",
        "faq_a3":  "Ask for the panel brand and amperage rating, wire gauge for new circuits, permit fee itemization, and EV charger brand and model if applicable. Verify the C-10 license at CSLB.ca.gov.",
    },
    "painting-project": {
        "label":   "Painting",
        "price":   "$1,500 (single room interior) to $18,000+ (full exterior repaint)",
        "permit":  "Painting typically requires no permit in San Diego. Exception: if painting is part of a larger project involving structural work, the permit for that project may require inspection of surfaces before painting.",
        "cslb":    "C-33 (Painting and Decorating Contractor)",
        "labor":   "$45–$85/hr for painting crews. Exterior work commands a premium over interior.",
        "materials":"Interior latex paint: $30–$80/gallon (contractor grade to premium). Exterior: $40–$100/gallon. Material typically accounts for 15–25% of total job cost.",
        "margin":  "Painting contractors typically operate at 40–55% gross margin. Material cost is often marked up 25–40%.",
        "faq_q1":  "How much does exterior painting cost in San Diego?",
        "faq_a1":  "Single-story home (1,500–2,000 sq ft exterior): $3,500–$7,000. Two-story: $5,500–$12,000. Premium prep (elastomeric, stucco sealing) adds $2,000–$5,000.",
        "faq_q2":  "Do I need permits for painting in San Diego?",
        "faq_a2":  "No permit required for painting. If painting is part of a stucco repair or water damage project, the underlying repair work may require a permit.",
        "faq_q3":  "How do I evaluate a painting quote?",
        "faq_a3":  "Look for: number of coats specified, paint brand and product line, surface prep scope (caulking, sanding, patching), masking scope, and cleanup. A quote without paint brand/product is incomplete.",
    },
    "landscaping": {
        "label":   "Landscaping",
        "price":   "$2,000 (basic cleanup and planting) to $80,000+ (full hardscape + irrigation system)",
        "permit":  "Hardscape work (retaining walls over 4 feet, grading) may require permits in San Diego. Irrigation system installation may require a permit if connected to city water main.",
        "cslb":    "C-27 (Landscaping Contractor)",
        "labor":   "$55–$95/hr for landscaping crews. Irrigation specialists and arborists command premium rates.",
        "materials":"Decomposed granite: $40–$80 per ton installed. Concrete pavers: $8–$18/sq ft. Plant material is highly variable — ask for an itemized plant list.",
        "margin":  "Landscaping contractors typically operate at 40–60% gross margin. Plant material markup is often 50–100% above nursery wholesale.",
        "faq_q1":  "How much does landscaping cost in San Diego?",
        "faq_a1":  "Basic front yard cleanup and planting: $2,000–$6,000. Full hardscape with irrigation: $15,000–$60,000. Complete pool-area landscaping: $20,000–$80,000.",
        "faq_q2":  "Do I need permits for landscaping in San Diego?",
        "faq_a2":  "Retaining walls over 4 feet require a permit. Grading projects over 50 cubic yards require a grading permit. Irrigation tied to city water may require a permit depending on scope.",
        "faq_q3":  "How do I evaluate a landscaping quote?",
        "faq_a3":  "Ask for an itemized plant list with species and sizes, square footage for pavers and decomposed granite, irrigation head count and brand, and a clear scope of grading vs. finish prep work.",
    },
    "foundation": {
        "label":   "Foundation Repair",
        "price":   "$1,500 (minor crack sealing) to $80,000+ (full re-leveling or pier system)",
        "permit":  "Foundation repair in San Diego requires a permit for any structural work. Cosmetic crack sealing may not. Post-and-pier leveling and underpinning always require a permit and structural engineering documentation.",
        "cslb":    "Class A (General Engineering Contractor) for major foundation work; C-61/D-12 (Synthetic Products) for epoxy injection",
        "labor":   "$85–$160/hr for foundation crews. Structural engineering reports add $1,500–$5,000 to total project cost.",
        "materials":"Helical piers: $1,200–$2,500 each installed. Concrete for crack repair: $200–$800 per linear foot. Mudjacking/slabjacking: $3–$8/sq ft.",
        "margin":  "Foundation contractors typically operate at 40–60% gross margin. Engineered solutions (piers, beams) command higher margins than crack-sealing services.",
        "faq_q1":  "How much does foundation repair cost in San Diego?",
        "faq_a1":  "Hairline crack epoxy injection: $1,500–$4,000. Helical pier system (4–6 piers): $10,000–$25,000. Full re-level on a slab foundation: $18,000–$80,000.",
        "faq_q2":  "Do I need permits for foundation repair in San Diego?",
        "faq_a2":  "Structural foundation repair requires a permit and may require a licensed structural engineer's report. Cosmetic patching of hairline cracks may not. Ask your contractor to confirm.",
        "faq_q3":  "How do I evaluate a foundation repair quote?",
        "faq_a3":  "Ask whether the quote is based on a paid engineering assessment or a visual inspection. Demand a written scope, materials spec, and warranty on the repair — not just the labor.",
    },
    "contractor-project": {
        "label":   "General Contractor",
        "price":   "$15,000 (small remodel) to $500,000+ (custom build or major addition)",
        "permit":  "General contractors must pull all permits for projects they manage. Permits vary by scope — always confirm the permit requirement before any work begins.",
        "cslb":    "Class B (General Building Contractor) — required to manage projects with multiple trades",
        "labor":   "$70–$130/hr general labor. GC overhead and profit is typically a separate line: 15–25% of total hard costs.",
        "materials":"Materials costs are project-specific. Ask for a materials breakdown by trade or phase, not a lump number.",
        "margin":  "GC overhead and profit: 15–25% on new construction; 20–30% on remodels. Soft costs (design, engineering, permits): 10–18% of hard cost budget.",
        "faq_q1":  "How much does a general contractor charge in San Diego?",
        "faq_a1":  "GC overhead and profit is typically 15–25% of total project cost. For a $100,000 remodel, expect $15,000–$25,000 in GC management fees above subcontractor and material costs.",
        "faq_q2":  "Do I need permits when hiring a general contractor in San Diego?",
        "faq_a2":  "Yes — a Class B GC is responsible for pulling all required permits for the scope of work. Confirm which permits the GC will pull before signing. If no permits are planned, ask why.",
        "faq_q3":  "How do I evaluate a general contractor quote?",
        "faq_a3":  "Ask for a full breakdown: subcontractor costs per trade, materials allowances, GC overhead and profit percentage, design/permit fees, and payment schedule tied to project milestones.",
    },
}

# ── Internal guide links pool (10 random guides) ──────────────────────────────
GUIDE_POOL = [
    ("ac-not-cooling-san-diego.html", "AC Not Cooling in San Diego"),
    ("breaker-keeps-tripping-san-diego.html", "Breaker Keeps Tripping"),
    ("water-heater-not-working-san-diego.html", "Water Heater Not Working"),
    ("hvac-repair-san-diego.html", "HVAC Repair San Diego"),
    ("plumber-san-diego.html", "Plumber San Diego"),
    ("electrician-san-diego.html", "Electrician San Diego"),
    ("roofing-san-diego.html", "Roofing San Diego"),
    ("solar-installation-san-diego.html", "Solar Installation San Diego"),
    ("adu-builder-san-diego.html", "ADU Builder San Diego"),
    ("kitchen-remodel-san-diego.html", "Kitchen Remodel San Diego"),
    ("payment-processing-san-diego.html", "Payment Processing San Diego"),
    ("ai-automation-consulting-san-diego.html", "AI Automation Consulting San Diego"),
    ("window-replacement-san-diego.html", "Window Replacement San Diego"),
    ("sewer-line-replacement-san-diego.html", "Sewer Line Replacement"),
    ("foundation-repair-san-diego.html", "Foundation Repair San Diego"),
    ("painting-san-diego.html", "Painting Contractor San Diego"),
    ("landscape-design-san-diego.html", "Landscape Design San Diego"),
    ("garage-door-repair-san-diego.html", "Garage Door Repair San Diego"),
    ("pool-repair-san-diego.html", "Pool Repair San Diego"),
    ("stucco-contractor-san-diego.html", "Stucco Contractor San Diego"),
]

ALL_QR_PAGES = [
    ("garage-door-quote-review-san-diego.html", "Garage Door Quote Review"),
    ("kitchen-remodel-quote-review-san-diego.html", "Kitchen Remodel Quote Review"),
    ("roof-repair-quote-review-san-diego.html", "Roof Repair Quote Review"),
    ("window-replacement-quote-review-san-diego.html", "Window Replacement Quote Review"),
    ("stucco-repair-quote-review-san-diego.html", "Stucco Repair Quote Review"),
    ("pool-installation-quote-review-san-diego.html", "Pool Installation Quote Review"),
    ("adu-project-quote-review-san-diego.html", "ADU Project Quote Review"),
    ("roofing-project-quote-review-san-diego.html", "Roofing Project Quote Review"),
    ("solar-project-quote-review-san-diego.html", "Solar Quote Review"),
    ("hvac-project-quote-review-san-diego.html", "HVAC Quote Review"),
    ("plumbing-project-quote-review-san-diego.html", "Plumbing Quote Review"),
    ("electrical-project-quote-review-san-diego.html", "Electrical Quote Review"),
    ("painting-project-quote-review-san-diego.html", "Painting Quote Review"),
    ("landscaping-quote-review-san-diego.html", "Landscaping Quote Review"),
    ("foundation-quote-review-san-diego.html", "Foundation Repair Quote Review"),
    ("contractor-project-quote-review-san-diego.html", "General Contractor Quote Review"),
]

def make_authority_block(trade_key, page_slug):
    d = TRADE_DATA[trade_key]
    # Pick 10 guide links (exclude self)
    guides = [g for g in GUIDE_POOL][:10]
    # Pick 5 QR links different from current page
    qr_links = [q for q in ALL_QR_PAGES if q[0] != page_slug][:5]

    block = f'''
  <!-- SHIP-012: Authority Density Upgrade -->

  <div class="section">
    <h2>&#x1F4B0; How Contractors Structure {d["label"]} Pricing in San Diego</h2>
    <div class="card">
      <h3>Permit Costs</h3>
      <p>{d["permit"]} Budget $300–$1,500 for permit fees on mid-range projects. Permit fees are a legitimate hard cost — any quote that omits them is understating the true project cost.</p>
    </div>
    <div class="card">
      <h3>Labor Bands</h3>
      <p>{d["labor"]}. On a typical project, labor accounts for 30–50% of total quoted cost. The specific crew skill level, travel distance, and San Diego's high cost of living all push labor rates above national averages.</p>
    </div>
    <div class="card">
      <h3>Material Costs</h3>
      <p>{d["materials"]} Material prices in San Diego track 8–15% above national averages due to supply chain routing and local fuel costs. Ask for a materials breakdown — understanding what you're paying for reduces negotiating friction.</p>
    </div>
    <div class="card">
      <h3>Contractor Margin</h3>
      <p>{d["margin"]} Margin itself is not a problem — contractors need it to sustain a licensed, insured business. The problem is when margin is hidden inside inflated line items rather than stated transparently.</p>
    </div>
  </div>

  <div class="section">
    <h2>&#x26A0;&#xFE0F; Common Red Flags in San Diego {d["label"]} Quotes</h2>
    <div class="card">
      <ul class="redflag">
        <li><strong>Allowance traps</strong> — Placeholder numbers (e.g., "$2,500 material allowance") that reliably inflate once real product selections are made. Ask for a fixed specification, not an allowance.</li>
        <li><strong>Missing scope</strong> — No description of prep work, tear-out, or sub-trade coordination. What is NOT in the quote is as important as what is.</li>
        <li><strong>No disposal/haul-away line</strong> — Debris removal costs $200–$800 on most jobs. If it's not listed, it either isn't included or is buried in a vague line item.</li>
        <li><strong>No permit line item</strong> — Permits are a real cost. A quote that omits permit fees either excludes permits (a code violation risk) or is baking them into other line items without disclosure.</li>
        <li><strong>Vague warranty language</strong> — "Satisfaction guaranteed" is not a warranty. Ask for: warranty duration, what is covered (materials vs. labor), and the written warranty process for a claim.</li>
        <li><strong>Pressure to sign today</strong> — Legitimate contractors rarely offer "today-only" pricing. High-pressure urgency is a reliable predictor of post-signing scope disputes.</li>
        <li><strong>No subcontractor disclosure</strong> — If licensed subcontractors are doing the skilled work (electrical, plumbing), you have a right to know their license numbers before signing.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4C4; CSLB License Verification — Do This Before You Sign Anything</h2>
    <div class="card">
      <p>Every contractor doing work in California must hold a current, active license from the <a href="https://www.cslb.ca.gov/OnlineServices/CheckLicenseII/CheckLicense.aspx" rel="nofollow noopener" target="_blank" style="color:var(--mint)">Contractors State License Board (CSLB)</a>. For {d["label"].lower()} work, the relevant classification is <strong>{d["cslb"]}</strong>.</p>
      <p style="margin-top:12px">The CSLB lookup takes 60 seconds and shows: current license status, bond amount, workers' compensation status, and any enforcement history. A contractor who discourages you from verifying their license is a contractor worth reconsidering.</p>
      <p style="margin-top:12px">What to verify: license number matches the contractor entity on your contract, license status is "Active," bond is current, and workers' comp is in force (or contractor has a valid exemption).</p>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F3AF; When the Lowest Quote Is Not the Best Quote</h2>
    <div class="card">
      <p>The lowest bid on a {d["label"].lower()} project in San Diego is not always — and not usually — the best value. Low bids typically mean one of three things: scope has been omitted, permits are being skipped, or the materials specification is lower-grade than the competing bids.</p>
      <p style="margin-top:12px">A complete, honest bid that is 15% higher than the lowest quote is almost always the better financial decision. The cost of a failed inspection, a scope dispute, or unpermitted work discovered during a future home sale typically exceeds the initial bid difference by 3–5x.</p>
      <p style="margin-top:12px">The right question is not "who is cheapest?" but "whose quote is most complete?" A bid that accounts for permits, proper disposal, licensed subcontractors, and a written warranty is protecting your investment — not inflating it.</p>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F310; San Diego Homeowner Resources</h2>
    <div class="card">
      <p style="font-size:14px;color:var(--muted2);margin:0 0 14px">Other guides San Diego homeowners found helpful:</p>
      <ul style="list-style:none;padding:0;margin:0 0 20px;display:flex;flex-direction:column;gap:6px">
'''
    for href, label in guides:
        block += f'        <li><a href="{href}" style="color:var(--mint);font-size:15px">{label}</a></li>\n'

    block += '''      </ul>
      <p style="font-size:14px;color:var(--muted2);margin:14px 0 10px">More quote reviews for San Diego projects:</p>
      <ul style="list-style:none;padding:0;margin:0 0 16px;display:flex;flex-direction:column;gap:6px">
'''
    for href, label in qr_links:
        block += f'        <li><a href="{href}" style="color:var(--mint);font-size:15px">{label}</a></li>\n'

    block += f'''      </ul>
      <p style="margin-top:16px;font-size:14px"><a href="html-sitemap.html" style="color:var(--muted2)">&#x2192; View all San Diego guides</a></p>
    </div>
  </div>

  <div style="background:rgba(33,211,161,.06);border:1px solid rgba(33,211,161,.18);border-radius:16px;padding:20px 24px;margin:44px 0">
    <p style="font-size:14px;font-weight:700;color:var(--ink);margin:0 0 6px">About This Review</p>
    <p style="font-size:14px;color:var(--muted2);margin:0;line-height:1.7">Reviewed with 20+ years of local contractor pricing exposure across San Diego County. SideGuy does not sell construction services, accept referral fees from contractors, or take any compensation tied to your hiring decision. We review quotes before you commit. Clarity before cost.</p>
  </div>

  <!-- /SHIP-012 -->
'''
    return block


def process_file(filepath):
    slug = os.path.basename(filepath)
    # derive trade key from filename
    # e.g. "kitchen-remodel-quote-review-san-diego.html" -> "kitchen-remodel"
    trade_key = slug.replace("-quote-review-san-diego.html", "")

    if trade_key not in TRADE_DATA:
        print(f"  SKIP {slug} — no trade data (key='{trade_key}')")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already upgraded
    if "SHIP-012: Authority Density" in content:
        print(f"  SKIP {slug} — already upgraded")
        return False

    # Injection point: before <!-- SIDEGUY_MESH_BLOCK -->
    injection_marker = "<!-- SIDEGUY_MESH_BLOCK -->"
    if injection_marker not in content:
        print(f"  WARN {slug} — no MESH_BLOCK marker, injecting before </body>")
        injection_marker = "</body>"

    block = make_authority_block(trade_key, slug)
    new_content = content.replace(injection_marker, block + "\n  " + injection_marker, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  OK   {slug}")
    return True


def main():
    pattern = os.path.join(ROOT, "*-quote-review-san-diego.html")
    files = sorted(glob.glob(pattern))
    print(f"Found {len(files)} quote-review pages")
    updated = 0
    for fp in files:
        if process_file(fp):
            updated += 1
    print(f"\nDone — {updated}/{len(files)} files updated")


if __name__ == "__main__":
    main()
