#!/usr/bin/env python3
"""
SideGuy Content Block Injector
Injects a "What Operators Should Know" section into pages that are missing it.
Uses the existing content_library and sideguy_classify infrastructure.
Safe to re-run: checks for presence before injecting.
"""
import os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from sideguy_classify import classify_topic
from content_library import get_content

injected = 0
skipped  = 0

for fname in sorted(os.listdir(ROOT)):
    if not fname.endswith('.html'):
        continue
    if fname.startswith('aaa-') or fname in ('404.html', 'hub.html', '-hub.html'):
        skipped += 1
        continue

    fpath = os.path.join(ROOT, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    if 'What Operators Should Know' in html:
        skipped += 1
        continue

    if '</body>' not in html:
        skipped += 1
        continue

    topic   = re.sub(r'\.html$', '', fname)
    topic   = re.sub(r'-san-diego$', '', topic)
    topic   = re.sub(r'^(aaa-|who-do-i-call-)', '', topic)
    topic   = topic.replace('-', ' ').strip()

    info    = classify_topic(topic)
    cats    = info['categories']
    content = get_content(topic, cats)

    block = (
        f'\n<section style="max-width:820px;margin:40px auto;padding:0 24px;">\n'
        f'  <h2 style="font-size:1.4rem;font-weight:700;color:#073044;margin-bottom:12px;">'
        f'What Operators Should Know</h2>\n'
        f'  <p style="color:#3f6173;line-height:1.7;">{content["intro"]}</p>\n\n'
        f'  <h3 style="font-size:1.1rem;font-weight:700;color:#073044;margin-top:24px;margin-bottom:8px;">'
        f'Common Mistake</h3>\n'
        f'  <p style="color:#3f6173;line-height:1.7;">{content["mistakes"]}</p>\n'
        f'</section>\n'
    )

    html = html.replace('</body>', block + '</body>', 1)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    injected += 1

print(f"Content differentiation injected.")
print(f"  Blocks added:    {injected}")
print(f"  Already present: {skipped}")
