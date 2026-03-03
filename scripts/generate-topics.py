#!/usr/bin/env python3
"""
SideGuy Topic Generator — 10k-Ready Edition
Appends new topics to seo-reserve/manifest.json, then runs build-pages.py.
Rules:
  - Append-only, never overwrites existing topics
  - Deduplication enforced
  - RUN_LIMIT caps new topics per run (safe for scheduled builds)
  - Re-run safe: successive runs pick up where the last left off
"""

import json, os, re, subprocess, sys

MANIFEST  = "seo-reserve/manifest.json"
RUN_LIMIT = 1200   # max new topics to add per run (tune as needed)

# ─────────────────────────────────────────────────────────────────────────────
# Seed data — extend these lists to grow toward 10k topics
# ─────────────────────────────────────────────────────────────────────────────

# 300+ industries
INDUSTRIES = [
    # Trades & Home Services
    "plumbers", "electricians", "HVAC companies", "landscapers",
    "general contractors", "roofing companies", "painting contractors",
    "solar installers", "pest control companies", "pool service companies",
    "window cleaners", "pressure washers", "junk removal companies",
    "carpet cleaners", "tile contractors", "flooring companies",
    "cabinet makers", "custom home builders", "fence companies",
    "garage door companies", "gutter cleaning companies",
    "tree service companies", "irrigation companies",
    "concrete contractors", "masonry contractors", "stucco contractors",
    "drywall contractors", "insulation contractors", "foundation repair companies",
    "waterproofing companies", "siding contractors", "deck builders",
    "patio contractors", "fireplace companies", "chimney sweep companies",
    "appliance repair companies", "locksmith companies", "security companies",
    "moving companies", "storage facilities", "towing companies",
    # Auto
    "auto repair shops", "car dealerships", "car washes", "auto detailers",
    "auto body shops", "tire shops", "oil change shops", "transmission shops",
    "auto glass companies", "auto parts stores",
    # Food & Beverage
    "restaurants", "food trucks", "catering companies", "bakeries",
    "coffee shops", "breweries", "wineries", "distilleries",
    "food distributors", "meal prep businesses", "ghost kitchens",
    "juice bars", "smoothie shops", "ice cream shops", "food manufacturers",
    # Health & Wellness
    "dentists", "chiropractors", "physical therapists", "optometrists",
    "veterinarians", "dermatologists", "plastic surgeons",
    "urgent care clinics", "pharmacies", "medical spas",
    "mental health practices", "occupational therapists",
    "home health agencies", "senior care facilities",
    "acupuncturists", "massage therapists", "personal trainers",
    "yoga studios", "pilates studios", "gyms", "CrossFit gyms",
    "nutrition coaches", "physical rehabilitation centers",
    "pediatric practices", "ob-gyn practices", "cardiology practices",
    "orthopedic practices", "behavioral health clinics",
    "sleep clinics", "IV therapy clinics", "weight loss clinics",
    # Beauty & Personal Care
    "nail salons", "hair salons", "barbershops", "tattoo shops",
    "cosmetic surgery practices", "threading salons", "spa owners",
    "lash studios", "brow studios", "tanning salons", "waxing studios",
    # Professional Services
    "law firms", "accounting firms", "bookkeepers", "financial advisors",
    "mortgage brokers", "insurance agencies", "real estate agents",
    "real estate investors", "property managers", "title companies",
    "escrow companies", "home inspectors", "appraisers",
    "tax preparation services", "HR consultants", "business coaches",
    "life coaches", "executive coaches", "management consultants",
    "IT support companies", "managed service providers",
    "cybersecurity firms", "data recovery services",
    "staffing agencies", "employment agencies", "recruiting firms",
    # Creative & Marketing
    "marketing agencies", "graphic designers", "web designers",
    "social media managers", "copywriters", "videographers",
    "photographers", "branding agencies", "PR agencies",
    "advertising agencies", "SEO agencies", "content agencies",
    "podcast production companies", "animation studios",
    # Education & Coaching
    "tutors", "music schools", "dance studios", "martial arts studios",
    "sports coaches", "driving schools", "language schools",
    "SAT prep companies", "coding bootcamps", "online course creators",
    "child care centers", "preschools", "after school programs",
    # Retail & E-commerce
    "clothing boutiques", "jewelry stores", "gift shops",
    "e-commerce businesses", "dropshippers", "wholesalers",
    "convenience stores", "grocery stores", "farmers markets",
    "sporting goods stores", "toy stores", "book stores",
    "furniture stores", "electronics retailers", "pet stores",
    "flower shops", "art galleries", "antique dealers",
    # Events & Hospitality
    "event planners", "wedding venues", "wedding photographers",
    "wedding caterers", "party rental companies", "DJ services",
    "photo booth companies", "balloon decorators", "floral designers",
    "hotels", "motels", "bed and breakfasts", "vacation rental managers",
    "short term rental hosts", "tour operators", "travel agents",
    # Logistics & Distribution
    "trucking companies", "freight brokers", "logistics companies",
    "courier services", "last mile delivery companies",
    "warehouse operators", "third party logistics companies",
    # Nonprofit & Community
    "nonprofits", "churches", "community organizations",
    "foundations", "trade associations",
    # Specialty
    "printing companies", "sign companies", "embroidery shops",
    "trophy and awards shops", "uniform suppliers",
    "funeral homes", "cremation services", "monument companies",
    "boat dealers", "marine repair shops", "RV dealers",
    "motorcycle dealers", "bicycle shops",
    "gym equipment suppliers", "medical equipment suppliers",
    "veterinary supply companies", "dental supply companies",
]

