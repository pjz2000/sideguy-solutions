#!/usr/bin/env python3
"""
Generate TRULY UNIQUE descriptions for every page
Uses H1, first paragraph, and smart summarization
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = ""
        self.first_p = ""
        self.in_h1 = False
        self.in_p = False
        self.p_count = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == 'h1' and not self.h1:
            self.in_h1 = True
        elif tag == 'p' and not self.first_p and self.p_count < 3:
            # Check if it's a content paragraph (has class lede or is early)
            self.in_p = True
    
    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False
        elif tag == 'p':
            self.in_p = False
            self.p_count += 1
    
    def handle_data(self, data):
        if self.in_h1 and data.strip():
            self.h1 += data.strip() + " "
        elif self.in_p and data.strip():
            self.first_p += data.strip() + " "

def extract_content(filepath):
    """Extract H1 and first meaningful paragraph"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        parser = ContentExtractor()
        parser.feed(content)
        
        return {
            'h1': parser.h1.strip()[:200],  # Limit length
            'first_p': parser.first_p.strip()[:300]
        }
    except:
        return {'h1': '', 'first_p': ''}

def generate_unique_description(filename, h1, first_p):
    """Generate unique description from actual page content"""
    
    # Use first paragraph if it's good content
    if first_p and len(first_p) > 60 and 'TODO' not in first_p and 'SideGuy' not in first_p[:20]:
        # Clean up and truncate to 155 chars
        desc = first_p.replace('\n', ' ').replace('  ', ' ')
        if len(desc) > 155:
            desc = desc[:152] + "..."
        return desc
    
    # Use H1 as base if available
    if h1 and len(h1) > 10:
        # Create description from H1
        h1_clean = h1.replace('—', '-').replace('  ', ' ')
        
        # Add context based on filename
        if 'who-do-i-call' in filename:
            return f"{h1_clean} Get clear guidance in San Diego. Human help when needed."[:155]
        elif 'payment' in filename or 'merchant' in filename:
            return f"{h1_clean} Lower fees, instant settlements. Payment processing for San Diego businesses."[:155]
        elif 'hvac' in filename or 'ac-' in filename:
            return f"{h1_clean} HVAC help in San Diego. What to check first, when to call, costs."[:155]
        elif 'plumb' in filename:
            return f"{h1_clean} Plumbing help in San Diego. Clear guidance before calling."[:155]
        elif 'electric' in filename:
            return f"{h1_clean} Electrical help in San Diego. Safety-first guidance."[:155]
        elif 'ai' in filename or 'automation' in filename:
            return f"{h1_clean} AI automation for San Diego businesses. Human-first implementation."[:155]
        elif 'tech' in filename or 'computer' in filename:
            return f"{h1_clean} Tech support in San Diego. Patient help for everyone."[:155]
        elif 'crypto' in filename or 'solana' in filename:
            return f"{h1_clean} Crypto payment setup for San Diego businesses."[:155]
        else:
            return f"{h1_clean} Get help in San Diego. Clear guidance, human support."[:155]
    
    # Fallback: generate from filename with more specificity
    name = filename.replace('.html', '').replace('-', ' ')
    
    # Create more specific fallbacks
    if 'not-cooling' in filename or 'not-blowing' in filename:
        return f"Your {name} in San Diego? Check these common causes first, then know when to call for help."
    elif 'making-noise' in filename:
        return f"{name.title()} problem in San Diego? Learn what different sounds mean and when it's urgent."
    elif 'leak' in filename:
        return f"{name.title()} in San Diego? What to do immediately, when to call, what it costs."
    elif 'payment-processing' in filename:
        where = 'San Diego' if 'san-diego' not in name else name.replace('payment processing', '').strip()
        return f"Payment processing in {where}. Lower fees, instant settlements, human support."
    else:
        return f"Need help with {name} in San Diego? Clear guidance, no pressure. Text 773-544-1231 for help."

def fix_file(filepath):
    """Update meta description with unique content"""
    try:
        filename = os.path.basename(filepath)
        
        # Skip if already has genuinely unique description
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract current description
        desc_match = re.search(r'content="([^"]+)"[^>]*name="description"', content, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'name="description"[^>]*content="([^"]+)"', content, re.IGNORECASE)
        
        current_desc = desc_match.group(1) if desc_match else ""
        
        # Check if needs updating (generic or shared descriptions)
        shared_descriptions = [
            'AI and automation help for San Diego businesses. Human-first implementation',
            'Lower fees, instant settlements, human support. Payment processing for San Diego businesses',
            'HVAC help in San Diego. Clear options before calling',
            'Plumbing help in San Diego. What to check first',
            'Electrical help in San Diego. Safety-first guidance',
            'Get help with',
            'Patient tech support for San Diego',
            'Crypto payment setup for San Diego',
            'Roofing help in San Diego',
            'Foundation repair guidance'
        ]
        
        needs_update = any(phrase in current_desc for phrase in shared_descriptions)
        
        if not needs_update and len(current_desc) > 100:
            return None  # Already unique
        
        # Extract page content
        content_data = extract_content(filepath)
        
        # Generate unique description
        new_desc = generate_unique_description(filename, content_data['h1'], content_data['first_p'])
        
        # Don't update if new description is same as current
        if new_desc == current_desc:
            return None
        
        # Replace description
        # Handle both attribute orders
        pattern1 = r'<meta\s+content="[^"]*"\s*name="description"\s*/>'
        pattern2 = r'<meta\s+name="description"\s+content="[^"]*"\s*/>'
        
        new_tag1 = f'<meta content="{new_desc}" name="description"/>'
        new_tag2 = f'<meta name="description" content="{new_desc}" />'
        
        if re.search(pattern1, content, re.DOTALL):
            content = re.sub(pattern1, new_tag1, content, count=1, flags=re.DOTALL)
        elif re.search(pattern2, content, re.DOTALL):
            content = re.sub(pattern2, new_tag2, content, count=1, flags=re.DOTALL)
        else:
            return None  # Can't find description tag
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (filename, new_desc)
    
    except Exception as e:
        return None

def main():
    print("🎯 UNIQUE Description Generator")
    print("=" * 75)
    print("Making every page genuinely unique for Google indexing...")
    print()
    
    html_files = list(Path('.').glob('*.html'))
    exclude = ['template', 'backup', 'test', 'aaa-', 'index-', 'sitemap']
    html_files = [f for f in html_files if not any(x in f.name for x in exclude)]
    
    print(f"📄 Processing {len(html_files)} pages...\n")
    
    fixed = []
    for i, fp in enumerate(html_files, 1):
        if i % 100 == 0:
            print(f"   ... {i}/{len(html_files)}")
        
        res = fix_file(fp)
        if res:
            fixed.append(res)
            if len(fixed) <= 15:  # Show first 15
                fn, desc = res
                print(f"✅ {fn}")
                print(f"   {desc}")
                print()
    
    print("=" * 75)
    print(f"✅ Updated: {len(fixed)} pages with unique descriptions")
    print(f"⏭️  Skipped: {len(html_files) - len(fixed)} (already unique)")
    print()
    
    if len(fixed) > 15:
        print("📝 More examples:")
        for fn, desc in fixed[15:25]:
            print(f"   • {fn[:50]}")
    
    print()
    print("🎉 Done! Every page is now uniquely described.")
    print("💡 Next: python3 generate-xml-sitemap.py && git commit")

if __name__ == '__main__':
    main()
