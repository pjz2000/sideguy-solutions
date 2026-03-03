#!/usr/bin/env python3
"""
SHIP-019 Part A: Rewrite 3 skeleton placeholder pages with real content.
SHIP-019 Part B: Freshness sweep — update "February 2026" → "March 2026"
                 and SHIP010_FRESHNESS dates and sitemap lastmod.
"""

import os, re, glob, json

ROOT = "/workspaces/sideguy-solutions"
BASE_URL = "https://sideguysolutions.com"
GUARD = "SHIP-019"

# ============================================================
# PART A — FULL PAGE REWRITES
# ============================================================

PAGES = {

"restaurant-tech-support-san-diego.html": {
  "title": "Restaurant Tech Support San Diego — POS, WiFi & System Help · SideGuy",
  "desc": "Restaurant tech support in San Diego — POS system issues, WiFi drops, printer problems, tablet setup. What to check first and when to call a pro.",
  "h1": "Restaurant Tech Support in San Diego — POS, WiFi &amp; System Help",
  "body": """
  <p>A POS crash during dinner service or a WiFi drop during a busy Saturday can cost hundreds in lost sales. This page covers the most common restaurant tech failures in San Diego, what to check yourself first, and when it's time to call a pro.</p>

  <h2>Most Common Restaurant Tech Problems</h2>

  <div class="card">
    <strong>POS System Down or Slow</strong>
    <p>Check internet connection first — most cloud POS systems (Toast, Square, Clover) require live internet. Restart the router, then the POS terminal. If on cellular backup, confirm signal strength. If the problem persists across a reboot, contact your POS vendor's 24/7 support line — not a generic IT shop.</p>
  </div>

  <div class="card">
    <strong>Receipt Printer Not Printing</strong>
    <p>Check paper roll (most common cause), then USB/ethernet cable. Clear any paper jam. If the printer is network-connected, confirm it has the same IP the POS is pointing to — routers sometimes reassign IPs after a restart. Set a static IP on the printer to prevent recurring issues.</p>
  </div>

  <div class="card">
    <strong>WiFi Dropping or Slow in Kitchen or Back of House</strong>
    <p>Restaurant environments are tough on WiFi — thick walls, metal equipment, microwave interference. Solutions in order of cost: (1) move your router to a central location, (2) add a mesh node or access point in the kitchen, (3) use 5 GHz for front-of-house tablets, 2.4 GHz for back-of-house (better range). Budget $150–$400 for a restaurant-grade mesh setup in San Diego.</p>
  </div>

  <div class="card">
    <strong>Tablet or Kiosk Not Responding</strong>
    <p>Force restart the device (hold power button 10 seconds). Check that the POS app hasn't logged out. If running iPads, confirm iOS auto-updates haven't changed permissions. Many restaurant POS outages after iOS updates are permissions issues, not connectivity.</p>
  </div>

  <div class="card">
    <strong>Credit Card Reader Errors</strong>
    <p>Tap the chip reader gently on the counter to clear debris — this solves about 30% of card reader errors. Re-pair Bluetooth readers. If errors continue, the reader may need a firmware update from your payment processor. Call their support with your serial number ready.</p>
  </div>

  <h2>When to Call a San Diego IT Pro</h2>
  <ul>
    <li>POS system won't come back online after a full restart cycle</li>
    <li>Multiple devices failing simultaneously (usually a router or switch)</li>
    <li>Network cabling needed in kitchen or bar area</li>
    <li>Setting up a new location or second POS station</li>
    <li>Security camera or door access system integration</li>
  </ul>

  <p style="margin-top:1.5rem">See also: <a href="/tech-help-hub-san-diego.html">Tech Help Hub</a> · <a href="/san-diego-tech-support.html">San Diego Tech Support</a> · <a href="/small-business-tech-help-san-diego.html">Small Business Tech Help</a></p>

  <a class="cta" href="sms:+17735441231">Text PJ — Fast Answer</a>
""",
},

"contractor-tech-support-san-diego.html": {
  "title": "Contractor Tech Support San Diego — Field Apps, Invoicing & Device Help · SideGuy",
  "desc": "Contractor tech support in San Diego — field app crashes, estimate software issues, payment terminal problems, device setup. What to check and who to call.",
  "h1": "Contractor Tech Support in San Diego — Apps, Invoicing &amp; Device Help",
  "parent_link": '<p style="margin:0 0 1.5rem;font-size:14px;color:var(--muted)">&#x2190; <a href="/contractor-services-hub-san-diego.html" style="color:inherit;text-decoration:underline">Contractor Services Hub</a></p>',
  "body": """
  <p>Field software crashes, estimate apps that won't sync, payment terminals that go offline on a job site — contractor tech problems tend to happen at the worst possible moment. Here's what to check first before calling anyone.</p>

  <h2>Most Common Contractor Tech Issues in San Diego</h2>

  <div class="card">
    <strong>Estimating or Project Management App Not Syncing</strong>
    <p>Most field apps (Jobber, ServiceTitan, Buildertrend, Housecall Pro) sync over internet. On a job site with weak signal, switch to a mobile hotspot. Force-close the app and reopen. If a quote isn't saving, take a screenshot first — some apps silently lose data when connectivity drops mid-save.</p>
  </div>

  <div class="card">
    <strong>Mobile Payment Terminal Offline on Job Site</strong>
    <p>Square, Stripe Reader, and Clover Go all require cell data or WiFi. If the client's WiFi is unreliable, enable a personal hotspot before you arrive. Keep a backup paper invoice in your truck — if you can't process on-site, text the invoice link from your phone. Most clients pay digitally within the hour.</p>
  </div>

  <div class="card">
    <strong>Tablet or Phone Running Field App Freezing</strong>
    <p>Close background apps (field apps are memory-heavy). Check that both the device OS and the app are current — outdated combinations cause the most freezes. For Android: Settings → Apps → [App] → Storage → Clear Cache. For iPhone: delete and reinstall (data is cloud-synced).</p>
  </div>

  <div class="card">
    <strong>QuickBooks or Invoicing Not Connecting to Bank</strong>
    <p>Bank feed disconnections are usually an expired login token — not a software bug. Go to Banking → Update, re-enter credentials, and re-authorize. If your bank recently updated their login system, disconnect and reconnect the bank account entirely in QuickBooks Online.</p>
  </div>

  <div class="card">
    <strong>Crew Devices Not Staying Connected</strong>
    <p>For multiple crew members using field apps, consider Apple Business Manager or Google Workspace for remote management. For small crews (under 5), a shared Google account per crew with app restrictions is a workable free solution.</p>
  </div>

  <h2>When to Get San Diego IT Help</h2>
  <ul>
    <li>Setting up a multi-user field software system for your crew</li>
    <li>Migrating from paper/spreadsheets to a field service app</li>
    <li>Network setup for a shop, yard, or satellite office</li>
    <li>Recurring sync failures your software vendor can't resolve</li>
    <li>Device management for a team of 3+ field technicians</li>
  </ul>

  <p style="margin-top:1.5rem">See also: <a href="/contractor-payment-processing-san-diego.html">Contractor Payment Processing</a> · <a href="/contractor-billing-tools-san-diego.html">Contractor Billing Tools</a> · <a href="/contractor-services-hub-san-diego.html">Contractor Services Hub</a></p>

  <a class="cta" href="sms:+17735441231">Text PJ — Fast Answer</a>
""",
},

"small-business-tech-help-san-diego.html": {
  "title": "Small Business Tech Help San Diego — Internet, Devices & Software · SideGuy",
  "desc": "Small business tech help in San Diego — slow internet, WiFi issues, software setup, device problems. Clear guidance on what to check first and when to call a pro.",
  "h1": "Small Business Tech Help in San Diego",
  "body": """
  <p>When your internet goes down, a device stops working, or software won't cooperate, the cost is real — every hour of downtime is lost productivity or lost sales. This page gives San Diego small business owners clear guidance on the most common tech issues and how to resolve them fast.</p>

  <h2>Internet & WiFi Problems</h2>

  <div class="card">
    <strong>Internet Down or Very Slow</strong>
    <p>First: restart your modem and router (unplug, wait 30 seconds, plug in modem first, then router). Check for outages using your ISP's status page or Downdetector.com. If speeds are consistently slow (not just today), run a speed test at fast.com — if you're getting less than 50% of your advertised speed, call your ISP and request a line test. San Diego ISPs: Cox, AT&T Fiber, Spectrum.</p>
  </div>

  <div class="card">
    <strong>WiFi Dead Zones in Your Location</strong>
    <p>A single router rarely covers a full retail space or office. A mesh WiFi system (Eero, Google Nest WiFi, TP-Link Deco) with 2–3 nodes typically costs $150–$300 and eliminates dead zones in spaces up to 4,000 sq ft. This is almost always worth doing before buying a more expensive internet plan.</p>
  </div>

  <h2>Computer & Device Issues</h2>

  <div class="card">
    <strong>Computer Running Slow</strong>
    <p>Restart first (not sleep — full restart). Check disk space: if you're under 10% free, the computer will slow dramatically. On Windows: Disk Cleanup + disable startup programs. On Mac: check Activity Monitor for runaway processes. If a business computer is over 5 years old and consistently slow, the repair cost often exceeds the value — replacement is usually the better call.</p>
  </div>

  <div class="card">
    <strong>Printer Not Working</strong>
    <p>Delete all pending print jobs first (they can block new prints even after a restart). Restart both the printer and the computer. On a network printer, confirm the IP address hasn't changed — assign a static IP in the printer's settings to prevent recurring issues. Most San Diego office printer problems resolve with these three steps.</p>
  </div>

  <h2>Software & Cloud Tool Problems</h2>

  <div class="card">
    <strong>Key Software Not Opening or Crashing</strong>
    <p>Check for pending updates — most crashes are version conflicts. Uninstall and reinstall if updates don't help. If cloud-based (Google Workspace, Microsoft 365, QuickBooks Online), clear your browser cache or try a different browser before assuming it's a software bug.</p>
  </div>

  <div class="card">
    <strong>Email Not Sending or Receiving</strong>
    <p>Check your sent folder — if emails aren't in sent, the problem is outbound (SMTP settings). Log in via webmail (Gmail, Outlook.com) to isolate whether it's the email client or the account. For business email on a custom domain, verify MX and SPF records haven't changed — domain registrar or IT help needed for that.</p>
  </div>

  <h2>When to Call a San Diego IT Pro</h2>
  <ul>
    <li>Recurring problems that keep coming back after fixes</li>
    <li>Network setup for a new office or retail location</li>
    <li>Moving from a consumer to a business internet plan</li>
    <li>Setting up business email on a custom domain</li>
    <li>Data backup and recovery needs</li>
    <li>Security incident — unusual account activity, ransomware, phishing</li>
  </ul>

  <p style="margin-top:1.5rem">See also: <a href="/tech-help-hub-san-diego.html">Tech Help Hub</a> · <a href="/san-diego-tech-support.html">San Diego Tech Support</a> · <a href="/restaurant-tech-support-san-diego.html">Restaurant Tech Support</a></p>

  <a class="cta" href="sms:+17735441231">Text PJ — Fast Answer</a>
""",
},

}

