#!/usr/bin/env python3
"""
SideGuy Solutions — Metadata Audit Script
Checks for duplicate titles, missing meta descriptions, and other SEO issues
"""
import os
import re
from collections import defaultdict
from pathlib import Path

def extract_metadata(filepath):
    """Extract title, H1, and meta description from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        
        return {
            'title': title_match.group(1).strip() if title_match else None,
            'h1': re.sub(r'<[^>]+>', '', h1_match.group(1)).strip() if h1_match else None,
            'description': desc_match.group(1).strip() if desc_match else None
        }
    except Exception as e:
        return None

def main():
    root_dir = Path('/workspaces/sideguy-solutions')
    html_files = list(root_dir.glob('*.html'))
    
    # Exclude system files
    html_files = [f for f in html_files if not f.name.startswith('.') and f.name not in ['sitemap.html', 'master-layout.html', 'master.html']]
    
    print(f"📊 Analyzing {len(html_files)} HTML pages...\n")
    
    # Track duplicates
    titles = defaultdict(list)
    h1s = defaultdict(list)
    descriptions = defaultdict(list)
    
    # Track missing
    missing_title = []
    missing_h1 = []
    missing_desc = []
    
    for filepath in html_files:
        meta = extract_metadata(filepath)
        if not meta:
            continue
        
        filename = filepath.name
        
        if meta['title']:
            titles[meta['title']].append(filename)
        else:
            missing_title.append(filename)
        
        if meta['h1']:
            h1s[meta['h1']].append(filename)
        else:
            missing_h1.append(filename)
        
        if meta['description']:
            descriptions[meta['description']].append(filename)
        else:
            missing_desc.append(filename)
    
    # Report findings
    print("=" * 60)
    print("🔍 METADATA AUDIT REPORT")
    print("=" * 60)
    
    # Duplicate titles
    duplicate_titles = {t: files for t, files in titles.items() if len(files) > 1}
    if duplicate_titles:
        print(f"\n⚠️  DUPLICATE TITLES: {len(duplicate_titles)} unique titles shared by multiple pages")
        for title, files in sorted(duplicate_titles.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            print(f"  '{title}' appears in {len(files)} pages")
    else:
        print("\n✅ No duplicate titles found")
    
    # Duplicate H1s
    duplicate_h1s = {h: files for h, files in h1s.items() if len(files) > 1}
    if duplicate_h1s:
        print(f"\n⚠️  DUPLICATE H1s: {len(duplicate_h1s)} unique H1s shared by multiple pages")
    else:
        print("\n✅ No duplicate H1s found")
    
    # Duplicate descriptions
    duplicate_descs = {d: files for d, files in descriptions.items() if len(files) > 1}
    if duplicate_descs:
        print(f"\n⚠️  DUPLICATE DESCRIPTIONS: {len(duplicate_descs)} unique descriptions shared by multiple pages")
        for desc, files in sorted(duplicate_descs.items(), key=lambda x: len(x[1]), reverse=True)[:3]:
            print(f"  '{desc[:60]}...' appears in {len(files)} pages")
    else:
        print("\n✅ No duplicate descriptions found")
    
    # Missing metadata
    if missing_title:
        print(f"\n⚠️  MISSING TITLES: {len(missing_title)} pages")
    else:
        print("\n✅ All pages have titles")
    
    if missing_h1:
        print(f"\n⚠️  MISSING H1s: {len(missing_h1)} pages")
    else:
        print("\n✅ All pages have H1s")
    
    if missing_desc:
        print(f"\n⚠️  MISSING DESCRIPTIONS: {len(missing_desc)} pages")
    else:
        print("\n✅ All pages have meta descriptions")
    
    print("\n" + "=" * 60)
    print(f"📈 Total pages analyzed: {len(html_files)}")
    print("=" * 60)
    
    # Save detailed report
    report_path = root_dir / 'metadata-audit-report.txt'
    with open(report_path, 'w') as f:
        f.write("SIDEGUY METADATA AUDIT REPORT\n")
        f.write(f"Generated: {Path(__file__).name}\n")
        f.write("=" * 60 + "\n\n")
        
        if duplicate_titles:
            f.write(f"DUPLICATE TITLES ({len(duplicate_titles)}):\n")
            for title, files in sorted(duplicate_titles.items(), key=lambda x: len(x[1]), reverse=True):
                f.write(f"\n'{title}' ({len(files)} pages):\n")
                for fn in files[:10]:
                    f.write(f"  - {fn}\n")
                if len(files) > 10:
                    f.write(f"  ... and {len(files) - 10} more\n")
        
        f.write("\n" + "=" * 60 + "\n")
    
    print(f"\n💾 Detailed report saved to: metadata-audit-report.txt")

if __name__ == '__main__':
    main()
