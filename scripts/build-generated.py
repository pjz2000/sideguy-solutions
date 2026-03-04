#!/usr/bin/env python3
"""
SIDEGUY AI Page Generator v1
Generates 13 topic pages → /generated/
Wires pillars to generated pages
Appends new URLs to sitemap.xml
"""

import os
import re
from datetime import datetime, timezone

STAMP = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
DATE = datetime.now(timezone.utc).strftime("%Y-%m-%d")
BASE = "/workspaces/sideguy-solutions"
DOMAIN = "https://sideguysolutions.com"
PHONE_DISPLAY = "773-544-1231"
PHONE_E164 = "+17735441231"

# ─── Shared CSS (matches clusters/longtail style) ──────────────────────────────

LIGHT_CSS = """:root{
  --bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;
  --ink:#073044;--muted:#3f6173;--muted2:#5e7d8e;
  --card:#ffffffcc;--card2:#ffffffb8;
  --stroke:rgba(7,48,68,.10);--stroke2:rgba(7,48,68,.07);
  --shadow:0 18px 50px rgba(7,48,68,.10);
  --mint:#21d3a1;--mint2:#00c7ff;--blue:#4aa9ff;--blue2:#1f7cff;
  --r:22px;--pill:999px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;
  background:radial-gradient(ellipse 130% 60% at 60% -10%,var(--bg1),var(--bg0) 55%),var(--bg0);
  color:var(--ink);line-height:1.65;min-height:100vh}
a{color:var(--blue2);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:880px;margin:0 auto;padding:28px 18px 90px}
.bc{font-size:.78rem;color:var(--muted2);margin-bottom:20px}
.bc a{color:var(--muted2)}
h1{font-size:clamp(1.5rem,4vw,2rem);font-weight:900;line-height:1.15;margin-bottom:10px}
.sub{font-size:1rem;color:var(--muted);margin-bottom:24px}
h2{font-size:1.1rem;font-weight:800;margin:26px 0 10px;color:var(--ink)}
h3{font-size:.95rem;font-weight:700;color:var(--muted2);margin:16px 0 6px}
p{color:var(--muted);font-size:.95rem;margin-bottom:12px}
ul{margin-left:20px;color:var(--muted);font-size:.95rem}
li{margin-bottom:5px}
li a{color:var(--blue2)}
ol{margin-left:20px;color:var(--muted);font-size:.95rem}
ol li{margin-bottom:8px}
.card{background:var(--card);border:1px solid var(--stroke);border-radius:16px;padding:20px;margin-bottom:14px}
.step-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-top:10px}
.step{background:rgba(255,255,255,.8);border:1px solid var(--stroke);border-radius:14px;padding:14px}
.step-num{font-size:.7rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--mint);margin-bottom:5px}
.step-title{font-size:.9rem;font-weight:800;color:var(--ink);margin-bottom:4px}
.step-body{font-size:.82rem;color:var(--muted)}
.pill-grid{display:flex;flex-wrap:wrap;gap:7px;margin-top:8px}
.pill-grid a{padding:6px 12px;border-radius:var(--pill);border:1px solid var(--stroke);
  background:rgba(255,255,255,.8);font-size:.82rem;font-weight:700;color:var(--ink);text-decoration:none}
.pill-grid a:hover{background:#fff;border-color:var(--mint)}
.related{background:rgba(0,199,255,.07);border:1px solid rgba(0,199,255,.18);border-radius:16px;padding:18px;margin-top:28px}
.related .label{font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted2);margin-bottom:10px}
.cta-box{background:linear-gradient(135deg,rgba(33,211,161,.12),rgba(0,199,255,.08));
  border:1px solid rgba(33,211,161,.25);border-radius:18px;padding:22px;margin-top:28px;text-align:center}
.cta-box p{color:var(--ink);font-weight:600;margin-bottom:10px}
.cta-box a.btn{display:inline-block;padding:11px 22px;background:var(--mint);color:#fff;
  font-weight:800;border-radius:var(--pill);font-size:.9rem}
.floating{position:fixed;bottom:20px;right:20px;z-index:999}
.floating a{display:flex;align-items:center;gap:8px;padding:11px 18px;
  background:linear-gradient(135deg,var(--mint),var(--mint2));
  color:#fff;font-weight:800;border-radius:var(--pill);
  box-shadow:0 8px 28px rgba(33,211,161,.35);text-decoration:none;font-size:.88rem}
.stamp{font-size:.7rem;color:var(--muted2);margin-top:28px;opacity:.7}"""

FLOAT = f'<div class="floating"><a href="sms:{PHONE_E164}">💬 Text PJ · {PHONE_DISPLAY}</a></div>'

def schema_breadcrumb(crumbs):
    items = [f'{{"@type":"ListItem","position":{i},"name":"{n}","item":"{u}"}}'
             for i, (n, u) in enumerate(crumbs, 1)]
    return ('{\n  "@context":"https://schema.org","@type":"BreadcrumbList",\n  '
            '"itemListElement":[\n    ' + ',\n    '.join(items) + '\n  ]\n}')

def schema_faq(pairs):
    entities = [f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
                for q, a in pairs]
    return ('{\n  "@context":"https://schema.org","@type":"FAQPage",\n  '
            '"mainEntity":[\n    ' + ',\n    '.join(entities) + '\n  ]\n}')

