#!/usr/bin/env python3
"""
SIDEGUY Concept Authority Engine
Wikipedia-style deep-reference pages for pillar-level search traffic.

Pages generated:
  concepts/ai-automation.html
  concepts/prediction-markets.html
  concepts/crypto-payments.html
  concepts/payment-processing.html
  concepts/index.html

Also updates: sitemap.xml, knowledge/sideguy-knowledge-map.html
"""

import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
CONCEPTS_DIR = ROOT / "concepts"
CONCEPTS_DIR.mkdir(exist_ok=True)

TODAY = date.today().isoformat()
DOMAIN = "https://sideguysolutions.com"
PHONE_DISPLAY = "773-544-1231"
PHONE_SMS = "+17735441231"

# ──────────────────────────────────────────────
# SHARED CSS  (light ocean — same as clusters/generated)
# ──────────────────────────────────────────────

CSS = """
  :root {
    --bg0:#eefcff; --bg1:#d7f5ff; --ink:#073044; --muted:#3f6173;
    --mint:#21d3a1; --mint2:#00c7ff; --blue2:#1f7cff;
    --r:22px; --pill:999px;
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body {
    font-family: -apple-system, system-ui, Segoe UI, Roboto, Inter, sans-serif;
    background: radial-gradient(ellipse at 60% 0%, #c5f4ff 0%, #eefcff 55%, #fff 100%);
    color: var(--ink);
    min-height: 100vh;
  }
  a{color:var(--blue2);text-decoration:none}
  a:hover{text-decoration:underline}

  /* nav */
  nav.bc {
    padding: 12px 24px;
    font-size: .8rem;
    color: var(--muted);
    border-bottom: 1px solid rgba(0,0,0,.06);
    background: rgba(255,255,255,.55);
    backdrop-filter: blur(6px);
  }
  nav.bc a { color: var(--muted); }

  /* layout */
  .wrap {
    max-width: 900px;
    margin: 0 auto;
    padding: 48px 24px 80px;
  }

  /* hero */
  .concept-badge {
    display: inline-block;
    background: var(--mint);
    color: #073044;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
    padding: 3px 12px;
    border-radius: var(--pill);
    margin-bottom: 14px;
  }
  h1 {
    font-size: clamp(1.8rem, 5vw, 2.8rem);
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 16px;
    color: var(--ink);
  }
  .lede {
    font-size: 1.1rem;
    color: var(--muted);
    margin-bottom: 36px;
    max-width: 680px;
    line-height: 1.65;
  }

  /* table of contents */
  .toc {
    background: rgba(255,255,255,.7);
    border: 1px solid rgba(0,0,0,.08);
    border-radius: var(--r);
    padding: 20px 28px;
    margin-bottom: 44px;
    max-width: 480px;
  }
  .toc h3 {
    font-size: .8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: var(--muted);
    margin-bottom: 10px;
  }
  .toc ol { padding-left: 18px; }
  .toc li { margin-bottom: 6px; font-size: .95rem; }

  /* sections */
  .concept-section { margin-bottom: 52px; }
  .concept-section h2 {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--bg1);
    color: var(--ink);
  }
  .concept-section p {
    font-size: 1rem;
    line-height: 1.7;
    color: #2a4555;
    margin-bottom: 14px;
  }
  .concept-section ul {
    padding-left: 22px;
    margin-bottom: 14px;
  }
  .concept-section li {
    margin-bottom: 6px;
    font-size: .97rem;
    line-height: 1.6;
    color: #2a4555;
  }

  /* definition box */
  .def-box {
    background: rgba(33,211,161,.12);
    border-left: 4px solid var(--mint);
    border-radius: 0 var(--r) var(--r) 0;
    padding: 18px 22px;
    margin: 20px 0 28px;
    font-size: 1.05rem;
    line-height: 1.65;
    color: var(--ink);
  }

  /* key facts grid */
  .facts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin: 20px 0;
  }
  .fact {
    background: rgba(255,255,255,.75);
    border: 1px solid rgba(0,0,0,.07);
    border-radius: 16px;
    padding: 16px 18px;
    text-align: center;
  }
  .fact-num {
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--blue2);
    margin-bottom: 4px;
  }
  .fact-label {
    font-size: .8rem;
    color: var(--muted);
    font-weight: 500;
  }

  /* CTA */
  .cta-box {
    background: linear-gradient(135deg, #073044 0%, #0e3d58 100%);
    border-radius: var(--r);
    padding: 32px 36px;
    color: #fff;
    margin: 52px 0 40px;
    display: flex;
    align-items: center;
    gap: 28px;
    flex-wrap: wrap;
  }
  .cta-box h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 6px; }
  .cta-box p  { font-size: .95rem; opacity: .8; margin: 0; }
  .cta-btn {
    flex-shrink: 0;
    background: var(--mint);
    color: #073044;
    font-weight: 700;
    padding: 12px 24px;
    border-radius: var(--pill);
    white-space: nowrap;
    text-decoration: none;
  }
  .cta-btn:hover { opacity: .9; text-decoration: none; }

  /* related pills */
  .related-wrap { margin: 0 0 52px; }
  .related-wrap h3 {
    font-size: .8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: var(--muted);
    margin-bottom: 12px;
  }
  .pills { display: flex; flex-wrap: wrap; gap: 8px; }
  .pill {
    background: rgba(255,255,255,.8);
    border: 1px solid rgba(0,0,0,.1);
    border-radius: var(--pill);
    padding: 6px 16px;
    font-size: .85rem;
    font-weight: 500;
    color: var(--ink);
    text-decoration: none;
  }
  .pill:hover { background: var(--mint); color: #073044; text-decoration: none; }

  /* FAQ */
  .faq { margin-bottom: 52px; }
  .faq h2 {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 20px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--bg1);
  }
  .faq-q {
    background: rgba(255,255,255,.7);
    border: 1px solid rgba(0,0,0,.07);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
  }
  .faq-q strong { display: block; margin-bottom: 6px; font-size: .97rem; }
  .faq-q p { font-size: .93rem; color: var(--muted); line-height: 1.6; margin:0; }

  /* floating */
  .floating {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 999;
  }
  .floatBtn {
    display: flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #0e3d58, #073044);
    color: #fff;
    padding: 12px 20px;
    border-radius: var(--pill);
    font-size: .9rem;
    font-weight: 600;
    text-decoration: none;
    box-shadow: 0 4px 20px rgba(0,0,0,.2);
  }
  .floatBtn:hover { opacity: .92; text-decoration: none; }

  footer {
    text-align: center;
    padding: 24px;
    font-size: .8rem;
    color: var(--muted);
    border-top: 1px solid rgba(0,0,0,.06);
  }

  @media(max-width:600px) {
    .cta-box { flex-direction: column; gap: 18px; }
    .floating { bottom: 16px; right: 16px; }
  }
"""


