#!/usr/bin/env python3
"""
SideGuy Solutions — XML Sitemap Generator
Generates proper XML sitemap for Google Search Console
"""
import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

def generate_sitemap():
    """Generate XML sitemap from HTML files"""
    root_dir = Path('/workspaces/sideguy-solutions')
    html_files = sorted(root_dir.glob('*.html'))
    
    # Exclude system/utility files
    exclude = {'sitemap.html', 'master-layout.html', 'master.html', 'sideguy-shell.html'}
    html_files = [f for f in html_files if f.name not in exclude and not f.name.startswith('.')]
    
    # Create XML structure
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    base_url = 'https://sideguy.solutions'
    lastmod = datetime.now().strftime('%Y-%m-%d')
    
    for filepath in html_files:
        url_elem = ET.SubElement(urlset, 'url')
        
        # Location
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = f"{base_url}/{filepath.name}"
        
        # Last modified
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = lastmod
        
        # Change frequency (monthly for most pages)
        changefreq = ET.SubElement(url_elem, 'changefreq')
        if filepath.name == 'index.html':
            changefreq.text = 'daily'
        elif 'payment' in filepath.name or 'solana' in filepath.name:
            changefreq.text = 'weekly'
        else:
            changefreq.text = 'monthly'
        
        # Priority
        priority = ET.SubElement(url_elem, 'priority')
        if filepath.name == 'index.html':
            priority.text = '1.0'
        elif 'who-do-i-call' in filepath.name:
            priority.text = '0.9'
        elif 'san-diego' in filepath.name:
            priority.text = '0.8'
        else:
            priority.text = '0.7'
    
    # Format and save
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space='  ')
    
    sitemap_path = root_dir / 'sitemap.xml'
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Generated sitemap.xml with {len(html_files)} URLs")
    print(f"📍 Location: {sitemap_path}")
    
    # Generate sitemap index if needed
    generate_sitemap_index(root_dir)

def generate_sitemap_index(root_dir):
    """Generate sitemap index file"""
    sitemapindex = ET.Element('sitemapindex', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    sitemap = ET.SubElement(sitemapindex, 'sitemap')
    loc = ET.SubElement(sitemap, 'loc')
    loc.text = 'https://sideguy.solutions/sitemap.xml'
    
    lastmod = ET.SubElement(sitemap, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    tree = ET.ElementTree(sitemapindex)
    ET.indent(tree, space='  ')
    
    index_path = root_dir / 'sitemap-index.xml'
    tree.write(index_path, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Generated sitemap-index.xml")

if __name__ == '__main__':
    generate_sitemap()