def head(title, desc, canonical, bc_sch, faq_sch):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{title}</title>
<link rel="canonical" href="{canonical}"/>
<meta name="description" content="{desc}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="SideGuy Solutions"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary"/>
<script type="application/ld+json">
{bc_sch}
</script>
<script type="application/ld+json">
{faq_sch}
</script>
<style>
{LIGHT_CSS}
</style>
</head>"""

# ─── PAGE DATA ─────────────────────────────────────────────────────────────────

PAGES = [
    {
        "slug": "ai-automation-for-plumbers",
        "title": "AI Automation for Plumbers | SideGuy",
        "h1": "AI Automation for Plumbers",
        "desc": "How plumbing contractors use AI to reduce missed calls, automate scheduling, and cut the admin work between service calls.",
        "answer": "Plumbers lose the most business to missed calls and slow follow-up — not to competition. AI closes those gaps without requiring tech skills.",
        "pillar_slug": "ai-automation",
        "pillar_name": "AI Automation",
        "cluster_slug": "ai-scheduling",
        "cluster_name": "AI Scheduling",
        "steps": [
            ("Missed Call Auto-Text", "Any new call that goes unanswered gets an auto-text: 'We missed you — reply here for fastest response.' Captures leads before they call the next plumber."),
            ("Booking Link After Every Estimate", "Send a booking link with every quote. Customer picks a slot without phone tag. Works 24/7."),
            ("Job Completion Auto-Invoice", "When a job is marked complete in your dispatch software, an invoice triggers automatically — payment link included."),
            ("Follow-Up Sequence", "3 days after job: text asking for a review. 30 days: check-in offer. Both automated, both your voice."),
        ],
        "watch_out": "Don't automate diagnosis or scope decisions. Customers call plumbers because something is wrong and they need a human judgment call. Keep the estimate and problem-solving human.",
        "faqs": [
            ("What AI tools are best for plumbers?",
             "Jobber, ServiceM8, and HouseCall Pro are built for trades. Add an auto-text tool (OpenPhone, Dialpad) for missed calls. These three tools handle 90% of plumber AI automation needs."),
            ("How much time can AI save a plumbing business?",
             "For a solo operator or small crew: 4–8 hours/week in scheduling, follow-up, and invoicing admin. For businesses with 5+ techs, the number scales significantly."),
            ("Does AI work for emergency plumbing services?",
             "For intake and triage, yes. An auto-text that collects problem description and address gets you information before you call back. The response itself always needs a human."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-scheduling.html", "AI Scheduling Cluster"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/longtail/ai-automation-for-contractors.html", "AI for Contractors"),
            ("/intelligence/decisions/should-i-use-ai.html", "Should I Use AI?"),
        ],
    },
    {
        "slug": "ai-automation-for-hvac",
        "title": "AI Automation for HVAC Companies | SideGuy",
        "h1": "AI Automation for HVAC Companies",
        "desc": "How HVAC operators use AI for intake, dispatch, appointment reminders, and calmer seasonal demand management.",
        "answer": "HVAC businesses have predictable seasonal spikes where call volume overwhelms small teams. AI absorbs the intake and scheduling load so your techs stay focused on service.",
        "pillar_slug": "ai-automation",
        "pillar_name": "AI Automation",
        "cluster_slug": "ai-scheduling",
        "cluster_name": "AI Scheduling",
        "steps": [
            ("Seasonal Intake Automation", "Summer + winter rush: auto-responder captures service type, address, and urgency so you can triage before calling back."),
            ("Appointment Reminders", "24h and 2h reminder texts reduce no-shows 20–40%. Standard in any modern scheduling system."),
            ("Maintenance Plan Renewals", "Annual maintenance agreements: renewal reminders auto-send 30 days before expiry. Most HVAC businesses under-use this."),
            ("Post-Service Review Request", "24h after job completion: auto-text requesting a Google review. Consistent execution compounds into significant review volume."),
        ],
        "watch_out": "Don't automate quoting for complex systems (new installs, equipment replacements). Walk-through and accurate sizing require human assessment. Automation is for intake and scheduling — not scope.",
        "faqs": [
            ("What software do HVAC companies use for AI automation?",
             "ServiceTitan is the industry standard for larger operations. Jobber and HouseCall Pro work well for smaller teams. All three handle scheduling, reminders, and invoicing."),
            ("Can AI handle emergency HVAC calls?",
             "For initial intake, yes — capturing location, system type, and problem description. Dispatching and prioritization should stay human, especially for urgent calls."),
            ("How do I reduce HVAC no-shows?",
             "Automated appointment reminders via text (24h before + 2h before) consistently reduce no-shows 20–40%. Most HVAC scheduling software includes this — enable it if you haven't."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-scheduling.html", "AI Scheduling Cluster"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/longtail/ai-automation-for-contractors.html", "AI for Contractors"),
            ("/longtail/how-to-stop-missed-calls.html", "Stop Missed Calls"),
        ],
    },
    {
        "slug": "ai-automation-for-landscapers",
        "title": "AI Automation for Landscapers | SideGuy",
        "h1": "AI Automation for Landscapers",
        "desc": "How landscaping operators use AI to quote faster, follow up consistently, and manage seasonal scheduling without extra admin.",
        "answer": "Landscaping is a high-quote-volume, high-seasonality business. AI reduces the gap between lead and estimate — the window where most jobs go to the faster competitor.",
        "pillar_slug": "ai-automation",
        "pillar_name": "AI Automation",
        "cluster_slug": "ai-workflow-automation",
        "cluster_name": "AI Workflow Automation",
        "steps": [
            ("Instant Lead Response", "New form submission or missed call: auto-text within 60 seconds asking for property address and service type. Speed wins the estimate appointment."),
            ("Quote Follow-Up Automation", "Day 2 after estimate: 'Any questions?' Day 5: 'Still available this week.' Day 10: 'Offer expires.' Three touchpoints, zero manual effort."),
            ("Seasonal Maintenance Reminders", "Spring cleanup + fall prep: scheduled broadcast texts to existing customers 3 weeks out. Recurring revenue without sales calls."),
            ("Photo Documentation in SOPs", "Before/after photos with timestamp → linked to job record → used for dispute prevention and portfolio. Automate the capture habit, not the photos themselves."),
        ],
        "watch_out": "Don't automate initial quotes for large or complex jobs (new installs, drainage work, major redesigns). These need an in-person visit and trust-building conversation.",
        "faqs": [
            ("What CRM do landscapers use?",
             "Jobber is the most popular among landscaping operators. It handles quoting, scheduling, invoicing, and basic automation. ServiceM8 and LMN (Landscape Management Network) are alternatives."),
            ("How do I automate landscaping estimates?",
             "For repeat/maintenance work: standardized price list + booking link. For new installs: auto-schedule the estimate visit, then quote manually. Full estimate automation without site visit creates problems."),
            ("Can AI help with landscaping crew scheduling?",
             "Yes — Jobber and similar tools route jobs geographically and assign crew based on availability. This is one of the highest-ROI automations for multi-crew operations."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-workflow-automation.html", "AI Workflow Automation"),
            ("/clusters/ai-scheduling.html", "AI Scheduling"),
            ("/longtail/ai-automation-for-contractors.html", "AI for Contractors"),
            ("/longtail/how-to-automate-invoices.html", "Automate Invoices"),
        ],
    },
    {
        "slug": "ai-automation-for-law-firms",
        "title": "AI Automation for Law Firms | SideGuy",
        "h1": "AI Automation for Law Firms",
        "desc": "How law firms use AI to summarize documents, draft routine communications, route intake, and protect billable time from admin work.",
        "answer": "Law firms have two expensive resources: attorney time and client trust. AI protects both by handling the administrative load that doesn't require legal judgment.",
        "pillar_slug": "ai-automation",
        "pillar_name": "AI Automation",
        "cluster_slug": "ai-workflow-automation",
        "cluster_name": "AI Workflow Automation",
        "steps": [
            ("Intake Triage Automation", "Online intake form captures matter type, urgency, and contact info → routes to the right attorney or practice group automatically."),
            ("Document Summarization", "AI tools (ChatGPT, Claude, Clio Draft) summarize long contracts, discovery documents, and case files in minutes. Reduces review time without replacing attorney review."),
            ("Routine Communication Drafts", "Status update emails, appointment confirmations, and follow-up prompts drafted by AI — attorney reviews and sends. Removes drafting friction without removing oversight."),
            ("Time Entry Prompting", "End-of-day AI prompt: 'Based on your calendar and activity, here are suggested time entries.' Reduces leakage, improves billing capture."),
        ],
        "watch_out": "AI cannot provide legal advice, assess case merit, or make strategic decisions. Do not use general-purpose AI tools with confidential client data unless the vendor has a signed BAA and data-handling policy. Client confidentiality is not negotiable.",
        "faqs": [
            ("Is AI safe for law firms to use?",
             "For non-confidential tasks (document structure, draft outlines, scheduling), general tools are fine. For anything involving client data, use tools with BAA agreements and data isolation — Clio, LexWorkplace, or enterprise-tier tools with proper data handling."),
            ("What AI tools do law firms use?",
             "Clio (practice management + AI features), Harvey AI (legal-specific), and Casetext (legal research) are purpose-built. Microsoft Copilot with proper M365 licensing handles drafting and scheduling."),
            ("Can AI replace paralegals?",
             "No — but it changes the work. AI handles first-draft, document review, and research support. Paralegals focus on quality control, client interaction, and nuanced legal support. Scope changes; headcount may not."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-workflow-automation.html", "AI Workflow Automation"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/intelligence/decisions/should-i-use-ai.html", "Should I Use AI?"),
            ("/intelligence/ai-reality/ai-vs-human-decisions.html", "AI vs Human Decisions"),
        ],
    },
    {
        "slug": "ai-automation-for-dentists",
        "title": "AI Automation for Dental Offices | SideGuy",
        "h1": "AI Automation for Dental Offices",
        "desc": "How dental practices use AI for scheduling, intake, appointment reminders, and documentation — without creating HIPAA exposure.",
        "answer": "Dental offices lose revenue to no-shows and lose time to phone scheduling. Both problems have well-tested AI solutions that work within HIPAA constraints.",
        "pillar_slug": "ai-automation",
        "pillar_name": "AI Automation",
        "cluster_slug": "ai-scheduling",
        "cluster_name": "AI Scheduling",
        "steps": [
            ("No-Show Reduction", "Automated appointment reminders via text and email (48h + 24h + 2h) consistently reduce no-shows 20–40%. All major dental software includes this."),
            ("Online Scheduling", "Patient self-scheduling for cleanings, exams, and hygiene appointments removes phone volume without removing control over complex procedure slots."),
            ("Digital Intake Forms", "Pre-visit medical history and insurance forms via text link. Patient completes before arrival — reduces check-in time and front-desk load."),
            ("Recall Automation", "6-month recall reminders to existing patients. Automated outreach for overdue cleanings. Sustainable recall protocol without staff calls."),
        ],
        "watch_out": "Any system handling scheduling data tied to patient identity may qualify as PHI under HIPAA — especially when linked to treatment type. Use dental-specific software (Dentrix, Eaglesoft, Open Dental, Weave) or confirm HIPAA compliance and BAA availability before deploying third-party tools.",
        "faqs": [
            ("Is appointment reminder software HIPAA compliant?",
             "Dental-specific platforms (Weave, RevenueWell, Lighthouse 360) are designed for HIPAA compliance and include BAA agreements. General texting tools are not. Use dental-purpose tools for patient communication."),
            ("What software do dental offices use for AI automation?",
             "Weave is the most popular for communication automation. Dentrix and Eaglesoft handle scheduling and recalls. NexHealth bridges scheduling, intake, and messaging in one HIPAA-compliant system."),
            ("How do I reduce dental no-shows?",
             "Three-step reminder sequence (2 days, 1 day, 2 hours before) + easy rescheduling link in the message reduces no-shows 20–40%. Make cancellation easy — patients who cancel are easier to reschedule than no-shows."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-scheduling.html", "AI Scheduling Cluster"),
            ("/longtail/ai-automation-for-medical-offices.html", "AI for Medical Offices"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/intelligence/decisions/should-i-use-ai.html", "Should I Use AI?"),
        ],
    },
    {
        "slug": "reduce-payment-processing-fees-restaurants",
        "title": "Reduce Payment Processing Fees for Restaurants | SideGuy",
        "h1": "Reduce Payment Processing Fees for Restaurants",
        "desc": "Plain-English steps restaurants take to lower effective payment processing rates without disrupting the guest experience.",
        "answer": "Restaurants run on thin margins. Payment fees averaging 2.5–3.5% on every card transaction are a meaningful cost — and most are partially negotiable.",
        "pillar_slug": "payments",
        "pillar_name": "Payments",
        "cluster_slug": "payment-fees",
        "cluster_name": "Payment Fees",
        "steps": [
            ("Know Your Effective Rate", "Total monthly fees ÷ total card volume = effective rate. Restaurant average is 2.5–3.2%. Above that is worth addressing."),
            ("Negotiate Your POS Contract", "Toast, Square, and Clover all have room to negotiate — especially at volume above $50k/month. Ask for interchange-plus pricing vs flat-rate."),
            ("Cash Discount / Dual Pricing", "Legal in all 50 states with proper disclosure. Post two prices (card vs cash). 3–4% cash discount passes processing cost to card payers. Reduces your effective rate to near-zero."),
            ("Reduce Keyed-In Transactions", "Phone orders keyed by staff carry a higher rate than card-present. Add an online order link or payment link to eliminate most manual entry."),
        ],
        "watch_out": "Cash discounting and surcharging require proper signage and compliance with card network rules. Improperly disclosed surcharges create chargebacks and potential processor violations. Post the policy clearly at point of entry and at point of sale.",
        "faqs": [
            ("What is a good payment processing rate for restaurants?",
             "2.2–2.8% effective rate for full-service restaurants is reasonable. Fast casual and counter-service with high debit mix can get lower. Above 3% is worth a conversation with your processor."),
            ("Can restaurants negotiate payment processing fees?",
             "Yes — once you're above $30–50k/month in card volume. Ask for interchange-plus pricing, rate review, and removal of junk monthly fees (PCI non-compliance, statement fees)."),
            ("Should restaurants use dual pricing?",
             "It depends on your guest mix and concept. High-volume fast casual: often worth it. Fine dining with corporate card guests: adds friction that may not be worth the savings."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-fees.html", "Payment Fees Cluster"),
            ("/longtail/why-payment-fees-are-so-high.html", "Why Fees Are High"),
            ("/longtail/how-to-reduce-payment-processing-fees.html", "Reduce Fees"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
    },
    {
        "slug": "reduce-payment-processing-fees-retail",
        "title": "Reduce Payment Processing Fees for Retail | SideGuy",
        "h1": "Reduce Payment Processing Fees for Retail",
        "desc": "How retail stores lower credit card processing costs, manage disputes, and reduce the per-transaction fee drag on margins.",
        "answer": "Retail has a natural advantage: high card-present volume, which commands lower interchange rates. Most retail operators aren't fully capturing that advantage.",
        "pillar_slug": "payments",
        "pillar_name": "Payments",
        "cluster_slug": "payment-fees",
        "cluster_name": "Payment Fees",
        "steps": [
            ("Tap-to-Pay Penetration", "NFC (contactless) transactions cost less than dip, and less than swipe. Make tap the default for every checkout. Signage and staff prompting help."),
            ("Debit Routing Optimization", "Debit transactions can route through different networks (Visa, Mastercard, or PIN debit networks). PIN debit typically costs less. Ask your processor about debit routing optimization."),
            ("Audit Monthly Statement", "Line-level review: PCI fee, batch fee, statement fee, monthly minimum. Most processors charge 4–8 line items beyond the base rate. Remove any you're not using."),
            ("Negotiate on Renewal", "Most retail POS contracts are 1–3 years. At renewal, request interchange-plus pricing and compare at least one alternative processor quote before signing."),
        ],
        "watch_out": "Switching POS systems to save on fees is usually not worth the operational disruption unless you're saving 0.5%+ effective rate AND the POS functionality is equivalent. Don't break your operations for marginal fee savings.",
        "faqs": [
            ("What is the average payment processing fee for retail?",
             "In-person retail averages 1.7–2.4% effective rate. High debit mix (grocery, convenience) can be 1.5% or lower. Specialty retail with high-end customers skews toward 2.2–2.8%."),
            ("Is it worth switching POS to get better payment rates?",
             "Only if the rate improvement covers switching costs AND the new POS has equivalent inventory, reporting, and staff management features. Rate alone is rarely enough justification."),
            ("What is debit routing optimization for retail?",
             "Federal law (Durbin Amendment) requires processors to support at least two unaffiliated debit networks. Your processor can route PIN debit transactions through lower-cost networks. Ask if this is enabled."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-fees.html", "Payment Fees Cluster"),
            ("/generated/reduce-payment-processing-fees-restaurants.html", "Fees for Restaurants"),
            ("/longtail/why-payment-fees-are-so-high.html", "Why Fees Are High"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
    },
    {
        "slug": "what-is-instant-settlement-for-business",
        "title": "What Is Instant Settlement for Business? | SideGuy",
        "h1": "What Is Instant Settlement for Business?",
        "desc": "Why payment settlement speed matters to operator cash flow — and when paying for instant settlement is actually worth it.",
        "answer": "Standard payment settlement takes 1–3 business days. Instant settlement moves funds to your account within minutes — for a fee. For cash-flow-constrained businesses, it's often cheaper than a credit line.",
        "pillar_slug": "payments",
        "pillar_name": "Payments",
        "cluster_slug": "instant-settlement",
        "cluster_name": "Instant Settlement",
        "steps": [
            ("Understand Your Settlement Gap", "How often does settlement timing cause you to delay vendor payments or draw on a credit line? That cost is your baseline to compare instant settlement against."),
            ("Calculate the Fee Break-Even", "Stripe Instant Payouts: 1%. Square Instant Deposit: 1.5%. On $20k/month, that's $200–300/month. Compare to your line of credit interest or overdraft fees."),
            ("Enable Selectively", "You don't need instant settlement on every transaction. Most processors let you trigger instant payouts when needed — only pay for it when cash timing actually matters."),
            ("ACH as Middle Option", "If same-day isn't critical but T+2 is painful, push for next-day ACH settlement from your bank. Often free or low-cost, no special feature required."),
        ],
        "watch_out": "Instant settlement is not irrevocable. Chargebacks can claw back settled funds weeks later. Don't spend instantly settled funds on non-reversible obligations if chargeback risk is high in your business.",
        "faqs": [
            ("What is instant settlement in payment processing?",
             "Instant settlement deposits card transaction funds into your bank account within minutes to hours, instead of the standard 1–3 business days. Most major processors offer it as a paid feature."),
            ("Which processors offer instant settlement?",
             "Stripe (Instant Payouts — 1%), Square (Instant Deposit — 1.5%), PayPal (Instant Transfer — 1%, capped at $25), and many integrated bank processors. Rates vary."),
            ("Is instant settlement worth it for small businesses?",
             "Worth it when: cash flow timing causes real operational friction or credit line usage. Not worth it when: you have adequate operating reserves and standard settlement timing doesn't cause problems."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/instant-settlement.html", "Instant Settlement Cluster"),
            ("/longtail/what-is-instant-settlement.html", "Instant Settlement Deep Dive"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
    },
    {
        "slug": "chargeback-prevention-for-small-business",
        "title": "Chargeback Prevention for Small Business | SideGuy",
        "h1": "Chargeback Prevention for Small Business",
        "desc": "Simple controls that reduce dispute rates and protect margins — before chargebacks start, not after they arrive.",
        "answer": "Most chargebacks are preventable. The operators who get hit hardest are usually missing three things: a recognizable billing name, documented fulfillment, and a fast complaint channel.",
        "pillar_slug": "payments",
        "pillar_name": "Payments",
        "cluster_slug": "chargebacks",
        "cluster_name": "Chargebacks",
        "steps": [
            ("Fix Your Billing Descriptor", "Your processor statement name should match your business name your customers recognize. 'MBR HOLDING LLC' causes disputes. 'Joe's HVAC' does not."),
            ("Document Fulfillment At Delivery", "Photo, signature, or delivery confirmation at point of service. Customer email with order summary. These are your evidence if disputed."),
            ("Add a Fast Complaint Path", "Phone number and email on every receipt and confirmation. Customers who can reach you easily call you first — not their bank."),
            ("Respond to Every Dispute", "Non-response is automatic loss. Set a calendar reminder for chargeback deadline monitoring. 15–20 days is typical; Stripe and Square give 7–10."),
        ],
        "watch_out": "Chargeback ratio above 1% of transaction count triggers processor monitoring and eventual account risk. Track your ratio monthly. If it's trending up, investigate the root cause before your processor does.",
        "faqs": [
            ("What causes most chargebacks for small businesses?",
             "The top causes: unrecognized billing descriptor (customer doesn't remember the purchase), friendly fraud (buyer's remorse filed as fraud), non-delivery disputes, and subscription billing misunderstandings."),
            ("How do I fight a chargeback?",
             "Submit evidence before the deadline: order confirmation, delivery proof, communication history, signed terms. One clear paragraph + supporting documents. Submit everything to the processor portal."),
            ("What is a chargeback ratio?",
             "Your chargeback ratio is total chargebacks divided by total transactions in a month. Card networks flag ratios above 0.9–1%. Above that threshold triggers processor reviews and potential account termination."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/chargebacks.html", "Chargebacks Cluster"),
            ("/longtail/how-to-handle-chargebacks.html", "How to Handle Chargebacks"),
            ("/clusters/payment-security.html", "Payment Security"),
            ("/decisions/switch-payment-processor.html", "Switch Processors?"),
        ],
    },
    {
        "slug": "best-crm-for-contractors",
        "title": "Best CRM for Contractors (How to Choose) | SideGuy",
        "h1": "Best CRM for Contractors",
        "desc": "A practical framework for picking a CRM that reduces missed leads, simplifies follow-up, and integrates with how contractors actually work.",
        "answer": "Contractors don't need a CRM — they need a system that captures leads, tracks jobs, and follows up automatically. The best one is the one your team will actually open.",
        "pillar_slug": "small-business-tech",
        "pillar_name": "Small Business Tech",
        "cluster_slug": "software-selection",
        "cluster_name": "Software Selection",
        "steps": [
            ("Define Your Actual Problem", "Is it missed leads? Slow invoicing? Disorganized follow-up? The CRM you need depends on which problem actually costs you money."),
            ("Try Trade-Specific First", "Jobber, ServiceM8, and HouseCall Pro are built for contractors. They combine CRM + scheduling + quoting + invoicing — no integration work."),
            ("Test on a Real Job", "Import 5 real customer records. Create a real quote. Send a real invoice. If it takes more than 20 minutes, it's going to be abandoned."),
            ("Check Mobile Experience", "Contractors are in the field. If the mobile app is bad, the system won't be used regardless of desktop features."),
        ],
        "watch_out": "Don't buy a full Salesforce or HubSpot Sales Pro setup for a small contracting business. The configuration overhead and training time will kill adoption before you get any value.",
        "faqs": [
            ("What CRM do contractors use most?",
             "Jobber is the most popular for small-to-mid contractors (1–25 employees). ServiceM8 is popular for solo operators and small crews. HouseCall Pro is strong for home services with multiple techs."),
            ("Does a solo contractor need a CRM?",
             "Not necessarily a formal CRM — but you need something. A simple Airtable base or Google Sheet with customer name, job status, and follow-up date is better than nothing and costs $0."),
            ("What are the key features for a contractor CRM?",
             "Lead capture, quote generation, job scheduling, automated follow-up, invoice creation, and payment collection. Ideally all in one tool. Integrations between separate tools introduce friction."),
        ],
        "related": [
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/clusters/software-selection.html", "Software Selection"),
            ("/clusters/customer-ops.html", "Customer Ops"),
            ("/longtail/best-crm-for-small-business.html", "Best CRM for Small Business"),
            ("/longtail/how-to-stop-missed-calls.html", "Stop Missed Calls"),
        ],
    },
    {
        "slug": "how-to-build-sops-for-small-business",
        "title": "How to Build SOPs for Small Business | SideGuy",
        "h1": "How to Build SOPs for Small Business",
        "desc": "A practical guide to writing standard operating procedures that your team will actually follow — and that scale well with AI tools.",
        "answer": "The biggest SOP mistake is writing them to cover edge cases instead of the common flow. Write for the 80%, not the 2%.",
        "pillar_slug": "small-business-tech",
        "pillar_name": "Small Business Tech",
        "cluster_slug": "sops-and-process",
        "cluster_name": "SOPs & Process",
        "steps": [
            ("Start With Your Most Repeated Task", "What does your team repeat daily or weekly that's inconsistent? That's your first SOP. Start there, not with the complex stuff."),
            ("Use the 3-Part Format", "Trigger (what starts this?), Steps (exactly what happens, in order), Done Criteria (how do we know it's complete?). One page max."),
            ("Write It During the Task", "Document the process as you're doing it — not from memory. Live documentation is 3x more accurate."),
            ("Test It With Someone Else", "Have a team member follow the SOP without your help. Every point of confusion is an edit. Fix it once; it runs forever."),
        ],
        "watch_out": "Don't build SOPs for work that requires judgment each time. SOPs are for repeatability. If the right answer changes based on context, that's a training situation — not an SOP situation.",
        "faqs": [
            ("How many SOPs does a small business need?",
             "Start with 5–10 covering your most common repeated processes. Intake, invoicing, follow-up, complaint handling, team onboarding. Quality over quantity — 5 good ones beat 50 unused ones."),
            ("What format should SOPs use?",
             "Trigger → numbered steps → done criteria. Add screenshots or a short video (Loom) for visual or software-based tasks. Store in Google Docs, Notion, or wherever your team actually works."),
            ("How often should SOPs be updated?",
             "Review quarterly or whenever a process changes. Put the last-updated date at the top. Stale SOPs with old steps actively cause mistakes — worse than no SOP."),
        ],
        "related": [
            ("/clusters/sops-and-process.html", "SOPs & Process Cluster"),
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/longtail/how-to-build-sops.html", "How to Build SOPs"),
            ("/clusters/time-saving-systems.html", "Time-Saving Systems"),
            ("/clusters/customer-ops.html", "Customer Ops"),
        ],
    },
    {
        "slug": "how-to-stop-missed-calls-for-contractors",
        "title": "How to Stop Missed Calls for Contractors | SideGuy",
        "h1": "How to Stop Missed Calls for Contractors",
        "desc": "Systems that capture contractor leads from missed calls before they dial the next number on Google.",
        "answer": "A missed call in a service business is usually a missed job. Contractors on site can't always answer — but they can have a system that responds in 60 seconds without them.",
        "pillar_slug": "small-business-tech",
        "pillar_name": "Small Business Tech",
        "cluster_slug": "customer-ops",
        "cluster_name": "Customer Ops",
        "steps": [
            ("Auto-Text on Missed Call", "Business phone systems (OpenPhone, Dialpad, Google Voice Business) auto-send a text on missed call. Message: 'Hey — we missed your call. Text back or we'll call you within [X time].'"),
            ("Call Forwarding to Backup", "Primary rings for 15 seconds → forwards to second number (partner, admin, answering service). Catches calls before they hit voicemail."),
            ("Voicemail-to-Text Transcription", "Most VoIP services transcribe voicemails to text and email/text them to you. You read the issue in 10 seconds vs listening to a 90-second voicemail."),
            ("Response Time Commitment", "Set and post a response standard: 'We reply within 2 hours during business hours.' Customers with a commitment feel heard even before you call back."),
        ],
        "watch_out": "AI phone agents for contractor intake are promising but imperfect. They sometimes misunderstand service types or urgency levels, frustrating customers who called because they have a real problem. If you use one, test it rigorously before going live.",
        "faqs": [
            ("What's the best missed call solution for contractors?",
             "OpenPhone is the most popular for small contractor teams — missed call auto-text, shared inbox, mobile app. $15–25/user/month. Pays for itself if it captures one job per month."),
            ("How fast do I need to respond to a missed call?",
             "Under 2 hours during business hours is acceptable. Under 30 minutes is good. Under 5 minutes (via auto-text) changes the outcome — customer stays engaged instead of calling your competitor."),
            ("Should contractors use an answering service?",
             "For high-volume periods (HVAC summer rush, emergency plumbing) or solo operators who can't answer on site — yes. Ruby Receptionists and Smith.ai are commonly used. More expensive but human-quality intake."),
        ],
        "related": [
            ("/clusters/customer-ops.html", "Customer Ops Cluster"),
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/longtail/how-to-stop-missed-calls.html", "Stop Missed Calls"),
            ("/longtail/best-crm-for-contractors.html", "Best CRM for Contractors"),
            ("/clusters/ai-scheduling.html", "AI Scheduling"),
        ],
    },
    {
        "slug": "how-to-automate-invoices-small-business",
        "title": "How to Automate Invoices for Small Business | SideGuy",
        "h1": "How to Automate Invoices for Small Business",
        "desc": "Reduce invoice admin time, speed up collections, and keep books clean with practical invoice automation for small operators.",
        "answer": "Delayed invoicing is usually a cash flow problem disguised as an admin problem. Automation closes the gap between work completed and money requested.",
        "pillar_slug": "small-business-tech",
        "pillar_name": "Small Business Tech",
        "cluster_slug": "time-saving-systems",
        "cluster_name": "Time-Saving Systems",
        "steps": [
            ("Job-Completion Trigger", "When a job is marked complete in your service software (Jobber, HouseCall Pro, ServiceM8), an invoice generates and sends automatically. Zero delay, zero manual step."),
            ("Recurring Invoice Setup", "Monthly retainer clients, maintenance agreements, memberships: set up once in Stripe or QuickBooks. They invoice, remind, and collect on schedule."),
            ("Three-Step Reminder Sequence", "Invoice due in 3 days → due today → 3 days overdue. Each auto-sends. Collections rate on invoices with automated follow-up is 20–40% faster."),
            ("One-Click Payment Links", "Every invoice includes a payment link (card, ACH, bank transfer). Remove friction from the payment path. Every step between invoice and payment reduces collection speed."),
        ],
        "watch_out": "Don't automate the conversation when a client disputes a line item or invoice amount. Automated responses to billing disputes damage the relationship. Keep financial dispute resolution human.",
        "faqs": [
            ("What software automates invoices for small businesses?",
             "Jobber and HouseCall Pro for service businesses (invoice on job completion). QuickBooks Online and FreshBooks for accounting-integrated automation. Stripe Invoicing for tech-forward operators. Wave for bootstrapped/free option."),
            ("How much time does invoice automation save?",
             "For a business sending 20–50 invoices/month, automated invoicing + follow-up typically saves 3–6 hours/month in admin time plus accelerates payment timing by 5–14 days on average."),
            ("Can I automate invoice reminders without annoying clients?",
             "Yes — keep reminders transactional (not pushy), send at reasonable times (morning, business days), and allow easy payment in-message. Clients expect payment reminders; tone matters more than presence."),
        ],
        "related": [
            ("/clusters/time-saving-systems.html", "Time-Saving Systems Cluster"),
            ("/pillars/small-business-tech.html", "Small Business Tech Pillar"),
            ("/longtail/how-to-automate-invoices.html", "Automate Invoices"),
            ("/clusters/sops-and-process.html", "SOPs & Process"),
            ("/clusters/customer-ops.html", "Customer Ops"),
        ],
    },
]

# ─── Build a page ──────────────────────────────────────────────────────────────

def build_page(p):
    slug = p["slug"]
    canonical = f"{DOMAIN}/generated/{slug}.html"
    pillar_url = f"{DOMAIN}/pillars/{p['pillar_slug']}.html"
    bc = schema_breadcrumb([
        ("SideGuy Solutions", DOMAIN),
        (p["pillar_name"], pillar_url),
        (p["h1"], canonical),
    ])
    faq_sch = schema_faq(p["faqs"])
    bc_nav = (f'<a href="/">SideGuy</a> › '
              f'<a href="/pillars/{p["pillar_slug"]}.html">{p["pillar_name"]}</a> › '
              f'<a href="/clusters/{p["cluster_slug"]}.html">{p["cluster_name"]}</a> › '
              f'{p["h1"]}')

    steps_html = ""
    for label, detail in p["steps"]:
        steps_html += f"""  <div class="step">
    <div class="step-num">Step</div>
    <div class="step-title">{label}</div>
    <div class="step-body">{detail}</div>
  </div>