STYLE_BLOCK = """  <style>
    :root{--bg0:#eefcff;--ink:#073044;--mint:#21d3a1;--muted:#3f6173;--muted2:#5e7d8e;--stroke:#c8eee7}
    *{box-sizing:border-box;margin:0;padding:0}
    body{font-family:-apple-system,system-ui,sans-serif;background:var(--bg0);color:var(--ink);padding:1.5rem}
    .wrap{max-width:720px;margin:0 auto}
    h1{font-size:1.7rem;line-height:1.2;margin-bottom:1rem}
    h2{font-size:1.2rem;margin:2rem 0 0.8rem;color:var(--ink)}
    p{line-height:1.65;color:var(--muted);margin-bottom:1rem}
    .card{background:#fff;border:1px solid var(--stroke);border-radius:8px;padding:1.2rem 1.4rem;margin-bottom:0.8rem}
    .card strong{color:var(--ink);display:block;margin-bottom:0.3rem}
    ul{padding-left:1.4rem;line-height:2;color:var(--muted);margin-bottom:1rem}
    .cta{background:var(--mint);color:#fff;display:inline-block;padding:0.7rem 1.6rem;border-radius:6px;text-decoration:none;font-weight:600;margin-top:1rem}
    a{color:var(--mint)}
  </style>"""

