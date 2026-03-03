#!/usr/bin/env python3
"""
SideGuy FAQ + Breadcrumb Schema Backfiller
Injects FAQPage and BreadcrumbList JSON-LD into all existing HTML pages
that don't already have them.

Derives the topic from the filename (reverse of slugify).
Safe to re-run: skips pages that already have FAQPage schema.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from sideguy_classify import classify_topic, CATEGORY_HUB_PATH, CATEGORY_HUB_LABELS, DOMAIN
from content_library  import get_content, make_faq_schema_json, make_breadcrumb_schema_json

SKIP_DIRS = {"_quarantine_backups", "node_modules", "seo-reserve"}

def topic_from_path(rel_path):
    """
    Convert a relative file path back to an approximate topic string.
    e.g. 'ai-automation-for-hvac-companies-san-diego.html' → 'ai automation for hvac companies'
         'hubs/industry-plumbers.html' → 'plumbers'
    """
    fname = os.path.basename(rel_path)
    # strip .html and trailing -san-diego
    topic = re.sub(r'\.html$', '', fname)
    topic = re.sub(r'-san-diego$', '', topic)
    # strip hub/pillar prefixes
    topic = re.sub(r'^(industry-|category-|city-)', '', topic)
    topic = re.sub(r'-master-guide$', '', topic)
    return topic.replace('-', ' ')

def breadcrumb_for(rel_path, title, categories, canonical):
    """Build (name, url) crumb list for this page."""
    crumbs = [("SideGuy Solutions", DOMAIN)]
    if categories:
        primary = categories[0]
        hub_path  = CATEGORY_HUB_PATH.get(primary, '')
        hub_label = CATEGORY_HUB_LABELS.get(primary, '')
        if hub_path:
            crumbs.append((hub_label, f"{DOMAIN}/{hub_path}"))
    crumbs.append((title, canonical))
    return crumbs

added = 0
skipped = 0

for dirpath, dirs, files in os.walk(ROOT):
    # prune dirs in-place so os.walk skips them
    dirs[:] = [
        d for d in dirs
        if not d.startswith('.') and d not in SKIP_DIRS
    ]

    for fname in files:
        if not fname.endswith('.html'):
            continue

        fpath    = os.path.join(dirpath, fname)
        rel_path = os.path.relpath(fpath, ROOT).replace('\\', '/')
        canonical = f"{DOMAIN}/{rel_path}"

        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()

        # Skip if already has FAQPage schema
        if '"FAQPage"' in html or "'FAQPage'" in html:
            skipped += 1
            continue

        # Derive topic and classify
        topic      = topic_from_path(rel_path)
        info       = classify_topic(topic)
        categories = info['categories']
        content    = get_content(topic, categories)

        # Build schema blocks
        faq_schema  = make_faq_schema_json(content['faqs'], canonical)

        # For title: try to extract from <title> tag
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        title = m.group(1).strip() if m else topic.title()

        crumbs           = breadcrumb_for(rel_path, title, categories, canonical)
        breadcrumb_schema = make_breadcrumb_schema_json(crumbs)

        inject = f"\n{faq_schema}\n{breadcrumb_schema}\n"
        html   = html.replace('</head>', inject + '</head>', 1)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        added += 1

print(f"FAQ + Breadcrumb schema added: {added}  |  Already had FAQPage: {skipped}")
