#!/usr/bin/env python3
"""
SIDEGUY CLARITY LAYER BATCH UPGRADER
Safe, human-approved batch deployment of clarity layer to next-best pages
"""

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path("/workspaces/sideguy-solutions")
SWARM_DIR = PROJECT_ROOT / "swarm"
STATE_DIR = SWARM_DIR / "state"
QUEUE_DIR = SWARM_DIR / "queue"
REPORT_FILE = PROJECT_ROOT / "docs" / "decision-report.md"

# Create directories
STATE_DIR.mkdir(parents=True, exist_ok=True)
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

DONE_FILE = STATE_DIR / "clarity-done.txt"
QUEUE_FILE = QUEUE_DIR / "clarity-queue.txt"
LOG_FILE = STATE_DIR / "clarity-log.txt"

# Phone number
PHONE_SMS = "sms:+17735441231"
PHONE_DISPLAY = "773-544-1231"

def log(msg):
    """Append-only log"""
    with open(LOG_FILE, 'a') as f:
        from datetime import datetime
        f.write(f"{datetime.now().isoformat()} | {msg}\n")
    print(f"✓ {msg}")

def get_done_list():
    """Read already-upgraded pages"""
    if not DONE_FILE.exists():
        return set()
    return set(DONE_FILE.read_text().strip().split('\n'))

def mark_done(slug):
    """Mark page as upgraded"""
    with open(DONE_FILE, 'a') as f:
        f.write(f"{slug}\n")

def get_next_batch(size=5):
    """Get next N pages from decision report"""
    if not REPORT_FILE.exists():
        print("❌ No decision report found. Run: python3 _decision_report.py")
        return []
    
    report = REPORT_FILE.read_text()
    done = get_done_list()
    
    # Extract Tier 1 candidates from report
    tier1_match = re.search(r'## Tier 1.*?\n\n(.*?)(?=\n##|$)', report, re.DOTALL)
    if not tier1_match:
        print("❌ No Tier 1 candidates found in report")
        return []
    
    candidates = []
    for line in tier1_match.group(1).split('\n'):
        line = line.strip()
        if not line or line.startswith('**') or line.startswith('##'):
            continue
        
        # Extract filename from markdown link or plain text
        match = re.search(r'\[([^\]]+\.html)\]|\b([a-z0-9-]+\.html)\b', line)
        if match:
            filename = match.group(1) or match.group(2)
            slug = filename.replace('.html', '')
            
            if slug not in done:
                # Extract score
                score_match = re.search(r'\*\*(\d+)\*\*', line)
                score = int(score_match.group(1)) if score_match else 0
                candidates.append((slug, score))
    
    # Sort by score descending, take top N
    candidates.sort(key=lambda x: x[1], reverse=True)
    return [slug for slug, score in candidates[:size]]