part_a_updated = 0

for fname, data in PAGES.items():
    fp = os.path.join(ROOT, fname)
    if not os.path.isfile(fp):
        print(f"  [WARN] {fname} not found")
        continue

    with open(fp) as f:
        content = f.read()

    if GUARD in content:
        print(f"  [skip] {fname} already rewritten")
        continue

    # Fix title
    content = re.sub(r'<title>[^<]+</title>', f'<title>{data["title"]}</title>', content)

    # Fix meta description (all variants)
    content = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*">',
        f'<meta name="description" content="{data["desc"]}">',
        content
    )
    # Also fix OG/twitter descriptions that got set to the bad placeholder
    old_og_desc = re.search(r'<meta property="og:description" content="([^"]*)">', content)
    if old_og_desc:
        content = content.replace(old_og_desc.group(), f'<meta property="og:description" content="{data["desc"]}">')
    old_tw_desc = re.search(r'<meta name="twitter:description" content="([^"]*)">', content)
    if old_tw_desc:
        content = content.replace(old_tw_desc.group(), f'<meta name="twitter:description" content="{data["desc"]}">')

    # Fix OG title and twitter title that contain the slug
    content = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        f'<meta property="og:title" content="{data["title"]}">',
        content
    )
    content = re.sub(
        r'<meta name="twitter:title" content="[^"]*">',
        f'<meta name="twitter:title" content="{data["title"]}">',
        content
    )

    # Fix WebPage schema name/description
    content = re.sub(
        r'"name": "[^"]+tech-support[^"]*",',
        f'"name": "{data["title"]}",',
        content
    )
    content = re.sub(
        r'"name": "small-business-tech-help[^"]*",',
        f'"name": "{data["title"]}",',
        content
    )
    content = re.sub(
        r'"description": "Original long-tail page for[^"]*"',
        f'"description": "{data["desc"]}"',
        content
    )

    # Inject style + real body content, replacing the skeleton body
    # Find the <body> tag and replace everything between it and first schema/mesh block
    # Strategy: replace the skeleton H1 + placeholder paragraph with style + real content
    slug = fname.replace(".html","")
    parent_link = data.get("parent_link","")

    # Build the replacement body section
    new_body_section = f"""{STYLE_BLOCK}
</head>

<body>
  <!-- {GUARD}: Full rewrite — 2026-03-03 -->
  <div class="wrap">
{('  ' + parent_link) if parent_link else ''}
  <h1>{data["h1"]}</h1>
{data["body"]}
  </div>"""

    # Replace from </head> through first known placeholder content
    # Find the span from </head> to the timestamp div
    old_body_start = re.search(
        r'</head>\s*\n<body>.*?<h1>[^<]*</h1>.*?<p>Published 2026-01-05\. Original long-tail content\.</p>(?:.*?&#x2190;.*?</p>)?',
        content,
        re.DOTALL
    )
    if old_body_start:
        content = content[:old_body_start.start()] + "\n" + new_body_section + "\n" + content[old_body_start.end():]
        with open(fp, "w") as f:
            f.write(content)
        print(f"  [rewrite] {fname}")
        part_a_updated += 1
    else:
        print(f"  [WARN] could not find body pattern in {fname} — skipping")

