#!/usr/bin/env python3
# ==============================================================
# SIDEGUY AUTO PAGE BUILDER
# "Look ma, no hands!"
# ==============================================================
# Reads manifests/page-topics.csv, generates one fully-styled
# HTML page per row into auto/<slug>.html
#
# Usage:  python3 scripts/auto-builder.py
# Flags:  FORCE=true   (env) — rebuild pages that already exist
# ==============================================================

import csv, os, datetime
from pathlib import Path

ROOT    = Path(__file__).parent.parent
AUTO    = ROOT / "auto"
AUTO.mkdir(exist_ok=True)

DOMAIN        = "https://sideguysolutions.com"
PHONE_DISPLAY = "773-544-1231"
PHONE_SMS     = "+17735441231"
TODAY         = datetime.date.today().isoformat()
FORCE         = os.getenv("FORCE", "").lower() in ("1", "true", "yes")

MANIFEST = ROOT / "manifests" / "page-topics.csv"

# ── CSS (shared light ocean theme) ───────────────────────────

CSS = """  :root{
    --bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;
    --mint:#21d3a1;--mint2:#00c7ff;--blue2:#1f7cff;
    --r:18px;--pill:999px;
  }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;
    background:radial-gradient(ellipse at 60% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);
    color:var(--ink);min-height:100vh;
  }
  a{color:var(--blue2);text-decoration:none}
  a:hover{text-decoration:underline}
  nav.bc{
    padding:11px 24px;font-size:.8rem;color:var(--muted);
    border-bottom:1px solid rgba(0,0,0,.06);
    background:rgba(255,255,255,.6);backdrop-filter:blur(6px);
    position:sticky;top:0;z-index:10;
  }
  nav.bc a{color:var(--muted)}
  .wrap{max-width:860px;margin:0 auto;padding:44px 24px 100px}
  .badge{
    display:inline-block;background:var(--mint);color:#073044;
    font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
    padding:3px 12px;border-radius:var(--pill);margin-bottom:12px;
  }
  h1{font-size:clamp(1.6rem,5vw,2.4rem);font-weight:800;line-height:1.15;margin-bottom:12px}
  .lede{font-size:1rem;color:var(--muted);line-height:1.65;margin-bottom:36px;max-width:680px}
  .section{margin-bottom:40px}
  .section h2{font-size:1.05rem;font-weight:800;text-transform:uppercase;
    letter-spacing:.06em;color:var(--muted);margin-bottom:14px;padding-bottom:8px;
    border-bottom:2px solid var(--bg1);}
  .card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
  .card{
    background:rgba(255,255,255,.78);border:1px solid rgba(0,0,0,.08);
    border-radius:var(--r);padding:18px 20px;color:var(--ink);display:block;
    transition:box-shadow .15s,transform .1s;
  }
  .card:hover{box-shadow:0 4px 20px rgba(0,0,0,.1);transform:translateY(-1px);text-decoration:none}
  .card-icon{font-size:1.5rem;margin-bottom:8px}
  .card-title{font-size:.97rem;font-weight:700;margin-bottom:4px}
  .card-desc{font-size:.82rem;color:var(--muted);line-height:1.5}
  .steps{list-style:none;counter-reset:steps;display:flex;flex-direction:column;gap:14px}
  .steps li{
    counter-increment:steps;padding:16px 20px;padding-left:56px;position:relative;
    background:rgba(255,255,255,.75);border:1px solid rgba(0,0,0,.07);border-radius:var(--r);
  }
  .steps li::before{
    content:counter(steps);position:absolute;left:16px;top:50%;transform:translateY(-50%);
    width:28px;height:28px;border-radius:50%;background:var(--mint);color:#073044;
    font-size:.8rem;font-weight:800;display:flex;align-items:center;justify-content:center;
  }
  .steps li strong{display:block;font-size:.95rem;margin-bottom:4px}
  .steps li span{font-size:.87rem;color:var(--muted)}
  .pill-row{display:flex;flex-wrap:wrap;gap:8px}
  .pill{
    background:rgba(255,255,255,.8);border:1px solid rgba(0,0,0,.1);
    border-radius:var(--pill);padding:6px 15px;font-size:.84rem;font-weight:500;color:var(--ink);
  }
  .pill:hover{background:var(--mint);color:#073044;text-decoration:none}
  .pill.accent{background:var(--blue2);color:#fff;border-color:var(--blue2)}
  .cta-box{
    background:linear-gradient(135deg,#073044 0%,#0e3d58 100%);
    border-radius:var(--r);padding:28px 32px;color:#fff;
    display:flex;align-items:center;gap:24px;flex-wrap:wrap;margin:40px 0 32px;
  }
  .cta-box h3{font-size:1.1rem;font-weight:700;margin-bottom:4px}
  .cta-box p{font-size:.9rem;opacity:.8;margin:0}
  .cta-btn{
    flex-shrink:0;background:var(--mint);color:#073044;font-weight:700;
    padding:11px 22px;border-radius:var(--pill);white-space:nowrap;
  }
  .cta-btn:hover{opacity:.9;text-decoration:none}
  .floating{position:fixed;bottom:22px;right:22px;z-index:999}
  .floatBtn{
    display:flex;align-items:center;gap:8px;
    background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;
    padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;
    text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.2);
  }
  .floatBtn:hover{opacity:.92;text-decoration:none}
  footer{
    text-align:center;padding:20px;font-size:.77rem;color:var(--muted);
    border-top:1px solid rgba(0,0,0,.06);margin-top:40px;
  }
  @media(max-width:600px){.cta-box{flex-direction:column;gap:16px}.floating{bottom:14px;right:14px}}"""

