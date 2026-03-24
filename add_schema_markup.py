#!/usr/bin/env python3
"""
SIDEGUY SCHEMA MARKUP GENERATOR v1
Adds JSON-LD structured data for SEO
"""

import os, glob, re, json
from datetime import datetime

PROJECT_ROOT = "/workspaces/sideguy-solutions"
os.chdir(PROJECT_ROOT)

print("📊 Adding schema markup to pages...")

def extract_title(content):
    """Extract page title from HTML"""
    match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    return match.group(1) if match else "SideGuy Solutions"

def extract_description(content):
    """Extract meta description"""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content, re.IGNORECASE)
    return match.group(1) if match else ""

def generate_article_schema(page, title, description):
    """Generate Article schema for content pages"""
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "author": {
            "@type": "Organization",
            "name": "SideGuy Solutions"
        },
        "publisher": {
            "@type": "Organization",
            "name": "SideGuy Solutions",
            "logo": {
                "@type": "ImageObject",
                "url": "https://sideguysolutions.com/og-preview.png"
            }
        },
        "datePublished": datetime.now().strftime("%Y-%m-%d"),
        "dateModified": datetime.now().strftime("%Y-%m-%d")
    }
    return schema

def generate_faq_schema(page_content):
    """Generate FAQ schema if page has Q&A patterns"""
    # Look for question patterns in content
    questions = re.findall(r'<h[23]>([^<]*\?[^<]*)</h[23]>', page_content, re.IGNORECASE)
    
    if len(questions) < 2:
        return None
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": []
    }
    
    for question in questions[:5]:  # Limit to 5 questions
        # Find next paragraph as answer (simplified)
        answer_match = re.search(rf'{re.escape(question)}.*?<p>(.*?)</p>', page_content, re.DOTALL | re.IGNORECASE)
        answer = answer_match.group(1) if answer_match else "See page for details."
        
        # Clean HTML tags from answer
        answer_clean = re.sub(r'<[^>]+>', '', answer).strip()[:300]
        
        schema["mainEntity"].append({
            "@type": "Question",
            "name": question.strip(),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer_clean
            }
        })
    
    return schema if len(schema["mainEntity"]) > 0 else None

def generate_breadcrumb_schema(page):
    """Generate breadcrumb navigation schema"""
    slug = page.replace(".html", "")
    parts = slug.split("-")
    
    items = [
        {
            "@type": "ListItem",
            "position": 1,
"name": "Home",
            "item": "https://sideguysolutions.com"
        }
    ]
    
    # Add category if detectable
    if "who-do-i-call" in slug:
        items.append({
            "@type": "ListItem",
            "position": 2,
            "name": "Decision Guides",
            "item": "https://sideguysolutions.com/#guides"
        })
    elif "-cost" in slug or "pricing" in slug:
        items.append({
            "@type": "ListItem",
            "position": 2,
            "name": "Cost Guides",
            "item": "https://sideguysolutions.com/#costs"
        })
    elif "ai-" in slug or "automation" in slug:
        items.append({
            "@type": "ListItem",
            "position": 2,
            "name": "AI & Automation",
            "item": "https://sideguysolutions.com/ai-automation-hub.html"
        })
    
    # Add current page
    items.append({
        "@type": "ListItem",
        "position": len(items) + 1,
        "name": extract_title(""),  # Will be filled from actual content
        "item": f"https://sideguysolutions.com/{page}"
    })
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    
    return schema

def add_schemas_to_page(filepath):
    """Add schema markup to a page if missing"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Skip if already has schema markup
    if 'application/ld+json' in content:
        return False
    
    # Skip if malformed
    if '</head>' not in content:
        return False
    
    page = os.path.basename(filepath)
    title = extract_title(content)
    description = extract_description(content)
    
    # Generate schemas
    schemas = []
    
    # Article schema (most pages)
    schemas.append(generate_article_schema(page, title, description))
    
    # FAQ schema (if applicable)
    faq = generate_faq_schema(content)
    if faq:
        schemas.append(faq)
    
    # Breadcrumb schema
    schemas.append(generate_breadcrumb_schema(page))
    
    # Format schema blocks
    schema_html = "\n"
    for schema in schemas:
        schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
        schema_html += f'<script type="application/ld+json">\n{schema_json}\n</script>\n'
    
    # Inject before </head>
    new_content = content.replace('</head>', f'{schema_html}</head>', 1)
    
    # Write back
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True

# Test on sample pages first
sample_pages = glob.glob("who-do-i-call-*.html")[:10]

print(f"🧪 Testing on {len(sample_pages)} sample pages...")

updated = 0
for page_path in sample_pages:
    if add_schemas_to_page(page_path):
        updated += 1
        print(f"  ✅ {os.path.basename(page_path)}")

print(f"\n✅ Added schema markup to {updated} pages")
print(f"\nTest complete! Review updated pages before full deployment.")
print(f"\nTo deploy to all pages, modify this script to process all valid_pages.")
