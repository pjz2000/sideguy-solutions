#!/usr/bin/env python3
"""
SHIP027 — Clarity Layer Upgrade
Replace <main> content in 15 high-intent pages with the
SideGuy Clarity Layer template, customized per topic.

Keeps: <head>, CSS, nav, breadcrumbs, right rail, floating PJ, scripts.
Replaces: Everything between <main ...> and </main>.
"""

import re
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path("/workspaces/sideguy-solutions")

# ─────────────────────────────────────────────
# PAGE CONTENT DEFINITIONS
# ─────────────────────────────────────────────

PAGES = {

    # ── HVAC ──────────────────────────────────

    "hvac-repair-san-diego.html": {
        "h1": "HVAC Repair in San Diego — What to Check First",
        "hook": "Before you call anyone for HVAC repair, check these three things. Most visits are avoidable — and the ones that aren't deserve the right technician.",
        "quick_answer": "Most HVAC problems in San Diego fall into three buckets: thermostat or electrical issues (often free to fix yourself), refrigerant or mechanical failure (needs a pro), or ductwork problems (sometimes urgent, sometimes not). A diagnostic visit typically runs $75–$150. Repair costs range from $150 for a capacitor to $1,500+ for a compressor. If your system is 15+ years old and the repair is over $1,000, replacement math starts to make sense.",
        "need_if": [
            "Your AC stopped cooling and resetting the thermostat or breaker didn't help",
            "You hear grinding, clicking, or banging from the unit",
            "Your energy bill spiked 30%+ with no obvious cause",
        ],
        "dont_need_if": [
            "Your AC is running but you want it colder — check your filter and thermostat settings first",
            "It's your first summer in San Diego and you're not sure what's normal — it probably is",
            "A neighbor told you to get a tune-up — annual maintenance is fine, but don't panic-buy",
        ],
        "cta": "Text PJ a photo of your thermostat and a quick description of what's happening. I'll tell you if it's a DIY fix, a real repair, or something you can wait on.",
        "faq": [
            ("How much does HVAC repair cost in San Diego?", "A diagnostic visit is $75–$150. Common repairs: capacitor ($150–$300), fan motor ($300–$600), compressor ($1,000–$2,500). If the quote feels high, get a second opinion before saying yes."),
            ("Should I repair or replace my AC unit?", "General rule: if the repair costs more than 50% of a new system and the unit is 12+ years old, replacement usually wins on lifetime cost. But context matters — text PJ and we'll walk through the math."),
            ("How do I find a good HVAC tech in San Diego?", "Look for someone licensed (C-20 in California), insured, and willing to explain the diagnosis before quoting. Avoid anyone who quotes a replacement without testing the existing system first."),
        ],
    },

    "ac-not-cooling-san-diego.html": {
        "h1": "AC Not Cooling in San Diego — What to Check Before You Call",
        "hook": "Your AC is running but the house won't cool down. Before you spend money on a service call, try these steps — about half the time, this solves it.",
        "quick_answer": "When your AC runs but doesn't cool, the most common causes are a dirty air filter (restricts airflow), a tripped breaker on the outdoor unit, or a thermostat set incorrectly. Check those three things first. If none of them fix it, you likely have a refrigerant leak, a bad capacitor, or a failing compressor — all of which need a licensed tech.",
        "need_if": [
            "You checked the filter, breaker, and thermostat and it's still not cooling",
            "The outdoor unit isn't spinning or is making unusual sounds",
            "You see ice forming on the refrigerant lines or indoor coil",
        ],
        "dont_need_if": [
            "You haven't checked your air filter yet — do that first, it's the #1 cause",
            "Your thermostat is set to 'ON' instead of 'AUTO' — switch it and wait 15 minutes",
            "It's 95°+ outside and your AC can't keep up — most systems are designed for a 20° differential, not Arctic temps",
        ],
        "cta": "Snap a photo of your thermostat and the outdoor unit. Text it to PJ and I'll walk you through what's likely happening — before you pay for a diagnosis.",
        "faq": [
            ("Why is my AC running but not cooling?", "Top causes: clogged filter, low refrigerant, bad capacitor, or a failing compressor. Start with the filter. If that's clean and the outdoor unit is running normally, call a tech — it's likely refrigerant or electrical."),
            ("How much does it cost to fix an AC that's not cooling?", "If it's a filter or thermostat issue: free. Capacitor: $150–$300. Refrigerant recharge: $200–$500. Compressor: $1,200–$2,500. The diagnostic visit itself is typically $75–$150."),
            ("Is it worth fixing a 15-year-old AC in San Diego?", "It depends on the repair. A $200 capacitor? Absolutely. A $2,000 compressor on a unit past its rated lifespan? Usually not — a new system gets you better efficiency and a warranty."),
        ],
    },

    "hvac-repair-san-diego-what-to-know.html": {
        "h1": "HVAC Repair in San Diego — What You Need to Know",
        "hook": "San Diego HVAC isn't like the rest of the country. Coastal humidity, inland heat, and marine-layer corrosion all change the equation. Here's what actually matters.",
        "quick_answer": "San Diego's HVAC needs are specific: coastal areas deal with salt corrosion on outdoor units, inland areas (Escondido, El Cajon) run hard in summer, and everywhere deals with marine layer humidity. A good HVAC tech here understands these differences. Budget $150–$400 for typical repairs, $5,000–$12,000 for full replacement with installation.",
        "need_if": [
            "Your unit is struggling to keep up during San Diego's September heat waves",
            "You live near the coast and your outdoor unit has visible corrosion",
            "Your system is more than 12 years old and repair costs are creeping up each year",
        ],
        "dont_need_if": [
            "You just moved to San Diego from somewhere with harsh winters — your system probably runs less here, not more",
            "Your landlord is responsible for HVAC maintenance — check your lease first",
            "You're being sold a whole-home air purification add-on — most San Diego homes don't need it",
        ],
        "cta": "Not sure what kind of HVAC system fits your San Diego home? Text PJ what you've got now and where you live — I'll tell you what actually matters for your area.",
        "faq": [
            ("Do I need a heat pump in San Diego?", "San Diego's mild climate makes heat pumps a strong fit. They cost more upfront ($7,000–$14,000 installed) but handle both heating and cooling efficiently. For most San Diego homes, they save money over 10 years vs. a traditional split system."),
            ("How often should I service my HVAC in San Diego?", "Once a year is standard. If you're coastal, twice — salt air accelerates corrosion on outdoor coils and electrical connections. Focus on coil cleaning and refrigerant checks."),
            ("What HVAC brands work best in San Diego's climate?", "Carrier, Trane, and Lennox all perform well here. More important than brand: proper sizing (Manual J calculation) and quality installation. A mediocre brand installed well beats a premium brand installed poorly."),
        ],
    },

    # ── PLUMBING / HOME ──────────────────────

    "plumbing-emergency-or-can-it-wait-san-diego.html": {
        "h1": "Plumbing Emergency or Can It Wait? — San Diego Guide",
        "hook": "Not every plumbing problem is a midnight emergency. Some are — and waiting makes them worse. Here's how to tell the difference.",
        "quick_answer": "True plumbing emergencies: burst pipes, sewage backup, gas smell near water heater, or water flooding into a living space. These need a plumber now. Everything else — slow drains, dripping faucets, running toilets, low water pressure — can wait for a weekday appointment and save you 50%+ on after-hours fees.",
        "need_if": [
            "Water is actively flooding into your home or you can't shut it off",
            "You smell sewage or gas — this is a safety issue, not just plumbing",
            "Your water heater is leaking from the bottom or making popping sounds",
        ],
        "dont_need_if": [
            "A faucet is dripping — annoying but not urgent, schedule it for next week",
            "A drain is slow — try a plunger or enzymatic cleaner before calling anyone",
            "Your toilet is running — the flapper costs $5 at Home Depot and 10 minutes to replace",
        ],
        "cta": "Not sure if your plumbing issue is urgent? Text PJ a quick description — I'll tell you if you need someone tonight or if Monday is fine.",
        "faq": [
            ("How much does an emergency plumber cost in San Diego?", "After-hours plumbing calls typically run $250–$500 just for the visit, plus parts and labor. Weekday rates are usually $150–$250 for the same call. If it can wait, wait."),
            ("How do I shut off my water in an emergency?", "Find your main shut-off valve — usually near the front of your home where the water line enters, or near the water meter at the street. Turn it clockwise. Every homeowner should know where this is before they need it."),
            ("When should I call a plumber vs. try DIY?", "DIY-friendly: clogged drains (plunger), running toilet (flapper), dripping faucet (cartridge). Call a pro: anything behind a wall, sewer line issues, water heater problems, or anything involving gas lines."),
        ],
    },

    "electric-bill-too-high.html": {
        "h1": "Electric Bill Too High? — What San Diego Homeowners Can Actually Do",
        "hook": "Your SDG&E bill spiked and you want to know why. It's probably not one big thing — it's usually three small things stacking up.",
        "quick_answer": "In San Diego, high electric bills are usually caused by: old or poorly maintained HVAC running too hard, time-of-use rate plans charging peak rates (4–9 PM), and vampire loads from devices you forgot about. Most households can cut 15–25% by adjusting usage timing, replacing air filters monthly, and checking for rate plan mismatches with SDG&E.",
        "need_if": [
            "Your bill jumped 40%+ and your usage habits haven't changed",
            "You're on a time-of-use plan and don't know what that means for your daily habits",
            "Your HVAC system is running constantly even in mild weather",
        ],
        "dont_need_if": [
            "Your bill went up $20–$30 in summer — that's normal seasonal variation in San Diego",
            "You recently added a hot tub, EV charger, or pool pump — the increase is expected",
            "Everyone on your street had the same increase — it's likely a rate change, not your home",
        ],
        "cta": "Text PJ your last two SDG&E bills (phone photo is fine). I'll compare the usage and rate breakdown and tell you exactly where the spike is coming from.",
        "faq": [
            ("Why is SDG&E so expensive?", "SDG&E has some of the highest rates in the country. Time-of-use rates mean electricity costs 2–3x more during peak hours (4–9 PM). Shifting heavy usage to off-peak hours is the single biggest money-saver."),
            ("Should I get solar to lower my electric bill?", "Solar makes financial sense for most San Diego homeowners — the sunshine hours are there. But the math depends on your roof, shading, current usage, and whether you buy or lease. Don't let a salesperson rush you."),
            ("What uses the most electricity in my home?", "In order: HVAC (40–50%), water heater (14–18%), appliances and electronics (15–20%), lighting (10%). Focus on the big two first."),
        ],
    },

    "who-do-i-call.html": {
        "h1": "Who Do I Call When I Don't Know What to Do?",
        "hook": "You've got a problem — something broke, something confusing showed up, or you're stuck between options. You don't even know which kind of professional handles this. Start here.",
        "quick_answer": "Most people aren't sure whether they need a plumber, electrician, HVAC tech, contractor, or someone else entirely. SideGuy exists for exactly this moment. Text PJ with a description of the problem and we'll route you to the right type of professional — or tell you it's a DIY fix.",
        "need_if": [
            "Something broke and you genuinely don't know who handles it",
            "You've gotten conflicting advice from the internet, neighbors, or a contractor",
            "You're about to spend money but aren't confident it's the right move",
        ],
        "dont_need_if": [
            "You already know what kind of pro you need — just look for licensed contractors with reviews",
            "It's a pure DIY question — YouTube is faster for that",
            "You're comparison-shopping and already have quotes — you're past the 'who do I call' stage",
        ],
        "cta": "Describe the problem in one or two sentences. Text PJ and you'll hear back with: who to call, what to expect, and what NOT to do in the meantime.",
        "faq": [
            ("Is SideGuy a referral service?", "No. SideGuy is a guidance layer. We help you understand your problem before you hire anyone. We don't take referral fees or push specific companies."),
            ("How fast will PJ respond?", "Usually within minutes during business hours, same day otherwise. It's a real human — not a bot, not a call center."),
            ("Does texting PJ cost anything?", "No. The initial guidance is free. If your situation needs deeper research or ongoing support, we'll tell you upfront."),
        ],
    },

    # ── PAYMENTS / STRIPE ────────────────────

    "Best-Payment-Processing-San-Diego.html": {
        "h1": "Best Payment Processing in San Diego — Honest Breakdown",
        "hook": "Every processor claims to be the cheapest. None of them are — for everyone. The best processor depends on your volume, ticket size, and type of business.",
        "quick_answer": "For most San Diego small businesses: Square or Stripe works fine under $10K/month in volume. Above that, interchange-plus processors (like Helcim or Payment Depot) save real money. If you're a restaurant or retail shop doing $20K+/month, you should be on interchange-plus and paying under 2.5% effective. If you're paying more than 3.5% on any plan, you're overpaying.",
        "need_if": [
            "You process more than $10,000/month and haven't reviewed your rates in over a year",
            "You're paying flat-rate pricing (2.9% + 30¢) on high volume — that's costing you",
            "You're locked into a contract with early termination fees and want to switch",
        ],
        "dont_need_if": [
            "You're a solo freelancer doing $2K/month — Square is fine, don't overthink it",
            "You just started your business and haven't processed your first $1,000 yet — use anything simple and revisit later",
            "Someone is cold-calling you about rates — those salespeople add fees you don't see upfront",
        ],
        "cta": "Text PJ your last processing statement (block out sensitive info). I'll tell you your effective rate, whether you're overpaying, and what a better setup would look like for your business.",
        "faq": [
            ("What's a fair credit card processing rate?", "2.5–2.9% + $0.30/transaction is standard for flat-rate. If you process over $10K/month, interchange-plus pricing gets you closer to 2.0–2.5% effective. Above 3.5%, you're overpaying."),
            ("Should I use Square, Stripe, or something else?", "Square: best for in-person retail and restaurants under $10K/month. Stripe: best for online and tech businesses. Above $10K/month, look at Helcim, Payment Depot, or traditional merchant accounts for lower rates."),
            ("Can I negotiate my processing fees?", "Yes, if you process $5K+/month. Bring 3 months of statements and a competitor quote. Ask for interchange-plus pricing, no monthly minimums, and month-to-month terms."),
        ],
    },

    "stripe-alternatives-for-small-business-san-diego.html": {
        "h1": "Stripe Alternatives for Small Business — San Diego Guide",
        "hook": "Stripe is great — until it isn't. If you're hitting volume, need in-person payments, or want lower fees, here's what to actually consider.",
        "quick_answer": "Stripe charges 2.9% + 30¢ per online transaction. That's fair for startups but expensive at scale. If you process over $10K/month, alternatives like Helcim (interchange-plus, no monthly fee), Square (better for in-person), or Payment Depot (flat monthly fee + interchange) can save $200–$800/month depending on your volume.",
        "need_if": [
            "You're paying Stripe $500+/month in fees and haven't compared alternatives",
            "You need in-person payment (Stripe Terminal works but Square does it better)",
            "Stripe froze your account or holds funds — this is common and frustrating",
        ],
        "dont_need_if": [
            "You're a developer who already has Stripe integrated and processes under $5K/month — the switching cost isn't worth it",
            "You only sell online to US customers and Stripe works fine — don't fix what isn't broke",
            "Someone is pushing you toward a 'better deal' with a long-term contract — that's usually worse",
        ],
        "cta": "Text PJ your monthly processing volume and whether you sell online, in-person, or both. I'll tell you if switching makes sense and what the actual savings would be.",
        "faq": [
            ("Why do people leave Stripe?", "Three main reasons: high fees at volume, account freezes/holds with no warning, and limited in-person payment options. Stripe is built for developers and online — it's not ideal for every business type."),
            ("What's the cheapest Stripe alternative?", "For online: Helcim (interchange-plus, no markup games). For in-person: Square (free hardware, simple). For high volume: Payment Depot (flat $79/month + interchange only). 'Cheapest' depends on how and how much you sell."),
            ("Is switching from Stripe hard?", "Technically, yes — if you've built custom integrations. Practically, most small businesses use Stripe's hosted checkout and can switch in a day. If you have a developer, a full migration takes 1–2 weeks."),
        ],
    },

    "stripe-alternatives-san-diego.html": {
        "h1": "Stripe Alternatives — What San Diego Businesses Should Know",
        "hook": "Picking a payment processor shouldn't require a finance degree. Here's a clear look at what's out there beyond Stripe and when switching actually makes sense.",
        "quick_answer": "Stripe is a solid default but not the best fit for every San Diego business. If you run a restaurant, retail shop, or service business doing mostly in-person transactions, Square is usually simpler and cheaper. For high-volume online businesses, Helcim or Stax save on interchange. The right answer depends on where you sell, how much you process, and whether you need hardware.",
        "need_if": [
            "Your business model has shifted (more in-person sales, subscriptions, or invoicing)",
            "Stripe's 2.9% + 30¢ is eating into thin margins on low-ticket items",
            "You're adding physical locations or mobile payments and Stripe Terminal feels clunky",
        ],
        "dont_need_if": [
            "Stripe is working fine and your volume is under $5K/month",
            "You're mid-launch and shouldn't be optimizing fees yet — get revenue first",
            "A sales rep is pressuring you with 'exclusive rates' — read the fine print",
        ],
        "cta": "Text PJ your business type (restaurant, SaaS, retail, etc.) and monthly volume. I'll tell you the two best options and what you'd save on each.",
        "faq": [
            ("Which payment processor has the lowest fees?", "It depends on volume. Under $5K/month: Square or Stripe (flat-rate is simpler). $5K–$25K/month: Helcim (interchange-plus). Over $25K/month: Payment Depot or Stax (flat monthly + interchange only)."),
            ("Do I need a merchant account in 2026?", "Traditional merchant accounts still offer the best rates for high-volume businesses ($50K+/month). For most small businesses under $25K/month, aggregators like Square, Stripe, and Helcim are simpler and have no setup process."),
            ("What about PayPal for business payments?", "PayPal works for invoicing and occasional payments but has the highest effective rates (2.99% + 49¢). It's not a primary processor — it's a supplementary option for customer convenience."),
        ],
    },

    "stripe-fees-for-small-business-san-diego.html": {
        "h1": "Stripe Fees for Small Business — What You're Actually Paying",
        "hook": "Stripe's pricing looks simple: 2.9% + 30¢. But the actual cost depends on your average transaction size, and most businesses don't realize how much that fixed 30¢ adds up.",
        "quick_answer": "Stripe charges 2.9% + $0.30 per successful transaction. On a $100 sale, that's $3.20 (3.2% effective). On a $10 sale, it's $0.59 (5.9% effective). The smaller your average ticket, the more that 30¢ fixed fee hurts. Additional costs: international cards (+1.5%), currency conversion (+1%), disputes ($15 each), Stripe Radar fraud detection (included, but chargebacks aren't).",
        "need_if": [
            "Most of your transactions are under $20 and you're losing 5–6% per sale to processing",
            "You process international payments regularly and the extra 1.5% is adding up",
            "You've never actually calculated your effective processing rate — just trusted the 2.9% headline",
        ],
        "dont_need_if": [
            "Your average transaction is $100+ and 3.2% effective feels reasonable for the convenience",
            "You process under $3K/month and the total fee amount is small regardless of rate",
            "You're comparing Stripe to processors with hidden monthly fees that wipe out the rate difference",
        ],
        "cta": "Text PJ your average transaction size and monthly volume. I'll calculate your actual effective Stripe rate and tell you if there's a cheaper option worth switching to.",
        "faq": [
            ("What's Stripe's actual fee per transaction?", "2.9% + $0.30 for US cards. Add 1.5% for international cards, 1% for currency conversion. Disputes cost $15 each. Stripe Connect, billing, and invoicing have additional fees depending on the product."),
            ("Is Stripe cheaper than Square?", "For online sales: similar pricing. For in-person sales: Square charges 2.6% + $0.10, which beats Stripe's in-person rate of 2.7% + $0.05 on tickets under $30. Square also provides free hardware to start."),
            ("How do I reduce my Stripe fees?", "Process more in-person (lower rates). Increase average ticket size. Negotiate volume pricing if you process $80K+/month. Or switch to interchange-plus pricing through a different processor."),
        ],
    },

    "stripe-fees-calculator.html": {
        "h1": "Stripe Fees Calculator — See What You're Really Paying",
        "hook": "Stop guessing. Plug in your numbers and see exactly how much Stripe takes from each sale — and whether a different processor would save you money.",
        "quick_answer": "Here's the math: Stripe takes 2.9% + $0.30 per successful US card transaction. On a $50 sale, that's $1.75 (3.5% effective). On a $200 sale, that's $6.10 (3.05% effective). The breakeven point where Stripe's per-transaction model becomes more expensive than interchange-plus pricing is typically around $8,000–$12,000/month depending on your average ticket size.",
        "need_if": [
            "You want to know your exact processing cost per sale, not just the headline rate",
            "You're comparing Stripe to other processors and need real numbers",
            "Your accountant asked about processing costs and you don't have a clear answer",
        ],
        "dont_need_if": [
            "You already track processing costs and know you're paying under 3% effective",
            "You process under $2K/month — the total fee difference between processors is negligible",
            "You're already on interchange-plus pricing — you're past the Stripe flat-rate stage",
        ],
        "cta": "Text PJ your monthly volume and average ticket size. I'll run the numbers across Stripe, Square, and Helcim — and show you the exact dollar difference.",
        "faq": [
            ("How do I calculate my Stripe fees?", "Formula: (transaction amount × 0.029) + $0.30 = fee per transaction. Multiply by your monthly transaction count. Example: 500 transactions at $40 average = $870/month in Stripe fees."),
            ("At what volume should I leave Stripe?", "When you're processing $8,000–$12,000/month consistently, interchange-plus pricing from Helcim, Stax, or a merchant account typically saves $100–$300/month. Below $5K/month, the savings usually aren't worth the switching effort."),
            ("Does Stripe charge monthly fees?", "Standard Stripe: no monthly fee. Stripe Premium (custom pricing): requires negotiation at $80K+/month. But compare carefully — some 'no monthly fee' competitors charge through higher per-transaction rates."),
        ],
    },

    "best-payment-processor-for-restaurants-san-diego.html": {
        "h1": "Best Payment Processor for Restaurants — San Diego",
        "hook": "Restaurants have specific payment needs: tips, split checks, kitchen ticket integration, and high transaction volume on thin margins. The right processor matters here.",
        "quick_answer": "For most San Diego restaurants: Square for Restaurants is the best starting point — free POS software, integrated tipping, and 2.6% + $0.10 in-person. If you process over $15K/month, Toast or a traditional merchant account with interchange-plus pricing saves serious money. Avoid any processor that requires a multi-year contract.",
        "need_if": [
            "You're opening a new restaurant and need POS + payment processing together",
            "Your current processor charges more than 3% effective on in-person transactions",
            "You need tableside payment, online ordering integration, or tip management",
        ],
        "dont_need_if": [
            "You run a ghost kitchen or food truck doing under $8K/month — Square or Stripe is fine",
            "You're happy with your Toast setup — switching POS systems mid-operation is painful",
            "A payment rep is offering 'restaurant-specific rates' — check if there are hidden monthly fees",
        ],
        "cta": "Text PJ your restaurant type (sit-down, counter service, food truck), monthly volume, and current processor. I'll tell you if you're overpaying and what to switch to.",
        "faq": [
            ("Is Square good for restaurants?", "Yes, for restaurants under $15K/month. The free POS is solid, tipping and split checks work well, and 2.6% + $0.10 is competitive. Above $15K/month, you should negotiate volume rates or switch to interchange-plus."),
            ("What about Toast?", "Toast is built for restaurants and has strong features: KDS integration, online ordering, and detailed reporting. But they lock you into their hardware and contracts can be rigid. Best for mid-to-high volume sit-down restaurants."),
            ("How do I handle tips with payment processing?", "Square, Toast, and Clover all handle tip adjustment automatically. Make sure your processor doesn't charge the processing fee on the tip amount (some do) — this adds up fast."),
        ],
    },

    "best-payment-processor-for-contractors-san-diego.html": {
        "h1": "Best Payment Processor for Contractors — San Diego",
        "hook": "Contractors deal with big invoices, irregular payment timing, and customers who prefer checks. Here's how to get paid faster without losing margin.",
        "quick_answer": "For San Diego contractors: Square Invoices or Stripe Invoicing handles online payments and deposits. For jobs over $1,000, ACH transfers (bank-to-bank) save 2–3% vs. credit card fees. Jobber or Housecall Pro combine scheduling, invoicing, and payments in one platform. Avoid giving discounts for cash — set up ACH instead.",
        "need_if": [
            "You're still chasing checks and want customers to pay digitally",
            "Big invoices ($2,000+) are eating 3% in credit card fees",
            "You want to collect deposits online before starting a job",
        ],
        "dont_need_if": [
            "All your clients pay by check within 30 days — the system works, keep it simple",
            "You do fewer than 10 jobs per month — a basic Square link is enough",
            "Someone is selling you a contractor-specific POS terminal — you don't need hardware",
        ],
        "cta": "Text PJ your average invoice size and how clients currently pay you. I'll recommend the setup that gets you paid fastest with the lowest fees.",
        "faq": [
            ("Should contractors accept credit cards?", "Yes — it speeds up payment by 2–3 weeks on average. But for invoices over $1,000, offer ACH as the primary option (0–1% fee) and credit card as a convenience option (2.9% fee). Most customers will choose ACH."),
            ("What's the best invoicing tool for contractors?", "Square Invoices (free, simple) for basic needs. Jobber or Housecall Pro ($40–$70/month) if you want scheduling, estimates, and payments in one place. QuickBooks if your accountant already uses it."),
            ("How do I collect deposits for jobs?", "Square and Stripe both let you send a payment link for a deposit amount. Set a policy (25–50% deposit) and include it in your estimate. It protects both sides."),
        ],
    },

    "best-payment-processor-for-medical-offices-san-diego.html": {
        "h1": "Best Payment Processor for Medical Offices — San Diego",
        "hook": "Medical payment processing has specific rules: copay collection, HIPAA considerations, and patient financing. Most generic advice doesn't apply to you.",
        "quick_answer": "Medical offices need HIPAA-compliant payment processing — not every processor qualifies. Square for Healthcare, Stripe (with BAA), and Rectangle Health are purpose-built options. For San Diego practices, the priority is usually: fast copay collection at check-in, patient financing for larger balances, and statement automation to reduce AR.",
        "need_if": [
            "You're collecting copays manually and chasing unpaid balances",
            "Your current processor isn't HIPAA-compliant (or you're not sure)",
            "You want to offer patient financing for procedures over $500",
        ],
        "dont_need_if": [
            "Your EHR already has integrated payments and it's working — don't add complexity",
            "You're a solo practitioner seeing 5–10 patients per day — Square with a reader is sufficient",
            "A payment company is promising 'healthcare-specific rates' — the rates are the same, they just add compliance features",
        ],
        "cta": "Text PJ your practice type, EHR system, and biggest payment headache. I'll tell you the best processor that integrates with what you already use.",
        "faq": [
            ("Does payment processing need to be HIPAA-compliant?", "Yes, if any patient health information is transmitted with the payment (which is common with patient portals and statement systems). Your processor should sign a Business Associate Agreement (BAA). Square, Stripe, and Rectangle Health all offer this."),
            ("How do I reduce unpaid patient balances?", "Collect copays at check-in (not after), offer payment plans for balances over $200, and send automated text/email statements. Moving from paper statements to digital reduces AR by 20–40% for most practices."),
            ("Should my medical office use Square or a dedicated healthcare processor?", "Square works for small practices with simple copay collection. Rectangle Health or Collectly is better for practices that need patient portal payments, automated statements, and financing integration."),
        ],
    },

    "best-payment-processor-for-ecommerce-san-diego.html": {
        "h1": "Best Payment Processor for Ecommerce — San Diego",
        "hook": "Online selling means every percentage point of processing fees comes directly out of your margin. The right processor depends on where you sell, how much, and to whom.",
        "quick_answer": "For most San Diego ecommerce businesses: Stripe is the default for custom sites and developer-friendly setups. Shopify Payments avoids third-party transaction fees if you're on Shopify. PayPal should be offered as a checkout option (customers trust it) but shouldn't be your primary processor. If you sell over $15K/month online, Helcim's interchange-plus pricing saves 0.3–0.7% per transaction.",
        "need_if": [
            "You sell online and processing fees exceed $500/month",
            "You sell internationally and currency conversion fees are adding up",
            "You're getting hit with chargebacks and need better fraud protection",
        ],
        "dont_need_if": [
            "You sell on Etsy, Amazon, or eBay — they handle processing and you can't change it",
            "Your Shopify store uses Shopify Payments and you're happy with it — it's already competitive",
            "You're under $3K/month in online sales — focus on growth, not fee optimization",
        ],
        "cta": "Text PJ your platform (Shopify, WooCommerce, custom), monthly volume, and average order size. I'll tell you the best processor and estimate your savings.",
        "faq": [
            ("Is Stripe the best for ecommerce?", "For developer-run custom stores, yes. For Shopify stores, Shopify Payments is better (avoids the 2% third-party fee). For high volume, interchange-plus processors beat both on cost."),
            ("How do I reduce ecommerce chargebacks?", "Ship with tracking, send confirmation emails with clear business name, and use Stripe Radar or similar fraud detection. Respond to disputes within 7 days with evidence. Chargeback rates above 1% can get your account flagged."),
            ("Should I offer PayPal as a checkout option?", "Yes — PayPal increases conversion by 5–15% because customers trust it. But process everything you can through your primary processor (lower fees) and offer PayPal as an alternative at checkout."),
        ],
    },
}


