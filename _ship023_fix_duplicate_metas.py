#!/usr/bin/env python3
"""
SHIP-023: Fix duplicate meta descriptions.
Targets specific duplicate pairs/groups with unique, differentiated descriptions.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
meta_re = re.compile(r'(<meta\s+name="description"\s+content=")[^"]*(")', re.IGNORECASE)

# Map of filename → unique description (max 160 chars)
FIXES = {
    # confused-about-ai pair
    "confused-about-ai.html":
        "AI explained simply — what it is, what it isn't, and whether it makes sense for your business. No jargon, no hype. SideGuy.",

    # thermostat pair
    "thermostat-not-working.html":
        "Thermostat not working? Quick triage guide — what to check before calling an HVAC tech. Covers common causes and cost ranges.",

    # testing pages sharing generic fallback
    "penetration-test-small-business.html":
        "Penetration testing for small businesses — what it is, when you actually need it, and what it costs. Honest guidance from SideGuy.",
    "index-test.html":
        "SideGuy Solutions test index — internal development page. Plain-language guidance for San Diego operators.",
    "seo-template.html":
        "SideGuy SEO template — internal page structure for San Diego problem/solution pages.",
    "soil-testing-san-diego.html":
        "Soil testing in San Diego — when to test, what results mean, and who to hire. Honest guidance before you build or plant.",
    "sideguy-latest.html":
        "SideGuy latest — fresh guidance for San Diego operators. Clarity before cost, human help available.",
    "radon-testing-san-diego.html":
        "Radon testing in San Diego — do you need it, how much it costs, and what to do with the results. No scare tactics.",
    "template-v304.html":
        "SideGuy v304 page template — internal development reference. San Diego operator guidance layer.",
    "backflow-testing-san-diego.html":
        "Backflow testing in San Diego — who requires it, what it costs, and how to find a licensed tester. Plain-language guide.",

    # future/AI world pages
    "future-operating-systems.html":
        "How future operating systems are changing the way we work — practical overview without the sci-fi hype. SideGuy.",
    "how-small-teams-replace-big-companies.html":
        "How small teams are replacing big companies in 2026 — the tools, tactics, and mindset shifts making it possible. SideGuy.",
    "human-skills-that-survive-ai.html":
        "Which human skills survive AI? A grounded, practical look at what stays valuable as automation expands. SideGuy.",
    "energy-systems-of-the-next-decade.html":
        "Energy systems of the next decade — what's actually changing in power, storage, and grid tech. No hype, real signals.",
    "robots-at-work-not-sci-fi.html":
        "Robots at work — what's actually deployed today vs sci-fi fantasy. A plain-language look at real automation in 2026.",
    "ai-world-2027.html":
        "AI in 2027 — what changed, what didn't, and what San Diego operators should actually pay attention to. SideGuy.",

    # aaa template/test pages
    "aaa-sideguy-handshake-.html":
        "SideGuy handshake page — plain-language intro to what SideGuy does and how to get help in San Diego.",
    "aaa-test-home.html":
        "SideGuy test home — internal development page. Guidance layer for San Diego operators.",
    "aaa-PJ-dashboard.html":
        "SideGuy operator dashboard — internal tool for managing San Diego guidance workflows.",
    "aaa-blanket-template.html":
        "SideGuy blanket template — internal page scaffold for San Diego problem/solution guidance pages.",
    "aaa-intake.html":
        "SideGuy intake page — start here for plain-language guidance on your San Diego business challenge.",
    "_template.html":
        "SideGuy page template — the base scaffold used for all San Diego guidance pages. Internal reference.",

    # tech-help pair
    "tech-help-for-non-technical-people.html":
        "Tech help for non-technical people — plain-language explanations of common tech problems. No jargon. SideGuy.",

    # aaa-help pair
    "aaa-help-in-san-diego-handshake.html":
        "Need help in San Diego? SideGuy connects you with honest guidance before any transaction. One text, clear options.",
    "aaa-side-guy-help.html":
        "SideGuy help — plain-language guidance for San Diego operators. Text PJ for a real human response. Clarity before cost.",

    # ai-help pair
    "ai-help.html":
        "AI help for small businesses — what tools actually work, what they cost, and how to get started without the hype. SideGuy.",

    # payments-for-operators pair
    "payments-for-operators.html":
        "Payments for operators — how to accept payments, reduce fees, and avoid common traps. Practical guide for small businesses.",

    # roof-leak pair
    "roof-leak-after-rain.html":
        "Roof leak after rain? Here's what to check first, how to triage damage, and when to call a roofer. San Diego guidance.",

    # payment-processing hub pair
    "san-diego-payment-processing.html":
        "San Diego payment processing — compare options, cut fees, and find a processor that fits your business. Free guidance.",

    # circuit-breaker pair
    "circuit-breaker-tripping.html":
        "Circuit breaker keeps tripping? Safety checklist, common causes, and when to call a licensed electrician. SideGuy.",

    # business-automation pair
    "who-do-i-call-business-automation-help.html":
        "Who do I call for business automation help? Honest breakdown of options, costs, and red flags. No sales pressure. SideGuy.",

    # garage-door pair
    "garage-door-wont-open.html":
        "Garage door won't open? Quick triage — what to check before calling a tech. Common causes, cost ranges, DIY vs pro.",

    # del-mar pair
    "del-mar-payment-processing.html":
        "Del Mar payment processing — local guidance on finding the right processor, reducing fees, and getting fair terms.",

    # instant-settlement pair
    "instant-settlement-payments.html":
        "Instant settlement payments explained — how they work, which processors offer them, and whether you actually need them.",

    # mobile-app pair
    "mobile-app-development.html":
        "Mobile app development guidance — what it costs, how long it takes, and how to vet a developer. No jargon. SideGuy.",

    # solar pair
    "solar-panel-not-working.html":
        "Solar panel not working? Step-by-step triage guide — what to check before calling a technician. Common fixes and costs.",

    # template pages
    "sideguy-universal-template.html":
        "SideGuy universal template — internal scaffold for San Diego guidance pages. Human-first clarity layer.",
    "air-quality-testing-san-diego.html":
        "Air quality testing in San Diego — when to test, what to test for, and how to find a certified professional.",
    "template.html":
        "SideGuy page template — base HTML scaffold for San Diego guidance pages. Internal reference.",
    "problem-template.html":
        "SideGuy problem template — the starting point for all problem/solution guidance pages. Internal reference.",
    "human-solution-template.html":
        "SideGuy human solution template — page scaffold for human-first guidance content. Internal reference.",
    "seo-page-template.html":
        "SideGuy SEO page template — structured scaffold for search-optimized San Diego guidance pages.",
    "template-san-diego-help.html":
        "SideGuy San Diego help template — base page structure for local guidance pages. Internal reference.",
    "asbestos-testing-san-diego.html":
        "Asbestos testing in San Diego — when it's required, who does it, what it costs, and what to do with results.",
    "penetration-testing-san-diego.html":
        "Penetration testing services in San Diego — what's included, who needs it, and realistic cost ranges. SideGuy.",
    "index-working-backup.html":
        "SideGuy working index backup — internal dev snapshot. Guidance layer for San Diego operators.",
    "index-backup.html":
        "SideGuy index backup — internal development reference. Plain-language guidance for San Diego operators.",
    "lead-testing-san-diego.html":
        "Lead testing in San Diego — when to test, what results mean, and what to do if lead is found. Calm, clear guidance.",
    "clean-template.html":
        "SideGuy clean template — minimal HTML scaffold for new San Diego guidance pages. Internal reference.",
    "mold-testing-san-diego.html":
        "Mold testing in San Diego — when you actually need it, what it costs, and what to do after getting results.",
}

def fix_file(fname, new_desc):
    fpath = os.path.join(ROOT, fname)
    if not os.path.exists(fpath):
        return False, "not found"
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    updated = meta_re.sub(lambda m: m.group(1) + new_desc + m.group(2), content, count=1)
    if updated == content:
        return False, "no change (meta tag not found)"
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(updated)
    return True, "ok"

fixed, skipped = [], []
for fname, desc in FIXES.items():
    ok, reason = fix_file(fname, desc)
    if ok:
        fixed.append(fname)
    else:
        skipped.append((fname, reason))

print(f"✅ SHIP-023 complete — {len(fixed)} duplicate meta descriptions fixed.")
if skipped:
    print(f"⚠️  {len(skipped)} skipped:")
    for f, r in skipped:
        print(f"   {f}: {r}")
