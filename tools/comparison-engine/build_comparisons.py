#!/usr/bin/env python3
"""
SideGuy Comparison Page Builder
Generates real, substantive X-vs-Y pages at root level (crawlable/indexable).
Each page has unique content, inline CSS matching site style, schema markup.
"""

from pathlib import Path
import datetime

ROOT = Path("/workspaces/sideguy-solutions")

# ── Per-pair content data ────────────────────────────────────────────────────
# Each entry: slug_a, slug_b, title_a, title_b, description, h1, intro,
#             a_pros, b_pros, verdict, faq pairs, schema_type

PAIRS = [
    {
        "a": "stripe",
        "b": "square",
        "title_a": "Stripe",
        "title_b": "Square",
        "page_title": "Stripe vs Square — Which Payment Processor Is Right for Your Business?",
        "meta_desc": "Stripe vs Square compared for small businesses in 2026 — real fees, setup complexity, best use cases, and when to switch. No sales pitch. Honest breakdown from SideGuy.",
        "h1": "Stripe vs Square: Which One Should Your Business Use?",
        "intro": "Stripe and Square are both solid payment processors, but they're built for different operators. Square is designed for in-person businesses — cafes, salons, retail. Stripe is built for developers and online-first businesses. Choosing the wrong one creates friction you'll feel every day.",
        "a_section_title": "When Stripe Makes Sense",
        "a_points": [
            "You sell primarily online (e-commerce, subscriptions, invoicing)",
            "You need custom payment flows, API integrations, or developer access",
            "You want international payments or multi-currency support",
            "You're building a marketplace or platform that charges other businesses",
            "You need advanced fraud tools (Stripe Radar) or flexible payout timing",
        ],
        "b_section_title": "When Square Makes Sense",
        "b_points": [
            "You operate a physical location (restaurant, salon, food truck, retail)",
            "You want all-in-one hardware + software with minimal setup",
            "You need a free POS with inventory, employee management, and appointments",
            "Your team isn't technical and needs something that just works out of the box",
            "You want free next-business-day deposits with no monthly fee to start",
        ],
        "cost_title": "Real Fee Comparison",
        "cost_body": "Both charge 2.9% + 30¢ for online card transactions and 2.6–2.7% for in-person swipes. The difference shows up in monthly fees (Square has a free tier; Stripe charges per feature add-on), hardware costs (Square sells its own readers; Stripe integrates with third-party terminals), and chargeback fees ($15–25 each on both platforms). Watch for Square's add-on fees if you use their payroll, marketing, or loyalty features — costs stack up fast.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "Most brick-and-mortar San Diego businesses are better served by Square — the hardware ecosystem, free POS, and simple onboarding win for in-person operations. If you're running an online business, a subscription service, or anything that needs a developer to touch the payments layer, use Stripe. If you're doing both, consider using Square in-person and Stripe online with a unified accounting integration.",
        "faqs": [
            ("Can I use both Stripe and Square?", "Yes. Many hybrid businesses use Square for in-person transactions (because of the hardware) and Stripe for online or recurring billing. They can both sync to QuickBooks or Xero."),
            ("Which has lower fees — Stripe or Square?", "They're nearly identical on standard rates. Stripe can get cheaper at high volume through negotiated interchange-plus pricing. Square's advantage is the free hardware reader and no monthly fee to start."),
            ("Does Square work for online stores?", "Yes, Square has an online store product. It's fine for basic e-commerce but Stripe + Shopify or WooCommerce gives you more flexibility and better developer tools for complex stores."),
            ("Which is easier to set up?", "Square wins for speed. You can be processing payments in 15 minutes. Stripe requires more configuration — especially for custom checkout flows — but their documentation is excellent."),
        ],
        "canonical_slug": "stripe-vs-square",
    },
    {
        "a": "zapier",
        "b": "make",
        "title_a": "Zapier",
        "title_b": "Make (formerly Integromat)",
        "page_title": "Zapier vs Make — Which Automation Tool Is Right for Your Business?",
        "meta_desc": "Zapier vs Make compared for small business automation in 2026 — real pricing, complexity tradeoffs, best use cases. Honest guide from SideGuy San Diego.",
        "h1": "Zapier vs Make: Which Automation Platform Should You Use?",
        "intro": "Both Zapier and Make connect your apps and automate repetitive tasks. The difference is who they're built for. Zapier is built for non-technical business owners who want quick wins. Make is built for people who want more control, visual logic, and lower cost at scale. Picking the wrong one means either paying too much or drowning in complexity.",
        "a_section_title": "When Zapier Makes Sense",
        "a_points": [
            "You want simple if-then automations without reading documentation",
            "You need 5,000+ app integrations out of the box — Zapier's library is the largest",
            "Speed matters more than cost — automations can be live in minutes",
            "Your team is non-technical and needs to manage automations themselves",
            "You have a small number of high-value automations rather than complex multi-step workflows",
        ],
        "b_section_title": "When Make Makes Sense",
        "b_points": [
            "You need complex, multi-step workflows with conditional logic and loops",
            "You're processing high volumes of data (Make charges per operation, not per task)",
            "You want visual scenario builders that show exactly how data flows",
            "Budget matters — Make is significantly cheaper at similar automation volume",
            "You need advanced error handling, data transformation, or HTTP request flexibility",
        ],
        "cost_title": "Real Pricing Comparison (2026)",
        "cost_body": "Zapier's free tier allows 100 tasks/month with 5 Zaps. Paid plans start at $19.99/month for 750 tasks. Make's free tier gives 1,000 operations/month. Paid plans start at $9/month for 10,000 operations. 'Operations' and 'tasks' aren't the same unit — a single Zapier task often equals multiple Make operations in a multi-step scenario. For most small businesses running 10–30 automations, Make ends up 40–60% cheaper at comparable workflow complexity.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "If you're just starting with automation and want to move fast, Zapier is worth paying the premium for the simplicity. If you've been using Zapier for 6+ months and your bill is climbing, auditing your automations and migrating complex ones to Make often cuts the cost in half. The two tools coexist fine — nothing stops you from using Zapier for simple triggers and Make for complex data workflows.",
        "faqs": [
            ("Is Make harder to learn than Zapier?", "Make has a steeper initial learning curve because of its visual canvas interface. Most people need 2–4 hours to feel comfortable. Zapier is closer to 30 minutes for a first automation."),
            ("Can I migrate from Zapier to Make?", "There's no automatic migration tool, but most Zapier workflows can be rebuilt in Make. For complex workflows Make often ends up cleaner because the visual builder forces you to think through data flow."),
            ("Which has better customer support?", "Zapier has faster support response times and better documentation. Make's community forums are active and the documentation has improved significantly in 2025."),
            ("Does Make work with as many apps as Zapier?", "Make has 1,500+ integrations vs Zapier's 5,000+. For most common business tools (Google, Slack, HubSpot, Shopify, QuickBooks) both have solid coverage. Niche apps are more likely to be on Zapier."),
        ],
        "canonical_slug": "zapier-vs-make",
    },
    {
        "a": "chatgpt",
        "b": "claude",
        "title_a": "ChatGPT",
        "title_b": "Claude",
        "page_title": "ChatGPT vs Claude — Which AI Assistant Is Better for Your Business?",
        "meta_desc": "ChatGPT vs Claude compared for business use in 2026 — writing quality, accuracy, context limits, pricing. Which AI assistant should your team actually use? Honest take from SideGuy.",
        "h1": "ChatGPT vs Claude: Which AI Assistant Should Your Business Use?",
        "intro": "ChatGPT and Claude are both AI assistants that can write, summarize, analyze, and answer questions. The real differences show up in context window size, writing tone, accuracy on complex tasks, and how they handle sensitive or nuanced business situations. For most business owners the question isn't which is 'smarter' — it's which one fits your specific workflows.",
        "a_section_title": "When ChatGPT Works Better",
        "a_points": [
            "You need broad tool integrations — ChatGPT connects to plugins, DALL-E, Bing search, and Code Interpreter",
            "Your team already uses Microsoft 365 (Copilot is built on GPT-4)",
            "You want to build custom GPTs for specific internal workflows",
            "You need image generation alongside text in the same tool",
            "You're using the API for automated pipelines — OpenAI's API ecosystem is the most mature",
        ],
        "b_section_title": "When Claude Works Better",
        "b_points": [
            "You're working with very long documents — Claude's 200k context window handles full contracts, reports, and codebases",
            "Tone and nuance matter — Claude's writing tends to be more natural and less formulaic",
            "You need accurate, careful reasoning on complex or sensitive business decisions",
            "You want an AI that pushes back thoughtfully rather than just agreeing",
            "You're doing legal, compliance, or financial document review where accuracy outweighs speed",
        ],
        "cost_title": "Pricing Comparison (2026)",
        "cost_body": "Both ChatGPT Plus and Claude Pro cost $20/month per user for the consumer tier. The API pricing differs: GPT-4o runs approximately $2.50/1M input tokens; Claude 3.5 Sonnet runs approximately $3/1M input tokens. For most small business use — drafting emails, summarizing documents, writing copy — the cost is negligible. API cost becomes a factor if you're building automated workflows processing thousands of documents.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "For day-to-day business writing and quick answers, both are excellent and the differences are subtle. Claude tends to produce cleaner first drafts with less editing needed. ChatGPT is better when you need tool integrations or image generation in the same session. If you're building AI into your business workflows via API, start with OpenAI for the ecosystem maturity, but test Claude for tasks where quality of reasoning matters more than speed.",
        "faqs": [
            ("Is Claude safer or more accurate than ChatGPT?", "Claude tends to be more cautious and will express uncertainty more readily. For business use this is often a feature — you want an AI that says 'I'm not sure' rather than confidently getting it wrong."),
            ("Can I use both?", "Yes. Many operators use ChatGPT for quick creative tasks and Claude for document-heavy or reasoning-heavy work. Both have browser extensions and API access."),
            ("Which is better for customer-facing content?", "Claude generally produces more natural-sounding copy that needs less editing. ChatGPT is more configurable with system prompts for maintaining consistent brand voice at scale."),
            ("Do either of these connect to my business tools?", "ChatGPT has more native integrations (Slack, Zapier, Notion, etc.). Claude integrates well via API and through Make/Zapier. Neither directly syncs to industry-specific software like Mindbody or ServiceTitan without a custom integration."),
        ],
        "canonical_slug": "chatgpt-vs-claude",
    },
    {
        "a": "ai-chatbot",
        "b": "live-chat",
        "title_a": "AI Chatbot",
        "title_b": "Live Chat",
        "page_title": "AI Chatbot vs Live Chat — What's Right for Your Small Business?",
        "meta_desc": "AI chatbot vs live chat compared for small business customer support in 2026 — real costs, response quality, when to use each. Honest guide from SideGuy San Diego.",
        "h1": "AI Chatbot vs Live Chat: Which One Should Your Business Use?",
        "intro": "The choice between an AI chatbot and live chat isn't really about technology — it's about what your customers need and what your team can actually staff. A chatbot that frustrates customers costs you more than it saves. Live chat that nobody answers destroys trust. The right answer depends on your volume, hours, and type of inquiries.",
        "a_section_title": "When an AI Chatbot Makes Sense",
        "a_points": [
            "You get the same 20 questions every day — hours, pricing, booking, address, return policy",
            "You need 24/7 coverage but can't staff overnight or weekend support",
            "Your inquiry volume is high enough that humans can't respond within 5 minutes",
            "Most inquiries can be resolved with information (not judgment calls)",
            "You want to qualify leads before a human gets involved",
        ],
        "b_section_title": "When Live Chat Makes Sense",
        "b_points": [
            "Your inquiries require judgment, empathy, or custom problem-solving",
            "You're in a high-trust industry (medical, legal, financial) where AI responses could mislead",
            "Your conversion rate depends on relationship and rapport, not just information",
            "You have the staff to respond within 2–3 minutes during business hours",
            "You're dealing with complaints, disputes, or emotionally charged situations",
        ],
        "cost_title": "Real Cost Comparison",
        "cost_body": "Basic AI chatbots (Tidio, ManyChat, Intercom Fin) run $30–150/month. Custom AI chatbots trained on your business data run $200–800/month or $2,000–8,000 to build. Live chat software (Intercom, Drift, Crisp) runs $50–400/month. The hidden cost of live chat is staffing — a dedicated chat agent costs $35,000–55,000/year fully loaded. For most small businesses, a hybrid model (AI handles FAQ + triage, humans handle escalations) costs $100–300/month total and outperforms either option alone.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "Don't choose between them — use both. Set up an AI chatbot to handle your top 10–15 FAQ responses 24/7 and automatically route everything else to a human (or to a contact form if outside business hours). This setup costs $50–150/month in software and takes 1–2 days to configure. The mistake most small businesses make is deploying a chatbot without a clear escalation path, which leaves customers stuck in loops.",
        "faqs": [
            ("Will customers know they're talking to an AI?", "Most AI chatbots should be transparent about being AI — and Google's guidelines increasingly expect this. The good news is customers are now comfortable with AI for informational queries. They just don't want it for emotional or complex issues."),
            ("How long does it take to set up an AI chatbot?", "A basic FAQ chatbot can be live in 1–2 days using tools like Tidio or Intercom. A well-trained chatbot that handles your specific business questions accurately takes 1–2 weeks of tuning."),
            ("What happens when the chatbot doesn't know the answer?", "The answer determines whether your chatbot helps or hurts. Good chatbots escalate gracefully: collect the customer's contact info, create a ticket, and notify a human. Bad chatbots loop endlessly. Set up escalation before you go live."),
            ("Is live chat better for conversions?", "For high-value purchases and service sales, yes. Human live chat on a pricing page can increase conversions 20–40%. For informational queries and low-ticket items, an AI chatbot is just as effective and available 24/7."),
        ],
        "canonical_slug": "ai-chatbot-vs-live-chat",
    },
    {
        "a": "manual-dispatch",
        "b": "ai-dispatch",
        "title_a": "Manual Dispatch",
        "title_b": "AI Dispatch",
        "page_title": "Manual Dispatch vs AI Dispatch — Is Automated Scheduling Worth It for Field Service?",
        "meta_desc": "Manual dispatch vs AI dispatch compared for field service businesses in 2026 — real ROI, costs, and when automation actually makes sense. Honest guide from SideGuy San Diego.",
        "h1": "Manual Dispatch vs AI Dispatch: Is the Switch Worth It for Your Field Business?",
        "intro": "Manual dispatch works fine until it doesn't. When you're scheduling 3–5 techs it's manageable. When you hit 8–15 techs, last-minute cancellations, and back-to-back service windows, manual coordination starts costing real money in wasted drive time and missed jobs. AI dispatch doesn't replace your dispatcher — it removes the parts that burn them out.",
        "a_section_title": "When Manual Dispatch Is Fine",
        "a_points": [
            "You have fewer than 5 field techs and a consistent, predictable schedule",
            "Your jobs are long-duration (4+ hours) where routing optimization matters less",
            "You have an experienced dispatcher who knows your customers personally",
            "You operate in a small geographic area where drive time is rarely a variable",
            "Your workflow is simple enough that a whiteboard or spreadsheet handles it",
        ],
        "b_section_title": "When AI Dispatch Pays Off",
        "b_points": [
            "You have 6+ techs with varying skills, certifications, or equipment requirements",
            "You're losing 45–90 minutes per day per tech to suboptimal routing",
            "Last-minute cancellations and reschedules create scheduling chaos",
            "You want customers to get live ETAs and status updates without calling your office",
            "Your dispatcher is spending more time on the phone managing schedules than on exceptions",
        ],
        "cost_title": "Real Cost & ROI",
        "cost_body": "AI dispatch software (ServiceTitan, Jobber, Housecall Pro, FieldEdge) runs $100–500/month depending on team size. The ROI calculation is straightforward: if you have 8 techs, even saving 30 minutes of drive time per tech per day equals 4 hours of billable time recovered daily. At $150/hour that's $600/day — nearly $150,000/year. Most field service operators with 6+ techs see positive ROI within 60–90 days of adoption.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "The break-even point for most San Diego field service companies is around 6 techs. Below that, the software cost and learning curve rarely justify the savings. Above that, not using AI dispatch is leaving money on the table every single day. The most common mistake: buying expensive dispatch software without training the dispatcher to trust the algorithm. If your dispatcher overrides it constantly, you paid for complexity with no benefit.",
        "faqs": [
            ("Will AI dispatch replace my dispatcher?", "No — and the vendors who suggest it will are overselling. AI dispatch handles routing optimization and schedule logic. Your dispatcher still handles customer relationships, emergency judgment calls, and anything the algorithm can't predict."),
            ("How long does it take to implement AI dispatch software?", "Basic setup takes 1–2 weeks. Full adoption — where your techs are comfortable with the app and your dispatcher trusts the routing — typically takes 4–8 weeks."),
            ("What's the best AI dispatch software for HVAC or plumbing?", "ServiceTitan is the industry leader but also the most expensive ($400–700/month+). Jobber and Housecall Pro are solid for companies under 15 techs at $150–300/month. The right choice depends on your CRM and invoicing needs, not just dispatch."),
            ("Can I try AI dispatch without committing?", "Most platforms offer 14–30 day free trials. Run the trial alongside your current process for 2 weeks, then compare jobs completed per day, average drive time, and customer wait times. The numbers will tell you whether it's worth it."),
        ],
        "canonical_slug": "manual-dispatch-vs-ai-dispatch",
    },
    {
        "a": "manual-booking",
        "b": "ai-booking",
        "title_a": "Manual Booking",
        "title_b": "AI Booking",
        "page_title": "Manual Booking vs AI Booking — Should Your Business Automate Appointments?",
        "meta_desc": "Manual booking vs AI booking compared for small businesses in 2026 — real costs, customer experience impact, and when to automate. Honest guide from SideGuy San Diego.",
        "h1": "Manual Booking vs AI Booking: When Does Automated Scheduling Actually Help?",
        "intro": "Manual booking means someone on your team confirms every appointment by phone, email, or text. AI booking means customers self-schedule around your real-time availability with automatic confirmations and reminders. The question isn't whether automation is better in theory — it's whether your customers' booking behavior actually matches what the software handles well.",
        "a_section_title": "When Manual Booking Is Fine",
        "a_points": [
            "Your appointments require consultation before scheduling (custom quotes, assessments)",
            "Your availability is irregular or capacity-constrained in ways software can't model",
            "You have very few bookings per week (under 20) and a team member handles it quickly",
            "Your customer base skews older and prefers phone calls",
            "Personal relationship is part of the service you provide",
        ],
        "b_section_title": "When AI Booking Pays Off",
        "b_points": [
            "More than 30% of your bookings come in outside business hours",
            "You're missing calls or responding to booking requests hours later",
            "No-show and cancellation rates are high — automated reminders cut these 30–50%",
            "Your service is standardized enough that customers can self-select the right appointment type",
            "You have repetitive confirmation and reminder tasks killing hours per week",
        ],
        "cost_title": "Real Cost Comparison",
        "cost_body": "Basic AI booking tools (Calendly, Acuity, Square Appointments) run $0–29/month. Industry-specific tools (Mindbody for fitness/wellness, Jane for health practitioners, Vagaro for salons) run $30–150/month. The ROI driver isn't the software cost — it's what your team does with the recovered time. If one admin spends 10 hours/week on manual booking coordination and that drops to 2 hours, you've recovered 8 hours of productivity per week. That's 400 hours/year.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "For any service business taking 30+ appointments per week, AI booking is a straightforward win. The one thing to get right: your confirmation and reminder message copy. Generic 'your appointment is confirmed' emails get ignored. Personalized reminders with specific instructions (what to bring, where to park, who to ask for) cut no-shows and create a better first impression than the call you were making before.",
        "faqs": [
            ("Will customers actually use online booking?", "Adoption depends on your customer base and how prominently you offer it. Most businesses that switch see 50–70% of new bookings self-schedule within 60 days, with older clients often still calling — which is fine since your team now only handles the edge cases."),
            ("What about complex bookings that need custom info?", "Most booking platforms let you add intake forms, custom questions, and conditional logic. For truly complex bookings (multi-step consultations, custom quotes), use the booking tool to capture initial info and have a follow-up step before confirming."),
            ("Does AI booking work for same-day appointments?", "Yes — real-time availability sync means customers can book same-day slots. The key is configuring a buffer window so you have enough time to prepare between bookings."),
            ("Which AI booking tool should I use?", "It depends on your industry. Salons: Vagaro or Fresha. Health/wellness: Jane or Mindbody. General service businesses: Acuity or Calendly. The right tool fits your existing workflow — don't switch your entire operation for a booking tool."),
        ],
        "canonical_slug": "manual-booking-vs-ai-booking",
    },
    {
        "a": "manual-scheduling",
        "b": "ai-scheduling",
        "title_a": "Manual Scheduling",
        "title_b": "AI Scheduling",
        "page_title": "Manual Scheduling vs AI Scheduling — What's Right for Your Business?",
        "meta_desc": "Manual scheduling vs AI scheduling compared for small businesses in 2026 — real tradeoffs, costs, and which approach fits your operation. Honest guide from SideGuy San Diego.",
        "h1": "Manual Scheduling vs AI Scheduling: Which Approach Fits Your Business?",
        "intro": "Employee scheduling is either a 20-minute task or a 2-hour headache depending on how many variables you manage: availability, certifications, overtime rules, customer preferences, and last-minute call-outs. Manual scheduling works until complexity outpaces your spreadsheet. AI scheduling tools earn their cost when they save more time than they add friction.",
        "a_section_title": "When Manual Scheduling Works Fine",
        "a_points": [
            "You have a small, consistent team (under 8 people) with predictable availability",
            "Your schedule rarely changes once set for the week",
            "You don't have complex labor rules (overtime thresholds, certification requirements)",
            "Your team communicates shift changes directly and it rarely causes problems",
            "You're spending under 2 hours per week on scheduling tasks",
        ],
        "b_section_title": "When AI Scheduling Pays Off",
        "b_points": [
            "You manage 10+ employees with varying availability, roles, and hourly costs",
            "Last-minute call-outs trigger a scramble to find replacements",
            "You're overspending on overtime because of inefficient shift distribution",
            "Compliance with labor laws (breaks, overtime, minor work permits) is a risk area",
            "Your team uses a mix of full-time, part-time, and on-call workers",
        ],
        "cost_title": "Real Cost Comparison",
        "cost_body": "Basic scheduling tools (When I Work, Homebase free tier, Google Sheets) run $0–4/employee/month. Mid-tier platforms (Deputy, 7shifts, Sling) run $3–8/employee/month. Enterprise platforms with AI optimization (Workforce.com, Legion) run $8–20/employee/month. For a 15-person team the delta between manual (free) and a solid AI scheduler ($60–120/month) is meaningful — but only if you're actually spending 4+ hours/week managing schedules today.",
        "verdict_title": "SideGuy Take",
        "verdict_body": "Most small businesses under 10 employees aren't struggling enough with scheduling to justify the monthly cost and adoption friction. If you're managing 12+ people across multiple shifts with variable availability, the AI scheduler pays for itself in your first week. The hidden benefit isn't the schedule itself — it's the reduction in the group chat chaos when someone calls out. Platforms like Deputy and Homebase let employees swap shifts with manager approval, which cuts your involvement to a confirmation tap.",
        "faqs": [
            ("Can AI scheduling predict when I'll need more staff?", "Higher-end platforms (Legion, Workforce.com) use historical data and demand forecasting to suggest staffing levels. For most small businesses this feature is overkill — the basic automation of preference-based scheduling and shift swapping is where the real ROI lives."),
            ("Will my employees actually use the app?", "Adoption is the biggest risk. Choose a platform your employees can download and navigate without training. Homebase and When I Work have the highest employee adoption rates among small businesses because the mobile UX is simple."),
            ("Does AI scheduling work for restaurants?", "Restaurants are the primary use case. 7shifts is built specifically for restaurants and integrates with POS systems (Toast, Square) to align staffing with sales forecasts. It's harder to justify general-purpose workforce tools when industry-specific ones exist."),
            ("What happens when my AI scheduler makes a bad call?", "Every platform lets managers override the AI-generated schedule. The goal isn't to replace your judgment — it's to give you a solid starting point that you adjust, rather than building from scratch every week."),
        ],
        "canonical_slug": "manual-scheduling-vs-ai-scheduling",
    },
]


