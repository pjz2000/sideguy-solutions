#!/usr/bin/env python3
"""
Direct metadata fixer using file replacement
"""

import os
import re
from pathlib import Path

def generate_description(filename):
    """Generate description based on filename"""
    
    name = filename.replace('.html', '').replace('-', ' ')
    
    # Category-based descriptions
    if 'who-do-i-call' in filename:
        topic = name.replace('who do i call', '').replace('for', '').strip()
        return f"Get clear guidance on {topic} in San Diego. Human help when needed. Text 773-544-1231."
    
    if 'payment' in filename or 'merchant' in filename:
        return "Lower fees, instant settlements, human support. Payment processing for San Diego businesses."
    
    if 'hvac' in filename or 'ac-' in filename or 'heater' in filename:
        return "HVAC help in San Diego. Clear options before calling. Understand the problem first. No pressure."
    
    if 'plumb' in filename or 'leak' in filename or 'drain' in filename or 'pipe' in filename or 'water' in filename and 'hot' in filename:
        return "Plumbing help in San Diego. What to check first, when to call, what it costs. Clear guidance."
    
    if 'electric' in filename or 'outlet' in filename or 'breaker' in filename or 'light' in filename:
        return "Electrical help in San Diego. Safety-first guidance before calling an electrician."
    
    if 'roof' in filename:
        return "Roofing help in San Diego. When to repair vs replace, cost guidance, who to call. Clear info."
    
    if 'foundation' in filename:
        return "Foundation repair guidance in San Diego. What to look for, when it's urgent, cost estimates."
    
    if 'ai' in filename or 'automat' in filename:
        return "AI and automation help for San Diego businesses. Human-first implementation. No hype."
    
    if 'crypto' in filename or 'solana' in filename:
        return "Crypto payment setup for San Diego businesses. Solana Pay integration, wallet setup help."
    
    if 'tech' in filename or 'computer' in filename:
        return "Patient tech support for San Diego. No judgment, clear explanations. Help for everyone."
    
    # Default
    return f"Get help with {name} in San Diego. Clear guidance, human support when needed."

def fix_file(filepath):
    """Replace generic description with unique one"""
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if has generic description
        generic_patterns = [
            'Something breaks. Something stops working',
            'SideGuy is a human guidance layer for San Diego operators',
        ]
        
        has_generic = any(pattern in content for pattern in generic_patterns)
        
        if not has_generic:
            return None  # Already unique
        
        filename = os.path.basename(filepath)
        new_desc = generate_description(filename)
        
        # Find and replace the entire meta description tag
        # Handle multi-line descriptions
        pattern = r'<meta[^>]*name="description"[^>]*content="[^"]*"[^>]*/>'
        if not re.search(pattern, content, re.DOTALL):
            # Try alternate attribute order
            pattern = r'<meta[^>]*content="[^"]*"[^>]*name="description"[^>]*/>'
        
        if re.search(pattern, content, re.DOTALL):
            new_tag = f'<meta name="description" content="{new_desc}" />'
            content = re.sub(pattern, new_tag, content, count=1, flags=re.DOTALL)
        else:
            return None  # Couldn't find tag
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (filename, new_desc)
    
    except Exception as e:
        print(f"❌ Error: {filepath}: {e}")
        return None

def main():
    print("🔧 Direct Metadata Fixer (Regex-based)")
    print("=" * 70)
    
    html_files = list(Path('.').glob('*.html'))
    exclude = ['test', 'backup', 'template', 'aaa-', 'index-']
    html_files = [f for f in html_files if not any(x in f.name for x in exclude)]
    
    print(f"📄 Processing {len(html_files)} pages...\n")
    
    fixed = []
    for i, filepath in enumerate(html_files, 1):
        if i % 100 == 0:
            print(f"   ... {i}/{len(html_files)}")
        
        result = fix_file(filepath)
        if result:
            fixed.append(result)
            if len(fixed) <= 10:
                fn, desc = result
                print(f"✅ {fn}")
                print(f"   {desc}")
                print()
    
    print("=" * 70)
    print(f"✅ Fixed: {len(fixed)} pages")
    print(f"⏭️  Skipped: {len(html_files) - len(fixed)} pages")
    print("\n🎉 Done! Run 'python3 generate-xml-sitemap.py' next")

if __name__ == '__main__':
    main()