# 20+ verbs for combinatorial generation
AI_VERBS = [
    "ai automation for",
    "ai tools for",
    "how ai helps",
    "ai scheduling for",
    "ai customer service for",
    "ai lead generation for",
    "ai follow up for",
    "ai workflow for",
    "ai invoicing for",
    "ai booking software for",
    "ai chatbot for",
    "automating operations for",
    "using ai to grow",
    "ai receptionist for",
    "ai intake forms for",
    "ai reputation management for",
    "ai proposal writing for",
    "ai quoting software for",
    "ai dispatch software for",
    "ai marketing automation for",
    "ai review management for",
    "ai employee training for",
]

# San Diego neighborhoods and North County cities
SD_CITIES = [
    "san diego", "chula vista", "la mesa", "el cajon", "escondido",
    "oceanside", "carlsbad", "encinitas", "national city", "santee",
    "lemon grove", "poway", "vista", "san marcos", "spring valley",
    "lakeside", "la jolla", "mission valley", "north park", "hillcrest",
    "point loma", "pacific beach", "mission beach", "clairemont",
    "kearny mesa", "mira mesa", "rancho bernardo", "rancho penasquitos",
    "del mar", "solana beach", "rancho santa fe", "4s ranch",
]

# Operator pain points
OPERATOR_PAIN_POINTS = [
    "how to stop losing leads after hours",
    "how to respond to leads faster",
    "how to stop chasing unpaid invoices",
    "how to reduce no show appointments",
    "how to get more google reviews automatically",
    "how to handle customer complaints faster",
    "how to stop wasting time on admin work",
    "how to reduce payroll costs with automation",
    "how to manage more clients with same staff",
    "how to onboard new customers faster",
    "how to collect payments faster",
    "how to stop missing follow up calls",
    "how to improve customer retention for service business",
    "how to automate referral requests",
    "how to automate upsell offers",
    "how to stop losing business to faster competitors",
    "how to reduce customer acquisition costs",
    "how to handle high call volume without hiring",
    "how to reduce time spent on quotes",
    "how to speed up job scheduling",
    "how to reduce time spent on estimates",
    "how to automate job follow ups",
    "how to get paid faster as a contractor",
    "how to reduce cancellations for service businesses",
    "how to automate maintenance reminders",
    "how to handle last minute cancellations with ai",
    "how to track jobs without spreadsheets",
    "how to manage subcontractors with ai",
    "how to dispatch faster with ai",
    "how to automate customer check ins",
]