def generate_clarity_content(slug, html):
    """Generate clarity layer content for a page based on its existing content"""
    
    # Extract current title
    title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        # Clean up title
        title = re.sub(r'\s*[|·•]\s*SideGuy.*$', '', title, flags=re.IGNORECASE)
        
        # Validate: if title is generic/mismatched, regenerate from slug
        generic_patterns = [
            r'^who do i call',
            r'^sideguy',
            r'^home$',
            r'^untitled',
            r'^page \d+',
        ]
        is_generic = any(re.search(pat, title, re.IGNORECASE) for pat in generic_patterns)
        
        # Also check if title is way too different from slug (template issue)
        slug_words = set(slug.lower().split('-'))
        title_words = set(re.findall(r'\b\w+\b', title.lower()))
        overlap = len(slug_words & title_words) / max(len(slug_words), 1)
        
        if is_generic or overlap < 0.3:
            # Generate from slug instead
            title = slug.replace('-', ' ').title()
            # Fix common words
            title = re.sub(r'\bSan Diego\b', 'San Diego', title, flags=re.IGNORECASE)
            title = re.sub(r'\bHvac\b', 'HVAC', title)
            title = re.sub(r'\bAc\b', 'AC', title)
            title = re.sub(r'\bAi\b', 'AI', title)
    else:
        # Fallback: generate from slug
        title = slug.replace('-', ' ').title()
    
    # Detect vertical/topic
    vertical = "service"
    if any(word in slug.lower() for word in ['hvac', 'ac-', 'furnace', 'heater', 'cooling', 'heating']):
        vertical = "hvac"
        topic_context = "HVAC system"
        decision_context = "repair, replace, or wait"
    elif any(word in slug.lower() for word in ['solar', 'panel', 'energy', 'electric-bill']):
        vertical = "solar"
        topic_context = "solar installation"
        decision_context = "install, wait, or explore alternatives"
    elif any(word in slug.lower() for word in ['stripe', 'payment', 'processor', 'fees']):
        vertical = "payments"
        topic_context = "payment processing"
        decision_context = "switch providers, negotiate, or optimize current setup"
    elif any(word in slug.lower() for word in ['plumb', 'pipe', 'drain', 'water', 'leak']):
        vertical = "plumbing"
        topic_context = "plumbing issue"
        decision_context = "repair, replace, or DIY"
    elif any(word in slug.lower() for word in ['electric', 'wiring', 'circuit', 'breaker']):
        vertical = "electrical"
        topic_context = "electrical work"
        decision_context = "repair, upgrade, or wait"
    else:
        topic_context = "this"
        decision_context = "proceed, wait, or explore alternatives"
    
    # Generate FAQ based on vertical
    if vertical == "hvac":
        faqs = [
            ("How do I know if I need repair or replacement?", 
             "Age matters. If your system is under 10 years, repair usually makes sense. Over 15 years, replacement often saves money long-term. In between, it depends on the specific issue and your budget."),
            ("What should I expect to pay?", 
             "Repairs typically run $150–800. Full replacements start around $5,000 for basic systems. Get 2-3 quotes, and text PJ if they seem wildly different."),
            ("Can I DIY any of this?", 
             "Filter changes and thermostat swaps, yes. Refrigerant work, electrical, or ductwork — no. Those require licensing for safety and warranty reasons.")
        ]
    elif vertical == "solar":
        faqs = [
            ("Is solar actually worth it in San Diego?", 
             "Usually yes — high electricity rates and strong sun make payback periods 6-10 years. But roof condition, shading, and financing terms matter."),
            ("What about the federal tax credit?", 
             "30% federal credit is available through 2032. You need enough tax liability to use it, or you can explore financing options that build it in."),
            ("How do I avoid getting oversold?", 
             "Get your last 12 months of electric bills, calculate your actual usage, and size the system to that — not to some inflated projection.")
        ]
    elif vertical == "payments":
        faqs = [
            ("How much should I be paying in fees?", 
             "For most small businesses: 2.6-2.9% + $0.10-0.30 per transaction is standard for card-present. Online is usually 2.9% + $0.30. Much higher than that, you're likely overpaying."),
            ("Is Stripe always the best option?", 
             "Not always. Stripe is great for online/tech businesses. But if you run high volume in-person transactions, Square or a merchant account might save you money."),
            ("Can I negotiate fees?", 
             "Depends. Stripe's rates are mostly fixed. But if you process $50K+/month, you can often negotiate with dedicated account managers or traditional merchant services.")
        ]
    elif vertical == "plumbing":
        faqs = [
            ("Is this an emergency or can it wait?", 
             "No water, sewage backing up, or major flooding = emergency. Slow drain, dripping faucet, or running toilet = not urgent, but will cost more if ignored."),
            ("What should emergency service cost?", 
             "After-hours plumbing runs $150-300 just to show up, then $100-200/hour. If it can wait until morning, you'll save half."),
            ("How do I know I'm not getting ripped off?", 
             "Get the diagnosis first, then the price. If they quote a huge number without explaining what's broken, get a second opinion.")
        ]
    else:
        faqs = [
            ("What should I do first?", 
             "Get clear on the actual problem. Write down symptoms, when they started, and what you've already tried. That helps any expert give you better guidance."),
            ("How do I know if I'm overpaying?", 
             "Get 2-3 quotes and ask each provider to break down what you're paying for. Big price differences usually mean different scopes of work, not price gouging."),
            ("Can I handle this myself?", 
             "Depends on complexity, risk, and your time. If it's simple and low-risk, DIY saves money. If it's technical or dangerous, hiring a pro is cheaper than fixing your mistakes.")
        ]
    
    # Build the clarity layer HTML
    content = f'''
  <section style="max-width:900px;margin:0 auto;padding:32px 20px;font-family:Inter,Arial,sans-serif;line-height:1.6;color:#0f172a;">

    <!-- SIDEGUY CLARITY LAYER -->
    <div style="background:linear-gradient(135deg,#ecfeff,#f0fdf4);border:1px solid #bae6fd;border-radius:18px;padding:28px 22px;margin-bottom:28px;">
      <p style="margin:0 0 10px 0;font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#0891b2;">
        SideGuy Clarity Layer
      </p>
      <h1 style="margin:0 0 12px 0;font-size:36px;line-height:1.1;">
        {title}
      </h1>
      <p style="margin:0 0 14px 0;font-size:18px;color:#334155;">
        Not sure if you actually need this? Text PJ before you spend money, waste time, or get pushed into the wrong solution.
      </p>
      <a href="{PHONE_SMS}" style="display:inline-block;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:#10b981;color:#ffffff;box-shadow:0 10px 30px rgba(16,185,129,.25);">
        Text PJ
      </a>
    </div>

    <!-- WHAT THEY'RE REALLY ASKING -->
    <div style="margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">What people are really trying to figure out</h2>
      <p style="font-size:17px;color:#334155;">
        Most people searching this are trying to avoid three things:
      </p>
      <ul style="padding-left:22px;color:#334155;font-size:17px;">
        <li>overpaying</li>
        <li>choosing the wrong option</li>
        <li>getting sold something they don't actually need</li>
      </ul>
      <p style="font-size:17px;color:#334155;">
        That's where SideGuy helps. We translate the issue into a clear next move.
      </p>
    </div>

    <!-- QUICK ANSWER -->
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:22px;margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">Quick answer</h2>
      <p style="font-size:17px;color:#334155;">
        When you're deciding about {topic_context}, most people are stuck between {decision_context}. The right choice depends on your specific situation — budget, timeline, and what you're trying to avoid. Text PJ with your details and get a straight answer before committing.
      </p>
    </div>

    <!-- YOU MIGHT NEED THIS IF -->
    <div style="margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">You might need this if…</h2>
      <ul style="padding-left:22px;color:#334155;font-size:17px;">
        <li>You're stuck between two options and need an outside perspective</li>
        <li>Quotes seem high but you're not sure if that's normal</li>
        <li>The problem keeps getting worse and you need to decide now</li>
      </ul>
    </div>

    <!-- YOU PROBABLY DON'T -->
    <div style="margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">You probably don't need help if…</h2>
      <ul style="padding-left:22px;color:#334155;font-size:17px;">
        <li>You've already done this before and know what to expect</li>
        <li>It's a simple, low-risk situation with one obvious solution</li>
        <li>You've gotten 3 similar quotes and they all make sense</li>
      </ul>
    </div>

    <!-- SIDEGUY ANGLE -->
    <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:16px;padding:22px;margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">Why people text SideGuy first</h2>
      <p style="font-size:17px;color:#334155;">
        Most sites either drown you in jargon or push you toward a purchase. SideGuy is built for clarity before cost.
        You get a human-first read on the situation before making a bigger move.
      </p>
    </div>

    <!-- CONTEXTUAL CTA -->
    <div style="margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">Best next step</h2>
      <p style="font-size:17px;color:#334155;">
        Text PJ your situation — what's broken, what quotes you've gotten, and what you're trying to avoid. You'll get a straight answer in minutes, not a sales pitch.
      </p>
      <a href="{PHONE_SMS}" style="display:inline-block;margin-top:10px;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:#0f172a;color:#ffffff;">
        Text PJ Now
      </a>
    </div>

    <!-- FAQ -->
    <div style="margin-bottom:28px;">
      <h2 style="font-size:28px;margin-bottom:12px;">Common questions</h2>
'''
    
    for q, a in faqs:
        content += f'''
      <h3 style="font-size:20px;margin:18px 0 8px 0;">{q}</h3>
      <p style="font-size:17px;color:#334155;">{a}</p>
'''
    
    content += f'''
    </div>

    <!-- BOTTOM CLOSE -->
    <div style="background:linear-gradient(135deg,#0f172a,#1e293b);color:#ffffff;border-radius:18px;padding:24px;">
      <h2 style="font-size:28px;margin-bottom:12px;color:#ffffff;">Clarity before cost</h2>
      <p style="font-size:17px;color:#cbd5e1;margin-bottom:14px;">
        If you're stuck between options, send PJ the details. A quick outside read can save you money, time, and a bad decision.
      </p>
      <a href="{PHONE_SMS}" style="display:inline-block;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:#10b981;color:#ffffff;">
        Text PJ
      </a>
    </div>

  </section>
'''
    
    return content

