#!/usr/bin/env python3
"""
Multiline-safe metadata fixer
"""
import os
import re
from pathlib import Path

def generate_desc(filename):
    """Generate category-based description"""
    if 'hvac' in filename or 'ac-' in filename or 'heater' in filename:
        return "HVAC help in San Diego. Clear options before calling. Understand the problem first."
    elif 'plumb' in filename or 'leak' in filename or 'drain' in filename or 'pipe' in filename:
        return "Plumbing help in San Diego. What to check first, when to call, what it costs."
    elif 'electric' in filename or 'outlet' in filename or 'breaker' in filename or 'light' in filename:
        return "Electrical help in San Diego. Safety-first guidance before calling an electrician."
    elif 'payment' in filename or 'merchant' in filename:
        return "Lower fees, instant settlements, human support. Payment processing for San Diego businesses."
    elif 'roof' in filename:
        return "Roofing help in San Diego. When to repair vs replace, cost guidance, who to call."
    elif 'foundation' in filename:
        return "Foundation repair guidance in San Diego. What to look for, when it's urgent, costs."
    elif 'ai' in filename or 'automat' in filename:
        return "AI and automation help for San Diego businesses. Human-first implementation. No hype."
    elif 'crypto' in filename or 'solana' in filename:
        return "Crypto payment setup for San Diego businesses. Solana Pay integration, wallet setup."
    elif 'tech' in filename or 'computer' in filename:
        return "Patient tech support for San Diego. No judgment, clear explanations. Help for everyone."
    elif 'who-do-i-call' in filename:
        topic = filename.replace('who-do-i-call-for-', '').replace('.html', '').replace('-', ' ')
        return f"Get clear guidance on {topic} in San Diego. Human help when needed."
    else:
        topic = filename.replace('.html', '').replace('-', ' ')
        return f"Get help with {topic} in San Diego. Clear guidance, human support when needed."

def fix_file(filepath):
    """Fix meta description in file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if needs fixing
        if 'Something breaks. Something stops working' not in content:
            return None
        
        filename = os.path.basename(filepath)
        new_desc = generate_desc(filename)
        
        # Pattern handles both attribute orders and multiline content
        # Pattern 1: content="..." name="description"
        pattern1 = r'<meta\s+content="[^"]*?"\s*name="description"\s*/>'
        if re.search(pattern1, content, re.DOTALL):
            new_tag = f'<meta content="{new_desc}" name="description"/>'
            content = re.sub(pattern1, new_tag, content, count=1, flags=re.DOTALL)
        else:
            # Pattern 2: name="description" content="..."
            pattern2 = r'<meta\s+name="description"\s+content="[^"]*?"\s*/>'
            if re.search(pattern2, content, re.DOTALL):
                new_tag = f'<meta name="description" content="{new_desc}" />'
                content = re.sub(pattern2, new_tag, content, count=1, flags=re.DOTALL)
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (filename, new_desc)
    
    except Exception as e:
        print(f"❌ Error: {filepath}: {e}")
        return None

def main():
    print("🔧 Multiline-Safe Metadata Fixer")
    print("=" * 70)
    
    html_files = list(Path('.').glob('*.html'))
    exclude = ['template', 'backup', 'test', 'aaa-', 'index-']
    html_files = [f for f in html_files if not any(x in f.name for x in exclude)]
    
    print(f"📄 Processing {len(html_files)} pages...\n")
    
    fixed = []
    for i, fp in enumerate(html_files, 1):
        if i % 100 == 0:
            print(f"   ... {i}/{len(html_files)}")
        
        res = fix_file(fp)
        if res:
            fixed.append(res)
            if len(fixed) <= 10:
                print(f"✅ {res[0]}")
                print(f"   {res[1][:75]}...")
                print()
    
    print("=" * 70)
    print(f"✅ Fixed: {len(fixed)} pages")
    print(f"⏭️  Skipped: {len(html_files) - len(fixed)} pages")
    print("\n🎉 Done! Next: python3 metadata-audit.py")

if __name__ == '__main__':
    main()
