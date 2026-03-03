#!/usr/bin/env python3
"""
SHIP-013: Sitewide Metadata Repair
- Fixes broken/template meta descriptions on vNext pages
- Standardizes short/generic titles
- Skips: QR cluster, aaa-* files, 404, _template, non-vNext pages
- Produces: fixed pages + report
"""

import re, glob, sys
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
REPO = Path('/workspaces/sideguy-solutions')
VNEXT_SIG = 'Who Do I Call? (Master Layout vNext)'

SKIP_FILES = {
    '_template.html', 'aaa-blanket-template.html', 'aaa-PJ-dashboard.html',
    'aaa-help-in-san-diego-handshake.html', 'aaa-intake.html',
    'aaa-side-guy-help.html', 'aaa-sideguy-handshake-.html',
    'aaa-test-home.html', '404.html', 'master.html', 'engine.html',
    'tickets.html', '-hub.html',
    # QR cluster (already have good metadata)
    'hvac-project-quote-review-san-diego.html',
    'plumbing-project-quote-review-san-diego.html',
    'electrical-project-quote-review-san-diego.html',
    'solar-project-quote-review-san-diego.html',
    'roofing-project-quote-review-san-diego.html',
    'contractor-project-quote-review-san-diego.html',
    'adu-project-quote-review-san-diego.html',
    'foundation-quote-review-san-diego.html',
    'landscaping-quote-review-san-diego.html',
    'painting-project-quote-review-san-diego.html',
    'garage-door-quote-review-san-diego.html',
}

TEMPLATE_DESC_MARKERS = [
    'Need help with', 'Clear guidance for San Diego. What to check first',
    'Human support available', 'in San Diego. What to check first',
    'Got a ', 'situation in San Diego', 'acting up in San Diego',
    'Plumber San Diego in San Diego',
]
GENERIC_TITLES = {'Who Do I Call? · SideGuy Solutions (San Diego)'}

# ── Service name extractor ───────────────────────────────────────────────────
def extract_service(h1: str, title: str) -> str:
    """Extract clean service name from H1, falling back to title."""
    # H1 sometimes has "in San Diego ServiceName" (broken template artifact)
    src = h1 or title
    svc = re.sub(r'^in San Diego\s+', '', src, flags=re.I).strip()
    # Remove trailing " · San Diego · SideGuy" etc.
    svc = re.sub(r'\s*[·|—]\s*(San Diego|SideGuy).*$', '', svc, flags=re.I).strip()
    # Remove leading/trailing "in San Diego"
    svc = re.sub(r'\s+in San Diego$', '', svc, flags=re.I).strip()
    svc = re.sub(r'^San Diego\s+', '', svc, flags=re.I).strip()
    # Title-case if all lower
    if svc and svc == svc.lower():
        svc = svc.title()
    return svc or 'This Service'

# ── Category detector ────────────────────────────────────────────────────────
def categorize(slug: str) -> str:
    s = slug.lower()
    if any(x in s for x in ['ac-','hvac','air-cond','heat','furnace','cooling',
                              'blowing','thermostat','mini-split','ductwork']):       return 'HVAC'
    if any(x in s for x in ['plumb','drain','leak','pipe','sewer','water-heat',
                              'toilet','faucet','shower','garbage-disposal']):        return 'PLUMBING'
    if any(x in s for x in ['electr','panel','outlet','wiring','breaker',
                              'circuit','generator','ev-charger','battery-backup']): return 'ELECTRICAL'
    if any(x in s for x in ['solar']):                                               return 'SOLAR'
    if any(x in s for x in ['roof','gutter','skylight','basement-water']):           return 'ROOFING'
    if any(x in s for x in ['payment','processing','credit-card','stripe',
                              'square','crypto','solana','fee','merchant',
                              'pos-','pos_','instant-pay','same-day-pay',
                              'lower-credit','field-service-pay','contractor-pay',
                              'service-business-pay']):                              return 'PAYMENTS'
    if any(x in s for x in ['ai-','ai_','artificial','automation','machine',
                              'agent','chatbot','llm','openai','gpt']):              return 'AI'
    if any(x in s for x in ['adu','contractor','handyman','foundation','landscap',
                              'painting','paint','garage-door','fence','deck',
                              'remodel','renovation','general-cont','flooring']):    return 'CONTRACTOR'
    if any(x in s for x in ['wifi','internet','tech','it-help','software',
                              'computer','network','vpn','saas','web-dev',
                              'app-','mobile-app','cloud']):                         return 'TECH'
    if any(x in s for x in ['locksmith','lawn','plumber','electrician','roofer',
                              'pest','window-rep','pool','tree','junk',
                              'carpet','pressure-wash']):                            return 'LOCAL_SERVICE'
    if any(x in s for x in ['carlsbad','chula-vista','encinit','escond',
                              'la-jolla','oceanside','santee','la-mesa','national',
                              'del-mar','solana-beach','rancho','north-county',
                              'cardiff','pacific-beach','mission-valley']):         return 'NEIGHBORHOOD'
    return 'OTHER'