# ── Per-industry content packs ────────────────────────────────
# Fallback used when industry not in map

DEFAULT_PACK = {
    "icon": "⚙️",
    "wins": [
        ("Missed call auto-text", "Reply instantly when you can't pick up — capture every lead."),
        ("Appointment reminders", "Automated texts reduce no-shows without manual follow-up."),
        ("Follow-up sequences", "Nurture leads on autopilot until they book or opt out."),
        ("Review requests", "Ask satisfied customers for reviews at the right moment."),
    ],
    "steps": [
        ("Map your highest-friction task", "Where do you lose the most time or leads right now?"),
        ("Pick one automation to start", "Missed call text-back is the easiest win for most operators."),
        ("Connect your existing tools", "Most automations work with whatever you already use."),
        ("Test with 10 real interactions", "Refine before scaling — small batches reveal edge cases fast."),
        ("Measure and iterate", "Track response rate, bookings, and no-shows before adding more."),
    ],
    "problems": [
        ("No-show rates stay high", "/problems/no-show-reduction-automation.html"),
        ("Missed calls go unanswered", "/problems/twilio-sms-not-delivering.html"),
        ("Follow-up takes too long", "/problems/zapier-task-failed-webhook-timeout.html"),
        ("Calendar keeps double-booking", "/problems/calendar-booking-double-booked-fix.html"),
    ],
}

