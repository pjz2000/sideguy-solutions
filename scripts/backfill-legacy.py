#!/usr/bin/env python3
"""
SideGuy Legacy Page Backfiller
One-pass backfill for ALL root HTML pages regardless of naming convention.
Adds whatever each page is missing: OG tags, JSON-LD schema, FAQ schema,
BreadcrumbList schema, and uplinks nav.

Safe to re-run: checks for each element before injecting.
"""
import os, re, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from sideguy_classify import (
    classify_topic, CATEGORY_HUB_PATH, CATEGORY_HUB_LABELS,
    PILLAR_MAP, PILLAR_LABELS, industry_hub_path, industry_hub_label,
    DOMAIN,
)
from content_library import get_content, make_faq_schema_json, make_breadcrumb_schema_json

TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.IGNORECASE | re.DOTALL)
DESC_RE  = re.compile(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', re.IGNORECASE)

def topic_from_filename(fname):
    t = re.sub(r'\.html$', '', fname)
    t = re.sub(r'-san-diego$', '', t)
    t = re.sub(r'^(aaa-|who-do-i-call-)', '', t)
    return t.replace('-', ' ').strip()

def make_og(url, title, desc):
    t = title.replace('"', '&quot;')
    d = desc.replace('"', '&quot;')
    return (
        f'<meta property="og:type" content="article"/>\n'
        f'<meta property="og:site_name" content="SideGuy Solutions"/>\n'
        f'<meta property="og:title" content="{t}"/>\n'
        f'<meta property="og:description" content="{d}"/>\n'
        f'<meta property="og:url" content="{url}"/>\n'
        f'<meta name="twitter:card" content="summary"/>\n'
        f'<meta name="twitter:title" content="{t}"/>\n'
        f'<meta name="twitter:description" content="{d}"/>\n'
    )

LOCAL_BIZ = """{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "SideGuy Solutions",
  "url": "https://sideguysolutions.com",
  "telephone": "+1-760-454-1860",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "San Diego",
    "addressRegion": "CA",
    "addressCountry": "US"
  },
  "areaServed": "United States",
  "sameAs": ["https://sideguysolutions.com"]
}"""

def make_schema(url, title):
    webpage = (
        '{{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "WebPage",\n'
        f'  "name": "{title.replace(chr(34), chr(39))}",\n'
        f'  "url": "{url}",\n'
        '  "isPartOf": {"@type": "WebSite", "url": "https://sideguysolutions.com"}\n'
        '}}'
    ).replace('{{', '{').replace('}}', '}')
    return (
        f'\n<script type="application/ld+json">\n{LOCAL_BIZ}\n</script>\n'
        f'<script type="application/ld+json">\n{webpage}\n</script>\n'
    )

def make_uplinks(topic):
    info  = classify_topic(topic)
    links = ['<a href="/hub.html">Operator Hub</a>']
    for cat in info['categories']:
        hp = CATEGORY_HUB_PATH.get(cat, '')
        hl = CATEGORY_HUB_LABELS.get(cat, '')
        if hp:
            links.append(f'<a href="/{hp}">{hl}</a>')
    ind = info['industry']
    if ind:
        links.append(f'<a href="/{industry_hub_path(ind)}">{industry_hub_label(ind)}</a>')
    for cat in info['categories']:
        pillar = PILLAR_MAP.get(cat, '')
        plabel = PILLAR_LABELS.get(cat, '')
        if pillar:
            links.append(f'<a href="/{pillar}">{plabel}</a>')
    if len(links) <= 1:
        return ''
    sep   = '<span style="opacity:.4;margin:0 4px;">/</span>'
    chain = sep.join(links)
    return (
        f'\n<nav style="max-width:820px;margin:12px auto 0;padding:0 24px;'
        f'font-size:.82rem;color:#3f6173;display:flex;flex-wrap:wrap;'
        f'align-items:center;gap:4px;">\n  {chain}\n</nav>'
    )

stats = {'og': 0, 'schema': 0, 'faq': 0, 'uplinks': 0, 'skipped': 0}

for fname in sorted(os.listdir(ROOT)):
    if not fname.endswith('.html'):
        continue
    # Skip admin/test pages
    if fname.startswith('aaa-') or fname in ('404.html', 'hub.html', '-hub.html'):
        stats['skipped'] += 1
        continue

    fpath    = os.path.join(ROOT, fname)
    page_url = f"{DOMAIN}/{fname}"

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    changed = False
    topic   = topic_from_filename(fname)
    info    = classify_topic(topic)
    cats    = info['categories']
    content = get_content(topic, cats)

    # Extract title + description from page
    mt = TITLE_RE.search(html)
    md = DESC_RE.search(html)
    title = mt.group(1).strip() if mt else topic.title()
    desc  = md.group(1).strip() if md else f"{title} — SideGuy Solutions, San Diego."

    head_inject = ''

    # 1. JSON-LD schema
    if 'application/ld+json' not in html:
        head_inject += make_schema(page_url, title)
        stats['schema'] += 1
        changed = True

    # 2. OG tags
    if 'og:title' not in html:
        head_inject += make_og(page_url, title, desc)
        stats['og'] += 1
        changed = True

    # 3. FAQ schema
    if '"FAQPage"' not in html:
        head_inject += make_faq_schema_json(content['faqs'], page_url) + '\n'
        stats['faq'] += 1
        changed = True

    # 4. Breadcrumb schema
    if '"BreadcrumbList"' not in html:
        crumbs = [("SideGuy Solutions", DOMAIN)]
        if cats:
            hp = CATEGORY_HUB_PATH.get(cats[0], '')
            hl = CATEGORY_HUB_LABELS.get(cats[0], '')
            if hp:
                crumbs.append((hl, f"{DOMAIN}/{hp}"))
        crumbs.append((title, page_url))
        head_inject += make_breadcrumb_schema_json(crumbs) + '\n'
        changed = True

    if head_inject:
        html = html.replace('</head>', head_inject + '</head>', 1)

    # 5. Uplinks nav
    if 'Operator Hub' not in html:
        nav = make_uplinks(topic)
        if nav:
            if '</header>' in html:
                html = html.replace('</header>', '</header>' + nav, 1)
                stats['uplinks'] += 1
                changed = True
            elif '<body>' in html:
                html = html.replace('<body>', '<body>' + nav, 1)
                stats['uplinks'] += 1
                changed = True
            elif '<body ' in html:
                # body with attributes
                html = re.sub(r'(<body[^>]*>)', r'\1' + nav, html, count=1)
                stats['uplinks'] += 1
                changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
    else:
        stats['skipped'] += 1

print(f"Legacy backfill complete:")
print(f"  OG tags added:       {stats['og']}")
print(f"  Schema added:        {stats['schema']}")
print(f"  FAQ schema added:    {stats['faq']}")
print(f"  Uplinks added:       {stats['uplinks']}")
print(f"  Already complete:    {stats['skipped']}")
