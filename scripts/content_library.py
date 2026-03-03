#!/usr/bin/env python3
"""
SideGuy Content Library
Provides topic-specific intro text, what-to-know body, common mistakes,
and FAQ Q&As keyed to category and topic keywords.

Usage:
    from content_library import get_content
    content = get_content(topic, categories)
    # content['intro'], content['know'], content['mistakes'], content['faqs']
"""

import random, re

# ── Per-category content pools ────────────────────────────────────────────────
# Each entry: list of strings. pick_variant() selects based on topic hash
# so the same topic always gets the same variant (deterministic, not random).

INTROS = {
    'ai-automation': [
        ("AI automation tools are everywhere right now — but most vendors oversell "
         "what they can actually deliver for a small business. The honest answer is "
         "that the right tool depends entirely on your existing workflow, team size, "
         "and how much time you're losing to manual tasks today."),
        ("The gap between the AI automation demo and the actual implementation is "
         "real. Most tools work well for specific, narrow tasks — scheduling reminders, "
         "draft responses, lead scoring. The wide-open 'replace your whole operation' "
         "pitch is still mostly fiction for most businesses."),
        ("AI automation for small businesses is genuinely useful in 2026 — but only "
         "when you start with a problem, not a solution. The businesses getting real "
         "value picked one painful manual task and automated just that. Not their "
         "whole operation. One thing."),
    ],
    'payments': [
        ("Payment processing fees are one of the most under-examined costs in a small "
         "business. Most operators don't know their actual effective rate — total fees "
         "divided by total sales volume. If you've never calculated it, you're probably "
         "paying more than you need to."),
        ("The payments industry has more competition than it did five years ago, which "
         "means your options are genuinely better. But most processors count on you not "
         "shopping around. The best rate you'll ever get is the one you negotiate."),
        ("Most payment processing complaints come down to one thing: hidden fees. "
         "Monthly minimums, PCI compliance fees, batch fees, statement fees — none of "
         "these are disclosed prominently. Ask for an itemized breakdown of your full "
         "cost before signing anything."),
    ],
    'crypto-solana': [
        ("Crypto payments have crossed from novelty to practical — but only on the right "
         "rails. Solana and USDC specifically are the combination that makes sense for "
         "business: near-zero transaction fees, instant settlement, and a dollar-pegged "
         "stablecoin that removes the volatility risk most people associate with crypto."),
        ("Accepting USDC on Solana isn't a political statement or a tech experiment "
         "anymore. For certain business types — especially those with tech-forward customers "
         "or international clients — it's a real cost reduction. Effective rate: "
         "essentially 0%. Compare that to your Stripe bill."),
        ("The honest case for crypto payments: it only makes sense if your customers "
         "are already crypto-comfortable, or you have a specific cost problem with "
         "traditional processing. Don't adopt it because it sounds innovative. Adopt it "
         "if the math works for your specific situation."),
    ],
    'san-diego': [
        ("San Diego's business landscape is competitive and diverse — trades, food, "
         "health, real estate, and tech support all exist in the same market. What works "
         "for an Encinitas surf shop is different from what works for a Kearny Mesa "
         "contractor. Local context matters."),
        ("San Diego operators are adopting automation and alternative payment rails faster "
         "than most local markets nationally. The North County and downtown corridors are "
         "particularly active. If you haven't looked at what your competitors are doing "
         "operationally, you're probably behind."),
        ("Finding reliable local help in San Diego for AI, automation, or payments "
         "requires vetting. The 'consultant' space is full of generalists who learned "
         "these tools last year. Ask for specific case studies from businesses your size "
         "before engaging anyone."),
    ],
    'general': [
        ("The terminology around this topic is evolving fast, and most vendors use "
         "confusion to their advantage. The clearest signal that a vendor is worth "
         "talking to: they explain the downside before the upside."),
        ("Most operator questions about this topic come down to two things: how much "
         "does it cost and how long does it take. The honest answer to both is 'it "
         "depends' — but you can get to a real number in one conversation if you ask "
         "the right questions."),
        ("The businesses that get the most out of any new tool or service share one "
         "trait: they defined success before they started. Not vaguely — specifically. "
         "A number, a timeline, and a way to measure it."),
    ],
}