INDUSTRY_PACKS = {
    "restaurants": {
        "icon": "🍽️",
        "wins": [
            ("Reservation reminders", "Automated texts cut no-shows by up to 40% for restaurants."),
            ("Order follow-up", "Post-visit review requests sent automatically after dining."),
            ("Waitlist management", "Text customers when their table is ready without a host calling."),
            ("Staff scheduling nudges", "Auto-reminders for shift confirmations before the week starts."),
        ],
        "steps": DEFAULT_PACK["steps"],
        "problems": DEFAULT_PACK["problems"],
    },
    "hvac": {
        "icon": "❄️",
        "wins": [
            ("Service reminders", "Annual tune-up reminders sent automatically to past customers."),
            ("After-hours lead capture", "Text-back for missed calls gets quotes started overnight."),
            ("Job status updates", "Auto-texts keep customers informed without dispatcher calls."),
            ("Review requests post-service", "Triggered reviews at job close — not weeks later."),
        ],
        "steps": DEFAULT_PACK["steps"],
        "problems": DEFAULT_PACK["problems"],
    },
    "dental": {
        "icon": "🦷",
        "wins": [
            ("Appointment reminders", "SMS reminders 48h and 2h before each appointment."),
            ("Recall automation", "Hygiene recall reminders sent at 6-month intervals automatically."),
            ("New patient intake", "Digital intake forms sent before the first appointment."),
            ("Review requests", "Post-visit review requests triggered after checkout."),
        ],
        "steps": DEFAULT_PACK["steps"],
        "problems": DEFAULT_PACK["problems"],
    },
    "real estate": {
        "icon": "🏡",
        "wins": [
            ("Lead follow-up sequences", "New inquiry? Auto-text within 90 seconds — before competitors call."),
            ("Open house reminders", "Automated reminders to registered attendees."),
            ("Listing updates", "Instant alerts to interested buyers when price drops."),
            ("Past client nurture", "Annual anniversary touches keep you top-of-mind for referrals."),
        ],
        "steps": DEFAULT_PACK["steps"],
        "problems": DEFAULT_PACK["problems"],
    },
    "contractors": {
        "icon": "🔨",
        "wins": [
            ("Missed call text-back", "Win jobs while you're on the roof — auto-text every missed call."),
            ("Estimate follow-up", "Automated follow-up on outstanding quotes before they go cold."),
            ("Job completion review", "Review request sent when the job is marked complete."),
            ("Seasonal outreach", "Spring/fall service reminders to your existing customer list."),
        ],
        "steps": DEFAULT_PACK["steps"],
        "problems": DEFAULT_PACK["problems"],
    },
}

def get_pack(industry: str) -> dict:
    return INDUSTRY_PACKS.get(industry.lower(), DEFAULT_PACK)

# ── Page builder ──────────────────────────────────────────────

def build_page(title: str, slug: str, industry: str, pillar_link: str) -> str:
    pack   = get_pack(industry)
    icon   = pack["icon"]
    canonical = f"{DOMAIN}/auto/{slug}.html"
    title_lower = title[0].lower() + title[1:]

    jsonld = f"""  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type":"ListItem","position":1,"name":"SideGuy Solutions","item":"{DOMAIN}/"}},
          {{"@type":"ListItem","position":2,"name":"AI Automation","item":"{DOMAIN}/ai-automation-hub.html"}},
          {{"@type":"ListItem","position":3,"name":"{title}","item":"{canonical}"}}
        ]
      }},
      {{
        "@type": "Article",
        "headline": "{title}",
        "description": "Practical guide to {title_lower} — real workflows, common problems, and what actually saves time.",
        "url": "{canonical}",
        "dateModified": "{TODAY}",
        "publisher": {{"@type":"Organization","name":"SideGuy Solutions","url":"{DOMAIN}"}}
      }}
    ]
  }}"""

    # Build quick-wins cards
    wins_html = ""
    for w_title, w_desc in pack["wins"]:
        wins_html += f"""    <a class="card" href="/ai-automation-hub.html">
      <div class="card-icon">{icon}</div>
      <div class="card-title">{w_title}</div>
      <div class="card-desc">{w_desc}</div>
    </a>
"""

    # Build steps
    steps_html = ""
    for s_title, s_desc in pack["steps"]:
        steps_html += f"    <li><strong>{s_title}</strong><span>{s_desc}</span></li>\n"

    # Build problem pills
    probs_html = ""
    for p_label, p_href in pack["problems"]:
        probs_html += f'    <a class="pill" href="{p_href}">{p_label}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title} | SideGuy Solutions</title>
  <meta name="description" content="Practical guide to {title_lower} — real workflows, quick wins, and what actually saves operators time."/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:title" content="{title} | SideGuy Solutions"/>
  <meta property="og:description" content="Practical guide to {title_lower} — real workflows, quick wins, and what actually saves operators time."/>
  <meta property="og:url" content="{canonical}"/>
  <meta property="og:type" content="article"/>
  <meta name="robots" content="index,follow"/>
  <script type="application/ld+json">
{jsonld}
  </script>
  <style>
{CSS}
  </style>
