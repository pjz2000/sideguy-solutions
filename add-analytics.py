#!/usr/bin/env python3
"""
Add Plausible Analytics to all HTML pages
Privacy-respecting, GDPR-compliant analytics
"""

import re
from pathlib import Path

def add_analytics(filepath):
    """Add Plausible script tag to HTML file if not present"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has analytics
    if 'plausible.io' in content or 'data-domain' in content:
        return False
    
    # Add Plausible script before </head>
    analytics_script = '  <script defer data-domain="sideguy.solutions" src="https://plausible.io/js/script.js"></script>\n</head>'
    
    if '</head>' in content:
        content = content.replace('</head>', analytics_script, 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("📊 Adding privacy-respecting analytics")
    print("=" * 60)
    
    html_files = list(Path('.').glob('*.html'))
    html_files = [f for f in html_files if not any(x in f.name for x in ['backup', 'template', 'test'])]
    
    added = 0
    skipped = 0
    
    for filepath in html_files:
        if add_analytics(filepath):
            added += 1
        else:
            skipped += 1
    
    print(f"✅ Added analytics: {added} pages")
    print(f"⏭️  Skipped (already has analytics): {skipped} pages")
    print(f"\n🎉 Analytics setup complete!")
    print(f"\n📈 View stats at: https://plausible.io/sideguy.solutions")

if __name__ == '__main__':
    main()