KNOW_BODY = {
    'ai-automation': [
        ("Start with the highest-friction task in your day — the one you or your team "
         "dreads most. That's usually the right first automation target. Not the most "
         "impressive one. The most annoying one.\n\n"
         "Proven ROI use cases for small businesses: appointment reminders, review "
         "request follow-ups, initial lead qualification, invoice generation, and basic "
         "FAQ responses. Speculative ones: anything requiring brand judgment or complex "
         "human reasoning."),
        ("Before any vendor conversation, calculate what one hour of your time costs. "
         "Then estimate how many hours per week a specific task takes. If the automation "
         "costs less than that over 12 months, the math probably works.\n\n"
         "The setup fee is often the hidden cost. Many tools charge $500–2,000 to "
         "configure. Ask what 'setup' includes and whether you own the configuration "
         "if you leave."),
        ("The most important question you can ask any AI automation vendor: 'Can you "
         "show me a customer in my industry who's been using this for 12 months?' "
         "Anyone can show a good demo. Case studies with actual metrics are rare.\n\n"
         "Red flags: guaranteed outcomes, no pilot period option, pressure to sign "
         "before seeing the product work in your environment."),
    ],
    'payments': [
        ("Pull your last 3 months of processor statements. Find the line items for "
         "interchange, assessments, processor markup, monthly fees, PCI fees, and any "
         "other line charges. Add them all. Divide by total volume. That's your "
         "effective rate. Most businesses are surprised.\n\n"
         "Interchange-plus pricing is almost always better than flat-rate at volume "
         "above $10k/month. If your processor won't give you interchange-plus, find "
         "one who will."),
        ("ACH/bank transfer processing runs 0.5–1% for most providers and works well "
         "for B2B payments or repeat customers. Square and Stripe don't promote this "
         "because their margins are better on card transactions.\n\n"
         "Chargebacks are the hidden cost most operators ignore until they're flagged. "
         "Each one costs $15–100 in fees plus the transaction itself. Clear billing "
         "descriptors and easy refund policies prevent most of them."),
        ("Negotiating with your processor is normal and expected. Most will drop rates "
         "if you ask with volume data in hand. Bring 3 months of statements and a "
         "competitor quote. Even a 0.3% reduction on $500k/year is $1,500 back.\n\n"
         "Month-to-month contracts are always worth the slightly higher base rate. "
         "The lock-in risk on payment processing is real — switching is painful."),
    ],
    'crypto-solana': [
        ("USDC on Solana is the practical choice for business payments. It's a "
         "dollar-pegged stablecoin — one USDC equals one dollar. Transaction fees "
         "are fractions of a cent. Settlement is final in under a second.\n\n"
         "To get started: set up a Phantom or Backpack wallet, generate a payment "
         "link or QR code, and decide how often you'll convert to USD. Tools like "
         "Helio, Sphere Pay, or Coinbase Commerce handle the checkout UX."),
        ("Converting USDC to USD is the part most operators worry about. In practice "
         "it takes 1–5 minutes via Coinbase or Kraken. You can set up automatic "
         "conversion so you never hold crypto overnight if that's the preference.\n\n"
         "Tax treatment: receiving USDC is ordinary income. Converting to USD is a "
         "taxable event but with minimal gain if you convert quickly. Tools like "
         "Koinly track this automatically."),
        ("The customer experience is the main barrier. Most customers have Coinbase "
         "or a wallet app — they just don't think to use it for local purchases. "
         "A 1–2% cash discount for crypto payments is enough incentive for many.\n\n"
         "Don't accept ETH or BTC directly unless you want price volatility exposure. "
         "USDC only, at least until you understand the space."),
    ],
    'san-diego': [
        ("San Diego's trade industry (HVAC, plumbing, electrical, solar) is among "
         "the most competitive in California. AI tools for scheduling, follow-up, "
         "and quoting are being adopted by the top 20–30% of operators. If you're "
         "not at least evaluating them, you're letting competitors get ahead on "
         "response time and customer experience.\n\n"
         "For restaurants and food service: review automation and loyalty follow-up "
         "have the fastest payback period. Most SD restaurants see ROI in under 60 days."),
        ("Local payment trends: San Diego businesses are seeing more crypto-curious "
         "customers than most California markets, particularly in North County and "
         "downtown. Several food trucks and service businesses already accept USDC.\n\n"
         "For high-ticket services (HVAC, roofing, solar): payment friction at close "
         "is real. Financing options and ACH alternatives are worth exploring "
         "specifically because customers are finalizing $5,000+ decisions."),
        ("AI consulting in San Diego ranges from legitimate to predatory. The "
         "legitimate ones: ask about your current workflow first and tell you what "
         "won't work before what will. The predatory ones: jump straight to demos "
         "and pricing.\n\n"
         "If you're evaluating a local AI consultant, ask them what the last "
         "implementation they did didn't work for, and why. That answer tells "
         "you everything."),
    ],
    'general': [
        ("Most operators looking into this topic are in one of two situations: "
         "they've heard it could help their business and want to understand it, "
         "or they've already been burned by a vendor and want a second opinion.\n\n"
         "Either way, the right starting point is the same: define the specific "
         "problem you're trying to solve, in plain language, before talking to "
         "anyone trying to sell you something."),
        ("The question most people don't ask but should: what does it cost if this "
         "doesn't work? Reversibility matters. Solutions where you can cancel in "
         "30 days with no penalty are almost always preferable to 12-month contracts, "
         "even if the monthly rate is higher.\n\n"
         "Ask every vendor: What's my exit path? What do I own if I leave? "
         "Who has access to my data? Their answers reveal a lot."),
        ("Success metrics matter more than features. Before any implementation, "
         "agree on what success looks like: a specific, measurable outcome with "
         "a timeline and a fallback plan.\n\n"
         "Common mistake: picking a vendor because they have the best website "
         "or the smoothest sales rep. The best vendor for a business your size "
         "is usually the one with the most experience serving businesses your size."),
    ],
}