# ──────────────────────────────────────────────
# CONCEPT DATA
# ──────────────────────────────────────────────

CONCEPTS = [

    # ── AI Automation ──────────────────────────────────────────────────────
    {
        "slug": "ai-automation",
        "title": "AI Automation",
        "meta_title": "AI Automation Explained — What It Is, How It Works | SideGuy",
        "meta_desc": "What AI automation is, how businesses use it, and where real-world automation actually works vs. where human judgment still wins.",
        "canonical": f"{DOMAIN}/concepts/ai-automation.html",
        "badge": "Concept Guide",
        "lede": "AI automation uses artificial intelligence to perform tasks traditionally done by humans — from scheduling reminders to analyzing documents. Understanding where it works well (and where it fails) is the difference between saving hours and making expensive mistakes.",
        "definition": "AI automation is the use of machine learning, natural language processing, or rule-based AI systems to execute repeatable tasks without continuous human input. It's distinct from traditional automation in that it can handle variability — unstructured data, natural language, and context-dependent decisions.",
        "facts": [
            ("~40%", "of small business tasks are automatable with current AI"),
            ("$0", "in software cost for basic starter workflows (Zapier free tier, Make, n8n)"),
            ("3–8 hrs/week", "typical time saved by contractors using AI scheduling + follow-up"),
            ("2026", "year most SMBs will have at least one AI-assisted workflow"),
        ],
        "toc": [
            ("What AI Automation Is", "what"),
            ("Common Types", "types"),
            ("Where It Works (and Where It Doesn't)", "where"),
            ("How Operators Use It", "operators"),
            ("The Human Layer", "human"),
            ("Frequently Asked Questions", "faq"),
        ],
        "sections": [
            {
                "id": "what",
                "heading": "What AI Automation Is",
                "content": [
                    "AI automation refers to the use of AI systems — machine learning models, large language models, or structured logic engines — to perform tasks that previously required human time and judgment.",
                    "It is not the same as traditional automation (like a scheduled email blast). AI automation can handle variability: interpreting a customer message, deciding which category it belongs to, generating a draft reply, and routing it to the right team member.",
                    "The key distinction: traditional automation follows fixed rules. AI automation can handle exceptions.",
                ],
            },
            {
                "id": "types",
                "heading": "Common Types of AI Automation",
                "content": [
                    "The following categories cover the majority of real-world operator use cases:",
                ],
                "bullets": [
                    "**Customer intake automation** — AI reads incoming messages, categorizes the request, and routes or replies",
                    "**Scheduling and reminders** — AI holds calendar logic, sends reminders, reschedules based on replies",
                    "**Document summarization** — AI reads long documents (contracts, intakes, call transcripts) and outputs key points",
                    "**Email and SMS follow-up** — Automated sequences that feel personal because they're context-aware",
                    "**Workflow orchestration** — Multi-step automations: trigger → enrich → route → notify → log",
                    "**Marketing content generation** — Drafting posts, emails, and product descriptions at scale",
                    "**Review response systems** — Monitoring and drafting replies to Google/Yelp reviews",
                ],
            },
            {
                "id": "where",
                "heading": "Where It Works — and Where It Doesn't",
                "content": [
                    "AI automation works best on tasks that are: high-volume, repetitive, text-based, and tolerant of occasional errors.",
                    "It struggles with: tasks requiring empathy, complex legal or ethical judgment, anything with high stakes and low error tolerance, and situations where context changes radically per case.",
                ],
                "bullets": [
                    "✅ Works well: intake triage, appointment reminders, FAQ responses, invoice generation",
                    "✅ Works well: review monitoring, lead follow-up sequences, content first drafts",
                    "⚠️ Use with caution: customer complaint resolution, pricing decisions, hiring",
                    "❌ Not ready: medical diagnosis, legal advice, situations requiring deep empathy",
                ],
            },
            {
                "id": "operators",
                "heading": "How Operators Are Using It",
                "content": [
                    "Real-world adoption patterns from San Diego and similar markets:",
                    "Contractors are using AI to auto-respond to missed calls with a text, book a callback time, and log the lead in their CRM — without touching their phone until the appointment is confirmed.",
                    "Restaurants are using AI to respond to Google reviews within 4 hours, maintain consistent tone, and flag anything requiring a manager's attention.",
                    "Medical offices are using AI intake forms that summarize the patient's stated issue before the front desk ever reads it, cutting intake time significantly.",
                ],
            },
            {
                "id": "human",
                "heading": "The Human Layer",
                "content": [
                    "The most common mistake operators make with AI automation is removing the human review step too early.",
                    "Effective automation includes a human checkpoint for anything that affects money, trust, or a relationship. The AI handles volume; the human handles exceptions and edge cases.",
                    "SideGuy's philosophy: automate the boring, protect the important. AI should reduce the number of decisions a human has to make — not eliminate the human from decisions that matter.",
                ],
            },
        ],
        "faqs": [
            ("Do I need technical skills to use AI automation?",
             "No. Tools like Zapier, Make (Integromat), and n8n offer no-code/low-code interfaces. Most operators start with a template and customize from there. SideGuy can help you figure out which setup makes sense for your situation."),
            ("How much does AI automation cost?",
             "Basic workflows are often free or under $50/month. Costs scale with volume and complexity. Most small operators spend $0–$200/month and save significantly more than that in labor hours."),
            ("Is AI automation secure?",
             "It depends entirely on which tools you use and what data flows through them. Avoid sending sensitive customer data (SSNs, payment details) through automation platforms not specifically certified for it. For HIPAA or PCI contexts, use compliant tools only."),
            ("How do I start?",
             "Pick one high-volume, low-stakes process — missed call follow-up, appointment reminders, or review responses. Automate just that. Measure before expanding. Text PJ if you want a second opinion before spending money on tools."),
        ],
        "related": [
            ("/pillars/ai-automation.html", "AI Automation Pillar"),
            ("/clusters/ai-workflow-automation.html", "Workflow Automation"),
            ("/clusters/ai-customer-service.html", "AI Customer Service"),
            ("/clusters/ai-scheduling.html", "Scheduling Automation"),
            ("/generated/ai-automation-for-contractors.html", "AI for Contractors"),
            ("/generated/ai-automation-for-plumbers.html", "AI for Plumbers"),
            ("/concepts/prediction-markets.html", "Prediction Markets"),
            ("/concepts/crypto-payments.html", "Crypto Payments"),
        ],
    },

    # ── Prediction Markets ────────────────────────────────────────────────
    {
        "slug": "prediction-markets",
        "title": "Prediction Markets",
        "meta_title": "Prediction Markets Explained — Kalshi, Polymarket, How They Work | SideGuy",
        "meta_desc": "Prediction markets explained. How platforms like Kalshi and Polymarket allow users to trade on real-world outcomes, and what operators need to know.",
        "canonical": f"{DOMAIN}/concepts/prediction-markets.html",
        "badge": "Concept Guide",
        "lede": "Prediction markets are exchanges where participants trade contracts based on the probability of future events — elections, economic data, weather, sports performance. They produce some of the most accurate probability forecasts available, often outperforming expert panels.",
        "definition": "A prediction market is a speculative market where the price of a contract reflects the market's collective probability estimate for an event. Contracts typically pay $1 if the event occurs and $0 if it doesn't. A contract trading at $0.63 implies a 63% market-implied probability.",
        "facts": [
            ("$1B+", "traded on Kalshi and Polymarket combined in recent cycles"),
            ("~5–8%", "typical overround (house edge) on prediction market contracts"),
            ("2023", "year Kalshi received CFTC approval for US event contracts"),
            ("63%", "accuracy rate of prediction markets vs 49% for expert panels (common finding)"),
        ],
        "toc": [
            ("What Prediction Markets Are", "what"),
            ("How They Work", "how"),
            ("Major Platforms", "platforms"),
            ("Use Cases", "uses"),
            ("Risks and Limits", "risks"),
            ("Frequently Asked Questions", "faq"),
        ],
        "sections": [
            {
                "id": "what",
                "heading": "What Prediction Markets Are",
                "content": [
                    "Prediction markets are financial exchanges where the traded asset is a binary outcome contract. You buy a position on whether something will happen — and your return depends entirely on whether it does.",
                    "Unlike opinion polls, prediction markets require participants to put real money behind their beliefs. This creates a strong incentive for accurate forecasting, which is why market prices often converge on accurate probabilities faster than other methods.",
                    "The concept has existed in various forms since the 1990s (Iowa Electronic Markets) but has exploded in mainstream use with crypto-native platforms and CFTC-regulated US exchanges.",
                ],
            },
            {
                "id": "how",
                "heading": "How They Work",
                "content": [
                    "Each contract represents a yes/no question about a future event. If the event resolves 'Yes,' the contract pays $1 per share. If 'No,' it pays $0.",
                    "You can buy contracts (betting on Yes) or sell them short (betting on No). Market prices fluctuate based on supply and demand — which is a proxy for collective probability estimates.",
                    "Settlement happens automatically when the event resolves, based on an authoritative source (official election results, government data releases, sports box scores, etc.).",
                ],
                "bullets": [
                    "Contract price $0.60 → market implies 60% probability",
                    "Buy at $0.60, event happens → profit $0.40 per share",
                    "Buy at $0.60, event doesn't happen → lose $0.60 per share",
                    "Liquidity varies widely: major political markets are deep; niche markets can be thin",
                ],
            },
            {
                "id": "platforms",
                "heading": "Major Platforms",
                "content": [
                    "The landscape has consolidated around a few major platforms, each with different regulatory status and audience:",
                ],
                "bullets": [
                    "**Kalshi** — CFTC-regulated, US-based, focus on economic and political events",
                    "**Polymarket** — Crypto-native (Polygon), global, very high liquidity on major events",
                    "**Metaculus** — Forecasting platform (play money + reputation, no real-money trading)",
                    "**PredictIt** — Legacy political markets platform, regulatory uncertainty",
                    "**Manifold Markets** — Play-money platform popular in tech/forecasting communities",
                ],
            },
            {
                "id": "uses",
                "heading": "Use Cases",
                "content": [
                    "Beyond speculation, prediction markets are increasingly used as information tools:",
                ],
                "bullets": [
                    "**Business planning** — reading market-implied probability of regulatory changes, rate decisions, or economic events",
                    "**Sports and DFS** — comparing prediction market implied probabilities against sportsbook lines to find pricing discrepancies",
                    "**Election analysis** — real-time aggregation of information faster than polling",
                    "**Risk management** — hedging business exposure to specific external outcomes",
                    "**Research** — academic study of collective intelligence and information aggregation",
                ],
            },
            {
                "id": "risks",
                "heading": "Risks and Limitations",
                "content": [
                    "Prediction markets are not perfect. Key limitations include:",
                ],
                "bullets": [
                    "**Thin markets** — Low liquidity in niche markets means prices are easily manipulated or simply wrong",
                    "**Regulatory risk** — US regulatory status for many platforms remains uncertain; rules can change",
                    "**Resolution disputes** — How a contract resolves can be ambiguous; platform decisions can be surprising",
                    "**Overconfidence** — Markets can be confidently wrong, especially on novel or unprecedented events",
                    "**Tax complexity** — Trading gains are taxable; record-keeping required",
                ],
            },
        ],
        "faqs": [
            ("Are prediction markets legal in the United States?",
             "Kalshi is CFTC-regulated and legal for US residents. Polymarket is a crypto-native platform that has faced US regulatory scrutiny — US residents faced access restrictions after a 2022 CFTC settlement. Status continues to evolve. Consult a financial advisor for your specific situation."),
            ("Can prediction markets be used to make investment decisions?",
             "They can be a useful signal in a broader research process. They aggregate information quickly. But they're not a substitute for fundamental analysis, especially for long-horizon decisions where market liquidity is low."),
            ("How do prediction markets relate to betting?",
             "Structurally similar — both involve staking money on outcome probabilities. Key differences: prediction markets often cover a much wider range of events (economic data, science milestones, regulatory decisions), and regulated platforms like Kalshi operate under CFTC oversight, not gambling regulators."),
            ("Where can I learn more about prediction market accuracy?",
             "Philip Tetlock's Superforecasting research is the foundational work. More recent studies comparing Kalshi/Metaculus forecasts against expert panels are published regularly. The core finding: markets outperform most other methods on well-defined, short-horizon questions."),
        ],
        "related": [
            ("/concepts/ai-automation.html", "AI Automation"),
            ("/concepts/crypto-payments.html", "Crypto Payments"),
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-security.html", "Payment Security"),
        ],
    },

    # ── Crypto Payments ────────────────────────────────────────────────────
    {
        "slug": "crypto-payments",
        "title": "Crypto Payments",
        "meta_title": "Crypto Payments Explained — Blockchain Settlement for Business | SideGuy",
        "meta_desc": "Crypto payments explained. How blockchain settlement works, why businesses are exploring it, and what operators actually need to know before accepting crypto.",
        "canonical": f"{DOMAIN}/concepts/crypto-payments.html",
        "badge": "Concept Guide",
        "lede": "Crypto payments use blockchain networks to transfer value directly between parties — without a bank, processor, or clearinghouse in between. For operators, the real question isn't whether crypto is interesting — it's whether the tradeoffs make sense for your business today.",
        "definition": "A crypto payment is a transfer of value recorded on a distributed blockchain ledger. No central intermediary holds or clears the funds. Settlement is final once confirmed on-chain — typically in seconds to minutes depending on the network. This differs fundamentally from card payments, which involve 3–7 parties and settle over 1–3 business days.",
        "facts": [
            ("<1 sec", "Solana transaction finality time"),
            ("~$0.001", "typical Solana transaction fee"),
            ("$0–2.5%", "typical operator fee range for crypto vs 2–3.5% for cards"),
            ("2026", "year stablecoin B2B payment volume is expected to surpass $1T globally"),
        ],
        "toc": [
            ("What Crypto Payments Are", "what"),
            ("How Blockchain Settlement Works", "how"),
            ("Networks That Matter for Operators", "networks"),
            ("Stablecoins vs Volatile Crypto", "stablecoins"),
            ("Real Operator Considerations", "operators"),
            ("Frequently Asked Questions", "faq"),
        ],
        "sections": [
            {
                "id": "what",
                "heading": "What Crypto Payments Are",
                "content": [
                    "A crypto payment moves value from one digital wallet to another using a blockchain network as the settlement layer. No bank approves the transaction. No processor takes a cut. No chargeback is possible after confirmation.",
                    "The absence of a chargeback mechanism is both an advantage (for operators) and a limitation (for customers who need recourse). It's a fundamental property of on-chain settlement, not a bug.",
                    "For most operators in 2026, crypto payments are most relevant for: B2B payments, international transfers, high-ticket transactions where card fees are painful, and situations where chargebacks are a serious business risk.",
                ],
            },
            {
                "id": "how",
                "heading": "How Blockchain Settlement Works",
                "content": [
                    "When a crypto payment is initiated, a signed transaction is broadcast to the network. Validators (miners or stakers) include it in a block. Once included and confirmed, the transfer is irreversible.",
                    "The settlement process has two stages: inclusion (the transaction is in a block) and finality (enough subsequent blocks make reversal economically infeasible). Speed varies by network.",
                ],
                "bullets": [
                    "**Bitcoin** — ~10 min per block, typically 3–6 confirmations for high-value transactions (~30–60 min)",
                    "**Ethereum** — ~12 sec blocks, ~15 min to practical finality",
                    "**Solana** — ~0.4 sec block time, near-instant finality for most transactions",
                    "**USDC/USDT on Solana** — Stablecoin + fast network: the practical combo for operator payments",
                ],
            },
            {
                "id": "networks",
                "heading": "Networks That Matter for Operators",
                "content": [
                    "Not all blockchains are equally useful for business payments. For operator use in 2026, the relevant networks are:",
                ],
                "bullets": [
                    "**Solana** — Fast, cheap, high throughput. The primary network for USDC payments in the SMB space.",
                    "**Ethereum + L2s** — Base, Arbitrum, Optimism offer low fees with Ethereum security. Growing B2B use.",
                    "**Bitcoin** — Primarily a store of value, not practical for small daily payments due to speed and fees.",
                    "**Stablecoin rails** — USDC, PYUSD (PayPal), and USDT provide crypto settlement with fiat-pegged value.",
                ],
            },
            {
                "id": "stablecoins",
                "heading": "Stablecoins vs Volatile Crypto",
                "content": [
                    "The biggest friction for operators accepting crypto historically was price volatility — accepting Bitcoin at $60,000 and having it worth $45,000 by the time you can spend it.",
                    "Stablecoins solve this. USDC, for example, is pegged 1:1 to the US dollar, redeemable at any Coinbase or Circle account, and settles on-chain in under a second on Solana.",
                    "For most operator use cases, the practical choice in 2026 is: accept USDC on Solana. You get crypto settlement speed and zero fees with no volatility risk.",
                ],
                "bullets": [
                    "✅ USDC — audited, 1:1 USD-backed, widely redeemable, Solana support",
                    "✅ PYUSD (PayPal) — fiat-backed, easy redemption for PayPal users",
                    "⚠️ USDT — widely used globally but less transparent reserves than USDC",
                    "❌ Bitcoin / ETH for operating accounts — volatility risk for most operators",
                ],
            },
            {
                "id": "operators",
                "heading": "Real Operator Considerations",
                "content": [
                    "Before accepting crypto payments, operators should think through four things:",
                    "**Taxes.** Crypto received as payment is taxable income at fair market value at time of receipt. Track every transaction. Use accounting software that handles crypto (Koinly, Cryptio, or a CPA who knows crypto).",
                    "**Redemption path.** How does the crypto become spendable dollars? Coinbase, Kraken, or a business bank that accepts crypto (Silvergate, Mercury, etc.) are the typical paths. Know this before you accept your first payment.",
                    "**Customer experience.** Most customers don't have crypto wallets. Crypto payments in 2026 are still a niche option — useful for specific customers and B2B situations, not a replacement for card acceptance.",
                    "**Chargebacks vs disputes.** You lose chargeback protection when accepting crypto. This is good for fraud-prone merchants; it's a risk if you ever need to issue refunds and the customer disputes your process.",
                ],
            },
        ],
        "faqs": [
            ("Should my small business accept crypto payments?",
             "Probably not as your only payment method. As an option for specific customers (B2B, high-ticket, international, crypto-native clients) — potentially yes. The fee savings are real, but the operational setup cost matters. Text PJ if you want a realistic assessment for your situation."),
            ("What's the simplest way to start accepting USDC?",
             "Create a Coinbase Commerce or Solana Pay account, generate a payment address, and share it with clients. For invoicing, tools like Request Finance or Utila handle the workflow. Off-ramp through Coinbase or your bank."),
            ("How do crypto payments affect accounting?",
             "Every crypto receipt is a taxable event (income at fair market value). Every crypto payment you make may also be a taxable event (capital gains/loss). Use Koinly or a CPA who handles crypto from day one — don't try to reconstruct this later."),
            ("Is there chargeback protection with crypto?",
             "No. On-chain transactions are irreversible once confirmed. This eliminates chargeback fraud (benefit for operators) but also means you must have a clear refund policy that doesn't depend on a network reversal — because one isn't possible."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/instant-settlement.html", "Instant Settlement"),
            ("/clusters/payment-security.html", "Payment Security"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/generated/what-is-instant-settlement-for-business.html", "Instant Settlement Guide"),
            ("/concepts/prediction-markets.html", "Prediction Markets"),
            ("/concepts/ai-automation.html", "AI Automation"),
        ],
    },

    # ── Payment Processing ────────────────────────────────────────────────
    {
        "slug": "payment-processing",
        "title": "Payment Processing",
        "meta_title": "Payment Processing Explained — Fees, Flow, and What You Actually Control | SideGuy",
        "meta_desc": "How payment processing really works — the fee buckets, money flow, chargeback mechanics, and what small business operators can actually control.",
        "canonical": f"{DOMAIN}/concepts/payment-processing.html",
        "badge": "Concept Guide",
        "lede": "Every card swipe triggers a cascade of fees, approvals, and settlement steps involving up to seven different entities. Most operators only see the final rate on their statement — and don't know which parts are negotiable. This page explains the mechanics clearly.",
        "definition": "Payment processing is the set of systems and intermediaries that authorize, clear, and settle a payment made with a credit or debit card. The process involves the cardholder, merchant, acquiring bank, card network (Visa/Mastercard), and issuing bank — each taking a cut through a layered fee structure.",
        "facts": [
            ("2–3.5%", "typical all-in rate for card payments in the US"),
            ("~1.8%", "average interchange fee on a consumer Visa credit card"),
            ("1–3 days", "time to settlement for most card transactions"),
            ("0.6%", "typical processor markup range (the negotiable part)"),
        ],
        "toc": [
            ("How a Card Payment Works", "flow"),
            ("The Fee Layers", "fees"),
            ("What Is Interchange", "interchange"),
            ("Processor Markup — the Negotiable Part", "markup"),
            ("Chargebacks Explained", "chargebacks"),
            ("Frequently Asked Questions", "faq"),
        ],
        "sections": [
            {
                "id": "flow",
                "heading": "How a Card Payment Works",
                "content": [
                    "When a customer taps their card at your terminal, a transaction flows through multiple systems in under two seconds:",
                ],
                "bullets": [
                    "1. **Authorization** — Your terminal sends the transaction to your acquirer/processor",
                    "2. **Network routing** — The processor routes it through Visa or Mastercard to the issuing bank",
                    "3. **Approval/Decline** — The issuer checks the cardholder's account and returns a response",
                    "4. **Capture** — At end of day (or batch close), authorized transactions are submitted for settlement",
                    "5. **Clearing** — The card network exchanges transaction data between acquirer and issuer",
                    "6. **Settlement** — Funds move from the issuing bank, through the network, to your acquiring bank",
                    "7. **Deposit** — Your processor deposits net funds (minus fees) to your bank account",
                ],
            },
            {
                "id": "fees",
                "heading": "The Fee Layers",
                "content": [
                    "Your processing statement shows one blended rate, but it's actually three stacked fees:",
                ],
                "bullets": [
                    "**Interchange** (~1.5–2.5%) — Paid to the cardholder's issuing bank. Set by Visa/Mastercard. Not negotiable.",
                    "**Assessment fees** (~0.13–0.15%) — Paid to the card network (Visa/Mastercard themselves). Not negotiable.",
                    "**Processor markup** (0.1–1%+) — Paid to your payment processor. This is the only negotiable part.",
                ],
            },
            {
                "id": "interchange",
                "heading": "What Is Interchange",
                "content": [
                    "Interchange is the largest component of card processing fees — typically 60–70% of your total rate. It's paid to the bank that issued the customer's card.",
                    "Interchange rates vary by: card type (credit vs debit), rewards level (basic vs premium rewards cards), business category (MCC code), and transaction type (card-present vs card-not-present).",
                    "A basic debit card might have an interchange rate of 0.8%. A premium travel rewards credit card might be 2.4%. You have no control over which card customers present — but you can optimize which transaction types you accept and how.",
                ],
            },
            {
                "id": "markup",
                "heading": "Processor Markup — the Negotiable Part",
                "content": [
                    "The processor markup is what your payment processor (Square, Stripe, Clover, Heartland, First Data, etc.) charges on top of interchange and assessments.",
                    "On a flat-rate model (Stripe at 2.9% + $0.30), the markup is baked into a single rate. On an interchange-plus model, the markup is listed separately (e.g., 'interchange + 0.25% + $0.10').",
                    "Interchange-plus pricing is almost always better for established businesses processing over $10,000/month. If you're on a flat rate and processing over $15k/month, you're likely overpaying.",
                    "Processor markups are negotiable at volume. Over $50k/month, most processors will negotiate. Before negotiating, you need to know your current effective rate — divide total processing fees by total volume processed.",
                ],
            },
            {
                "id": "chargebacks",
                "heading": "Chargebacks Explained",
                "content": [
                    "A chargeback occurs when a cardholder disputes a charge with their bank instead of requesting a refund from the merchant directly. The issuing bank can forcibly reverse the transaction.",
                    "From the merchant's perspective: funds are debited immediately upon dispute, a chargeback fee is assessed ($15–$100), and you have a limited window to respond with evidence.",
                    "Chargeback prevention is about documentation and process: signed authorizations, clear refund policies, delivery confirmation, and prompt customer service responses reduce dispute rates significantly.",
                ],
                "bullets": [
                    "Dispute reason codes tell you why — friendly fraud, item not received, unauthorized, etc.",
                    "Win rates on disputes with good documentation: 30–60% depending on category",
                    "High chargeback rates (over 1%) trigger processor warnings and potential account termination",
                    "Chargeback monitoring programs exist at 0.65% (Visa) and 1% (Mastercard) thresholds",
                ],
            },
        ],
        "faqs": [
            ("What's the difference between a payment processor and a payment gateway?",
             "A gateway is the software that securely captures and transmits card data. A processor is the entity that routes and settles transactions. Many companies (Stripe, Square) combine both functions. Some setups use a separate gateway (Authorize.net) with a backend processor (TSYS, First Data)."),
            ("How do I find my actual effective rate?",
             "Divide your total processing fees (from your statement) by your total dollar volume processed. That's your effective rate. Compare it to interchange-plus benchmarks for your business type. If you're over 2.5% on mostly card-present transactions, you're likely overpaying."),
            ("Can I pass card fees to customers?",
             "In most US states, yes — surcharging is legal but regulated. You must disclose the surcharge clearly at point of sale. Rules vary by state and card network. Debit cards cannot be surcharged under Visa/Mastercard rules. Cash discount programs are a common alternative."),
            ("What's the safest way to handle payment disputes?",
             "Document everything. For card-not-present: get signed authorization, save IP + device data, confirm delivery. Respond to every dispute within the window with organized evidence. Use a processor that provides chargeback alerts (Ethoca, Verifi) so you can resolve disputes before they escalate."),
        ],
        "related": [
            ("/pillars/payments.html", "Payments Pillar"),
            ("/clusters/payment-fees.html", "Payment Fees"),
            ("/clusters/chargebacks.html", "Chargebacks"),
            ("/clusters/instant-settlement.html", "Instant Settlement"),
            ("/clusters/payment-security.html", "Payment Security"),
            ("/concepts/crypto-payments.html", "Crypto Payments"),
            ("/decisions/switch-payment-processor.html", "Should I Switch Processors?"),
        ],
    },
]


# ──────────────────────────────────────────────
# PAGE BUILDER
# ──────────────────────────────────────────────

def build_concept_page(c: dict) -> str:
    # Table of contents
    toc_items = "\n".join(
        f'      <li><a href="#{anchor}">{label}</a></li>'
        for label, anchor in c["toc"]
    )

    # Key facts
    facts_html = "\n".join(
        f'''      <div class="fact">
        <div class="fact-num">{num}</div>
        <div class="fact-label">{label}</div>
      </div>'''
        for num, label in c["facts"]
    )

    # Sections
    sections_html = ""
    for s in c["sections"]:
        paras = ""
        for p in s.get("content", []):
            paras += f"    <p>{p}</p>\n"
        bullets = ""
        if "bullets" in s:
            items = "\n".join(
                f"      <li>{b.replace('**', '<strong>', 1).replace('**', '</strong>', 1) if '**' in b else b}</li>"
                for b in s["bullets"]
            )
            bullets = f"    <ul>\n{items}\n    </ul>\n"
        sections_html += f"""
  <div class="concept-section" id="{s['id']}">
    <h2>{s['heading']}</h2>
{paras}{bullets}  </div>
"""

    # FAQ items + JSON-LD
    faq_html = ""
    faq_schema_items = []
    for q, a in c["faqs"]:
        faq_html += f"""    <div class="faq-q">
      <strong>{q}</strong>
      <p>{a}</p>
    </div>
"""
        faq_schema_items.append(f"""    {{
      "@type": "Question",
      "name": "{q.replace('"', '&quot;')}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a.replace('"', '&quot;')}"
      }}
    }}""")

    faq_schema = ",\n".join(faq_schema_items)

    # Related pills
    pills_html = "\n".join(
        f'      <a class="pill" href="{href}">{label}</a>'
        for href, label in c["related"]
    )

    title_clean = c["title"].replace(" ", "%20")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{c['meta_title']}</title>
  <meta name="description" content="{c['meta_desc']}"/>
  <link rel="canonical" href="{c['canonical']}"/>
  <meta property="og:title" content="{c['meta_title']}"/>
  <meta property="og:description" content="{c['meta_desc']}"/>
  <meta property="og:url" content="{c['canonical']}"/>
  <meta property="og:type" content="article"/>
  <meta name="robots" content="index,follow"/>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"Concepts","item":"{DOMAIN}/concepts/index.html"}},
          {{"@type":"ListItem","position":3,"name":"{c['title']}","item":"{c['canonical']}"}}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
{faq_schema}
        ]
      }}
    ]
  }}
  </script>
  <style>
{CSS}
  </style>
