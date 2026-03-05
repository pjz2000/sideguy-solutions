"""
CTR Title Fixer
Rewrites <title> and meta description for 0-click pages that have real impressions.
Focused on pages position < 25 — showing up in search but not getting clicked.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (filename, new_title, new_description)
# Strategy:
#  - Position 1-5 with 0 clicks = title/desc not matching searcher intent
#  - Include: specific benefit, local signal, action cue, no generic fluff
TARGETS = [
    (
        "mobile-payment-processing.html",
        "Mobile Payment Processing San Diego — Accept Cards Anywhere Today · SideGuy",
        "No card reader? No contracts. San Diego field workers, food trucks, and contractors start accepting cards in under 10 minutes. Free setup help from a local advisor. Text PJ: 773-544-1231.",
    ),
    (
        "contractor-payment-processing.html",
        "Contractor Payment Processing San Diego — Lower Fees, Faster Deposits · SideGuy",
        "San Diego contractors: stop paying 3%+ per swipe. Get lower rates, same-day settlement, and a real human if something breaks. Free comparison from a local advisor. Text PJ: 773-544-1231.",
    ),
    (
        "same-day-payment-processing.html",
        "Same-Day Payment Processing San Diego — Accept Cards Within Hours · SideGuy",
        "Need to take payments today? San Diego businesses get a full payment setup with no contracts, no waiting. A local advisor walks you through it. Text PJ now: 773-544-1231.",
    ),
    (
        "solana-development-san-diego.html",
        "Solana Development San Diego — Build on Solana, Settle to USD · SideGuy",
        "Custom Solana development for San Diego businesses — smart contracts, crypto payments that settle to USD instantly, and Web3 integrations. Free consultation with PJ: 773-544-1231.",
    ),
    (
        "software-development-hub-san-diego.html",
        "Software Development San Diego — What It Costs & Who to Hire · SideGuy",
        "Facing a software problem in San Diego? Plain-English help on web dev, app builds, API fixes, and AI tools — before you pay a developer. Free guidance from PJ: 773-544-1231.",
    ),
    (
        "ai-for-real-estate-teams-san-diego.html",
        "AI for Real Estate Teams San Diego — What It Does & What It Costs · SideGuy",
        "San Diego real estate teams: lead follow-up bots, automated drip, CRM syncing — what AI can actually do and what it costs. No hype. Text PJ: 773-544-1231.",
    ),
    (
        "San-Diego-Field-Service-Payments.html",
        "Field Service Payment Processing San Diego — Accept Cards On-Site · SideGuy",
        "San Diego plumbers, HVAC techs, and landscapers: accept card payments on-site with no monthly fees. Local setup help and honest fee comparison. Text PJ: 773-544-1231.",
    ),
    (
        "San-Diego-SaaS-Development.html",
        "SaaS Development San Diego — Build or Fix Your SaaS Product · SideGuy",
        "San Diego SaaS builders: architecture advice, MVP development, or fixing a broken product. Plain-English guidance on what to build and who to hire. Free consult with PJ: 773-544-1231.",
    ),
    (
        "san-diego-palm-tree-trimming.html",
        "Palm Tree Trimming San Diego — Costs, What to Expect & Who to Call · SideGuy",
        "San Diego palm tree trimming in 2026: typical costs ($150–600+), when to trim, and how to find a licensed arborist who won't overcharge you. Free local guidance.",
    ),
    (
        "domain-expired-san-diego.html",
        "Domain Expired San Diego — How to Recover It Before It's Gone · SideGuy",
        "Domain expired or expiring soon? You have a short window before it goes to auction. San Diego businesses: here's exactly what to do right now and who to call. Free guidance.",
    ),
    (
        "ai-lead-generation-systems-san-diego.html",
        "AI Lead Generation San Diego — Automated Prospecting That Actually Works · SideGuy",
        "San Diego businesses: AI tools that find, qualify, and follow up with leads automatically. See what's realistic, what it costs, and how to start without wasted spend. Text PJ: 773-544-1231.",
    ),
    (
        "ai-business-solutions-san-diego.html",
        "AI Business Solutions San Diego — Save Time, Cut Costs, Grow Faster · SideGuy",
        "San Diego business owners: which AI automations actually save time, what they realistically cost, and how to start without breaking what works. Honest guide. Text PJ: 773-544-1231.",
    ),
    (
        "tech-help-hub-san-diego.html",
        "Tech Help San Diego — Software, Payments & AI for Business Owners · SideGuy",
        "San Diego business owner confused by tech decisions? Plain-English guides on software, payment systems, AI tools, and IT problems. Text PJ for free advice: 773-544-1231.",
    ),
]

updated = []
skipped = []

for filename, new_title, new_desc in TARGETS:
    path = ROOT / filename
    if not path.exists():
        skipped.append(filename)
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")
    original = text

    # Replace <title>...</title>
    text = re.sub(
        r'<title>[^<]*</title>',
        f'<title>{new_title}</title>',
        text, count=1
    )

    # Replace meta description — handles both attribute orders and quote styles
    text = re.sub(
        r'<meta\s+(?:name=["\']description["\']\s+content=["\'][^"\']*["\']|content=["\'][^"\']*["\']\s+name=["\']description["\'])\s*/?>',
        f'<meta name="description" content="{new_desc}"/>',
        text, count=1, flags=re.IGNORECASE
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        updated.append(filename)
    else:
        skipped.append(f"{filename} (no match)")

print(f"CTR title fix complete")
print(f"  Updated : {len(updated)}")
print(f"  Skipped : {len(skipped)}")
for f in updated:
    print(f"  ✓ {f}")
for f in skipped:
    print(f"  ✗ {f}")
