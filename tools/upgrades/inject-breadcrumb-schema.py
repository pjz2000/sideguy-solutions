#!/usr/bin/env python3
"""
inject-breadcrumb-schema.py

Reads the breadcrumb <nav class="bc"> HTML already present on pages,
parses the anchor links, and injects BreadcrumbList JSON-LD before </head>.

Idempotent — skips pages already containing BreadcrumbList schema.

Usage:
  python3 tools/upgrades/inject-breadcrumb-schema.py --dry-run
  python3 tools/upgrades/inject-breadcrumb-schema.py --run
  python3 tools/upgrades/inject-breadcrumb-schema.py --run --limit=5000
"""

import os
import re
import json
import sys
from pathlib import Path

ROOT = Path(
    os.popen("git rev-parse --show-toplevel 2>/dev/null || pwd").read().strip()
)

BASE_URL = "https://sideguysolutions.com"

BC_NAV_RE  = re.compile(r'<nav[^>]+class=["\'][^"\']*bc[^"\']*["\'][^>]*>(.*?)</nav>', re.IGNORECASE | re.DOTALL)
ANCHOR_RE  = re.compile(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
SPAN_RE    = re.compile(r'<span[^>]*>(.*?)</span>', re.IGNORECASE | re.DOTALL)

def strip_tags(html: str) -> str:
    text = re.sub(r'<[^>]+>', '', html)
    text = (text
            .replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            .replace('&#39;', "'").replace('&quot;', '"').replace('&nbsp;', ' '))
    return ' '.join(text.split()).strip()


def resolve_url(href: str) -> str:
    if href.startswith('http'):
        return href
    if href.startswith('/'):
        return BASE_URL + href
    return BASE_URL + '/' + href


def parse_breadcrumbs(nav_html: str) -> list:
    """Extract ordered list of (name, url) from breadcrumb nav."""
    items = []

    # Anchors = linked crumbs
    for m in ANCHOR_RE.finditer(nav_html):
        href = m.group(1).strip()
        label = strip_tags(m.group(2))
        if not label or href in ('#', ''):
            continue
        # Skip separator spans inside anchor text
        label = re.sub(r'\s*/\s*', '', label).strip()
        if not label:
            continue
        items.append((label, resolve_url(href)))

    # Last crumb is a <span> (current page, no link)
    spans = SPAN_RE.findall(nav_html)
    for s in spans:
        label = strip_tags(s)
        if label and label not in ('/', '·', '—', '›', '>'):
            # Use page URL from canonical if available (we'll patch later)
            items.append((label, None))

    return items


def get_canonical(content: str) -> str | None:
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if m:
        return m.group(1)
    return None


def build_schema_block(items: list) -> str:
    entities = []
    for i, (name, url) in enumerate(items, 1):
        item = {
            "@type": "ListItem",
            "position": i,
            "name": name,
        }
        if url:
            item["item"] = url
        entities.append(item)

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": entities
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(schema, indent=2, ensure_ascii=False)
        + '\n</script>'
    )


def process_file(filepath: Path, dry_run: bool) -> str:
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return 'error'

    if 'BreadcrumbList' in content:
        return 'skip-has-schema'

    if '</head>' not in content:
        return 'skip-no-head'

    nav_m = BC_NAV_RE.search(content)
    if not nav_m:
        return 'skip-no-breadcrumb'

    items = parse_breadcrumbs(nav_m.group(1))
    if len(items) < 2:
        return 'skip-too-short'

    # Fill in current page URL for last crumb if missing
    canonical = get_canonical(content)
    if items[-1][1] is None and canonical:
        items[-1] = (items[-1][0], canonical)

    schema_block = build_schema_block(items)
    new_content = content.replace('</head>', f'{schema_block}\n</head>', 1)

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return 'updated'


def main():
    dry_run = '--dry-run' in sys.argv
    live    = '--run' in sys.argv

    if not dry_run and not live:
        print("Usage:")
        print("  python3 tools/upgrades/inject-breadcrumb-schema.py --dry-run")
        print("  python3 tools/upgrades/inject-breadcrumb-schema.py --run")
        print("  python3 tools/upgrades/inject-breadcrumb-schema.py --run --limit=5000")
        sys.exit(1)

    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=')[1])

    mode = 'DRY RUN' if dry_run else 'LIVE'
    print(f"inject-breadcrumb-schema.py — {mode}")
    print(f"Root: {ROOT}")
    if limit:
        print(f"Limit: {limit} updates")
    print()

    pages = sorted(ROOT.glob('*.html'))
    counts = {}

    for page in pages:
        if limit and counts.get('updated', 0) >= limit:
            break

        result = process_file(page, dry_run=dry_run)
        counts[result] = counts.get(result, 0) + 1

        if result == 'updated':
            print(f"{'[DRY] ' if dry_run else ''}Breadcrumb schema → {page.name}")

    print()
    print("Results:")
    print(f"  Schema injected:    {counts.get('updated', 0)}")
    print(f"  Already had schema: {counts.get('skip-has-schema', 0)}")
    print(f"  No breadcrumb nav:  {counts.get('skip-no-breadcrumb', 0)}")
    print(f"  Too few crumbs:     {counts.get('skip-too-short', 0)}")
    print(f"  No </head>:         {counts.get('skip-no-head', 0)}")
    print(f"  Errors:             {counts.get('error', 0)}")
    print()
    if dry_run and counts.get('updated', 0) > 0:
        print("Re-run with --run to apply changes.")


if __name__ == '__main__':
    main()
