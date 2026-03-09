#!/usr/bin/env python3
"""
SHIP-020: Accessibility Upgrade — Add skip-to-content link and clarify semantic tags
Batch-edits all root-level HTML files to improve accessibility and semantic structure.
"""
import os
import re

def insert_skip_link(content):
    # Insert skip link right after <body>
    skip_html = '<a href="#main-content" class="skip-link" style="position:absolute;left:0;top:0;background:#fff;color:#073044;padding:8px 16px;border-radius:8px;z-index:1000;">Skip to content</a>'
    return re.sub(r'(<body[^>]*>)', r'\1\n' + skip_html, content, flags=re.IGNORECASE)


def add_main_id(content):
    # Add id="main-content" to <main> if not present
    return re.sub(r'<main(?![^>]*id=)', r'<main id="main-content"', content, flags=re.IGNORECASE)


def add_aria_labels(content):
    # Add ARIA labels to nav and main if not present
    content = re.sub(r'<nav(?![^>]*aria-label)', r'<nav aria-label="Breadcrumb navigation"', content, flags=re.IGNORECASE)
    content = re.sub(r'<main(?![^>]*aria-label)', r'<main aria-label="Main content"', content, flags=re.IGNORECASE)
    return content


def process_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()
    updated = insert_skip_link(original)
    updated = add_main_id(updated)
    updated = add_aria_labels(updated)
    if updated != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        return True
    return False


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    html_files = [f for f in os.listdir(root) if f.endswith('.html')]
    changed = []
    for fname in html_files:
        fpath = os.path.join(root, fname)
        if process_file(fpath):
            changed.append(fname)
    print(f"Accessibility upgraded in {len(changed)} files.")
    for fname in changed:
        print(f"  ✓ {fname}")

if __name__ == '__main__':
    main()
