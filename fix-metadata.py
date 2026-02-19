#!/usr/bin/env python3
"""
SideGuy Metadata Fixer
Generates unique, descriptive titles and meta descriptions for all pages.
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

class MetadataExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1 = ""
        self.first_p = ""
        self.in_title = False
        self.in_h1 = False
        self.in_p = False
        self.p_count = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'h1':
            self.in_h1 = True
        elif tag == 'p' and not self.first_p:
            self.in_p = True
        elif tag == 'meta':
            attrs_dict = dict(attrs)
            if attrs_dict.get('name') == 'description':
                self.description = attrs_dict.get('content', '')
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'h1':
            self.in_h1 = False
        elif tag == 'p':
            self.in_p = False
            self.p_count += 1
    
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif self.in_h1:
            self.h1 += data
        elif self.in_p and self.p_count == 0:
            self.first_p += data

def extract_page_data(html_content):
    """Extract title, description, h1, and first paragraph from HTML"""
    parser = MetadataExtractor()
    parser.feed(html_content)
    return {
        'title': parser.title.strip(),
        'description': parser.description.strip(),
        'h1': parser.h1.strip(),
        'first_p': parser.first_p.strip()
    }

def generate_metadata(filename, page_data):
    """Generate unique title and description based on page content and filename"""
    
    # Extract topic from filename
    name = filename.replace('.html', '').replace('-', ' ')
    
    # Use H1 if it's not generic
    h1 = page_data['h1']
    generic_h1s = ['who do i call', 'sideguy solutions', 'help', 'home']
    
    if h1 and not any(g in h1.lower() for g in generic_h1s):
        base_title = h1
    else:
        # Build from filename
        base_title = name.title()
    
    # Generate SEO title (max 60 chars)
    if 'san diego' not in base_title.lower():
        title = f"{base_title} · San Diego · SideGuy"
    else:
        title = f"{base_title} · SideGuy"
    
    # Trim if too long
    if len(title) > 60:
        title = title[:57] + "..."
    
    # Generate meta description (max 155 chars)
    first_p = page_data['first_p']
    
    # Craft description from content or filename
    if first_p and len(first_p) > 30 and 'TODO' not in first_p:
        description = first_p[:152] + "..." if len(first_p) > 155 else first_p
    else:
        # Build descriptive content from filename/h1
        if 'who-do-i-call' in filename:
            topic = name.replace('who do i call', '').replace('for', '').strip()
            description = f"Get clear guidance on {topic} in San Diego. Human help when you need it. Text 773-544-1231."
        elif 'payment-processing' in filename:
            description = "Lower fees, instant settlements, human support. Payment processing for San Diego businesses. Text 773-544-1231."
        elif 'hvac' in filename or 'ac-' in filename or 'heater' in filename:
            description = "HVAC help in San Diego. Clear options before you call anyone. Human guidance layer for home service decisions."
        elif 'plumb' in filename or 'leak' in filename or 'water' in filename:
            description = "Plumbing help in San Diego. What to check first, when to call, what it costs. Clarity before calling."
        elif 'electric' in filename or 'outlet' in filename or 'breaker' in filename:
            description = "Electrical help in San Diego. Safety-first guidance before calling an electrician. Text 773-544-1231."
        elif 'ai-' in filename or 'automation' in filename:
            description = "AI and automation help for San Diego businesses. Human-first implementation. No hype, just what works."
        elif 'crypto' in filename or 'solana' in filename:
            description = "Crypto payment setup for San Diego businesses. Solana Pay integration, wallet setup, compliance help."
        elif 'tech-help' in filename or 'tech-support' in filename:
            description = "Patient tech support for San Diego. No judgment, clear explanations. Help for non-technical people."
        else:
            description = f"Get help with {name} in San Diego. Clear guidance, human support when needed. SideGuy Solutions."
    
    return title, description

def fix_metadata_in_file(filepath):
    """Update title and meta description in HTML file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract current data
        page_data = extract_page_data(content)
        filename = os.path.basename(filepath)
        
        # Check if needs fixing - look for generic descriptions
        generic_phrases = [
            'Something breaks. Something stops working',
            'SideGuy is a human guidance layer for San Diego operators',
            'Broken HTML index snapshot'
        ]
        
        needs_fix = False
        if not page_data['description'] or any(phrase in page_data['description'] for phrase in generic_phrases):
            needs_fix = True
        elif len(page_data['description']) < 30:  # Too short
            needs_fix = True
        
        if not needs_fix:
            return None  # Already has unique description
        
        # Generate new metadata
        new_title, new_description = generate_metadata(filename, page_data)
        
        # Replace title
        title_pattern = r'<title>.*?</title>'
        new_title_tag = f'<title>{new_title}</title>'
        content = re.sub(title_pattern, new_title_tag, content, count=1, flags=re.DOTALL)
        
        # Replace meta description
        desc_pattern = r'<meta name="description" content=".*?" />'
        new_desc_tag = f'<meta name="description" content="{new_description}" />'
        content = re.sub(desc_pattern, new_desc_tag, content, count=1, flags=re.DOTALL)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (filename, new_title, new_description)
    
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return None

def main():
    """Fix metadata for all HTML pages in root directory"""
    
    print("🔧 SideGuy Metadata Fixer")
    print("=" * 60)
    
    # Get all HTML files in root
    html_files = list(Path('.').glob('*.html'))
    
    # Filter out test/backup files
    html_files = [f for f in html_files if not any(x in f.name for x in ['test', 'backup', 'template', 'aaa-'])]
    
    print(f"📄 Found {len(html_files)} HTML pages to process\n")
    
    fixed_count = 0
    skipped_count = 0
    
    for filepath in html_files:
        result = fix_metadata_in_file(filepath)
        if result:
            filename, title, desc = result
            fixed_count += 1
            if fixed_count <= 10:  # Show first 10
                print(f"✅ {filename}")
                print(f"   Title: {title}")
                print(f"   Desc:  {desc[:80]}...")
                print()
        else:
            skipped_count += 1
    
    print("=" * 60)
    print(f"✅ Fixed: {fixed_count} pages")
    print(f"⏭️  Skipped (already unique): {skipped_count} pages")
    print(f"📊 Total: {len(html_files)} pages")
    print("\n🎉 Metadata fix complete!")

if __name__ == '__main__':
    main()