"""

    faq_html = ""
    for q, a in p["faqs"]:
        faq_html += f"    <h3>{q}</h3>\n    <p>{a}</p>\n"

    related_pills = "\n".join(f'      <a href="{u}">{n}</a>' for u, n in p["related"])

    return f"""{head(p['title'], p['desc'], canonical, bc, faq_sch)}
<body>
<div class="wrap">
  <nav class="bc">{bc_nav}</nav>

  <h1>{p["h1"]}</h1>
  <p class="sub">{p["answer"]}</p>

  <div class="step-grid">
{steps_html}  </div>

  <div class="card" style="margin-top:14px">
    <h2>Watch Out For</h2>
    <p>{p["watch_out"]}</p>
  </div>

  <div class="card">
    <h2>Frequently Asked Questions</h2>
{faq_html}  </div>

  <div class="related">
    <div class="label">Related Knowledge</div>
    <div class="pill-grid">
{related_pills}
      <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a>
    </div>
  </div>

  <div class="cta-box">
    <p>Want a quick operator take on your situation?</p>
    <a href="sms:{PHONE_E164}" class="btn">💬 Text PJ · {PHONE_DISPLAY}</a>
  </div>

  <p class="stamp">Updated: {STAMP} · SideGuy Solutions</p>
</div>
{FLOAT}
</body>
</html>"""

# ─── Update pillar pages ───────────────────────────────────────────────────────

def wire_pillar(pillar_slug, pages_for_pillar):
    path = f"{BASE}/pillars/{pillar_slug}.html"
    if not os.path.exists(path):
        print(f"  SKIP: {path} not found")
        return
    with open(path) as f:
        content = f.read()

    marker = "<!-- SIDEGUY_GENERATED_PAGES -->"
    if marker in content:
        print(f"  Already wired: pillars/{pillar_slug}.html")
        return

    li_items = "\n".join(
        f'          <li><a href="/generated/{p["slug"]}.html">{p["h1"]}</a></li>'
        for p in pages_for_pillar
    )
    block = f"""\n      {marker}
      <div class="card" style="margin-top:14px">
        <h2>Problem Pages</h2>
        <ul>
{li_items}
        </ul>
      </div>"""

    # Insert before closing </div> of .layout
    content = content.replace('  <div class="footer">', block + '\n  <div class="footer">', 1)
    with open(path, "w") as f:
        f.write(content)
    print(f"  Wired: pillars/{pillar_slug}.html (+{len(pages_for_pillar)} pages)")

# ─── Update sitemap ────────────────────────────────────────────────────────────

def update_sitemap(slugs):
    sitemap_path = f"{BASE}/sitemap.xml"
    with open(sitemap_path) as f:
        content = f.read()

    added = 0
    for slug in slugs:
        url = f"{DOMAIN}/generated/{slug}.html"
        loc = f"<loc>{url}</loc>"
        if loc not in content:
            entry = f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{DATE}</lastmod>\n  </url>\n"
            content = content.replace("</urlset>", entry + "</urlset>", 1)
            added += 1

    with open(sitemap_path, "w") as f:
        f.write(content)
    print(f"  Sitemap: +{added} URLs added")

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(f"{BASE}/generated", exist_ok=True)

    # Build all pages
    for p in PAGES:
        path = f"{BASE}/generated/{p['slug']}.html"
        with open(path, "w") as f:
            f.write(build_page(p))
        print(f"Created: generated/{p['slug']}.html")

    # Wire pillars
    print("\nWiring pillars...")
    from collections import defaultdict
    by_pillar = defaultdict(list)
    for p in PAGES:
        by_pillar[p["pillar_slug"]].append(p)
    for pillar_slug, pages in by_pillar.items():
        wire_pillar(pillar_slug, pages)

    # Update sitemap
    print("\nUpdating sitemap...")
    update_sitemap([p["slug"] for p in PAGES])

    print(f"\nDone: {len(PAGES)} pages generated in generated/")
    print("\nGSC priority submit list:")
    for p in PAGES:
        print(f"  {DOMAIN}/generated/{p['slug']}.html")