# ── Description templates ────────────────────────────────────────────────────
# Each template takes (svc) and produces a description.
# Keep under 155 chars; use svc as the unique differentiator.

DESC_TEMPLATES = {
    'HVAC': [
        lambda svc: f"{svc} in San Diego — what to check before calling, when it's urgent, and what repairs cost in 2026. Free honest guidance from SideGuy.",
        lambda svc: f"San Diego {svc.lower()} help — step-by-step checks, repair vs replace guidance, and typical HVAC costs in 2026. No sales pitch, always free.",
    ],
    'PLUMBING': [
        lambda svc: f"{svc} in San Diego — what's urgent, what can wait, and what licensed plumbers charge in 2026. Free guidance, no referral fees.",
        lambda svc: f"San Diego {svc.lower()} — when to call a plumber, DIY limits, and realistic 2026 cost ranges. Honest help, no commission.",
    ],
    'ELECTRICAL': [
        lambda svc: f"{svc} in San Diego — safety steps first, permit requirements, and what licensed electricians charge in 2026. Free guidance.",
        lambda svc: f"San Diego {svc.lower()} help — what to check first, permit info, and 2026 electrician costs. Human guidance, no upsell.",
    ],
    'SOLAR': [
        lambda svc: f"{svc} in San Diego — what to check before calling, inverter reset steps, and when a technician is actually needed. Free guidance.",
        lambda svc: f"San Diego {svc.lower()} — troubleshooting guide, monitoring app tips, and what San Diego solar service calls cost in 2026.",
    ],
    'ROOFING': [
        lambda svc: f"{svc} in San Diego — what to check after a storm, what repairs cost, and what your contractor must include. Free guidance.",
        lambda svc: f"San Diego {svc.lower()} help — spot the difference between cosmetic and structural damage, and get fair repair cost context.",
    ],
    'PAYMENTS': [
        lambda svc: f"{svc} — honest breakdown for San Diego businesses. Real fee rates, no hidden costs, setup help from a local advisor.",
        lambda svc: f"San Diego {svc.lower()} — compare options, understand real fees, and get human help choosing the right processor. No pitch.",
    ],
    'AI': [
        lambda svc: f"{svc} — practical AI guidance for San Diego businesses. Honest cost breakdowns, realistic timelines, no hype. Human help available.",
        lambda svc: f"San Diego {svc.lower()} — what it actually costs, what it can do, and whether it's right for your business. Honest guidance.",
    ],
    'TECH': [
        lambda svc: f"{svc} in San Diego — step-by-step troubleshooting in plain language. What to check before calling, and when to call.",
        lambda svc: f"San Diego {svc.lower()} help — plain-language guide to fixing the problem yourself, and who to call if you can't.",
    ],
    'CONTRACTOR': [
        lambda svc: f"{svc} in San Diego — what the job costs in 2026, what to ask before hiring, and how to verify a contractor's license.",
        lambda svc: f"San Diego {svc.lower()} guidance — realistic cost ranges, red-flag checklist, and free quote review before you sign.",
    ],
    'LOCAL_SERVICE': [
        lambda svc: f"{svc} in San Diego — who to call, what to expect, and what the job typically costs in 2026. Free guidance from SideGuy.",
        lambda svc: f"Need a {svc.lower()} in San Diego? Know what fair pricing looks like in 2026 and what questions to ask. Always free.",
    ],
    'NEIGHBORHOOD': [
        lambda svc: f"{svc} — local guidance for San Diego businesses and homeowners. Honest advice, real fee context, no sales pitch.",
        lambda svc: f"San Diego {svc.lower()} — what local businesses pay, how to get started, and a human advisor when you need one.",
    ],
    'OTHER': [
        lambda svc: f"{svc} in San Diego — clear guidance on what to check first, who to call, and what it costs in 2026. Free human help.",
        lambda svc: f"San Diego {svc.lower()} help — plain-language answers before you spend money. What to know, who to trust, and what's fair.",
    ],
}

def make_desc(svc: str, cat: str, variant: int = 0) -> str:
    templates = DESC_TEMPLATES.get(cat, DESC_TEMPLATES['OTHER'])
    tmpl = templates[variant % len(templates)]
    d = tmpl(svc)
    if len(d) > 155:
        d = d[:152] + '...'
    return d