# ─────────────────────────────────────────────
# TEMPLATE BUILDER
# ─────────────────────────────────────────────

def build_clarity_section(data):
    """Build the clarity layer HTML from page data."""

    need_items = "\n".join(
        f'      <li>{item}</li>' for item in data["need_if"]
    )
    dont_items = "\n".join(
        f'      <li>{item}</li>' for item in data["dont_need_if"]
    )
    faq_html = ""
    for i, (q, a) in enumerate(data["faq"]):
        margin = 'margin:0 0 8px;' if i == 0 else 'margin:18px 0 8px;'
        faq_html += f'''
    <h3 style="font-size:20px;{margin}">{q}</h3>
    <p style="font-size:17px;color:#334155;">{a}</p>
'''

    return f'''
<!-- ═══ SIDEGUY CLARITY LAYER v1 ═══ -->
<section class="clarity-layer" style="max-width:900px;margin:0 auto;padding:32px 20px;line-height:1.6;">

  <!-- HERO / HOOK -->
  <div style="background:linear-gradient(135deg,#ecfeff,#f0fdf4);border:1px solid #bae6fd;border-radius:18px;padding:28px 22px;margin-bottom:28px;">
    <p style="margin:0 0 10px 0;font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#0891b2;">
      SideGuy Clarity Layer
    </p>
    <h1 style="margin:0 0 12px 0;font-size:36px;line-height:1.1;color:var(--ink,#0f172a);">
      {data["h1"]}
    </h1>
    <p style="margin:0 0 14px 0;font-size:18px;color:#334155;">
      {data["hook"]}
    </p>
    <a href="sms:+17735441231" style="display:inline-block;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:var(--mint,#10b981);color:#ffffff;box-shadow:0 10px 30px rgba(16,185,129,.25);">
      Text PJ
    </a>
  </div>

  <!-- WHAT THEY'RE REALLY ASKING -->
  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">What people are really trying to figure out</h2>
    <p style="font-size:17px;color:#334155;">
      Most people searching this are trying to avoid three things:
    </p>
    <ul style="padding-left:22px;color:#334155;font-size:17px;">
      <li>overpaying</li>
      <li>choosing the wrong option</li>
      <li>getting sold something they do not actually need</li>
    </ul>
    <p style="font-size:17px;color:#334155;">
      That is where SideGuy helps. We translate the issue into a clear next move.
    </p>
  </div>

  <!-- QUICK ANSWER -->
  <div style="background:rgba(255,255,255,0.7);border:1px solid var(--stroke,#e2e8f0);border-radius:16px;padding:22px;margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Quick answer</h2>
    <p style="font-size:17px;color:#334155;">
      {data["quick_answer"]}
    </p>
  </div>

  <!-- YOU MIGHT NEED THIS IF -->
  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">You might need this if&#8230;</h2>
    <ul style="padding-left:22px;color:#334155;font-size:17px;">
{need_items}
    </ul>
  </div>

  <!-- YOU PROBABLY DON'T -->
  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">You probably do not need this if&#8230;</h2>
    <ul style="padding-left:22px;color:#334155;font-size:17px;">
{dont_items}
    </ul>
  </div>

  <!-- SIDEGUY ANGLE -->
  <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:16px;padding:22px;margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Why people text SideGuy first</h2>
    <p style="font-size:17px;color:#334155;">
      Most sites either drown you in jargon or push you toward a purchase. SideGuy is built for clarity before cost.
      You get a human-first read on the situation before making a bigger move.
    </p>
  </div>

  <!-- CONTEXTUAL CTA -->
  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Best next step</h2>
    <p style="font-size:17px;color:#334155;">
      {data["cta"]}
    </p>
    <a href="sms:+17735441231" style="display:inline-block;margin-top:10px;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:var(--ink,#0f172a);color:#ffffff;">
      Text PJ Now
    </a>
  </div>

  <!-- FAQ -->
  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Common questions</h2>
{faq_html}
  </div>

  <!-- BOTTOM CLOSE -->
  <div style="background:linear-gradient(135deg,#0f172a,#1e293b);color:#ffffff;border-radius:18px;padding:24px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:#ffffff;">Clarity before cost</h2>
    <p style="font-size:17px;color:#cbd5e1;margin-bottom:14px;">
      If you are stuck between options, send PJ the details. A quick outside read can save you money, time, and a bad decision.
    </p>
    <a href="sms:+17735441231" style="display:inline-block;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:var(--mint,#10b981);color:#ffffff;">
      Text PJ
    </a>
  </div>

</section>
<!-- ═══ /SIDEGUY CLARITY LAYER v1 ═══ -->
'''


