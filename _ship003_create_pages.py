#!/usr/bin/env python3
"""SHIP-003: Create 5 top-impression missing pages with pricing + comparison + FAQ + CTA."""

import os

BASE = "/workspaces/sideguy-solutions"
PHONE_SMS = "sms:+17735441231"
PHONE_DISPLAY = "773-544-1231"

HEAD_TPL = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<link rel="canonical" href="https://sideguy.solutions/{slug}"/>
<meta name="description" content="{meta}"/>
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
table.compare{{width:100%;border-collapse:collapse;font-size:15px}}
table.compare th{{background:var(--mint);color:#fff;padding:12px 14px;text-align:left}}
table.compare td{{padding:11px 14px;border-bottom:1px solid var(--stroke);color:var(--muted)}}
table.compare tr:last-child td{{border-bottom:none}}
table.compare tr:nth-child(even) td{{background:rgba(33,211,161,.06)}}
.bullets{{list-style:none;padding:0;margin:0}}
.bullets li{{padding:10px 0 10px 32px;position:relative;border-bottom:1px solid var(--stroke);font-size:16px;color:var(--muted);line-height:1.5}}
.bullets li:last-child{{border-bottom:none}}
.bullets li::before{{content:"→";position:absolute;left:0;color:var(--mint);font-weight:700}}
.cta-box{{background:linear-gradient(135deg,var(--mint),var(--blue));color:#fff;padding:40px 36px;border-radius:var(--r);text-align:center;margin:48px 0}}
.cta-box h2{{margin:0 0 12px;font-size:28px}}
.cta-box p{{margin:0 0 24px;font-size:17px;opacity:.95;line-height:1.6}}
.cta-box a{{display:inline-block;background:#fff;color:var(--ink);padding:16px 32px;border-radius:var(--pill);text-decoration:none;font-weight:700;font-size:17px;box-shadow:0 8px 24px rgba(0,0,0,.15)}}
details{{border:1px solid var(--stroke);border-radius:16px;padding:18px 22px;margin-bottom:12px;background:var(--card)}}
summary{{font-weight:700;font-size:17px;cursor:pointer;color:var(--ink)}}
details p{{margin:12px 0 0;color:var(--muted);line-height:1.7;font-size:15px}}
.floating{{position:fixed;bottom:24px;right:24px;display:flex;align-items:center;gap:10px;z-index:999}}
.floatBtn{{background:var(--mint);color:#fff;padding:14px 20px;border-radius:var(--pill);text-decoration:none;font-weight:700;font-size:15px;box-shadow:0 8px 28px rgba(33,211,161,.35)}}
@media(max-width:640px){{h1{{font-size:32px}}.cta-box{{padding:28px 20px}}table.compare{{font-size:13px}}}}
</style>
</head>
<body>
<div class="wrap">
  <div class="hub-back">&#x2190; <a href="{hub_href}">{hub_label}</a> &mdash; {hub_desc}</div>
"""

TAIL_TPL = """\
  <div class="floating">
    <a class="floatBtn" href="{phone_sms}">Text PJ &mdash; {phone_display}</a>
  </div>
</div>
{schema}
</body>
</html>
"""

def schema_local(name, description, url):
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{name}",
  "description": "{description}",
  "url": "{url}",
  "telephone": "+17735441231",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "San Diego",
    "addressRegion": "CA",
    "addressCountry": "US"
  }},
  "areaServed": "San Diego, CA"
}}
</script>"""

def schema_faq(pairs):
    items = "\n    ".join(
        f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}'
        for q, a in pairs
    )
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {items}
  ]
}}
</script>"""


# ─────────────────────────────────────────────────────────────
# PAGE 1: mobile-payment-systems-san-diego.html
# ─────────────────────────────────────────────────────────────
p1_slug = "mobile-payment-systems-san-diego.html"
p1_title = "Mobile Payment Systems San Diego — What Works for Local Businesses | SideGuy Solutions"
p1_meta = "Comparing mobile payment systems for San Diego businesses. Stripe, Square, Clover, PayPal — real costs, real limits, and what to ask before you sign. Free guidance."

p1_faq_pairs = [
    ("What is the cheapest mobile payment system in San Diego?", "For most micro-businesses, Square's free reader has the lowest entry cost — 2.6% + 10¢ per tap/swipe. But if you process over $15,000/month, a merchant account through a local processor will cost less overall."),
    ("Is Square or Stripe better for mobile businesses?", "Square is simpler to start — hardware ships fast, no monthly fee on the base plan. Stripe is more flexible if you also sell online or need API integrations. Both work well in San Diego."),
    ("Do I need a business account to use a mobile payment system?", "No — personal debit works for setup, but you'll want a business bank account within 30–60 days to avoid holds and simplify taxes."),
    ("What fees should I expect?", "Typical mobile rates: 2.6–2.9% + 10–30¢ per transaction. Monthly fees range from $0 (Square basic) to $99+ (Clover). Watch for batch fees, chargeback fees, and early termination clauses."),
    ("Can I use a mobile payment system for recurring billing?", "Yes — Square, Stripe, and PayPal all support recurring invoices. For true subscription billing with dunning management, Stripe is the strongest option."),
    ("What if I have bad credit — will they approve me?", "Square and PayPal use soft credit pulls and approve most applicants instantly. Traditional merchant accounts do a hard pull and may decline or hold funds for 3–6 months if you're high-risk."),
]

p1_body = f"""\
  <h1>Mobile Payment Systems for San Diego Businesses — Honest Comparison</h1>
  <div class="lede">Stripe vs Square vs Clover vs PayPal — the differences are real, and the wrong choice costs money. Here's what matters for San Diego mobile and field-service businesses before you commit to a system.</div>

  <div class="section">
    <h2>&#x1F4B3; Side-by-Side Cost Comparison</h2>
    <div class="card" style="overflow-x:auto">
      <table class="compare">
        <thead><tr><th>System</th><th>Swipe/Tap Rate</th><th>Monthly Fee</th><th>Hardware Cost</th><th>Best For</th></tr></thead>
        <tbody>
          <tr><td>Square</td><td>2.6% + 10¢</td><td>$0–$60</td><td>Free–$299</td><td>Retail, food trucks, pop-ups</td></tr>
          <tr><td>Stripe</td><td>2.7% + 5¢</td><td>$0</td><td>$59–$299</td><td>Online + in-person hybrid</td></tr>
          <tr><td>Clover</td><td>2.3–2.6%</td><td>$15–$95</td><td>$49–$999</td><td>Restaurants, full POS setups</td></tr>
          <tr><td>PayPal Zettle</td><td>2.29% + 9¢</td><td>$0</td><td>$29–$199</td><td>Occasional sellers, events</td></tr>
          <tr><td>Local Merchant Acct</td><td>~1.5–2.0%</td><td>$25–$75</td><td>Varies</td><td>High-volume businesses ($15k+/mo)</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:14px;color:var(--muted2);margin-top:10px;padding:0 4px">Rates as of 2025. Always verify current pricing directly with the provider — fees change.</p>
  </div>

  <div class="section">
    <h2>&#x1F501; When Should You Switch Mobile Payment Systems?</h2>
    <div class="card">
      <ul class="bullets">
        <li>Your current processor holds funds for more than 2 business days</li>
        <li>You're paying over 2.9% on card-present transactions</li>
        <li>The hardware keeps dropping connections at job sites</li>
        <li>You're locked into a contract with an early termination fee</li>
        <li>You need offline mode but your current system doesn't support it</li>
        <li>You're adding recurring billing or invoicing and the current system can't do it</li>
        <li>You got a chargeback and had no dispute support from your processor</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4B0; Typical Pricing for San Diego Field-Service Businesses</h2>
    <div class="card">
      <ul class="bullets">
        <li><strong>Under $5,000/month:</strong> Square or PayPal — no monthly fee makes sense</li>
        <li><strong>$5,000–$15,000/month:</strong> Stripe or Clover — consider a plan with interchange-plus pricing</li>
        <li><strong>Over $15,000/month:</strong> Negotiate a merchant account — you should be paying closer to 1.5–1.8% effective rate</li>
        <li><strong>Multi-location or franchise:</strong> Clover or a dedicated ISO — centralized reporting is worth the premium</li>
      </ul>
    </div>
  </div>

  <div class="cta-box">
    <h2>Not Sure Which System Fits Your Business?</h2>
    <p>Text PJ your monthly volume and current processor. We'll tell you if you're overpaying and which system makes sense for your setup — no sales pitch, just clarity.</p>
    <a href="{PHONE_SMS}">Text PJ &mdash; {PHONE_DISPLAY}</a>
  </div>

  <div class="section">
    <h2>&#x2753; Frequently Asked Questions</h2>
"""
for q, a in p1_faq_pairs:
    p1_body += f"    <details><summary>{q}</summary><p>{a}</p></details>\n"
p1_body += "  </div>\n"

p1_schema = schema_local(
    "SideGuy Solutions — Mobile Payment Systems Guidance San Diego",
    "Honest guidance on mobile payment systems for San Diego small businesses. Compare Square, Stripe, Clover, and merchant accounts.",
    f"https://sideguy.solutions/{p1_slug}"
) + "\n" + schema_faq(p1_faq_pairs)

p1 = HEAD_TPL.format(
    title=p1_title, slug=p1_slug, meta=p1_meta,
    hub_href="payment-processing-hub-san-diego.html",
    hub_label="Payment Processing Hub", hub_desc="San Diego payment guidance"
) + p1_body + TAIL_TPL.format(
    phone_sms=PHONE_SMS, phone_display=PHONE_DISPLAY, schema=p1_schema
)


# ─────────────────────────────────────────────────────────────
# PAGE 2: ai-business-solutions-san-diego.html
# ─────────────────────────────────────────────────────────────
p2_slug = "ai-business-solutions-san-diego.html"
p2_title = "AI Business Solutions San Diego — What Actually Works for Small Businesses | SideGuy Solutions"
p2_meta = "Realistic AI solutions for San Diego small businesses. What to automate first, what it costs, and which vendors to avoid. Plain-language guidance before you spend."

p2_faq_pairs = [
    ("What AI tools are actually useful for small businesses in San Diego?", "Start with the basics: AI-drafted emails and estimates (ChatGPT/Claude), automated scheduling and follow-up (Calendly + Zapier), and AI call answering (Signpost, Smith.ai). Most businesses see ROI within 60 days on these three."),
    ("How much does an AI business solution cost?", "Entry-level: $50–$200/month for off-the-shelf tools. Custom automations: $2,000–$8,000 one-time build. Full AI consultant engagement: $150–$300/hour. Most San Diego small businesses start with $100–$300/month and scale from there."),
    ("Do I need a developer to set up AI tools for my business?", "For most off-the-shelf tools (Zapier, Make, Notion AI, HubSpot AI), no. For custom integrations or training models on your business data, yes — budget for a few hours of technical setup."),
    ("What should I automate first?", "Follow-up messages after leads go cold. Estimate generation. Review request texts after a job is complete. These three automations consistently save 5–10 hours per week for San Diego service businesses."),
    ("Is AI a good fit for my type of business?", "AI adds the most value when there's repetitive communication, scheduling, or document generation. HVAC, plumbing, landscaping, cleaning, and professional services all see strong ROI. Highly custom or relationship-intensive work — less so."),
    ("What are the risks of AI for my business?", "Over-automation of customer communication is the #1 mistake. Customers can tell when they're talking to a bot. Use AI for back-office tasks first; keep client-facing touchpoints human until you've tested carefully."),
]

p2_body = f"""\
  <h1>AI Business Solutions for San Diego — What&#8217;s Worth It in 2025</h1>
  <div class="lede">AI tools range from genuinely useful to expensive distractions. This is the honest breakdown for San Diego small business owners: what to try first, what it costs, and how to avoid wasting money on demos that don't deliver.</div>

  <div class="section">
    <h2>&#x1F4CA; AI Solution Options — Cost and Complexity Comparison</h2>
    <div class="card" style="overflow-x:auto">
      <table class="compare">
        <thead><tr><th>Approach</th><th>Monthly Cost</th><th>Setup Time</th><th>Tech Skill Needed</th><th>Best For</th></tr></thead>
        <tbody>
          <tr><td>Off-the-shelf AI tools (Zapier, HubSpot, etc.)</td><td>$50–$300</td><td>1–3 days</td><td>Low (no code)</td><td>Automating follow-ups, scheduling</td></tr>
          <tr><td>AI call answering (Smith.ai, Signpost)</td><td>$200–$500</td><td>1–2 days</td><td>Very low</td><td>Capturing leads 24/7</td></tr>
          <tr><td>Custom automations (Zapier/Make workflows)</td><td>$100–$400</td><td>1–2 weeks</td><td>Low–Medium</td><td>Multi-step business processes</td></tr>
          <tr><td>AI consulting + custom build</td><td>$500–$2,000</td><td>2–6 weeks</td><td>Handled for you</td><td>Complex workflows, integrations</td></tr>
          <tr><td>Enterprise AI platform</td><td>$2,000–$10,000+</td><td>Months</td><td>High or outsourced</td><td>Large orgs with dedicated IT</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F501; Best First AI Automations for San Diego Businesses</h2>
    <div class="card">
      <ul class="bullets">
        <li><strong>Lead follow-up texts:</strong> Auto-text new leads within 5 minutes of form submission (Zapier + Twilio, ~$30/month)</li>
        <li><strong>Review requests:</strong> Text customers 24 hours after job completion — Google reviews climb fast</li>
        <li><strong>AI estimates:</strong> Feed your labor + material data to ChatGPT or Claude to draft estimates in seconds</li>
        <li><strong>Call answering after hours:</strong> Smith.ai or Signpost captures leads while you're on job sites</li>
        <li><strong>Invoice reminders:</strong> Automated 7/14/30-day payment reminders (QuickBooks, Wave, or custom Zapier)</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x26A0;&#xFE0F; Red Flags When Evaluating AI Vendors</h2>
    <div class="card" style="border-left:4px solid var(--red)">
      <ul class="bullets">
        <li>Demo uses generic data — ask to see it working with your actual business type</li>
        <li>No clear ROI timeline — any good vendor should show payback within 90 days for basic tools</li>
        <li>Annual contract required before a trial period</li>
        <li>"Custom AI" that turns out to be a reskinned ChatGPT with a monthly subscription markup</li>
        <li>Vendor can't explain what happens to your customer data</li>
      </ul>
    </div>
  </div>

  <div class="cta-box">
    <h2>Not Sure What AI Can Actually Do for Your Business?</h2>
    <p>Text PJ a quick description of your biggest time drain. We'll tell you whether there's an AI fix, what it costs, and which vendors to talk to — no upsell, just honest answers.</p>
    <a href="{PHONE_SMS}">Text PJ &mdash; {PHONE_DISPLAY}</a>
  </div>

  <div class="section">
    <h2>&#x2753; Frequently Asked Questions</h2>
"""
for q, a in p2_faq_pairs:
    p2_body += f"    <details><summary>{q}</summary><p>{a}</p></details>\n"
p2_body += "  </div>\n"

p2_schema = schema_local(
    "SideGuy Solutions — AI Business Solutions San Diego",
    "Plain-language AI business solutions guidance for San Diego small businesses. What to automate, what it costs, and how to avoid wasting money.",
    f"https://sideguy.solutions/{p2_slug}"
) + "\n" + schema_faq(p2_faq_pairs)

p2 = HEAD_TPL.format(
    title=p2_title, slug=p2_slug, meta=p2_meta,
    hub_href="ai-agent-automation.html",
    hub_label="AI Automation Hub", hub_desc="San Diego AI automation guidance"
) + p2_body + TAIL_TPL.format(
    phone_sms=PHONE_SMS, phone_display=PHONE_DISPLAY, schema=p2_schema
)


# ─────────────────────────────────────────────────────────────
# PAGE 3: payment-processing-solutions-san-diego.html
# ─────────────────────────────────────────────────────────────
p3_slug = "payment-processing-solutions-san-diego.html"
p3_title = "Payment Processing Solutions San Diego — Compare Your Options | SideGuy Solutions"
p3_meta = "Honest comparison of payment processing solutions for San Diego businesses. Stripe, Square, merchant accounts, and crypto — real rates, real pros and cons. Free guidance."

p3_faq_pairs = [
    ("What is the best payment processing solution for a San Diego small business?", "It depends on your volume. Under $10k/month: Square. $10k–$50k/month: Stripe or a local merchant account with interchange-plus pricing. Over $50k/month: negotiate directly with a processor — you have leverage."),
    ("What is interchange-plus pricing?", "A transparent pricing model where you pay the actual card network cost (interchange) plus a fixed markup. Far better than flat-rate pricing at higher volumes — saves 0.3–0.8% on most transactions."),
    ("How long does it take to switch payment processors?", "Typically 1–5 business days for setup. If you're switching POS hardware, add 1–2 weeks for shipping. Plan the switch on a slow week — there's always a short test period before going live."),
    ("What are hidden fees to watch for?", "Statement fees ($5–$15/month), batch fees ($0.05–$0.25/day), chargeback fees ($15–$35 each), PCI non-compliance fees ($30–$100/month if you don't complete an annual questionnaire), and early termination fees (up to $500)."),
    ("Can I accept payments without a merchant account?", "Yes — Square, Stripe, and PayPal are payment facilitators that handle the merchant account for you. It's simpler but usually more expensive per transaction than a true merchant account."),
    ("What is the cheapest way to accept cards in San Diego?", "For occasional payments: PayPal Zettle at 2.29% + 9¢. For regular business: Square's free reader at 2.6% + 10¢. For high volume: negotiate a merchant account targeting under 2%."),
]

p3_body = f"""\
  <h1>Payment Processing Solutions for San Diego Businesses — Real Comparison</h1>
  <div class="lede">There are dozens of payment processors and no shortage of sales reps pushing their platforms. This is the neutral breakdown: what each type of solution costs, what it's good for, and when you should switch.</div>

  <div class="section">
    <h2>&#x1F4B3; Payment Processing Solutions Compared</h2>
    <div class="card" style="overflow-x:auto">
      <table class="compare">
        <thead><tr><th>Solution Type</th><th>Card Rate</th><th>Monthly Fee</th><th>Setup Time</th><th>Best For</th></tr></thead>
        <tbody>
          <tr><td>Square (free plan)</td><td>2.6% + 10¢</td><td>$0</td><td>Same day</td><td>New or micro businesses</td></tr>
          <tr><td>Stripe</td><td>2.7% + 5¢</td><td>$0</td><td>1–2 days</td><td>Online + in-person hybrid</td></tr>
          <tr><td>Clover</td><td>2.3–2.6%</td><td>$15–$95</td><td>3–5 days</td><td>Full-service retail/restaurant POS</td></tr>
          <tr><td>Merchant Account (ISO)</td><td>~1.5–2.0% effective</td><td>$25–$75</td><td>1–2 weeks</td><td>High-volume ($15k+/month)</td></tr>
          <tr><td>Crypto (Solana, USDC)</td><td>0.1–0.3%</td><td>$0–$30</td><td>1–3 days</td><td>Businesses open to crypto</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F501; Signs You Need a Better Payment Processing Solution</h2>
    <div class="card">
      <ul class="bullets">
        <li>Paying more than 2.5% effective rate on card-present transactions at $10k+/month volume</li>
        <li>Funds held for more than 2 business days regularly</li>
        <li>No detailed reporting — you can't easily see fee breakdowns</li>
        <li>Chargebacks handled slowly or with no support</li>
        <li>You're on a flat-rate plan but processing over $15,000/month — interchange-plus would be cheaper</li>
        <li>Your processor doesn't offer payment links, invoicing, or recurring billing</li>
        <li>Contract has early termination fees you weren't told about upfront</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4B0; What You Should Realistically Pay</h2>
    <div class="card">
      <ul class="bullets">
        <li><strong>Under $5,000/month:</strong> 2.6–2.9% is normal — not worth the complexity of a merchant account</li>
        <li><strong>$5,000–$15,000/month:</strong> Target 2.2–2.5% effective rate. Ask any processor for interchange-plus pricing.</li>
        <li><strong>$15,000–$50,000/month:</strong> Target 1.8–2.2% effective rate. Multiple processors should compete for your business.</li>
        <li><strong>Over $50,000/month:</strong> Target sub-1.8%. Consider a dedicated ISO or direct processor relationship.</li>
      </ul>
    </div>
  </div>

  <div class="cta-box">
    <h2>Want a Second Opinion on Your Processing Costs?</h2>
    <p>Text PJ your current monthly volume and processing rate. We'll tell you in plain language whether you're paying too much and who to talk to next.</p>
    <a href="{PHONE_SMS}">Text PJ &mdash; {PHONE_DISPLAY}</a>
  </div>

  <div class="section">
    <h2>&#x2753; Frequently Asked Questions</h2>
"""
for q, a in p3_faq_pairs:
    p3_body += f"    <details><summary>{q}</summary><p>{a}</p></details>\n"
p3_body += "  </div>\n"

p3_schema = schema_local(
    "SideGuy Solutions — Payment Processing Solutions San Diego",
    "Neutral comparison of payment processing solutions for San Diego businesses. Real rates, hidden fees explained, free guidance.",
    f"https://sideguy.solutions/{p3_slug}"
) + "\n" + schema_faq(p3_faq_pairs)

p3 = HEAD_TPL.format(
    title=p3_title, slug=p3_slug, meta=p3_meta,
    hub_href="payment-processing-hub-san-diego.html",
    hub_label="Payment Processing Hub", hub_desc="San Diego payment guidance"
) + p3_body + TAIL_TPL.format(
    phone_sms=PHONE_SMS, phone_display=PHONE_DISPLAY, schema=p3_schema
)


# ─────────────────────────────────────────────────────────────
# PAGE 4: electronic-payment-solutions-san-diego.html
# ─────────────────────────────────────────────────────────────
p4_slug = "electronic-payment-solutions-san-diego.html"
p4_title = "Electronic Payment Solutions San Diego — Tap, Swipe, or Invoice | SideGuy Solutions"
p4_meta = "Electronic payment solutions for San Diego businesses — tap-to-pay, invoicing, ACH, QR codes, and more. Honest comparison of what works and what it costs."

p4_faq_pairs = [
    ("What are electronic payment solutions?", "Any non-cash payment method: credit/debit cards (tap, swipe, chip), ACH bank transfers, digital wallets (Apple Pay, Google Pay), QR code payments, invoicing platforms, and buy-now-pay-later. Most businesses need 2–3 of these."),
    ("What is the cheapest electronic payment method?", "ACH (bank transfer) is the cheapest — typically $0.25–$1.50 flat per transaction regardless of amount, making it ideal for invoices over $500. Card payments at 2–3% cost more per transaction but are faster for customers to use."),
    ("Does tap-to-pay cost more than swiping?", "No — most processors charge the same rate for tap (NFC), swipe (magstripe), and chip (EMV). All three are considered card-present transactions with lower fraud risk than online payments."),
    ("What is ACH payment processing?", "ACH transfers money directly between bank accounts. Slower (1–3 business days) but cheaper than cards. Great for recurring billing, B2B invoices, payroll, and large transactions. Square, Stripe, and most invoicing platforms support ACH."),
    ("Do customers in San Diego prefer tap-to-pay?", "Yes — contactless payment adoption in San Diego is high. If you don't have a tap-capable reader, you're creating friction. Most Square, Stripe, and Clover hardware supports tap-to-pay out of the box."),
    ("Can I send electronic invoices and still accept cash?", "Absolutely. Most businesses use multiple payment types. Square and Stripe let you record cash payments manually while also sending electronic invoices and accepting card/ACH."),
]

p4_body = f"""\
  <h1>Electronic Payment Solutions for San Diego Businesses — What to Use and When</h1>
  <div class="lede">Electronic payments cover everything from tap-to-pay at a register to ACH bank transfers for large invoices. This is the plain-language breakdown of what each method costs and when to use it for a San Diego business.</div>

  <div class="section">
    <h2>&#x1F4B3; Electronic Payment Methods Compared</h2>
    <div class="card" style="overflow-x:auto">
      <table class="compare">
        <thead><tr><th>Method</th><th>Typical Cost</th><th>Speed to Funds</th><th>Customer Friction</th><th>Best For</th></tr></thead>
        <tbody>
          <tr><td>Tap-to-Pay (NFC)</td><td>2.6% + 10¢</td><td>1–2 days</td><td>Very low</td><td>In-person, retail, food</td></tr>
          <tr><td>Chip (EMV)</td><td>2.6% + 10¢</td><td>1–2 days</td><td>Low</td><td>In-person counter transactions</td></tr>
          <tr><td>Online / Card-not-present</td><td>2.9% + 30¢</td><td>1–2 days</td><td>Low</td><td>E-commerce, invoices</td></tr>
          <tr><td>ACH Bank Transfer</td><td>$0.25–$1.50 flat</td><td>2–3 days</td><td>Medium</td><td>Large invoices, recurring billing</td></tr>
          <tr><td>Digital Wallets (Apple/Google Pay)</td><td>Same as tap</td><td>1–2 days</td><td>Very low</td><td>Mobile-first customers</td></tr>
          <tr><td>QR Code Payment</td><td>2.6–2.9%</td><td>1–2 days</td><td>Low</td><td>Tables, menus, service drop-offs</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F501; When to Add a New Electronic Payment Method</h2>
    <div class="card">
      <ul class="bullets">
        <li>Customers are asking "can I pay by Zelle/Venmo?" — consider adding ACH or a digital wallet option</li>
        <li>You have large invoices ($500+) but are paying 2.9% card fees — switch those to ACH</li>
        <li>You're doing outdoor events, markets, or field work — tap-to-pay hardware is essential</li>
        <li>Repeat customers paying the same amount monthly — set up recurring billing instead of re-invoicing</li>
        <li>Your current hardware doesn't accept tap or chip — chargeback liability increased in 2015 for swipe-only businesses</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4B0; What Electronic Payments Should Cost</h2>
    <div class="card">
      <ul class="bullets">
        <li><strong>Card-present transactions:</strong> 2.3–2.7% is competitive. Above 2.9% consistently — time to renegotiate.</li>
        <li><strong>Online/invoiced card payments:</strong> 2.7–3.2% is normal. ACH alternatives at $0.25–$1.50 flat save money on large amounts.</li>
        <li><strong>ACH processing:</strong> Should be under $1.00 per transaction at most processors. Some charge 0.5–1% capped at $5–$10 for larger amounts.</li>
        <li><strong>Digital wallets:</strong> No extra fee — charged same rate as tap/swipe. Never pay a surcharge for Apple Pay.</li>
      </ul>
    </div>
  </div>

  <div class="cta-box">
    <h2>Which Electronic Payment Setup Fits Your Business?</h2>
    <p>Text PJ your business type and monthly volume. We'll map out the right mix of payment methods for your situation — no sales pitch, just honest recommendations.</p>
    <a href="{PHONE_SMS}">Text PJ &mdash; {PHONE_DISPLAY}</a>
  </div>

  <div class="section">
    <h2>&#x2753; Frequently Asked Questions</h2>
"""
for q, a in p4_faq_pairs:
    p4_body += f"    <details><summary>{q}</summary><p>{a}</p></details>\n"
p4_body += "  </div>\n"

p4_schema = schema_local(
    "SideGuy Solutions — Electronic Payment Solutions San Diego",
    "Electronic payment solutions guidance for San Diego businesses — tap, ACH, digital wallets, QR codes. Honest comparison with real costs.",
    f"https://sideguy.solutions/{p4_slug}"
) + "\n" + schema_faq(p4_faq_pairs)

p4 = HEAD_TPL.format(
    title=p4_title, slug=p4_slug, meta=p4_meta,
    hub_href="payment-processing-hub-san-diego.html",
    hub_label="Payment Processing Hub", hub_desc="San Diego payment guidance"
) + p4_body + TAIL_TPL.format(
    phone_sms=PHONE_SMS, phone_display=PHONE_DISPLAY, schema=p4_schema
)


# ─────────────────────────────────────────────────────────────
# PAGE 5: battery-backup-installation-san-diego.html
# ─────────────────────────────────────────────────────────────
p5_slug = "battery-backup-installation-san-diego.html"
p5_title = "Battery Backup Installation San Diego — Costs, Options, and What to Ask | SideGuy Solutions"
p5_meta = "Battery backup installation in San Diego — whole-home vs panel-level, Tesla Powerwall vs Enphase vs LG Chem. Real costs, what SDG&E NEM 3.0 means for you, free guidance."

p5_faq_pairs = [
    ("How much does a battery backup system cost in San Diego?", "A single battery (10–13.5 kWh) installed typically runs $12,000–$18,000 before incentives. With the federal 30% tax credit, your out-of-pocket drops to $8,400–$12,600. Two batteries for whole-home backup run $18,000–$30,000 before incentives."),
    ("What is the best battery backup for San Diego homes?", "Tesla Powerwall 3 (13.5 kWh), Enphase IQ Battery 5P, and LG Chem RESU are the three most commonly installed in San Diego. Powerwall has the best all-in-one integration; Enphase is best if you already have an Enphase solar system."),
    ("Is battery backup worth it in San Diego without solar?", "Grid-only battery installations are less common and harder to get approved as standalone systems, but SDG&E's Time-of-Use rates (peak at 4–9pm) mean you can charge cheap overnight and discharge during expensive hours — potentially saving $80–$200/month."),
    ("How does NEM 3.0 affect battery backup in San Diego?", "Under NEM 3.0 (April 2023+), SDG&E pays much less for excess solar exported to the grid. Battery storage becomes essential to capture your solar generation for use at peak pricing hours rather than exporting it cheap."),
    ("How long does battery backup installation take?", "Typically 1–3 days for a single battery. Permit approval from San Diego adds 2–6 weeks to the timeline in most cases. Tesla and Enphase Certified installers handle permitting — ask your installer for recent permit turnaround times."),
    ("What rebates or incentives are available for battery backup in San Diego?", "Federal ITC (30% tax credit) applies to batteries paired with solar. SGIP (California Self-Generation Incentive Program) provides $200–$1,000/kWh rebates for qualifying installations — waitlist varies. SDG&E has no direct battery rebate as of 2025 but offers TOU rate plans that improve ROI."),
]

p5_body = f"""\
  <h1>Battery Backup Installation in San Diego — What It Costs and What to Ask</h1>
  <div class="lede">Whether you&#8217;re worried about outages, want to maximize solar under NEM 3.0, or just want to stop paying SDG&E peak rates, here&#8217;s the honest breakdown of battery backup options, costs, and how to evaluate an installer&#8217;s quote.</div>

  <div class="section">
    <h2>&#x1F50B; Top Battery Backup Systems Compared</h2>
    <div class="card" style="overflow-x:auto">
      <table class="compare">
        <thead><tr><th>System</th><th>Capacity</th><th>Installed Cost (est.)</th><th>With 30% ITC Credit</th><th>Best For</th></tr></thead>
        <tbody>
          <tr><td>Tesla Powerwall 3</td><td>13.5 kWh</td><td>$14,500–$17,500</td><td>~$10,000–$12,250</td><td>Whole-home integration, solar pairing</td></tr>
          <tr><td>Enphase IQ Battery 5P</td><td>5 kWh (expandable)</td><td>$8,000–$12,000</td><td>~$5,600–$8,400</td><td>Enphase solar systems, modular builds</td></tr>
          <tr><td>LG Chem RESU 16H</td><td>16 kWh</td><td>$15,000–$20,000</td><td>~$10,500–$14,000</td><td>High capacity needs</td></tr>
          <tr><td>Franklin WH</td><td>13.6 kWh</td><td>$13,000–$16,500</td><td>~$9,100–$11,550</td><td>Multi-battery whole-home setups</td></tr>
          <tr><td>Generac PWRcell</td><td>9–18 kWh</td><td>$12,000–$22,000</td><td>~$8,400–$15,400</td><td>Flexible capacity scalability</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:14px;color:var(--muted2);margin-top:10px;padding:0 4px">Costs are estimates based on San Diego installer quotes as of 2025. Get at least 3 quotes. Federal ITC is 30% — confirm eligibility with your tax advisor.</p>
  </div>

  <div class="section">
    <h2>&#x1F501; Signs It&#8217;s Time to Add Battery Backup</h2>
    <div class="card">
      <ul class="bullets">
        <li>You have solar under NEM 3.0 and are exporting power during the day at low rates</li>
        <li>SDG&E outages in your area (Wildfire Transmission Shutdowns) interrupting work or medical equipment</li>
        <li>Your SDG&E TOU bill spikes on peak-tier hours (4–9pm weekdays)</li>
        <li>You&#8217;re adding solar and want to maximize ROI under current NEM 3.0 export rates</li>
        <li>You work from home and power outages cost you client hours</li>
        <li>You have a pool pump, medical equipment, or EV charger that can&#8217;t go offline</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>&#x1F4B0; What a Reasonable Battery Quote Should Include</h2>
    <div class="card">
      <ul class="bullets">
        <li>Battery brand, model, and exact kWh capacity listed</li>
        <li>Labor and equipment costs broken out separately</li>
        <li>Permit fees and expected timeline (San Diego permits often take 4–6 weeks)</li>
        <li>Inverter type (if applicable — some batteries have built-in inverters)</li>
        <li>Load coverage details: what circuits are backed up vs. whole-home</li>
        <li>Installer&#8217;s CSLB license number and Tesla/Enphase certification (if applicable)</li>
        <li>Monitoring app access and any ongoing maintenance fees</li>
        <li>Utility interconnection documentation handled by installer</li>
      </ul>
    </div>
  </div>

  <div class="cta-box">
    <h2>Got a Battery Backup Quote? Text It to PJ.</h2>
    <p>We&#8217;ll check the pricing, flag anything missing, and tell you whether the system is actually sized right for your home. Free second opinion before you commit $10,000+.</p>
    <a href="{PHONE_SMS}">Text PJ &mdash; {PHONE_DISPLAY}</a>
  </div>

  <div class="section">
    <h2>&#x2753; Frequently Asked Questions</h2>
"""
for q, a in p5_faq_pairs:
    p5_body += f"    <details><summary>{q}</summary><p>{a}</p></details>\n"
p5_body += "  </div>\n"

p5_schema = schema_local(
    "SideGuy Solutions — Battery Backup Installation San Diego",
    "Battery backup installation guidance for San Diego homeowners. Compare Tesla Powerwall, Enphase, LG Chem — real costs, NEM 3.0 context, free second opinion on quotes.",
    f"https://sideguy.solutions/{p5_slug}"
) + "\n" + schema_faq(p5_faq_pairs)

p5 = HEAD_TPL.format(
    title=p5_title, slug=p5_slug, meta=p5_meta,
    hub_href="solar-battery-backup-install.html",
    hub_label="Solar Battery Install", hub_desc="San Diego solar &amp; battery guidance"
) + p5_body + TAIL_TPL.format(
    phone_sms=PHONE_SMS, phone_display=PHONE_DISPLAY, schema=p5_schema
)


# ─────────────────────────────────────────────────────────────
# WRITE ALL PAGES
# ─────────────────────────────────────────────────────────────
pages = [
    (p1_slug, p1),
    (p2_slug, p2),
    (p3_slug, p3),
    (p4_slug, p4),
    (p5_slug, p5),
]

for slug, content in pages:
    path = os.path.join(BASE, slug)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    size = os.path.getsize(path)
    print(f"CREATED: {slug} ({size:,} bytes)")

print("\nAll 5 SHIP-003 pages written.")
