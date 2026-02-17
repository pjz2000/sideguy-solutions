#!/usr/bin/env python3
"""
Add Schema.org LocalBusiness markup to all pages
Helps Google understand location and services
"""

import re
from pathlib import Path

SCHEMA_MARKUP = '''
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "SideGuy Solutions",
    "description": "Human-first guidance for San Diego operators",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "San Diego",
      "addressRegion": "CA",
      "addressCountry": "US"
    },
    "telephone": "+1-773-544-1231",
    "areaServed": {
      "@type": "City",
      "name": "San Diego"
    },
    "priceRange": "$$"
  }
  </script>'''

def add_schema(filepath):
    """Add schema markup before </body> tag"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has schema
    if 'application/ld+json' in content or '@type' in content:
        return False
    
    # Add before </body>
    if '</body>' in content:
        content = content.replace('</body>', f'{SCHEMA_MARKUP}\n</body>', 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    print("📍 Adding Schema.org LocalBusiness markup")
    print("=" * 60)
    
    html_files = list(Path('.').glob('*.html'))
    html_files = [f for f in html_files if not any(x in f.name for x in ['backup', 'template', 'test', 'hub'])]
    
    added = 0
    skipped = 0
    
    for filepath in html_files:
        if add_schema(filepath):
            added += 1
            if added <= 5:
                print(f"✅ {filepath.name}")
        else:
            skipped += 1
    
    print("=" * 60)
    print(f"✅ Added schema: {added} pages")
    print(f"⏭️  Skipped (already has schema): {skipped} pages")
    print(f"\n🎉 Schema markup complete!")
    print(f"\n📊 This helps Google understand you're a San Diego local business")

if __name__ == '__main__':
    main()