</head>
<body>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> › <a href="/concepts/index.html">Concepts</a> › {c['title']}
</nav>

<main class="wrap">

  <div class="concept-badge">{c['badge']}</div>
  <h1>{c['title']}</h1>
  <p class="lede">{c['lede']}</p>

  <div class="def-box">
    <strong>Definition:</strong> {c['definition']}
  </div>

  <div class="facts-grid">
{facts_html}
  </div>

  <div class="toc">
    <h3>On This Page</h3>
    <ol>
{toc_items}
    </ol>
  </div>

{sections_html}

  <div class="faq" id="faq">
    <h2>Frequently Asked Questions</h2>
{faq_html}  </div>

  <div class="cta-box">
    <div>
      <h3>Still have questions? Text PJ.</h3>
      <p>Real human, San Diego. No pitch — just a straight answer on what makes sense for your situation.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_SMS}">💬 Text {PHONE_DISPLAY}</a>
  </div>

  <div class="related-wrap">
    <h3>Related Knowledge</h3>
    <div class="pills">
{pills_html}
    </div>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> · San Diego ·
    <a href="/concepts/index.html">All Concepts</a> ·
    <a href="tel:{PHONE_SMS}">{PHONE_DISPLAY}</a>
    <br><small>Page updated {TODAY}</small>
  </footer>