MISTAKES = {
    'ai-automation': [
        "Starting with the most complex use case instead of the simplest.",
        "Buying a platform before running a 30-day single-use-case pilot.",
        "Not involving the staff who will actually use it in the selection process.",
        "Assuming the AI will figure out your workflow — it needs to be configured.",
        "Signing a 12-month contract before seeing it work in your actual environment.",
    ],
    'payments': [
        "Never calculating your actual effective rate (total fees ÷ total volume).",
        "Accepting the first rate offered without negotiating.",
        "Using flat-rate pricing above $10k/month in volume.",
        "Ignoring monthly, PCI, and batch fees that add up quietly.",
        "Locking into a long-term contract before testing the service.",
    ],
    'crypto-solana': [
        "Accepting volatile assets (BTC, ETH) instead of USDC stablecoins.",
        "Not setting up automatic conversion to USD, leading to price exposure.",
        "Skipping the tax tracking setup — every transaction is a taxable event.",
        "Choosing a complex setup when a simple Coinbase Commerce link would work.",
        "Trying to force crypto payment adoption on customers who aren't ready.",
    ],
    'san-diego': [
        "Hiring a consultant without asking for San Diego-specific case studies.",
        "Adopting a tool because a competitor is using it, without evaluating fit.",
        "Underestimating the difference between North County and downtown customer behavior.",
        "Not accounting for California-specific labor and compliance rules in automation.",
        "Skipping the pilot phase and doing a full rollout based on a demo.",
    ],
    'general': [
        "Choosing based on a demo without verifying customer references.",
        "Signing long contracts before testing the solution in your environment.",
        "Not defining what success looks like before starting.",
        "Letting urgency from a salesperson push you past due diligence.",
        "Solving the symptom instead of diagnosing the actual problem.",
    ],
}

