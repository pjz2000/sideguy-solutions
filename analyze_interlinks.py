#!/usr/bin/env python3
"""
SIDEGUY SMART INTERLINKER v1
Creates contextual links between related pages
Enhances user navigation and SEO link equity
"""

import os
import glob
import re
from collections import defaultdict

PROJECT_ROOT = "/workspaces/sideguy-solutions"
os.chdir(PROJECT_ROOT)

print("🔗 Building smart interlink map...")

# Find all HTML pages
all_pages = glob.glob("*.html")

# Filter out junk
valid_pages = [p for p in all_pages if not any(x in p for x in 
    ["backup", "tmp", "temp", "_template", "sitemap.", "index-backup"])]

print(f"📄 Analyzing {len(valid_pages)} pages...")

# Build topic clusters
clusters = defaultdict(list)

for page in valid_pages:
    # Extract topic keywords from filename
    slug = page.replace(".html", "")
    
    # Topic extraction patterns
    if "who-do-i-call" in slug:
        clusters["decision-guide"].append(page)
        
        # Extract specific service type
        if "hvac" in slug or "ac-" in slug:
            clusters["hvac"].append(page)
        elif "plumb" in slug:
            clusters["plumbing"].append(page)
        elif "electrical" in slug or "electric" in slug:
            clusters["electrical"].append(page)
        elif "payment" in slug or "processing" in slug:
            clusters["payments"].append(page)
        elif "software" in slug or "ai" in slug or "automation" in slug:
            clusters["software-ai"].append(page)
        elif "foundation" in slug:
            clusters["foundation"].append(page)
        elif "roof" in slug:
            clusters["roofing"].append(page)
    
    if "-cost" in slug or "pricing" in slug or "how-much" in slug:
        clusters["cost-guides"].append(page)
        
    if "-vs-" in slug or "compare" in slug or "versus" in slug:
        clusters["comparisons"].append(page)
        
    if "stablecoin" in slug or "crypto" in slug or "solana" in slug or "blockchain" in slug:
        clusters["crypto-payments"].append(page)
        
    if "ai-" in slug or "automation" in slug or "workflow" in slug:
        clusters["ai-automation"].append(page)
        
    if "san-diego" in slug:
        clusters["san-diego"].append(page)
        
    # Extract North County cities
    if any(city in slug for city in ["escondido", "carlsbad", "encinitas", "san-marcos", "oceanside", "vista"]):
        clusters["north-county"].append(page)

# Find related pages function
def find_related(page, max_results=6):
    """Find most relevant related pages"""
    related = set()
    slug = page.replace(".html", "")
    
    # Find pages in same clusters
    for cluster_name, pages in clusters.items():
        if page in pages:
            # Add other pages from same cluster
            related.update([p for p in pages if p != page][:4])
    
    # Find pages with similar keywords
    keywords = set(re.findall(r'\b\w{4,}\b', slug.lower()))
    for other_page in valid_pages:
        if other_page == page:
            continue
        other_slug = other_page.replace(".html", "")
        other_keywords = set(re.findall(r'\b\w{4,}\b', other_slug.lower()))
        
        # If 2+ keywords match, it's related
        overlap = keywords & other_keywords
        if len(overlap) >= 2:
            related.add(other_page)
    
    # Return up to max_results, sorted
    return sorted(list(related))[:max_results]

# Generate interlink recommendations
interlink_map = {}
for page in valid_pages[:100]:  # Limit to 100 for testing
    related = find_related(page)
    if related:
        interlink_map[page] = related

# Output recommendations
print(f"\n✅ Generated interlink map for {len(interlink_map)} pages")
print(f"📊 Topic clusters found:")
for cluster_name, pages in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
    print(f"   - {cluster_name}: {len(pages)} pages")

# Save interlink map
print("\n💾 Saving interlink recommendations...")
with open("interlink-map.txt", "w") as f:
    f.write("SIDEGUY INTERLINK RECOMMENDATIONS\n")
    f.write("=" * 60 + "\n\n")
    
    for page, related in sorted(interlink_map.items()):
        f.write(f"{page}:\n")
        for rel_page in related:
            f.write(f"  → {rel_page}\n")
        f.write("\n")

print(f"✅ Saved to interlink-map.txt")

# Generate HTML snippet for manual insertion
print("\n📝 Sample interlink block (for manual testing):")
print("""
<div class="related-pages" style="margin:48px 0;padding:24px;background:#f3fbff;border-radius:12px;border:1px solid #d1e8ed;">
  <h3 style="margin:0 0 16px;font-size:1.1em;color:#073044;">Related Topics</h3>
  <ul style="margin:0;padding-left:1.2em;line-height:1.8;color:#073044;">
    <li><a href="/[PAGE1]" style="color:#1f7cff;text-decoration:none;">[Title 1]</a></li>
    <li><a href="/[PAGE2]" style="color:#1f7cff;text-decoration:none;">[Title 2]</a></li>
    <li><a href="/[PAGE3]" style="color:#1f7cff;text-decoration:none;">[Title 3]</a></li>
  </ul>
</div>
""")

print("\n✅ Interlink analysis complete!")
print(f"\nNext steps:")
print(f"  1. Review interlink-map.txt")
print(f"  2. Test on sample pages")
print(f"  3. Deploy interlinking script for full site")