def process_page(slug):
    """Apply clarity layer to a single page"""
    filepath = PROJECT_ROOT / f"{slug}.html"
    
    if not filepath.exists():
        log(f"SKIP {slug} (file not found)")
        return False
    
    html = filepath.read_text(encoding='utf-8')
    
    # Check if already has clarity layer
    if 'SIDEGUY CLARITY LAYER' in html:
        log(f"SKIP {slug} (already has clarity layer)")
        mark_done(slug)
        return True
    
    # Check for <main> tags
    main_open = re.search(r'<main[^>]*>', html)
    main_close = re.search(r'</main>', html)
    
    if not main_open or not main_close:
        log(f"SKIP {slug} (no <main> tags)")
        return False
    
    # Generate clarity content
    clarity_content = generate_clarity_content(slug, html)
    
    # Replace <main> content
    new_html = (
        html[:main_open.end()] +
        clarity_content +
        html[main_close.start():]
    )
    
    # Write back
    filepath.write_text(new_html, encoding='utf-8')
    mark_done(slug)
    log(f"UPGRADED {slug}")
    return True

def preview_batch(batch):
    """Show what will be upgraded"""
    print("\n" + "="*60)
    print(f"  BATCH PREVIEW: {len(batch)} pages")
    print("="*60)
    for i, slug in enumerate(batch, 1):
        filepath = PROJECT_ROOT / f"{slug}.html"
        status = "✓ exists" if filepath.exists() else "✗ missing"
        print(f"{i:2d}. {slug:50s} {status}")
    print("="*60 + "\n")

