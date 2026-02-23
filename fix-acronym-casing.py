#!/usr/bin/env python3
"""
fix-acronym-casing.py
Fixes incorrectly-cased acronyms in <title>, <h1>-<h3>, and <meta description>
tags across all HTML pages.

Skips .bak files. Only modifies files that actually change.
"""

import os
import re

# Acronyms to fix: (wrong_pattern, correct)
# Using word-boundary matching (\b) to avoid partial-word replacements.
FIXES = [
    (r'\bAi\b',   'AI'),
    (r'\bHvac\b', 'HVAC'),
    (r'\bSeo\b',  'SEO'),
    (r'\bApi\b',  'API'),
    (r'\bUi\b',   'UI'),
    (r'\bCrm\b',  'CRM'),
    (r'\bUx\b',   'UX'),
    (r'\bIot\b',  'IoT'),
    (r'\bErp\b',  'ERP'),
    (r'\bAdu\b',  'ADU'),
    (r'\bVpn\b',  'VPN'),
    (r'\bLlm\b',  'LLM'),
    (r'\bGpu\b',  'GPU'),
    (r'\bAc\b',   'AC'),   # Air Conditioning — safe within title-case service pages
]

# Tags/attributes to target (will only fix content within these)
# Matches: <title>...</title>, <h1>...</h1>, <h2>...</h2>, <h3>...</h3>
# and meta description content="..."
TAG_PATTERNS = [
    # Block tags: capture opening tag + content + closing tag
    (r'(<title>)(.*?)(</title>)',          re.DOTALL),
    (r'(<h1[^>]*>)(.*?)(</h1>)',           re.DOTALL),
    (r'(<h2[^>]*>)(.*?)(</h2>)',           re.DOTALL),
    (r'(<h3[^>]*>)(.*?)(</h3>)',           re.DOTALL),
    # Meta description: capture content="..." value
    (r'(name=["\']description["\'][^>]*content=["\'])(.*?)(["\'])',   re.DOTALL),
    (r'(content=["\'])(.*?)(["\'](?:\s*/?>|\s+name=["\']description))', re.DOTALL),
]


def fix_text(text):
    """Apply all acronym fixes to a text string."""
    for pattern, replacement in FIXES:
        text = re.sub(pattern, replacement, text)
    return text


def fix_tag_content(html):
    """Fix acronym casing only within targeted HTML tags/attributes."""
    # Fix block tags: title, h1, h2, h3
    for tag in ['title', 'h1', 'h2', 'h3']:
        pattern = r'(<' + tag + r'[^>]*>)(.*?)(</' + tag + r'>)'
        def replacer(m, tag=tag):
            return m.group(1) + fix_text(m.group(2)) + m.group(3)
        html = re.sub(pattern, replacer, html, flags=re.DOTALL | re.IGNORECASE)

    # Fix meta description content
    # Pattern: <meta ... name="description" ... content="VALUE" ... />
    # or:      <meta ... content="VALUE" ... name="description" ... />
    def fix_meta_desc(m):
        before = m.group(1)
        content = m.group(2)
        after = m.group(3)
        return before + fix_text(content) + after

    # name="description" content="..."
    html = re.sub(
        r'(name=["\']description["\'][^>]*?content=["\'])(.*?)(["\'])',
        fix_meta_desc,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )
    # content="..." name="description"
    html = re.sub(
        r'(content=["\'])(.*?)(["\'][^>]*?name=["\']description["\'])',
        fix_meta_desc,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    return html


def process_file(filepath):
    """Process a single HTML file. Returns True if file was modified."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()

    updated = fix_tag_content(original)

    if updated != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return True
    return False


def main():
    html_files = sorted(
        f for f in os.listdir('.')
        if f.endswith('.html')
        and not f.endswith('.bak')
        and os.path.isfile(f)
    )

    modified = []
    for fname in html_files:
        if process_file(fname):
            modified.append(fname)

    print(f"Processed: {len(html_files)} files")
    print(f"Modified:  {len(modified)} files")
    if modified:
        print("\nChanged files:")
        for f in modified:
            print(f"  {f}")


if __name__ == '__main__':
    main()
