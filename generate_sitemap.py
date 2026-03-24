#!/usr/bin/env python3
"""
SIDEGUY SITEMAP GENERATOR v2
Fast, clean, excludes junk
"""

import os
import glob
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = "/workspaces/sideguy-solutions"
os.chdir(PROJECT_ROOT)

print("🧹 Generating clean sitemap...")

# Backup old sitemap
if os.path.exists("sitemap.xml"):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    os.rename("sitemap.xml", f"sitemap.backup.{timestamp}.xml")
    print(f"✅ Backed up old sitemap")

# Find valid HTML files (root level only)
all_html = glob.glob("*.html")

# Filter out junk
valid_pages = []
for page in all_html:
    # Skip patterns
    skip_patterns = [
        "backup", "tmp", "temp", "_template",
        "sitemap.", "index-backup", "index-working",
        ".ship010.tmp", ".ship", ".tmp"
    ]
    
    if any(pattern in page for pattern in skip_patterns):
        continue
    
    # Skip empty files
    if os.path.getsize(page) == 0:
        continue
    
    valid_pages.append(page)

valid_pages.sort()

print(f"📄 Found {len(valid_pages)} valid pages")

# Generate sitemap.xml
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    
    for page in valid_pages:
        # Get last modified date
        mtime = os.path.getmtime(page)
        lastmod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        
        # Priority logic
        priority = "0.7"
        changefreq = "monthly"
        
        if page in ["index.html", "-hub.html"]:
            priority = "1.0"
            changefreq = "weekly"
        elif "who-do-i-call" in page or "-cost" in page:
            priority = "0.9"
            changefreq = "weekly"
        elif "san-diego" in page:
            priority = "0.8"
            changefreq = "monthly"
        
        f.write(f'  <url>\n')
        f.write(f'    <loc>https://sideguysolutions.com/{page}</loc>\n')
        f.write(f'    <lastmod>{lastmod}</lastmod>\n')
        f.write(f'    <changefreq>{changefreq}</changefreq>\n')
        f.write(f'    <priority>{priority}</priority>\n')
        f.write(f'  </url>\n')
    
    f.write('</urlset>\n')

print(f"✅ sitemap.xml created with {len(valid_pages)} URLs")

# Generate sitemap.html (human-readable)
with open("sitemap.html", "w", encoding="utf-8") as f:
    f.write('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SideGuy Solutions — All Pages</title>
<style>
body{font-family:system-ui,sans-serif;background:#f7fbff;color:#073044;padding:32px;max-width:1200px;margin:auto}
h1{margin-bottom:6px}
.meta{color:#5e7d8e;margin-bottom:24px;font-size:0.95rem}
.search{margin-bottom:24px}
.search input{width:100%;max-width:400px;padding:10px;border:2px solid #d1e8ed;border-radius:8px;font-size:1rem}
ul{columns:3;column-gap:24px;list-style-type:none;padding:0}
li{margin:6px 0;break-inside:avoid}
a{text-decoration:none;color:#1f7cff;font-size:0.9rem}
a:hover{text-decoration:underline}
.count{font-weight:700;color:#21d3a1}
@media(max-width:900px){ul{columns:2}}
@media(max-width:600px){ul{columns:1}}
</style>
<script>
function filterPages() {
  const query = document.getElementById('search').value.toLowerCase();
  const links = document.querySelectorAll('ul li');
  links.forEach(li => {
    const text = li.textContent.toLowerCase();
    li.style.display = text.includes(query) ? 'list-item' : 'none';
  });
}
</script>
</head>
<body>
<h1>SideGuy Solutions — All Pages</h1>
<div class="meta">
Total: <span class="count">''' + str(len(valid_pages)) + ''' pages</span><br>
Last updated: ''' + datetime.now().strftime("%B %d, %Y %H:%M") + '''<br>
<a href="/">← Home</a> · <a href="/sitemap.xml">sitemap.xml</a>
</div>
<div class="search">
<input type="text" id="search" placeholder="Search pages..." onkeyup="filterPages()">
</div>
<ul>
''')
    
    for page in valid_pages:
        title = page.replace(".html", "").replace("-", " ").title()
        f.write(f'<li><a href="/{page}">{title}</a></li>\n')
    
    f.write('''</ul>
</body>
</html>''')

print(f"✅ sitemap.html created (searchable index)")
print("")
print("📊 Summary:")
print(f"  - Valid pages: {len(valid_pages)}")
print(f"  - Backups excluded: ✓")
print(f"  - Templates excluded: ✓")
print(f"  - Empty files excluded: ✓")
print("")
print("✅ Sitemap generation complete!")