FAQS = {
    'ai-automation': [
        ("How much does AI automation cost for a small business?",
         "Setup ranges from free (basic tools like Zapier) to $500–2,000 for "
         "managed implementations. Most small businesses start with 1–2 automations "
         "costing $50–200/month. Define the problem first, then find the tool — "
         "not the other way around."),
        ("How long does AI automation take to set up?",
         "Simple automations (appointment reminders, review requests) take 1–3 days. "
         "Complex workflows (lead scoring, multi-step CRM integration) take 2–6 weeks. "
         "If a vendor says they can set up a complex system in 48 hours, ask what "
         "corners they're cutting."),
        ("Will AI automation replace my employees?",
         "For repetitive, well-defined tasks — it may reduce hours needed. For "
         "relationship-based or judgment-heavy work — no. Most real implementations "
         "augment staff rather than replace them. The honest vendors will tell you "
         "exactly which tasks are and aren't automatable for your specific setup."),
    ],
    'payments': [
        ("What's a fair credit card processing rate for a small business?",
         "2.5–2.9% + $0.30 per transaction is typical for flat-rate pricing. "
         "If you process over $10k/month, interchange-plus pricing usually gets "
         "you to 2.0–2.5% effective. Above 3.5% on flat-rate, you're overpaying "
         "and should get competing quotes."),
        ("Can I negotiate my payment processing fees?",
         "Yes — especially if you process over $5–10k/month. Come to the conversation "
         "with 3 months of statements and a competitor quote. Ask specifically for "
         "interchange-plus pricing, waived monthly fees, and a month-to-month contract. "
         "Most processors have room to move."),
        ("What's the difference between Square, Stripe, and traditional merchant accounts?",
         "Square and Stripe are flat-rate, easy to start, and slightly higher cost. "
         "Traditional merchant accounts (through banks or ISOs) are cheaper at high "
         "volume but have monthly fees, multi-year contracts, and slow setup. "
         "For under $20k/month, Square or Stripe usually wins on simplicity."),
    ],
    'crypto-solana': [
        ("Is accepting crypto payments legal for a US business?",
         "Yes. You report received crypto as ordinary income at fair market value "
         "on the day received. USDC (a dollar-pegged stablecoin) is the lowest-risk "
         "option because its value doesn't fluctuate. Consult a crypto-literate "
         "CPA for your specific situation."),
        ("How do customers actually pay me in crypto?",
         "You share a wallet address, QR code, or payment link. They send USDC or SOL. "
         "You receive it in seconds. Tools like Helio, Sphere Pay, or Coinbase Commerce "
         "generate professional payment pages that look like normal checkout flows."),
        ("Do I need technical knowledge to accept Solana payments?",
         "Basic setup (getting a wallet, generating a payment link) takes about an hour "
         "with no technical background. Services like Coinbase Commerce abstract most "
         "of the complexity. You need a business wallet, a way to receive funds, "
         "and a process to convert to USD."),
    ],
    'san-diego': [
        ("Are there AI consultants in San Diego who work with small businesses?",
         "Yes, but vet carefully. Ask for specific case studies from businesses "
         "your size in San Diego — not generic demos. The best local consultants "
         "do assessments before proposals and tell you what won't work as readily "
         "as what will."),
        ("What industries in San Diego are adopting AI the fastest?",
         "Medical offices, real estate, restaurants, and contractors are seeing "
         "the most adoption. HVAC and solar are growing fast due to scheduling and "
         "follow-up automation ROI. Trades that rely on relationship trust are "
         "slower to adopt but the early movers are pulling ahead."),
        ("Is San Diego a good market for alternative payment options like crypto?",
         "More than most local markets. North County and downtown San Diego have "
         "higher concentrations of crypto-comfortable customers. Food trucks, "
         "tech-adjacent services, and younger-demographic businesses report the "
         "most success. High-ticket trades are exploring it for large invoice payments."),
    ],
    'general': [
        ("How do I find a trustworthy vendor for this?",
         "Ask for references from businesses your size — not general testimonials. "
         "Require a 30-day pilot before signing long-term contracts. Get full pricing "
         "in writing, including all fees. Ask: what does it cost if this doesn't work? "
         "Vendors who can't answer that clearly are a red flag."),
        ("What should I realistically budget for this?",
         "Start with the minimum viable spend to test the concept. Most implementations "
         "don't need to cost more than $200–500/month to start. Scale spend only after "
         "you have proof it's working. Avoid large upfront investments before seeing "
         "it operate in your actual environment."),
        ("How do I know if it's actually working?",
         "Define success before you start: a specific metric (hours saved per week, "
         "revenue per lead, fees reduced) with a 90-day target. If you can't measure "
         "it, you can't manage it. Any vendor who resists defining metrics upfront "
         "is protecting themselves from accountability."),
    ],
}