</main>

<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_SMS}" aria-label="Text PJ">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ · {PHONE_DISPLAY}
  </a>
</div>

</body>
</html>
"""


# ──────────────────────────────────────────────
# CONCEPTS INDEX PAGE
# ──────────────────────────────────────────────

def build_index_page(concepts: list) -> str:
    cards_html = ""
    for c in concepts:
        href = f"/concepts/{c['slug']}.html"
        cards_html += f"""      <a class="node" href="{href}">
        <div class="node-title">{c['title']}</div>
        <div class="node-desc">{c['lede'][:120].rstrip()}…</div>
        <span class="pill" style="margin-top:10px;display:inline-block;">Read →</span>
      </a>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Concept Guides — SideGuy Solutions | Business, Payments, AI</title>
  <meta name="description" content="Wikipedia-style concept guides from SideGuy. Clear explanations of AI automation, payment processing, crypto payments, prediction markets, and more."/>
  <link rel="canonical" href="{DOMAIN}/concepts/index.html"/>
  <meta property="og:title" content="Concept Guides — SideGuy Solutions"/>
  <meta property="og:description" content="Clear, operator-first explanations of AI, payments, crypto, and business technology."/>
  <meta name="robots" content="index,follow"/>
  <style>
{CSS}
    .node-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 18px;
      margin: 30px 0;
    }}
    .node {{
      background: rgba(255,255,255,.75);
      border: 1px solid rgba(0,0,0,.08);
      border-radius: var(--r);
      padding: 22px 24px;
      text-decoration: none;
      color: var(--ink);
      transition: box-shadow .15s;
    }}
    .node:hover {{
      box-shadow: 0 4px 20px rgba(0,0,0,.1);
      text-decoration: none;
    }}
    .node-title {{
      font-size: 1.05rem;
      font-weight: 700;
      margin-bottom: 7px;
    }}
    .node-desc {{
      font-size: .87rem;
      color: var(--muted);
      line-height: 1.55;
    }}
  </style>
