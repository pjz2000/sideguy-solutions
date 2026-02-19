#!/usr/bin/env python3
"""
Add Related Links sections to pages for internal linking
Helps Google discover pages and understand relationships
"""

import os
import re
from pathlib import Path

# Define related page clusters
CLUSTERS = {
    'hvac': {
        'hub': 'hvac-problems-hub-san-diego.html',
        'pages': [
            ('ac-not-cooling-san-diego.html', 'AC Not Cooling'),
            ('ac-blowing-warm-air.html', 'AC Blowing Warm Air'),
            ('ac-making-noise.html', 'AC Making Noise'),
            ('ac-not-turning-on.html', 'AC Not Turning On'),
            ('heater-not-turning-on-san-diego.html', 'Heater Not Working'),
            ('hvac-repair-san-diego.html', 'HVAC Repair'),
        ]
    },
    'plumbing': {
        'hub': 'plumbing-problems-hub-san-diego.html',
        'pages': [
            ('clogged-drain-san-diego.html', 'Clogged Drain'),
            ('no-hot-water-san-diego.html', 'No Hot Water'),
            ('low-water-pressure-san-diego.html', 'Low Water Pressure'),
            ('water-leak-under-sink-san-diego.html', 'Water Leak'),
            ('toilet-running-constantly-san-diego.html', 'Toilet Running'),
        ]
    },
    'electrical': {
        'pages': [
            ('outlet-not-working-san-diego.html', 'Outlet Not Working'),
            ('breaker-keeps-tripping-san-diego.html', 'Breaker Tripping'),
            ('flickering-lights-san-diego.html', 'Flickering Lights'),
        ]
    },
    'payment': {
        'hub': 'payment-processing-hub-san-diego.html',
        'pages': [
            ('payment-processing-san-diego.html', 'Payment Processing'),
            ('instant-settlements-san-diego.html', 'Instant Settlements'),
            ('lower-credit-card-fees-san-diego.html', 'Lower Credit Card Fees'),
            ('contractor-payments-san-diego.html', 'Contractor Payments'),
        ]
    },
    'tech': {
        'hub': 'tech-help-hub-san-diego.html',
        'pages': [
            ('wifi-keeps-dropping-san-diego.html', 'WiFi Dropping'),
            ('computer-wont-turn-on-san-diego.html', 'Computer Won\'t Turn On'),
            ('internet-slow-san-diego.html', 'Slow Internet'),
        ]
    }
}

def get_related_links(filename, category):
    """Generate HTML for related links section"""
    
    if category not in CLUSTERS:
        return ""
    
    cluster = CLUSTERS[category]
    links_html = []
    
    # Add hub link if exists and not current page
    if 'hub' in cluster and cluster['hub'] != filename:
        links_html.append(f'<a href="{cluster["hub"]}" style="color:var(--mint);text-decoration:none;font-weight:600;">→ See All {category.upper()} Problems</a>')
    
    # Add related page links (exclude current page)
    for page_file, page_title in cluster['pages']:
        if page_file != filename:
            links_html.append(f'<a href="{page_file}" style="color:var(--ink);text-decoration:none;">• {page_title}</a>')
    
    if not links_html:
        return ""
    
    # Create related section HTML
    html = f'''
<!-- Related Problems -->
<section style="margin:48px auto 24px;padding:32px;max-width:800px;background:var(--card);border-radius:var(--r);border:1px solid var(--stroke);box-shadow:var(--shadow);">
  <h3 style="margin:0 0 16px;font-size:20px;color:var(--ink);">Related Problems</h3>
  <div style="display:flex;flex-direction:column;gap:12px;">
    {chr(10).join(f'    {link}' for link in links_html)}
  </div>
</section>
'''
    return html

def detect_category(filename):
    """Detect which cluster a file belongs to"""
    fn_lower = filename.lower()
    
    if any(x in fn_lower for x in ['hvac', 'ac-', 'heater', 'air-condition']):
        return 'hvac'
    elif any(x in fn_lower for x in ['plumb', 'drain', 'water', 'toilet', 'leak']):
        return 'plumbing'
    elif any(x in fn_lower for x in ['electric', 'outlet', 'breaker', 'light']):
        return 'electrical'
    elif any(x in fn_lower for x in ['payment', 'merchant', 'contractor-payment']):
        return 'payment'
    elif any(x in fn_lower for x in ['tech', 'computer', 'wifi', 'internet']):
        return 'tech'
    
    return None

def add_related_links(filepath):
    """Add related links section before footer"""
    try:
        filename = os.path.basename(filepath)
        category = detect_category(filename)
        
        if not category:
            return None  # Not in a cluster
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if already has related links
        if 'Related Problems' in content or 'Related Pages' in content:
            return None
        
        # Generate related links HTML
        related_html = get_related_links(filename, category)
        if not related_html:
            return None
        
        # Insert before the closing </main> tag
        if '</main>' in content:
            content = content.replace('</main>', f'{related_html}</main>', 1)
        else:
            return None
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (filename, category)
    
    except Exception as e:
        return None

def main():
    print("🔗 Internal Linking System")
    print("=" * 70)
    print("Adding related problem links for better SEO...")
    print()
    
    html_files = list(Path('.').glob('*.html'))
    exclude = ['template', 'backup', 'test', 'aaa-', 'index-', 'sitemap', 'master', 'hub']
    html_files = [f for f in html_files if not any(x in f.name for x in exclude)]
    
    print(f"📄 Processing {len(html_files)} pages...\n")
    
    added = {'hvac': [], 'plumbing': [], 'electrical': [], 'payment': [], 'tech': []}
    
    for i, fp in enumerate(html_files, 1):
        if i % 100 == 0:
            print(f"   ... {i}/{len(html_files)}")
        
        res = add_related_links(fp)
        if res:
            filename, category = res
            added[category].append(filename)
            if sum(len(v) for v in added.values()) <= 10:
                print(f"✅ {filename} → {category} cluster")
    
    print()
    print("=" * 70)
    print("📊 Internal Links Added:")
    for cat, files in added.items():
        if files:
            print(f"   {cat.upper()}: {len(files)} pages")
    
    total = sum(len(v) for v in added.values())
    print(f"\n✅ Total: {total} pages now have related problem links")
    print("💡 This helps Google discover & understand page relationships")
    print("\n🎉 Done! Ready to commit and push.")

if __name__ == '__main__':
    main()
