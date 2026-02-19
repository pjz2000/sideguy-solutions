#!/usr/bin/env python3
"""
Robust Metadata Fixer for SideGuy
Handles multi-line descriptions and generates unique content
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def generate_description(filename, h1_text="", first_paragraph=""):
    """Generate SEO-optimized description based on page context"""
    
    name = filename.replace('.html', '').replace('-', ' ')
    
    # Use first paragraph if it's good
    if first_paragraph and len(first_paragraph) > 40 and 'TODO' not in first_paragraph:
        desc = first_paragraph[:152] + "..." if len(first_paragraph) > 155 else first_paragraph
        return desc
    
    # Category-based descriptions
    if 'who-do-i-call' in filename:
        topic = name.replace('who do i call', '').replace('for', '').strip()
        return f"Get clear guidance on {topic} in San Diego. Human help when you need it. Text 773-544-1231."
    
    if 'payment-processing' in filename or 'merchant' in filename:
        return "Lower fees, instant settlements, human support. Payment processing for San Diego businesses."
    
    if 'hvac' in filename or 'ac-' in filename or 'heater' in filename or 'air-condition' in filename:
        return "HVAC help in San Diego. Clear options before you call anyone. Understand your problem first."
    
    if 'plumb' in filename or 'leak' in filename or 'drain' in filename or 'pipe' in filename:
        return "Plumbing help in San Diego. What to check first, when to call, what it costs. Clarity before calling."
    
    if 'electric' in filename or 'outlet' in filename or 'breaker' in filename or 'light' in filename:
        return "Electrical help in San Diego. Safety-first guidance before calling an electrician."
    
    if 'roof' in filename:
        return "Roofing help in San Diego. When to repair vs replace, what it costs, who to call. Clear guidance."
    
    if 'foundation' in filename:
        return "Foundation repair guidance in San Diego. What to look for, when it's urgent, cost estimates."
    
    if 'ai-' in filename or 'automation' in filename:
        return "AI and automation help for San Diego businesses. Human-first implementation. No hype, just what works."
    
    if 'crypto' in filename or 'solana' in filename:
        return "Crypto payment setup for San Diego businesses. Solana Pay integration, wallet setup, compliance help."
    
    if 'tech-help' in filename or 'tech-support' in filename or 'computer' in filename:
        return "Patient tech support for San Diego. No judgment, clear explanations. Help for non-technical people."
    
    # Default fallback
    return f"Get help with {name} in San Diego. Clear guidance, human support when needed. SideGuy Solutions."

def fix_page(filepath):
    """Fix metadata in a single page"""
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        filename = os.path.basename(filepath)
        
        # Get current description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        current_desc = desc_tag.get('content', '') if desc_tag else ''
        
        # Check if needs fixing
        generic_phrases = [
            'Something breaks. Something stops working',
            'SideGuy is a human guidance layer for San Diego operators',
            'Broken HTML index snapshot'
        ]
        
        needs_fix = False
        if not current_desc:
            needs_fix = True
        elif any(phrase in current_desc for phrase in generic_phrases):
            needs_fix = True
        elif len(current_desc) < 30:
            needs_fix = True
        
        if not needs_fix:
            return None  # Already good
        
        # Extract context
        h1 = soup.find('h1')
        h1_text = h1.get_text().strip() if h1 else ''
        
        first_p = soup.find('p', class_='lede') or soup.find('p')
        first_p_text = first_p.get_text().strip() if first_p else ''
        
        # Generate new description
        new_description = generate_description(filename, h1_text, first_p_text)
        
        # Update or create description tag
        if desc_tag:
            desc_tag['content'] = new_description
        else:
            # Insert after title
            title_tag = soup.find('title')
            if title_tag:
                new_desc_tag = soup.new_tag('meta', attrs={'name': 'description', 'content': new_description})
                title_tag.insert_after(new_desc_tag)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return (filename, new_description)
    
    except Exception as e:
        print(f"❌ Error: {filepath}: {e}")
        return None

def main():
    print("🔧 Robust SideGuy Metadata Fixer")
    print("=" * 70)
    
    # Get all HTML files in root
    html_files = list(Path('.').glob('*.html'))
    
    # Filter out test/backup/template files
    exclude_patterns = ['test', 'backup', 'template', 'aaa-', 'index-']
    html_files = [f for f in html_files if not any(x in f.name for x in exclude_patterns)]
    
    print(f"📄 Processing {len(html_files)} pages...\n")
    
    fixed = []
    skipped = 0
    
    for i, filepath in enumerate(html_files, 1):
        if i % 100 == 0:
            print(f"   ... processed {i}/{len(html_files)} pages")
        
        result = fix_page(filepath)
        if result:
            fixed.append(result)
            if len(fixed) <= 10:  # Show first 10
                filename, desc = result
                print(f"✅ {filename}")
                print(f"   {desc[:75]}...")
                print()
        else:
            skipped += 1
    
    print("=" * 70)
    print(f"✅ Fixed: {len(fixed)} pages")
    print(f"⏭️  Skipped (already unique): {skipped} pages")
    print(f"📊 Total: {len(html_files)} pages")
    
    if len(fixed) > 10:
        print(f"\n📝 Sample of pages fixed:")
        for filename, desc in fixed[10:20]:
            print(f"   • {filename}")
    
    print("\n🎉 Metadata fix complete!")
    print("\n💡 Next step: Run 'python3 generate-xml-sitemap.py' to update sitemap")

if __name__ == '__main__':
    main()