def _pick(pool, topic):
    """Deterministically pick a variant from a list based on topic string hash."""
    return pool[hash(topic) % len(pool)]


def get_content(topic: str, categories: list) -> dict:
    """
    Returns a dict with keys:
      intro    - differentiated intro paragraph (str)
      know     - "what you should know" body (str, may contain \\n\\n for paragraphs)
      mistakes - list of 3 mistake strings
      faqs     - list of (question, answer) tuples (3 items)
    """
    # Pick primary category for content selection
    priority = ['ai-automation', 'payments', 'crypto-solana', 'san-diego']
    cat = 'general'
    for p in priority:
        if p in categories:
            cat = p
            break

    intro    = _pick(INTROS[cat], topic)
    know     = _pick(KNOW_BODY[cat], topic)
    mistakes = MISTAKES[cat][:3]  # always use first 3 for clean display
    faqs     = FAQS[cat]

    return {
        'intro':    intro,
        'know':     know,
        'mistakes': mistakes,
        'faqs':     faqs,
        'category': cat,
    }


def make_faq_schema_json(faqs: list, page_url: str) -> str:
    """Return a <script> block with FAQPage JSON-LD."""
    entities = []
    for q, a in faqs:
        q_safe = q.replace('"', '\\"')
        a_safe = a.replace('"', '\\"').replace('\n', ' ')
        entities.append(
            f'    {{\n'
            f'      "@type": "Question",\n'
            f'      "name": "{q_safe}",\n'
            f'      "acceptedAnswer": {{\n'
            f'        "@type": "Answer",\n'
            f'        "text": "{a_safe}"\n'
            f'      }}\n'
            f'    }}'
        )
    body = ',\n'.join(entities)
    return (
        '<script type="application/ld+json">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "FAQPage",\n'
        '  "mainEntity": [\n'
        + body + '\n'
        '  ]\n'
        '}\n'
        '</script>'
    )


def make_breadcrumb_schema_json(crumbs: list) -> str:
    """
    crumbs: list of (name, url)
    Returns a <script> block with BreadcrumbList JSON-LD.
    """
    items = []
    for i, (name, url) in enumerate(crumbs, 1):
        n_safe = name.replace('"', '\\"')
        items.append(
            f'    {{\n'
            f'      "@type": "ListItem",\n'
            f'      "position": {i},\n'
            f'      "name": "{n_safe}",\n'
            f'      "item": "{url}"\n'
            f'    }}'
        )
    body = ',\n'.join(items)
    return (
        '<script type="application/ld+json">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "BreadcrumbList",\n'
        '  "itemListElement": [\n'
        + body + '\n'
        '  ]\n'
        '}\n'
        '</script>'
    )