def build_page(p: dict) -> str:
    a, b = p["title_a"], p["title_b"]
    slug = p["canonical_slug"]
    faq_schema = ",\n    ".join([
        f'''{{"@type":"Question","name":{q!r},"acceptedAnswer":{{"@type":"Answer","text":{ans!r}}}}}'''
        for q, ans in p["faqs"]
    ])
    faq_html = "\n".join([
        f'<details><summary><strong>{q}</strong></summary><p>{ans}</p></details>'
        for q, ans in p["faqs"]
    ])
    a_points_html = "\n".join(f"<li>{pt}</li>" for pt in p["a_points"])
    b_points_html = "\n".join(f"<li>{pt}</li>" for pt in p["b_points"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{p["page_title"]} · SideGuy</title>
<link rel="canonical" href="https://sideguysolutions.com/{slug}.html"/>
<meta name="description" content="{p["meta_desc"]}"/>
<script defer data-domain="sideguysolutions.com" src="https://plausible.io/js/script.js"></script>
<meta property="og:title" content="{p["page_title"]} · SideGuy">
<meta property="og:description" content="{p["meta_desc"]}">
<meta property="og:url" content="https://sideguysolutions.com/{slug}.html">
<meta property="og:image" content="https://sideguysolutions.com/og-preview.png"/>
<meta property="og:type" content="article">
<meta property="og:site_name" content="SideGuy Solutions">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{p["page_title"]}">
<meta name="twitter:description" content="{p["meta_desc"]}">
<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"FAQPage",
  "mainEntity":[{faq_schema}]
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org",
  "@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"https://sideguysolutions.com"}},
    {{"@type":"ListItem","position":2,"name":"Comparisons","item":"https://sideguysolutions.com/comparisons-hub.html"}},
    {{"@type":"ListItem","position":3,"name":"{a} vs {b}","item":"https://sideguysolutions.com/{slug}.html"}}
  ]
}}
</script>
<style>
:root{{--bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;--ink:#073044;--muted:#3f6173;--muted2:#5e7d8e;--card:#ffffffcc;--stroke:rgba(7,48,68,.10);--shadow:0 18px 50px rgba(7,48,68,.10);--mint:#21d3a1;--blue:#4aa9ff;--r:22px;--pill:999px}}
*{{box-sizing:border-box}}html,body{{height:100%;margin:0}}
body{{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;color:var(--ink);background:radial-gradient(1200px 900px at 22% 10%,#ffffff 0%,var(--bg0) 25%,var(--bg1) 60%,var(--bg2) 100%);-webkit-font-smoothing:antialiased}}
.wrap{{max-width:860px;margin:0 auto;padding:40px 24px 80px}}
h1{{font-size:42px;letter-spacing:-.03em;line-height:1.1;margin:0 0 16px}}
@media(max-width:640px){{h1{{font-size:30px}}}}
.lede{{font-size:19px;line-height:1.6;color:var(--muted);margin:0 0 40px;max-width:720px}}
h2{{font-size:26px;margin:40px 0 16px;color:var(--ink)}}
h3{{font-size:20px;margin:32px 0 12px}}
.vs-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:24px 0 36px}}
@media(max-width:580px){{.vs-grid{{grid-template-columns:1fr}}}}
.vs-card{{background:var(--card);padding:24px;border-radius:var(--r);border:1px solid var(--stroke);box-shadow:var(--shadow);backdrop-filter:blur(12px)}}
.vs-card h3{{margin:0 0 12px;font-size:18px;color:var(--ink)}}
.vs-card ul{{margin:0;padding-left:20px;color:var(--muted);font-size:15px;line-height:1.7}}
.cost-box{{background:var(--card);padding:24px 28px;border-radius:var(--r);border:1px solid var(--stroke);margin:8px 0 36px;box-shadow:var(--shadow)}}
.cost-box h2{{margin-top:0}}
.verdict{{background:linear-gradient(135deg,rgba(33,211,161,.12),rgba(74,169,255,.10));padding:28px 32px;border-radius:var(--r);border:1px solid rgba(33,211,161,.25);margin:8px 0 36px}}
.verdict h2{{margin-top:0;color:var(--ink)}}
.verdict p{{font-size:16px;line-height:1.7;margin:0;color:var(--muted)}}
.faq-block{{margin:8px 0 36px}}
.faq-block details{{background:var(--card);border:1px solid var(--stroke);border-radius:16px;padding:18px 22px;margin-bottom:10px;box-shadow:0 4px 16px rgba(7,48,68,.06)}}
.faq-block details summary{{cursor:pointer;font-size:16px;line-height:1.5;list-style:none}}
.faq-block details summary::-webkit-details-marker{{display:none}}
.faq-block details p{{margin:12px 0 0;font-size:15px;line-height:1.7;color:var(--muted)}}
.cta{{background:linear-gradient(135deg,var(--mint),var(--blue));color:#fff;padding:32px;border-radius:var(--r);text-align:center;margin:48px 0}}
.cta h3{{margin:0 0 10px;font-size:22px}}.cta p{{margin:0 0 20px;font-size:16px;opacity:.95}}
.cta a{{display:inline-block;background:#fff;color:var(--ink);padding:14px 28px;border-radius:var(--pill);text-decoration:none;font-weight:700;box-shadow:0 8px 24px rgba(0,0,0,.15)}}
.breadcrumb{{font-size:.82rem;color:var(--muted);margin-bottom:32px}}
.breadcrumb a{{color:var(--muted);text-decoration:none}}.breadcrumb a:hover{{color:var(--ink)}}
.breadcrumb span{{opacity:.4;margin:0 6px}}
</style>
</head>
<body>
<a href="#main-content" style="position:absolute;left:0;top:0;background:#fff;color:#073044;padding:8px 16px;border-radius:8px;z-index:1000;clip:rect(0,0,0,0);focus:clip(auto)">Skip to content</a>
<div class="wrap" id="main-content">
<nav aria-label="Breadcrumb" class="breadcrumb">
  <a href="/">SideGuy</a><span>/</span><a href="/comparisons-hub.html">Comparisons</a><span>/</span>{a} vs {b}
</nav>

<h1>{p["h1"]}</h1>
<p class="lede">{p["intro"]}</p>

<div class="vs-grid">
  <div class="vs-card">
    <h3>{p["a_section_title"]}</h3>
    <ul>{a_points_html}</ul>
  </div>
  <div class="vs-card">
    <h3>{p["b_section_title"]}</h3>
    <ul>{b_points_html}</ul>
  </div>
</div>

<div class="cost-box">
  <h2>{p["cost_title"]}</h2>
  <p style="font-size:16px;line-height:1.75;color:var(--muted);margin:0">{p["cost_body"]}</p>
</div>

<div class="verdict">
  <h2>{p["verdict_title"]}</h2>
  <p>{p["verdict_body"]}</p>
</div>

<h2 id="faq">Common Questions</h2>
<div class="faq-block">{faq_html}</div>

<div class="cta">
  <h3>Not sure which is right for your situation?</h3>
  <p>Text PJ — get a straight answer with no sales pitch. Free, fast, human.</p>
  <a href="sms:+17735441231">Text 773-544-1231</a>
</div>

<p style="font-size:13px;color:var(--muted2);margin-top:40px">
  <a href="/" style="color:var(--muted2)">SideGuy Solutions</a> &middot;
  San Diego, CA &middot;
  <a href="/tech-help-hub-san-diego.html" style="color:var(--muted2)">Tech Help Hub</a>
</p>
</div>
</body>
</html>"""


if __name__ == "__main__":
    generated = []
    for p in PAIRS:
        slug = p["canonical_slug"]
        out = ROOT / f"{slug}.html"
        if out.exists():
            print(f"SKIP (exists): {slug}.html")
            continue
        out.write_text(build_page(p), encoding="utf-8")
        generated.append(slug)
        print(f"GENERATED: {slug}.html")

    print(f"\nDone — {len(generated)} pages generated.")
    if generated:
        print("Slugs:", generated)