</head>
<body>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> › Concepts
</nav>

<main class="wrap">

  <div class="concept-badge">Reference Library</div>
  <h1>Concept Guides</h1>
  <p class="lede">
    Wikipedia-style deep-reference pages on the topics that matter most
    to operators — payments, AI automation, crypto infrastructure, and
    business technology. Clear definitions, real-world mechanics, no hype.
  </p>

  <div class="node-grid">
{cards_html}  </div>

  <div class="cta-box">
    <div>
      <h3>Need clarity on something specific?</h3>
      <p>Text PJ. Real human, San Diego. Straight answer, no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_SMS}">💬 Text {PHONE_DISPLAY}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> · San Diego ·
    <a href="tel:{PHONE_SMS}">{PHONE_DISPLAY}</a>
  </footer>

</main>

<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_SMS}" aria-label="Text PJ">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ · {PHONE_DISPLAY}
  </a>
</div>

</body>
</html>
"""


# ──────────────────────────────────────────────
# SITEMAP UPDATE
# ──────────────────────────────────────────────

def update_sitemap(slugs: list):
    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.exists():
        print("  sitemap.xml not found — skipping")
        return
    content = sitemap_path.read_text()
    added = 0
    insert_before = "</urlset>"
    new_urls = ""
    for slug in slugs:
        url = f"{DOMAIN}/concepts/{slug}.html"
        if url not in content:
            new_urls += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
            added += 1
    if new_urls:
        content = content.replace(insert_before, new_urls + insert_before)
        sitemap_path.write_text(content)
    print(f"  Sitemap: {added} URLs added")


# ──────────────────────────────────────────────
# KNOWLEDGE MAP UPDATE
# ──────────────────────────────────────────────

def update_knowledge_map(concepts: list):
    km_path = ROOT / "knowledge" / "sideguy-knowledge-map.html"
    if not km_path.exists():
        print("  Knowledge map not found — skipping")
        return
    content = km_path.read_text()
    if "SIDEGUY_CONCEPTS_SECTION" in content:
        print("  Knowledge map already has Concept Authority section — skipping")
        return

    node_cards = ""
    for c in concepts:
        node_cards += f"""      <a class="node" href="/concepts/{c['slug']}.html">
        <span class="node-type type-guide">Concept</span>
        <div class="node-icon">📖</div>
        <div class="node-title">{c['title']}</div>
        <div class="node-desc">{c['meta_desc'][:90].rstrip()}…</div>
      </a>
