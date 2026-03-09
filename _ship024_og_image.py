#!/usr/bin/env python3
"""
SHIP-024: Add og:image and twitter:image tags to all HTML files missing them.
Uses SideGuy's canonical social preview image hosted at sideguysolutions.com.
Also adds twitter:image to any page already having twitter:card but missing twitter:image.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

OG_IMAGE_URL    = "https://sideguysolutions.com/og-preview.png"
OG_IMAGE_TAG    = f'<meta property="og:image" content="{OG_IMAGE_URL}"/>'
TW_IMAGE_TAG    = f'<meta name="twitter:image" content="{OG_IMAGE_URL}"/>'

og_image_re  = re.compile(r'og:image',        re.IGNORECASE)
tw_image_re  = re.compile(r'twitter:image',   re.IGNORECASE)
og_url_re    = re.compile(r'(<meta\s+property="og:url"[^>]*/?>)', re.IGNORECASE)
tw_card_re   = re.compile(r'(<meta\s+name="twitter:card"[^>]*/?>)', re.IGNORECASE)

def process(fpath):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    changed = False

    # -- og:image --
    if not og_image_re.search(content):
        m = og_url_re.search(content)
        if m:
            content = content[:m.end()] + '\n' + OG_IMAGE_TAG + content[m.end():]
            changed = True

    # -- twitter:image --
    if not tw_image_re.search(content):
        m = tw_card_re.search(content)
        if m:
            content = content[:m.end()] + '\n' + TW_IMAGE_TAG + content[m.end():]
            changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed

def main():
    html_files = [f for f in os.listdir(ROOT) if f.endswith('.html')]
    fixed = 0
    for fname in html_files:
        if process(os.path.join(ROOT, fname)):
            fixed += 1
    print(f"✅ SHIP-024 complete — og:image / twitter:image added to {fixed} files.")

if __name__ == '__main__':
    main()
