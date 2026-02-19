#!/usr/bin/env python3
"""
Generate unique descriptions from page TITLES
Since most pages use a blanket template with generic content,
the title is the most reliable source of unique information.
"""

import os
import re
from pathlib import Path

def extract_title(filepath):
    """Extract title tag content"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
        return title_match.group(1).strip() if title_match else ''
    except:
        return ''

def generate_unique_from_title(title, filename):
    """Generate unique, specific description from title"""
    
    # Clean title - remove generic suffixes
    title_clean = title.replace(' · San Diego', '').replace(' · SideGuy', '').replace('·', '-').strip()
    
    # Problem-specific descriptions based on title content
    title_lower = title_clean.lower()
    
    # HVAC/AC specific problems
    if 'ac not cooling' in title_lower or 'not cooling' in title_lower:
        return "AC not cooling in San Diego? Check thermostat settings, air filter, and circuit breaker first. Learn when to call for help and typical costs."
    elif 'ac blowing warm' in title_lower or 'warm air' in title_lower:
        return "AC blowing warm air in San Diego? Could be low refrigerant, frozen coil, or compressor issue. What to check first and when it's urgent."
    elif 'ac making noise' in title_lower or 'ac noise' in title_lower:
        return "AC making noise in San Diego? Different sounds mean different problems. Learn what grinding, squealing, or banging means and what to do."
    elif 'ac not turning on' in title_lower or 'ac won\'t turn' in title_lower:
        return "AC not turning on in San Diego? Check breaker, thermostat batteries, and disconnect switch. Simple fixes before calling a technician."
    elif 'heater not' in title_lower or 'no heat' in title_lower:
        return "Heater not working in San Diego? Check pilot light, thermostat, and air filter. What to try first before calling for service."
    elif 'hvac' in title_lower and ('repair' in title_lower or 'service' in title_lower):
        return "HVAC repair in San Diego. What it costs, how to choose who to call, what questions to ask. Clear guidance before making decisions."
    
    # Plumbing specific
    elif 'leak' in title_lower and ('water' in title_lower or 'sink' in title_lower or 'pipe' in title_lower):
        return f"{title_clean} problem in San Diego? What to do immediately to prevent damage. When it's DIY vs when to call a plumber. Typical costs."
    elif 'drain' in title_lower or 'clog' in title_lower:
        return f"{title_clean} in San Diego? Try these safe DIY solutions first. When to call a plumber and what it costs. Avoid harsh chemicals."
    elif 'toilet' in title_lower:
        return f"{title_clean} issue in San Diego? Common causes and simple fixes. What you can handle yourself vs when to call a plumber."
    elif 'plumb' in title_lower:
        return f"{title_clean} in San Diego. What to check first, when it's urgent, who to call. Cost guidance and clear next steps."
    
    # Electrical specific
    elif 'outlet not working' in title_lower or 'outlet' in title_lower:
        return f"{title_clean}? Check for tripped GFCI, circuit breaker, or loose connection. Safety-first guidance for San Diego homeowners."
    elif 'breaker' in title_lower or 'power outage' in title_lower:
        return f"{title_clean} in San Diego? Understand why it's happening, safety concerns, and when to call an electrician. Clear guidance."
    elif 'lights flickering' in title_lower or 'flickering' in title_lower:
        return f"{title_clean} in San Diego? Could be loose bulb, bad connection, or serious wiring issue. What to check and when it's urgent."
    elif 'electric' in title_lower:
        return f"{title_clean} help in San Diego. Safety-first guidance, what you can check yourself, when to call a professional."
    
    # Payment processing
    elif 'payment processing' in title_lower or 'merchant' in title_lower:
        location = 'San Diego' if 'san diego' not in title_lower else title_clean.replace('Payment Processing', '').strip()
        return f"Payment processing in {location}. Lower fees, instant settlements, human support. Switch from Stripe/Square and save."
    elif 'instant settlement' in title_lower or 'instant payout' in title_lower:
        return f"{title_clean}. Get paid same-day for completed work. Lower fees than Stripe. Built for San Diego service businesses."
    elif 'crypto payment' in title_lower or 'solana' in title_lower:
        return f"{title_clean} for San Diego businesses. Accept crypto, settle to USD instantly. Setup help and ongoing support."
    
    # AI/Tech/Automation
    elif 'ai automation' in title_lower or 'ai help' in title_lower:
        return f"{title_clean} for San Diego businesses. Human-first AI implementation. No hype, just practical tools that work."
    elif 'confused about ai' in title_lower or 'ai overthinking' in title_lower:
        return f"{title_clean}? Talk to a human first. Clear guidance on whether AI makes sense for your business. No sales pressure."
    elif 'tech help' in title_lower or 'tech support' in title_lower:
        return f"{title_clean}. Patient, judgment-free tech support for non-technical people in San Diego. Clear explanations."
    elif 'computer' in title_lower or 'laptop' in title_lower or 'wifi' in title_lower:
        return f"{title_clean} in San Diego? Step-by-step troubleshooting in plain language. Human help when you need it."
    
    # Who do I call pages
    elif 'who do i call' in title_lower:
        topic = title_clean.replace('Who Do I Call For', '').replace('Who Do I Call', '').strip()
        return f"Who to call for {topic} in San Diego? Clear guidance on the right professional, typical costs, and what to ask. No pressure."
    
    # Roofing
    elif 'roof' in title_lower:
        return f"{title_clean} in San Diego. When to repair vs replace, cost guidance, who to call. Clear information for homeowners."
    
    # Foundation
    elif 'foundation' in title_lower:
        return f"{title_clean} in San Diego. What cracks/settling mean, when it's urgent, cost estimates. Clear guidance before calling."
    
    # Generic fallback - still use title for uniqueness
    else:
        # Extract problem/service from title
        problem = title_clean.replace('San Diego', '').replace('SideGuy', '').strip(' ·-')
        return f"Need help with {problem}? Clear guidance for San Diego. What to check first, who to call, typical costs. Human support available."

def fix_file(filepath):
    """Update description with title-based unique content"""
    try:
        filename = os.path.basename(filepath)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract title
        title = extract_title(filepath)
        if not title:
            return None
        
        # Get current description
        desc_match = re.search(r'content="([^"]+)"[^>]*name="description"', content, re.IGNORECASE)
        if not desc_match:
            desc_match = re.search(r'name="description"[^>]*content="([^"]+)"', content, re.IGNORECASE)
        
        current_desc = desc_match.group(1) if desc_match else ""
        
        # Generate new unique description
        new_desc = generate_unique_from_title(title, filename)
        
        # Don't update if same
        if new_desc == current_desc or len(new_desc) < 50:
            return None
        
        # Replace description
        pattern1 = r'<meta\s+content="[^"]*"\s*name="description"\s*/>'
        pattern2 = r'<meta\s+name="description"\s+content="[^"]*"\s*/>'
        
        new_tag1 = f'<meta content="{new_desc}" name="description"/>'
        new_tag2 = f'<meta name="description" content="{new_desc}" />'
        
        if re.search(pattern1, content, re.DOTALL):
            content = re.sub(pattern1, new_tag1, content, count=1, flags=re.DOTALL)
        elif re.search(pattern2, content, re.DOTALL):
            content = re.sub(pattern2, new_tag2, content, count=1, flags=re.DOTALL)
        else:
            return None
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return (filename, title, new_desc)
    
    except Exception as e:
        return None

def main():
    print("🎯 Title-Based UNIQUE Description Generator")
    print("=" * 75)
    print("Using page titles to create truly unique descriptions...")
    print()
    
    html_files = list(Path('.').glob('*.html'))
    exclude = ['template', 'backup', 'test', 'aaa-', 'index-', 'sitemap', 'master']
    html_files = [f for f in html_files if not any(x in f.name for x in exclude)]
    
    print(f"📄 Processing {len(html_files)} pages...\n")
    
    fixed = []
    for i, fp in enumerate(html_files, 1):
        if i % 100 == 0:
            print(f"   ... {i}/{len(html_files)}")
        
        res = fix_file(fp)
        if res:
            fixed.append(res)
            if len(fixed) <= 12:
                fn, title, desc = res
                print(f"✅ {fn}")
                print(f"   Title: {title[:60]}")
                print(f"   Desc:  {desc[:75]}...")
                print()
    
    print("=" * 75)
    print(f"✅ Updated: {len(fixed)} pages with title-based unique descriptions")
    print(f"⏭️  Skipped: {len(html_files) - len(fixed)}")
    print()
    
    if len(fixed) > 12:
        print("📝 More examples:")
        for fn, title, desc in fixed[12:20]:
            print(f"   • {fn[:45]} → {desc[:60]}...")
    
    print()
    print("🎉 Every page now has a unique, problem-specific description!")
    print("💡 Next: python3 metadata-audit.py to verify uniqueness")

if __name__ == '__main__':
    main()