</head>
<body>

<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> ›
  <a href="/ai-automation-hub.html">AI Automation</a> ›
  {title}
</nav>

<main class="wrap">
  <div class="badge">Operator Guide · {industry.title()}</div>
  <h1>{icon} {title}</h1>
  <p class="lede">
    Practical guide for {industry} operators — what AI automation actually saves time on,
    where it fits in your workflow, and how to start without breaking anything.
  </p>

  <!-- Quick Wins -->
  <div class="section">
    <h2>⚡ Quick Wins for {industry.title()} Operators</h2>
    <div class="card-grid">
{wins_html}    </div>
  </div>

  <!-- How to Start -->
  <div class="section">
    <h2>🚀 How to Start</h2>
    <ol class="steps">
{steps_html}    </ol>
  </div>

  <!-- Common Problems -->
  <div class="section">
    <h2>🔧 Common Problems</h2>
    <p style="color:var(--muted);font-size:.93rem;margin-bottom:14px;line-height:1.6">
      Problems operators in {industry} run into when setting up automation — with plain-English fixes.
    </p>
    <div class="pill-row">
{probs_html}    </div>
    <div style="margin-top:12px">
      <a class="pill accent" href="/problems/index.html">Browse All 500 Problem Guides →</a>
    </div>
  </div>

  <!-- Related -->
  <div class="section">
    <h2>📖 Related Guides</h2>
    <div class="pill-row">
      <a class="pill" href="/concepts/ai-automation.html">AI Automation (concept)</a>
      <a class="pill" href="{pillar_link}">Workflow Automation Cluster</a>
      <a class="pill" href="/ai-automation-hub.html">AI Automation Hub</a>
      <a class="pill" href="/knowledge-hub.html">Knowledge Hub</a>
      <a class="pill" href="/problems/index.html">Problem Library</a>
    </div>
  </div>

  <!-- CTA -->
  <div class="cta-box">
    <div>
      <h3>Have a specific {industry} automation question?</h3>
      <p>Text PJ — real human, San Diego. Straight answer, no pitch.</p>
    </div>
    <a class="cta-btn" href="sms:{PHONE_SMS}">💬 Text {PHONE_DISPLAY}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/ai-automation-hub.html">AI Automation Hub</a> ·
    <a href="/knowledge-hub.html">Knowledge Hub</a> ·
    <a href="tel:{PHONE_SMS}">{PHONE_DISPLAY}</a>
    <br><small>Updated {TODAY}</small>
  </footer>
</main>

<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_SMS}">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
    Text PJ · {PHONE_DISPLAY}
  </a>
</div>

</body>
</html>
"""

# ── Main ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== SideGuy Auto Page Builder ===\n")
    built = skipped = 0

    with MANIFEST.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            title       = row["topic"].strip()
            slug        = row["slug"].strip()
            industry    = row.get("industry", "operators").strip()
            pillar_link = row.get("pillar_link", "/clusters/ai-workflow-automation.html").strip()
            path        = AUTO / f"{slug}.html"

            if path.exists() and not FORCE:
                print(f"  SKIP  {slug}.html")
                skipped += 1
                continue

            html = build_page(title, slug, industry, pillar_link)
            path.write_text(html)
            print(f"  BUILT {slug}.html  ({len(html):,} chars)")
            built += 1

    print(f"\n  Built: {built}   Skipped: {skipped}")
    print(f"\n  Pages → {AUTO}")
    print(f"  Run `python3 scripts/generate-sitemap.py` to update the sitemap.")
