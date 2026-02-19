#!/usr/bin/env python3
"""
Add Schema.org markup to all pages.
Adds two blocks per page:
  1. LocalBusiness — tells Google about SideGuy Solutions
  2. WebPage — page-specific name/description drawn from <title> and <meta description>
"""

import re
import json
from pathlib import Path


def extract_title(content):
    m = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return "SideGuy Solutions — San Diego Help"


def extract_description(content):
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', content, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return "Clear guidance for San Diego. What to check first, who to call, typical costs."


def build_schema(title, description, url_slug):
    """Build combined LocalBusiness + WebPage JSON-LD."""
    page_url = f"https://sideguy.solutions/{url_slug}"

    local_biz = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "SideGuy Solutions",
        "description": "Human-first guidance for San Diego home and business owners",
        "url": "https://sideguy.solutions",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "San Diego",
            "addressRegion": "CA",
            "addressCountry": "US"
        },
        "telephone": "+1-773-544-1231",
        "areaServed": {
            "@type": "City",
            "name": "San Diego"
        },
        "priceRange": "$$"
    }

    webpage = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": page_url,
        "isPartOf": {
            "@type": "WebSite",
            "name": "SideGuy Solutions",
            "url": "https://sideguy.solutions"
        }
    }

    block = (
        f'\n  <script type="application/ld+json">\n'
        f'  {json.dumps(local_biz, indent=2)}\n'
        f'  </script>\n'
        f'  <script type="application/ld+json">\n'
        f'  {json.dumps(webpage, indent=2)}\n'
        f'  </script>'
    )
    return block


def add_schema(filepath):
    """Add schema markup before </body> tag."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has schema
    if 'application/ld+json' in content:
        return False

    if '</body>' not in content:
        return False

    title = extract_title(content)
    description = extract_description(content)
    url_slug = filepath.name

    schema_block = build_schema(title, description, url_slug)
    content = content.replace('</body>', f'{schema_block}\n</body>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    print("📍 Adding Schema.org LocalBusiness + WebPage markup")
    print("=" * 60)

    skip_patterns = ['backup', '.bak', 'template', 'aaa-test', 'new-page']
    html_files = [
        f for f in Path('.').glob('*.html')
        if not any(x in f.name for x in skip_patterns)
    ]
    html_files.sort()

    added = 0
    skipped = 0

    for filepath in html_files:
        if add_schema(filepath):
            added += 1
            if added <= 10:
                print(f"  ✅ {filepath.name}")
        else:
            skipped += 1

    if added > 10:
        print(f"  ... and {added - 10} more")

    print("=" * 60)
    print(f"✅ Schema added:   {added} pages")
    print(f"⏭️  Already had it: {skipped} pages")
    print(f"\n🎉 Done! Google can now understand each page individually.")

if __name__ == '__main__':
    main()