# ── Title builder ────────────────────────────────────────────────────────────
def make_title(svc: str, existing: str, cat: str) -> str | None:
    """Return new title or None if existing is already good."""
    existing = existing.strip()
    # Skip if title is already reasonable
    if existing in GENERIC_TITLES:
        pass  # always fix
    elif len(existing) >= 35 and len(existing) <= 65:
        return None  # good enough, don't touch
    elif len(existing) > 65:
        # Too long — trim. Use svc + San Diego | SideGuy pattern
        pass
    # else: too short or generic — fix

    # Build target
    # Don't double-insert "San Diego" if svc already has it
    has_sd = 'san diego' in svc.lower()
    if cat in ('PAYMENTS', 'AI'):
        t = f"{svc} San Diego | SideGuy" if not has_sd else f"{svc} | SideGuy"
    else:
        t = f"{svc} San Diego | SideGuy" if not has_sd else f"{svc} | SideGuy"

    if len(t) > 65:
        # Truncate svc
        max_svc = 65 - len(' San Diego | SideGuy')
        svc_short = svc[:max_svc].rstrip()
        t = f"{svc_short} San Diego | SideGuy" if not has_sd else f"{svc_short} | SideGuy"

    return t if t != existing else None

# ── Main repair loop ─────────────────────────────────────────────────────────
def is_desc_broken(desc: str) -> bool:
    if not desc: return True
    return any(m in desc for m in TEMPLATE_DESC_MARKERS)

def run():
    files = sorted(REPO.glob('*.html'))
    fixed, skipped_skip, skipped_good, skipped_non_vnext, errors = [], [], [], [], []

    # Use slug hash to pick variant — spreads across templates evenly
    for i, fp in enumerate(files):
        fname = fp.name
        if fname in SKIP_FILES:
            skipped_skip.append(fname)
            continue

        try:
            txt = fp.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            errors.append((fname, str(e)))
            continue

        if VNEXT_SIG not in txt:
            skipped_non_vnext.append(fname)
            continue

        title_m = re.search(r'<title>([^<]+)</title>', txt)
        desc_m  = re.search(r'<meta content="([^"]+)" name="description"', txt)
        h1_m    = re.search(r'<h1[^>]*>([^<]+)</h1>', txt)

        if not title_m:
            skipped_good.append(fname)
            continue

        existing_title = title_m.group(1).strip()
        existing_desc  = desc_m.group(1).strip() if desc_m else ''
        h1             = h1_m.group(1).strip() if h1_m else ''

        desc_broken  = is_desc_broken(existing_desc)
        title_broken = (existing_title in GENERIC_TITLES or len(existing_title) < 30)

        if not desc_broken and not title_broken:
            skipped_good.append(fname)
            continue

        svc  = extract_service(h1, existing_title)
        cat  = categorize(fname)
        var  = hash(fname) % 2  # spread across 2 variants per category

        new_txt = txt
        changed = False

        # Fix description
        if desc_broken:
            new_desc = make_desc(svc, cat, var)
            if desc_m:
                old_meta = desc_m.group(0)
                new_meta = f'<meta content="{new_desc}" name="description"/>'
                new_txt = new_txt.replace(old_meta, new_meta, 1)
            else:
                # Inject after canonical
                canon_end = new_txt.find('/>')
                # Find the canonical tag first
                canon_m = re.search(r'<link rel="canonical"[^>]*/>', new_txt)
                if canon_m:
                    insert_after = canon_m.end()
                    new_meta = f'\n<meta name="description" content="{new_desc}"/>'
                    new_txt = new_txt[:insert_after] + new_meta + new_txt[insert_after:]
                else:
                    # fallback: after <title>
                    title_end = new_txt.find('</title>') + len('</title>')
                    new_meta = f'\n<meta name="description" content="{new_desc}"/>'
                    new_txt = new_txt[:title_end] + new_meta + new_txt[title_end:]
            changed = True

        # Fix title (only when clearly broken)
        if title_broken:
            new_title = make_title(svc, existing_title, cat)
            if new_title:
                new_txt = new_txt.replace(
                    f'<title>{existing_title}</title>',
                    f'<title>{new_title}</title>',
                    1
                )
                changed = True

        if changed:
            fp.write_text(new_txt, encoding='utf-8')
            fixed.append(fname)

    # ── Report ───────────────────────────────────────────────────────────────
    print(f'\n{"="*60}')
    print(f'SHIP-013 Metadata Repair — Complete')
    print(f'{"="*60}')
    print(f'  Pages fixed:           {len(fixed)}')
    print(f'  Pages already good:    {len(skipped_good)}')
    print(f'  Pages skipped (list):  {len(skipped_skip)}')
    print(f'  Non-vNext (skipped):   {len(skipped_non_vnext)}')
    print(f'  Errors:                {len(errors)}')
    if errors:
        print('\nErrors:')
        for f, e in errors: print(f'  {f}: {e}')
    print(f'\nSample of fixed pages:')
    for f in fixed[:10]:
        print(f'  {f}')
    if len(fixed) > 10:
        print(f'  ... and {len(fixed)-10} more')
    return fixed

if __name__ == '__main__':
    fixed = run()
    sys.exit(0)