# Small business AI use cases
SMALL_BIZ_USE_CASES = [
    "how small businesses automate scheduling",
    "how small businesses automate customer follow up",
    "how ai reduces admin work for small business",
    "how ai improves customer response times for small business",
    "how to use ai for small business marketing",
    "how ai helps small businesses compete with large companies",
    "how to automate social media for small business",
    "how to automate email marketing for small business",
    "how to automate appointment reminders",
    "how to automate review requests for local business",
    "how to automate payroll for small business",
    "how to automate accounts receivable",
    "how to automate accounts payable",
    "how to automate expense tracking",
    "how to automate employee onboarding",
    "how to use ai for hiring",
    "how to automate sales pipeline",
    "how to automate project management",
    "how to automate inventory management",
    "how to automate purchase orders",
    "how to automate vendor communications",
    "how to automate contract management",
    "how to automate compliance reporting",
    "how to automate customer onboarding",
    "how to automate refund processing",
    "how to automate delivery notifications",
    "how to automate IT support tickets",
    "how to automate helpdesk responses",
    "how to automate meeting scheduling",
    "how to automate quote generation",
    "how to automate proposal writing with ai",
    "how ai handles customer complaints automatically",
    "how to build an ai receptionist for small business",
    "how to use ai for local seo",
    "how to automate google review responses",
    "how ai agents handle inbound leads",
    "how to generate leads with ai automation",
    "how to reduce overhead with ai tools",
    "how to scale a service business with ai",
    "how to reduce employee burnout with ai tools",
]

# Payments verticals
PAYMENTS_TOPICS = [
    "how small businesses reduce credit card fees",
    "solana payments for local businesses",
    "crypto payment processing for local businesses",
    "how merchants accept crypto payments",
    "future of payment rails for small businesses",
    "how to accept usdc payments",
    "how to accept solana payments",
    "how to reduce stripe fees",
    "stripe alternatives for small business",
    "crypto merchant processing explained",
    "how blockchain payments work for merchants",
    "stablecoin merchant payments explained",
    "usdc vs stripe for small business",
    "how to get paid in crypto without volatility",
    "crypto payroll for small business",
    "how to convert crypto to cash same day",
    "accepting bitcoin payments without risk",
    "low fee payment processing for restaurants",
    "low fee payment processing for contractors",
    "low fee payment processing for service businesses",
    "low fee payment processing for subscription businesses",
    "low fee payment processing for medical practices",
    "low fee payment processing for ecommerce",
    "low fee payment processing for high risk businesses",
    "low fee payment processing for event businesses",
    "how to avoid chargeback fees",
    "how to reduce payment processing overhead",
    "how crypto reduces transaction fees",
    "web3 payments for main street businesses",
    "how solana makes payments cheap and fast",
    "how to set up a crypto payment terminal",
    "crypto payment gateway comparison",
    "best crypto payment processors for small business",
    "how to accept payments on solana",
    "how to use phantom wallet for business payments",
    "how to use coinbase commerce for small business",
    "how to invoice clients in crypto",
    "should small businesses accept crypto",
    "risks of accepting crypto payments",
    "benefits of accepting crypto payments",
    "how to handle crypto taxes for small business",
    "crypto accounting for small business",
    "crypto bookkeeping for merchants",
    "how restaurants can save on payment fees",
    "how food trucks accept crypto payments",
    "how contractors get paid in crypto",
    "how freelancers accept crypto",
    "how to accept international payments without fees",
    "cross border payments for small business",
    "how to reduce payment friction for customers",
    "contactless crypto payments for retail",
    "qr code crypto payments for local business",
    "apple pay alternatives for small business",
    "ach payments vs credit cards for small business",
    "how to reduce effective rate for credit card processing",
    "how to audit your payment processor fees",
    "interchange plus pricing explained for small business",
    "flat rate vs interchange plus card processing",
    "how to negotiate credit card processing rates",
    "best payment processor for contractors",
    "best payment processor for restaurants",
    "best payment processor for medical offices",
    "best payment processor for ecommerce",
]

# San Diego local topics
SAN_DIEGO_LOCAL = [
    "san diego ai consulting for small business",
    "ai automation for san diego contractors",
    "crypto payment consulting san diego",
    "reduce credit card fees san diego business",
    "ai automation services san diego",
    "san diego small business automation",
    "san diego crypto payment processing",
    "hire an ai consultant in san diego",
    "san diego tech consulting for operators",
    "ai tools for san diego restaurants",
    "ai tools for san diego real estate",
    "ai automation for san diego property managers",
    "ai automation for san diego law firms",
    "ai automation for san diego medical offices",
    "ai automation for san diego plumbers",
    "ai automation for san diego electricians",
    "ai automation for san diego roofing companies",
    "ai automation for san diego cleaning companies",
    "ai automation for san diego landscapers",
    "ai automation for san diego car dealerships",
    "cryptocurrency payments san diego restaurant",
    "solana payments san diego small business",
    "reduce stripe fees san diego",
    "local business automation san diego",
    "small business technology help san diego",
    "san diego operator ai tools",
    "san diego startup automation consulting",
    "ai intake forms for san diego medical offices",
    "automated scheduling for san diego businesses",
    "san diego crypto merchant account",
    "best payment processing for san diego restaurants",
    "how san diego businesses reduce overhead with ai",
    "san diego business efficiency consulting",
]

