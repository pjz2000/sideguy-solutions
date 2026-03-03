#!/usr/bin/env python3
"""
SideGuy Uplinks Backfiller
Adds the correct authority-network nav bar to pages that pre-date the uplinks system.
Uses classify_topic to determine the right category hub + industry hub + pillar per page.
Safe to re-run: skips pages that already have the uplinks nav.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from sideguy_classify import (
    classify_topic, slugify,
    CATEGORY_HUB_PATH, CATEGORY_HUB_LABELS,
    PILLAR_MAP, PILLAR_LABELS,
    industry_hub_path, industry_hub_label,
)

SKIP_DIRS  = {"_quarantine_backups", "node_modules", "seo-reserve", "hubs", "pillars"}
UPLINK_MARKER = "Operator Hub"

# Matches the -san-diego.html slug convention for generated pages only
GENERATED_RE = re.compile(r'^(.+)-san-diego\.html$')

def topic_from_filename(fname):
    m = GENERATED_RE.match(fname)
    if not m:
        return None
    return m.group(1).replace('-', ' ')

def build_uplinks_nav(topic, depth_prefix=""):
    """
    Returns the uplinks <nav> HTML for a given topic.
    depth_prefix: '../' for pages inside subdirs (unused for root pages).
    """
    info  = classify_topic(topic)
    links = [f'<a href="{depth_prefix}hub.html">Operator Hub</a>']

    for cat in info['categories']:
        hub_path  = CATEGORY_HUB_PATH.get(cat, '')
        hub_label = CATEGORY_HUB_LABELS.get(cat, '')
        if hub_path:
            links.append(f'<a href="{depth_prefix}{hub_path}">{hub_label}</a>')

    ind = info['industry']
    if ind:
        links.append(f'<a href="{depth_prefix}{industry_hub_path(ind)}">{industry_hub_label(ind)}</a>')

    for cat in info['categories']:
        pillar = PILLAR_MAP.get(cat, '')
        plabel = PILLAR_LABELS.get(cat, '')
        if pillar:
            links.append(f'<a href="{depth_prefix}{pillar}">{plabel}</a>')

    if len(links) <= 1:
        return ""

    sep   = '<span style="opacity:.4;margin:0 4px;">/</span>'
    chain = sep.join(links)
    return (
        f'\n<nav style="max-width:820px;margin:12px auto 0;padding:0 24px;'
        f'font-size:.82rem;color:#3f6173;display:flex;flex-wrap:wrap;'
        f'align-items:center;gap:4px;">\n  {chain}\n</nav>'
    )

added   = 0
skipped = 0

for fname in os.listdir(ROOT):
    if not fname.endswith('.html'):
        continue

    fpath = os.path.join(ROOT, fname)

    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Skip pages that already have uplinks
    if UPLINK_MARKER in html:
        skipped += 1
        continue

    topic = topic_from_filename(fname)
    if not topic:
        skipped += 1
        continue

    nav = build_uplinks_nav(topic)
    if not nav:
        skipped += 1
        continue

    # Inject after </header>
    if '</header>' in html:
        html = html.replace('</header>', '</header>' + nav, 1)
    else:
        skipped += 1
        continue

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    added += 1

print(f"Uplinks added: {added}  |  Skipped (already had or non-generated): {skipped}")