# ─────────────────────────────────────────────
# FILE PROCESSOR
# ─────────────────────────────────────────────

def process_page(filename):
    filepath = PROJECT_ROOT / filename
    if not filepath.exists():
        print(f"  SKIP (not found): {filename}")
        return False

    html = filepath.read_text(encoding="utf-8")
    data = PAGES[filename]

    # Find <main ...> and </main> boundaries
    main_open = re.search(r'<main[^>]*>', html)
    main_close_match = re.search(r'</main>', html)

    if not main_open or not main_close_match:
        print(f"  SKIP (no <main> tags): {filename}")
        return False

    # Build new content
    clarity_html = build_clarity_section(data)

    # Replace content between <main...> and </main>
    new_html = (
        html[:main_open.end()]
        + "\n"
        + clarity_html
        + "\n"
        + html[main_close_match.start():]
    )

    filepath.write_text(new_html, encoding="utf-8")
    print(f"  OK: {filename}")
    return True


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 50)
    print("SHIP027 — Clarity Layer Upgrade")
    print(f"Pages to process: {len(PAGES)}")
    print("=" * 50)

    ok = 0
    fail = 0

    for filename in sorted(PAGES.keys()):
        if process_page(filename):
            ok += 1
        else:
            fail += 1

    print()
    print(f"Done: {ok} upgraded, {fail} skipped")


if __name__ == "__main__":
    main()