# Future tech topics
FUTURE_TECH = [
    "how ai agents will help small businesses",
    "future of ai automation for operators",
    "how businesses deploy ai workflows",
    "how ai copilots help local companies",
    "how agentic ai changes small business operations",
    "what is an ai agent for business",
    "how to deploy an ai agent for customer service",
    "how ai phones answer calls for small business",
    "how ai reads contracts for small business",
    "how ai drafts proposals automatically",
    "how ai scores leads automatically",
    "how ai follows up with prospects automatically",
    "how ai handles billing disputes",
    "how ai manages social media automatically",
    "how ai analyzes business data for owners",
    "how ai predicts slow seasons for small business",
    "how ai helps with cash flow forecasting",
    "how ai prevents chargebacks",
    "how businesses use gpt for operations",
    "how businesses use claude for operations",
    "how to build an ai employee for your business",
    "no code ai tools for small business owners",
    "low cost ai tools for local business",
    "how to get started with ai for free",
    "ai automation roi for small business",
    "how to measure results of ai automation",
    "how to pick an ai automation vendor",
    "questions to ask an ai consultant",
    "red flags when hiring an ai consultant",
    "how to avoid bad ai automation vendors",
    "what ai cannot do for small business",
    "how to test ai before buying",
    "how to pilot ai automation safely",
    "how ai reduces cost per lead for service businesses",
    "how ai reduces no shows for service businesses",
    "how ai increases repeat customers",
    "how ai improves google reviews automatically",
    "how ai helps with employee retention",
    "how ai writes job descriptions",
    "how ai screens job applicants",
]

# ─────────────────────────────────────────────────────────────────────────────
# Combinatorial generator
# ─────────────────────────────────────────────────────────────────────────────

def generate_all_topics():
    topics = set()

    # AI verbs × all industries
    for verb in AI_VERBS:
        for industry in INDUSTRIES:
            topics.add(f"{verb} {industry}")

    # San Diego city × top industries × two patterns
    for city in SD_CITIES[:15]:   # top 15 SD cities to keep volume manageable
        for industry in INDUSTRIES[:60]:
            topics.add(f"ai automation for {industry} in {city}")

    # Pre-built curated lists
    for t in SMALL_BIZ_USE_CASES + PAYMENTS_TOPICS + SAN_DIEGO_LOCAL \
           + FUTURE_TECH + OPERATOR_PAIN_POINTS:
        topics.add(t)

    return topics


def normalize(topic):
    return re.sub(r'\s+', ' ', topic.strip().lower())


def main():
    with open(MANIFEST) as f:
        data = json.load(f)

    existing = {normalize(t) for t in data["topics"]}
    print(f"Existing topics in manifest: {len(existing)}")

    raw        = generate_all_topics()
    new_topics = sorted(t for t in raw if normalize(t) not in existing)
    print(f"New unique topics available: {len(new_topics)}")

    if not new_topics:
        print("Nothing to add — manifest is up to date.")
        return

    # Apply run limit
    batch = new_topics[:RUN_LIMIT]
    print(f"Adding {len(batch)} topics this run (RUN_LIMIT={RUN_LIMIT}).")

    data["topics"].extend(batch)
    with open(MANIFEST, "w") as f:
        json.dump(data, f, indent=2)
    print(f"manifest.json now has {len(data['topics'])} topics total.")
    if len(new_topics) > RUN_LIMIT:
        remaining = len(new_topics) - RUN_LIMIT
        print(f"  {remaining} topics remain — will be added on the next run.")

    # Run the page builder (which also regenerates sitemap)
    builder = os.path.join(os.path.dirname(__file__), "build-pages.py")
    result  = subprocess.run(["python3", builder], check=True)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

