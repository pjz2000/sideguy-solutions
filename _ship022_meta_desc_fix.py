#!/usr/bin/env python3
"""
SHIP-022: Meta Description Fix
Auto-generates unique, actionable meta descriptions for all HTML files missing one.
Derives description from <title> tag and page slug for uniqueness.
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

meta_re     = re.compile(r'<meta\s+name="description"\s+content="[^"]*"[^>]*/?\s*>', re.IGNORECASE)
title_re    = re.compile(r'<title>([^<]+)</title>', re.IGNORECASE)
canonical_re= re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"', re.IGNORECASE)
charset_re  = re.compile(r'(<meta[^>]+charset[^>]+>)', re.IGNORECASE)

def slug_to_phrase(slug):
    """Convert a filename slug to a human-readable phrase."""
    slug = slug.replace('.html', '').replace('-', ' ').replace('_', ' ')
    # Remove trailing san-diego if present (we'll add it back nicely)
    slug = re.sub(r'\s+san diego\s*$', '', slug, flags=re.IGNORECASE).strip()
    return slug.strip()

def build_description(fname, title, canonical):
    """Build a unique, actionable ~150-char meta description from available signals."""
    phrase = slug_to_phrase(fname)

    # Determine topic category from slug
    slug_lower = fname.lower()

    if 'who-do-i-call' in slug_lower:
        desc = f"Not sure who to call for {phrase} in San Diego? Plain-language guidance — no sales pressure. Clarity before cost. SideGuy."
    elif 'ai-automation' in slug_lower or 'ai-marketing' in slug_lower or 'ai-invoicing' in slug_lower or 'ai-scheduling' in slug_lower or 'ai-intake' in slug_lower:
        desc = f"AI automation guidance for {phrase} in San Diego — honest costs, realistic timelines, no hype. Human help available."
    elif 'hvac' in slug_lower or 'ac-not' in slug_lower or 'heater' in slug_lower or 'thermostat' in slug_lower or 'furnace' in slug_lower:
        desc = f"HVAC help for {phrase} in San Diego — what to check first, who to call, and how to avoid overpaying. SideGuy."
    elif 'plumb' in slug_lower or 'drain' in slug_lower or 'leak' in slug_lower or 'water-heater' in slug_lower:
        desc = f"Plumbing guidance for {phrase} in San Diego — step-by-step triage, cost ranges, and who to call. SideGuy."
    elif 'electrical' in slug_lower or 'panel' in slug_lower or 'circuit' in slug_lower:
        desc = f"Electrical guidance for {phrase} in San Diego — safety checklist, permit info, and honest contractor tips. SideGuy."
    elif 'payment' in slug_lower or 'stripe' in slug_lower or 'fees' in slug_lower or 'invoic' in slug_lower:
        desc = f"Payment processing guidance for {phrase} in San Diego — fee comparison, red flags, and free review. SideGuy."
    elif 'roofing' in slug_lower or 'roof' in slug_lower:
        desc = f"Roofing guidance for {phrase} in San Diego — cost ranges, permit checklist, and how to vet contractors. SideGuy."
    elif 'remodel' in slug_lower or 'kitchen' in slug_lower or 'bathroom' in slug_lower:
        desc = f"Remodeling guidance for {phrase} in San Diego — realistic budgets, permit info, and contractor vetting tips. SideGuy."
    elif 'foundation' in slug_lower or 'settling' in slug_lower:
        desc = f"Foundation guidance for {phrase} in San Diego — what's urgent, what's not, and who to trust. SideGuy."
    elif 'garage' in slug_lower:
        desc = f"Garage door guidance for {phrase} in San Diego — cost breakdown, permit info, and honest contractor tips. SideGuy."
    elif 'landscap' in slug_lower or 'deck' in slug_lower or 'fence' in slug_lower:
        desc = f"Landscaping guidance for {phrase} in San Diego — realistic costs, local tips, and free quote review. SideGuy."
    elif 'seo' in slug_lower or 'ranking' in slug_lower or 'google' in slug_lower:
        desc = f"SEO and local ranking guidance for {phrase} in San Diego — what actually works, no agency fluff. SideGuy."
    elif 'software' in slug_lower or 'app' in slug_lower or 'tech' in slug_lower or 'it-help' in slug_lower:
        desc = f"Tech and software guidance for {phrase} in San Diego — plain-language help, no jargon. SideGuy."
    elif 'business' in slug_lower or 'operator' in slug_lower or 'owner' in slug_lower:
        desc = f"Business guidance for {phrase} in San Diego — honest, plain-language help before you spend money. SideGuy."
    elif 'quote' in slug_lower or 'cost' in slug_lower or 'price' in slug_lower:
        desc = f"Cost and quote guidance for {phrase} in San Diego — real ranges, red flags, and free review. SideGuy."
    elif 'confused' in slug_lower or 'help' in slug_lower:
        desc = f"Confused about {phrase} in San Diego? Get plain-language guidance — talk to a human first. SideGuy."
    elif 'hub' in slug_lower or 'directory' in slug_lower or 'index' in slug_lower:
        desc = f"San Diego {phrase} resource hub — curated guidance, honest answers, clarity before cost. SideGuy Solutions."
    elif '1-year' in slug_lower or 'quit' in slug_lower or 'burnout' in slug_lower:
        desc = f"Struggling with {phrase}? Honest, practical guidance for San Diego business owners. You're not alone. SideGuy."
    elif 'discouraged' in slug_lower or 'struggling' in slug_lower:
        desc = f"Feeling discouraged about {phrase}? Real talk and practical next steps for San Diego operators. SideGuy."
    else:
        # Generic fallback derived from title or phrase
        clean_title = title.replace(' · SideGuy', '').replace(' · SideGuy Solutions', '').strip() if title else phrase.title()
        desc = f"{clean_title} in San Diego — plain-language guidance and real help from SideGuy. Clarity before cost."

    # Trim to 160 chars safely
    if len(desc) > 160:
        desc = desc[:157].rsplit(' ', 1)[0] + '...'

    return desc


def has_meta_desc(content):
    return bool(meta_re.search(content))


def insert_meta_desc(content, desc):
    """Insert <meta name="description" ...> after <link rel="canonical"> or after <meta charset>."""
    meta_tag = f'<meta name="description" content="{desc}"/>'

    # Prefer inserting after canonical
    canon_match = canonical_re.search(content)
    if canon_match:
        insert_pos = canon_match.end()
        return content[:insert_pos] + '\n' + meta_tag + content[insert_pos:]

    # Fallback: after charset meta
    charset_match = charset_re.search(content)
    if charset_match:
        insert_pos = charset_match.end()
        return content[:insert_pos] + '\n' + meta_tag + content[insert_pos:]

    # Last resort: after <head>
    head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
    if head_match:
        insert_pos = head_match.end()
        return content[:insert_pos] + '\n' + meta_tag + content[insert_pos:]

    return content


def main():
    html_files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    fixed = []
    skipped = []

    for fname in html_files:
        fpath = os.path.join(ROOT, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception as e:
            skipped.append((fname, str(e)))
            continue

        if has_meta_desc(content):
            continue  # already has one

        # Extract title and canonical for context
        title_m = title_re.search(content)
        title = title_m.group(1).strip() if title_m else ''
        canon_m = canonical_re.search(content)
        canonical = canon_m.group(1).strip() if canon_m else ''

        desc = build_description(fname, title, canonical)
        updated = insert_meta_desc(content, desc)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(updated)

        fixed.append((fname, desc))

    print(f"\n✅ SHIP-022 complete — meta descriptions added to {len(fixed)} files.")
    if skipped:
        print(f"⚠️  Skipped {len(skipped)} files (read errors).")
    print("\nSample of changes:")
    for fname, desc in fixed[:10]:
        print(f"  {fname}\n    → {desc}\n")

if __name__ == '__main__':
    main()