print(f"\nPart A done — {part_a_updated} skeleton pages fully rewritten\n")


# ============================================================
# PART B — FRESHNESS SWEEP
# ============================================================

def is_prod(fname):
    if fname[0].isupper(): return False
    if fname.startswith("aaa-") or fname.startswith("_"): return False
    skip = {"template.html","seo-page-template.html","seo-template.html",
            "sideguy-universal-template.html","template-san-diego-help.html",
            "template-v304.html","clean-template.html","human-solution-template.html",
            "index-backup.html","index-test.html","index-working-backup.html","-hub.html"}
    return fname not in skip

all_html = sorted(glob.glob(os.path.join(ROOT, "*.html")))
part_b_updated = 0

for fp in all_html:
    fname = os.path.basename(fp)
    if not is_prod(fname):
        continue

    with open(fp) as f:
        content = f.read()

    if "noindex" in content.lower():
        continue

    changed = False

    # 1. Visible "Updated February 2026" → "Updated March 2026"
    if "Updated February 2026" in content:
        content = content.replace("Updated February 2026", "Updated March 2026")
        changed = True

    # 2. SHIP010_FRESHNESS hidden date
    if "Updated: 2026-02-23" in content:
        content = content.replace("Updated: 2026-02-23", "Updated: 2026-03-03")
        changed = True
    if "Updated: 2026-02-24" in content:
        content = content.replace("Updated: 2026-02-24", "Updated: 2026-03-03")
        changed = True

    # 3. Also update January 2026 references in the freshness timestamp span only
    # (not in body content — leave date-specific article content alone)
    if "Updated January 2026" in content:
        content = content.replace("Updated January 2026", "Updated March 2026")
        changed = True

    if changed:
        with open(fp, "w") as f:
            f.write(content)
        part_b_updated += 1

print(f"Part B done — {part_b_updated} pages freshness-updated to March 2026\n")

# ============================================================
# PART B-2 — SITEMAP LASTMOD UPDATE
# ============================================================

sitemap_path = os.path.join(ROOT, "sitemap.xml")
with open(sitemap_path) as f:
    sitemap = f.read()

# Count before
old_feb24 = sitemap.count("<lastmod>2026-02-24</lastmod>")
old_feb23 = sitemap.count("<lastmod>2026-02-23</lastmod>")

sitemap = sitemap.replace("<lastmod>2026-02-24</lastmod>", "<lastmod>2026-03-03</lastmod>")
sitemap = sitemap.replace("<lastmod>2026-02-23</lastmod>", "<lastmod>2026-03-03</lastmod>")

with open(sitemap_path, "w") as f:
    f.write(sitemap)

updated_count = old_feb24 + old_feb23
print(f"Part B-2 done — sitemap.xml: {updated_count} lastmod entries updated to 2026-03-03\n")

# ============================================================
# SUMMARY
# ============================================================
print("=" * 60)
print("SHIP-019 COMPLETE")
print(f"  Part A: {part_a_updated} skeleton pages fully rewritten with real content")
print(f"  Part B: {part_b_updated} pages updated to 'March 2026' freshness")
print(f"  Part B-2: sitemap.xml — {updated_count} lastmod → 2026-03-03")
print("=" * 60)
