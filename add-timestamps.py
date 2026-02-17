#!/usr/bin/env python3
"""
Add 'Last Updated' timestamp to all pages for SEO freshness
"""

import re
from pathlib import Path

def add_timestamp(filepath):
    """Add last-updated display to HTML file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has timestamp
    if 'id="lastUpdated"' in content or 'Last updated' in content:
        return False
    
    # Find the footer or end of main content
    timestamp_html = '''
    <div style="margin-top:32px;padding:16px;text-align:center;font-size:13px;color:var(--muted2);">
      <span id="lastUpdated">Updated February 2026</span>
    </div>
'''
    
    # Try to insert before </main> or </body>
    if '</main>' in content:
        content = content.replace('</main>', f'{timestamp_html}</main>', 1)
    elif '</body>' in content:
        content = content.replace('</body>', f'{timestamp_html}</body>', 1)
    else:
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True

def main():
    print("📅 Adding 'Last Updated' timestamps")
    print("=" * 60)
    
    html_files = list(Path('.').glob('*.html'))
    html_files = [f for f in html_files if not any(x in f.name for x in ['backup', 'template', 'test'])]
    
    added = 0
    skipped = 0
    
    for filepath in html_files:
        if add_timestamp(filepath):
            added += 1
            if added <= 5:
                print(f"✅ {filepath.name}")
        else:
            skipped += 1
    
    print("=" * 60)
    print(f"✅ Added timestamps: {added} pages")
    print(f"⏭️  Skipped: {skipped} pages")
    print(f"\n🎉 Timestamp addition complete!")

if __name__ == '__main__':
    main()