"""

    section = f"""
  <!-- SIDEGUY_CONCEPTS_SECTION -->
  <div class="cluster-group">
    <div class="cluster-header">
      <div class="cluster-icon">📖</div>
      <div>
        <div class="cluster-title">Concept Authority Guides</div>
        <div class="cluster-sub">Wikipedia-style deep-reference on payments, AI, crypto, and business tech</div>
      </div>
      <a class="cluster-cta" href="/concepts/index.html">All Concepts →</a>
    </div>
    <div class="node-grid">
{node_cards}    </div>
  </div>
  <!-- END SIDEGUY_CONCEPTS_SECTION -->
"""

    # Insert before the Topic Gap Link section or before microFooter
    if "<!-- SIDEGUY_TOPIC_GAP_LINK -->" in content:
        content = content.replace(
            "<!-- SIDEGUY_TOPIC_GAP_LINK -->",
            section + "<!-- SIDEGUY_TOPIC_GAP_LINK -->",
            1
        )
    elif '<div class="microFooter"' in content:
        content = content.replace(
            '<div class="microFooter"',
            section + '<div class="microFooter"',
            1
        )
    else:
        print("  Could not find insertion point — skipping knowledge map update")
        return

    km_path.write_text(content)
    print("  Knowledge map updated with Concept Authority section")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SideGuy Concept Authority Engine ===\n")

    slugs_built = []

    for concept in CONCEPTS:
        path = CONCEPTS_DIR / f"{concept['slug']}.html"
        if path.exists():
            print(f"  SKIP (exists): concepts/{concept['slug']}.html")
            slugs_built.append(concept["slug"])
            continue
        html = build_concept_page(concept)
        path.write_text(html)
        print(f"  BUILT: concepts/{concept['slug']}.html  ({len(html):,} chars)")
        slugs_built.append(concept["slug"])

    # Concepts index
    index_path = CONCEPTS_DIR / "index.html"
    if not index_path.exists():
        html = build_index_page(CONCEPTS)
        index_path.write_text(html)
        print(f"  BUILT: concepts/index.html  ({len(html):,} chars)")
    else:
        print("  SKIP (exists): concepts/index.html")
    slugs_built.append("index")

    print()
    update_sitemap([c["slug"] for c in CONCEPTS])
    update_knowledge_map(CONCEPTS)

    print(f"\n=== Done — {len(CONCEPTS)} concept pages + index ===")
    print("\nNext: git add concepts/ knowledge/sideguy-knowledge-map.html sitemap.xml")
    print("      git commit -m 'Add: Concept Authority Engine'")
    print("\nGSC URLs to submit:")
    for c in CONCEPTS:
        print(f"  {DOMAIN}/concepts/{c['slug']}.html")
    print(f"  {DOMAIN}/concepts/index.html")