def run_batch(size=5, auto_approve=False):
    """Run a batch upgrade"""
    
    print("\n🧠 SIDEGUY CLARITY LAYER BATCH UPGRADER\n")
    
    # Get next batch
    batch = get_next_batch(size)
    
    if not batch:
        print("✅ No more pages to upgrade. All done!")
        return
    
    # Preview
    preview_batch(batch)
    
    # Require approval unless auto
    if not auto_approve:
        response = input(f"Upgrade these {len(batch)} pages? [y/N]: ").strip().lower()
        if response != 'y':
            print("❌ Cancelled.")
            return
    
    # Process
    print("\n⚡ Processing...\n")
    success = 0
    failed = 0
    
    for slug in batch:
        if process_page(slug):
            success += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "="*60)
    print(f"  BATCH COMPLETE")
    print("="*60)
    print(f"✓ Upgraded: {success}")
    print(f"✗ Failed:   {failed}")
    print(f"📊 Total clarity pages: {len(get_done_list())}")
    print("="*60 + "\n")
    
    log(f"BATCH COMPLETE: {success} upgraded, {failed} failed")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="SideGuy Clarity Layer Batch Upgrader")
    parser.add_argument('-n', '--number', type=int, default=5, help="Batch size (default: 5)")
    parser.add_argument('-y', '--yes', action='store_true', help="Auto-approve (no confirmation)")
    parser.add_argument('--status', action='store_true', help="Show current status")
    parser.add_argument('--sync', action='store_true', help="Sync already-upgraded pages to done list")
    
    args = parser.parse_args()
    
    if args.status:
        done = get_done_list()
        print(f"\n📊 STATUS")
        print(f"Total clarity pages: {len(done) if done != {''} else 0}")
        print(f"Log: {LOG_FILE}")
        print(f"Done list: {DONE_FILE}\n")
    elif args.sync:
        # Sync existing clarity layer pages to done list
        count = 0
        for filepath in PROJECT_ROOT.glob("*.html"):
            html = filepath.read_text(encoding='utf-8', errors='ignore')
            if 'SIDEGUY CLARITY LAYER' in html:
                slug = filepath.stem
                mark_done(slug)
                count += 1
        print(f"✓ Synced {count} existing clarity layer pages to done list")
    else:
        run_batch(size=args.number, auto_approve=args.yes)
