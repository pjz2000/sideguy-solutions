#!/usr/bin/env python3
"""Build SideGuy cluster pages for AI automation sub-topics."""
import os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLUSTERS_DIR = os.path.join(ROOT, "clusters")
os.makedirs(CLUSTERS_DIR, exist_ok=True)

SHARED_STYLE = """
  :root{
    --bg0:#eefcff;--bg1:#d7f5ff;--bg2:#bfeeff;
    --ink:#073044;--muted:#3f6173;--muted2:#5e7d8e;
    --card:#ffffffcc;--card2:#ffffffb8;
    --stroke:rgba(7,48,68,.10);--stroke2:rgba(7,48,68,.07);
    --shadow:0 18px 50px rgba(7,48,68,.10);
    --mint:#21d3a1;--mint2:#00c7ff;--blue:#4aa9ff;--blue2:#1f7cff;
    --r:22px;--pill:999px;
  }
  *{box-sizing:border-box}
  html,body{height:100%}
  body{margin:0;font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,Arial,sans-serif;color:var(--ink);background:radial-gradient(1200px 900px at 22% 10%,#ffffff 0%,var(--bg0) 25%,var(--bg1) 60%,var(--bg2) 100%);-webkit-font-smoothing:antialiased;overflow-x:hidden;}
  body:before{content:"";position:fixed;inset:-20%;background:radial-gradient(closest-side at 18% 20%,rgba(33,211,161,.18),transparent 55%),radial-gradient(closest-side at 78% 28%,rgba(74,169,255,.16),transparent 52%);pointer-events:none;z-index:0;}
  main{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:24px 24px 120px;}
  nav.bc{font-size:.82rem;color:var(--muted);display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin-bottom:28px;}
  nav.bc a{color:var(--blue2);text-decoration:none;font-weight:600;}
  nav.bc a:hover{text-decoration:underline;}
  nav.bc span{opacity:.4;margin:0 2px;}
  .tag{display:inline-block;padding:4px 12px;border-radius:var(--pill);font-size:.75rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;background:linear-gradient(135deg,var(--mint),var(--blue2));color:#fff;margin-bottom:16px;}
  h1{font-size:clamp(1.7rem,4vw,2.4rem);font-weight:900;line-height:1.18;letter-spacing:-.02em;margin:0 0 14px;}
  .intro{font-size:1.05rem;color:var(--muted);line-height:1.65;margin:0 0 28px;max-width:660px;}
  .card{background:var(--card);border:1px solid var(--stroke);border-radius:var(--r);padding:22px 26px;box-shadow:var(--shadow);backdrop-filter:blur(12px);margin-bottom:18px;}
  .card h2{font-size:1.05rem;font-weight:800;margin:0 0 12px;}
  .card p{font-size:.9rem;color:var(--muted);line-height:1.6;margin:0 0 10px;}
  .card p:last-child{margin:0;}
  .section-label{font-size:.78rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--muted2);margin:28px 0 12px;}
  .pill-grid{display:flex;flex-wrap:wrap;gap:8px;}
  .pill-link{padding:7px 12px;border-radius:10px;background:rgba(255,255,255,.72);border:1px solid var(--stroke);text-decoration:none;color:var(--ink);font-size:.82rem;font-weight:600;transition:background .14s,transform .14s;}
  .pill-link:hover{background:rgba(255,255,255,.95);transform:translateY(-1px);}
  .checklist{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-direction:column;gap:8px;}
  .checklist li{display:flex;align-items:flex-start;gap:10px;font-size:.9rem;line-height:1.5;}
  .checklist li:before{content:"✓";color:var(--mint);font-weight:900;flex-shrink:0;margin-top:1px;}
  .faq-item{border-top:1px solid var(--stroke);padding:14px 0;}
  .faq-item h3{font-size:.93rem;font-weight:800;margin:0 0 6px;}
  .faq-item p{font-size:.875rem;color:var(--muted);line-height:1.6;margin:0;}
  .cta-card{background:linear-gradient(135deg,rgba(33,211,161,.15),rgba(0,199,255,.12));border:1px solid rgba(33,211,161,.30);border-radius:var(--r);padding:22px 26px;margin-top:24px;text-align:center;}
  .cta-card h2{font-size:1rem;font-weight:800;margin:0 0 8px;}
  .cta-card p{font-size:.875rem;color:var(--muted);margin:0 0 14px;line-height:1.55;}
  .cta-card a.btn{display:inline-block;padding:11px 26px;border-radius:var(--pill);background:linear-gradient(135deg,var(--mint),var(--mint2));color:#fff;font-weight:800;text-decoration:none;font-size:.875rem;}
  .related-knowledge{margin-top:24px;padding:16px 18px;background:rgba(255,255,255,.55);border:1px solid rgba(7,48,68,.09);border-radius:16px;}
  .related-knowledge .rk-label{font-size:.72rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:#5e7d8e;margin-bottom:8px;}
  .microFooter{margin-top:28px;font-size:11px;color:rgba(7,48,68,.55);}
  .microFooter a{color:rgba(31,124,255,.85);text-decoration:none;font-weight:700;}
  .floating{position:fixed;right:18px;bottom:16px;z-index:999;display:flex;align-items:center;gap:10px;}
  .floatPill{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.66);border:1px solid var(--stroke2);box-shadow:0 18px 55px rgba(7,48,68,.14);backdrop-filter:blur(14px);min-width:200px;}
  .floatPill .t1{font-weight:900;font-size:12px;color:rgba(7,48,68,.88);display:flex;align-items:center;gap:8px;}
  .chatDot{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 0 0 3px rgba(255,255,255,.9);}
  .floatPill .t2{font-size:11px;color:rgba(7,48,68,.62);}
  .floatBtn{width:54px;height:54px;border-radius:999px;background:radial-gradient(circle at 30% 20%,#ffffff,rgba(33,211,161,.95) 52%,rgba(0,199,255,.95) 100%);border:1px solid rgba(255,255,255,.8);box-shadow:0 0 0 4px rgba(255,255,255,.92),0 22px 60px rgba(0,199,255,.22);position:relative;text-decoration:none;display:flex;align-items:center;justify-content:center;}
  @keyframes pulse{0%,100%{opacity:.65;transform:scale(1)}50%{opacity:1;transform:scale(1.12)}}
  .floatBtn:after{content:"";position:absolute;inset:-16px;border-radius:999px;background:radial-gradient(circle,rgba(33,211,161,.28),transparent 62%);filter:blur(7px);animation:pulse 2.2s ease-in-out infinite;z-index:-1;}
""".strip()

FLOAT_BTN = """
<div class="floating">
  <div class="floatPill">
    <div class="t1"><span class="chatDot"></span>Still have a question?</div>
    <div class="t2">Text PJ · real human · San Diego</div>
  </div>
  <a class="floatBtn" href="sms:+17735441231" aria-label="Text PJ">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
  </a>
</div>
""".strip()

RELATED = """
  <div class="related-knowledge">
    <div class="rk-label">Related Knowledge</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;">
      <a href="/knowledge/sideguy-knowledge-map.html" style="padding:6px 11px;border-radius:9px;background:linear-gradient(135deg,rgba(99,102,241,.12),rgba(74,169,255,.10));border:1px solid rgba(99,102,241,.22);text-decoration:none;color:#073044;font-size:.8rem;font-weight:700;">🗺 Knowledge Map</a>
      <a href="/pillars/ai-automation.html" style="padding:6px 11px;border-radius:9px;background:rgba(255,255,255,.7);border:1px solid rgba(7,48,68,.10);text-decoration:none;color:#073044;font-size:.8rem;font-weight:700;">📖 AI Automation Pillar</a>
      <a href="/intelligence/decisions/should-i-use-ai.html" style="padding:6px 11px;border-radius:9px;background:rgba(255,255,255,.7);border:1px solid rgba(7,48,68,.10);text-decoration:none;color:#073044;font-size:.8rem;font-weight:700;">🤖 Should I Use AI?</a>
      <a href="/hubs/category-ai-automation.html" style="padding:6px 11px;border-radius:9px;background:rgba(255,255,255,.7);border:1px solid rgba(7,48,68,.10);text-decoration:none;color:#073044;font-size:.8rem;font-weight:700;">⚡ AI Automation Hub</a>
    </div>
  </div>
""".strip()


def pretty(slug):
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def get_industries(prefix):
    pattern = os.path.join(ROOT, f"{prefix}-for-*-san-diego.html")
    files = glob.glob(pattern)
    industries = []
    for f in sorted(files):
        name = os.path.basename(f)
        ind = name.replace(f"{prefix}-for-", "").replace("-san-diego.html", "")
        industries.append(ind)
    return industries


def pill_links(industries, prefix, extra_style=""):
    lines = []
    for ind in industries:
        label = pretty(ind)
        href = f"/{prefix}-for-{ind}-san-diego.html"
        lines.append(f'      <a class="pill-link" href="{href}"{extra_style}>{label}</a>')
    return "\n".join(lines)


def schema_faq(pairs):
    items = []
    for q, a in pairs:
        items.append(f"""    {{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{"@type":"Answer","text":"{a}"}}
    }}""")
    return "{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"FAQPage\",\n  \"mainEntity\": [\n" + ",\n".join(items) + "\n  ]\n}"


def schema_breadcrumb(items):
    crumbs = []
    for i, (name, url) in enumerate(items, 1):
        crumbs.append(f'    {{"@type":"ListItem","position":{i},"name":"{name}","item":"{url}"}}')
    return "{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"BreadcrumbList\",\n  \"itemListElement\": [\n" + ",\n".join(crumbs) + "\n  ]\n}"


# ── 1. AI Customer Service ────────────────────────────────────────────────────
cs_industries = get_industries("ai-customer-service")
cs_pills = pill_links(cs_industries, "ai-customer-service")

cs_bc = schema_breadcrumb([
    ("SideGuy Solutions", "https://sideguysolutions.com"),
    ("AI Automation Hub", "https://sideguysolutions.com/hubs/category-ai-automation.html"),
    ("AI Customer Service Cluster", "https://sideguysolutions.com/clusters/ai-customer-service.html"),
])
cs_faq = schema_faq([
    ("What is AI customer service?", "AI customer service uses automated tools to handle common customer questions, route tickets, and draft responses — so your team focuses on complex or emotional issues that need a human."),
    ("Is AI customer service good for small businesses?", "Yes, for repetitive FAQ-style interactions. The best implementation keeps humans for anything requiring relationship context or emotional judgment."),
    ("How much does AI customer service software cost?", "Entry-level tools run $20–$80/month. Mid-tier tools with CRM integration run $100–$400/month. ROI depends entirely on how many repetitive questions your team currently handles manually."),
])

cs_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>AI Customer Service for San Diego Businesses — Industry Guide | SideGuy</title>
<link rel="canonical" href="https://sideguysolutions.com/clusters/ai-customer-service.html"/>
<meta name="description" content="How AI customer service automation works for {len(cs_industries)} San Diego industries — from accountants to yoga studios. Honest breakdown, no vendor hype."/>
<meta property="og:title" content="AI Customer Service for San Diego Businesses"/>
<meta property="og:description" content="How AI customer service automation works across {len(cs_industries)} industries. Honest breakdown, no vendor hype."/>
<meta property="og:url" content="https://sideguysolutions.com/clusters/ai-customer-service.html"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="SideGuy Solutions"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary"/>
<script type="application/ld+json">
{cs_bc}
</script>
<script type="application/ld+json">
{cs_faq}
</script>
<style>
{SHARED_STYLE}
</style>
</head>
<body>
<main>
  <nav class="bc">
    <a href="/">SideGuy Solutions</a>
    <span>/</span>
    <a href="/hubs/category-ai-automation.html">AI Automation Hub</a>
    <span>/</span>
    <span>AI Customer Service</span>
  </nav>

  <span class="tag">Cluster Hub</span>
  <h1>AI Customer Service for San Diego Businesses</h1>
  <p class="intro">Customer service is the single most common area where AI saves real time. Here is how it works across {len(cs_industries)} industries — and what to watch out for before you automate anything.</p>

  <div class="card">
    <h2>💬 What AI Customer Service Actually Does</h2>
    <p>Most AI customer service tools do three things well: answer the same questions repeatedly, route incoming requests to the right person, and draft replies for a human to review. That is the useful zone.</p>
    <p>Where it falls apart: anything requiring empathy, relationship context, or judgment calls. A frustrated long-term client deserves a human response, not a bot.</p>
    <ul class="checklist">
      <li>Handles FAQ-style questions without staff time</li>
      <li>Routes tickets before a human reads them</li>
      <li>Drafts replies for quick human review and send</li>
      <li>Works 24/7 for after-hours inquiries</li>
    </ul>
  </div>

  <div class="card">
    <h2>🏭 Industry-Specific Pages — {len(cs_industries)} Industries</h2>
    <p>Each page covers how AI customer service applies to that specific business type — costs, tools, and what to check before buying anything.</p>
    <div class="pill-grid" style="margin-top:14px;">
{cs_pills}
    </div>
  </div>

  <div class="card">
    <h2>📋 Before You Buy Anything</h2>
    <ul class="checklist">
      <li>List your top 10 most repeated questions. If fewer than 5 are truly identical every time, the ROI is probably low.</li>
      <li>Check whether your CRM or booking system already has built-in automation before adding a new tool.</li>
      <li>Build a human review step for any AI reply that goes to a paying customer.</li>
      <li>Run the AI in parallel with your current process for 2 weeks before replacing it.</li>
    </ul>
  </div>

  <div class="card">
    <h2>Honest Answers</h2>
    <div class="faq-item">
      <h3>What is AI customer service?</h3>
      <p>AI customer service uses automated tools to handle common customer questions, route tickets, and draft responses — so your team focuses on complex or emotional issues that need a human.</p>
    </div>
    <div class="faq-item">
      <h3>Is AI customer service good for small businesses?</h3>
      <p>Yes, for repetitive FAQ-style interactions. The best implementation keeps humans for anything requiring relationship context or emotional judgment.</p>
    </div>
    <div class="faq-item">
      <h3>How much does AI customer service software cost?</h3>
      <p>Entry-level tools run $20–$80/month. Mid-tier tools with CRM integration run $100–$400/month. ROI depends entirely on how many repetitive questions your team currently handles manually.</p>
    </div>
  </div>

  <div class="cta-card">
    <h2>Not sure which tool is right for your business?</h2>
    <p>Text PJ. Describe your situation and get an honest answer — not a product recommendation.</p>
    <a class="btn" href="sms:+17735441231">Text PJ · 773-544-1231</a>
  </div>

{RELATED}

  <div class="microFooter">
    <a href="/hubs/category-ai-automation.html">← AI Automation Hub</a> &nbsp;·&nbsp;
    <a href="/clusters/ai-scheduling.html">AI Scheduling →</a>
  </div>
</main>
{FLOAT_BTN}
</body>
</html>"""

with open(os.path.join(CLUSTERS_DIR, "ai-customer-service.html"), "w") as f:
    f.write(cs_html)
print(f"✓ ai-customer-service.html ({len(cs_industries)} industry links)")


# ── 2. AI Scheduling ──────────────────────────────────────────────────────────
sched_industries = get_industries("ai-scheduling")
sched_pills = pill_links(sched_industries, "ai-scheduling")

sched_bc = schema_breadcrumb([
    ("SideGuy Solutions", "https://sideguysolutions.com"),
    ("AI Automation Hub", "https://sideguysolutions.com/hubs/category-ai-automation.html"),
    ("AI Scheduling Cluster", "https://sideguysolutions.com/clusters/ai-scheduling.html"),
])
sched_faq = schema_faq([
    ("What is AI scheduling automation?", "AI scheduling tools automate the booking, rescheduling, and reminder process — eliminating phone tag and reducing no-shows. They work best for service businesses with appointment-based models."),
    ("Which businesses benefit most from AI scheduling?", "Any appointment-based business: chiropractors, salons, HVAC companies, personal trainers, dentists. If your team spends more than 30 minutes a day managing the calendar manually, AI scheduling has a clear ROI."),
    ("What does AI scheduling cost?", "Basic tools like Calendly start under $20/month. Industry-specific tools (with intake forms, CRM sync, revenue recovery) typically run $50–$200/month."),
])

sched_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>AI Scheduling Automation for San Diego Businesses — Industry Guide | SideGuy</title>
<link rel="canonical" href="https://sideguysolutions.com/clusters/ai-scheduling.html"/>
<meta name="description" content="How AI scheduling automation works for {len(sched_industries)} San Diego industries — reduce no-shows, eliminate phone tag, and free up staff time. Honest breakdown."/>
<meta property="og:title" content="AI Scheduling Automation for San Diego Businesses"/>
<meta property="og:description" content="How AI scheduling automation works across {len(sched_industries)} industries. Reduce no-shows, eliminate phone tag."/>
<meta property="og:url" content="https://sideguysolutions.com/clusters/ai-scheduling.html"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="SideGuy Solutions"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary"/>
<script type="application/ld+json">
{sched_bc}
</script>
<script type="application/ld+json">
{sched_faq}
</script>
<style>
{SHARED_STYLE}
</style>
</head>
<body>
<main>
  <nav class="bc">
    <a href="/">SideGuy Solutions</a>
    <span>/</span>
    <a href="/hubs/category-ai-automation.html">AI Automation Hub</a>
    <span>/</span>
    <span>AI Scheduling</span>
  </nav>

  <span class="tag">Cluster Hub</span>
  <h1>AI Scheduling Automation for San Diego Businesses</h1>
  <p class="intro">Phone tag, double-bookings, and no-shows are all largely solvable problems. Here is how AI scheduling works across {len(sched_industries)} industries — and what to configure before you go live.</p>

  <div class="card">
    <h2>📅 What AI Scheduling Actually Solves</h2>
    <p>The core problem with manual scheduling is the back-and-forth: someone calls, you're busy, they call back, you miss it again. AI scheduling eliminates this for standard appointments while keeping humans available for complex cases.</p>
    <ul class="checklist">
      <li>24/7 self-booking — customers book when they want, not during business hours</li>
      <li>Automated reminders reduce no-shows by 30–60% (industry average)</li>
      <li>Rescheduling workflows handle cancellations without staff intervention</li>
      <li>Intake forms collect information before the appointment</li>
    </ul>
  </div>

  <div class="card">
    <h2>🏭 Industry-Specific Pages — {len(sched_industries)} Industries</h2>
    <p>Each page covers tools, costs, and what actually matters for that specific business type.</p>
    <div class="pill-grid" style="margin-top:14px;">
{sched_pills}
    </div>
  </div>

  <div class="card">
    <h2>⚠️ What to Configure Before Going Live</h2>
    <ul class="checklist">
      <li>Set buffer time between appointments — AI will book back-to-back unless you stop it.</li>
      <li>Define which appointment types should require human confirmation.</li>
      <li>Test the full booking flow as a customer before turning it on.</li>
      <li>Connect it to your existing calendar — conflicts from a disconnected system are worse than no automation.</li>
      <li>Build a fallback: a clear path for customers who can't navigate self-booking.</li>
    </ul>
  </div>

  <div class="card">
    <h2>Honest Answers</h2>
    <div class="faq-item">
      <h3>What is AI scheduling automation?</h3>
      <p>AI scheduling tools automate the booking, rescheduling, and reminder process — eliminating phone tag and reducing no-shows. They work best for service businesses with appointment-based models.</p>
    </div>
    <div class="faq-item">
      <h3>Which businesses benefit most from AI scheduling?</h3>
      <p>Any appointment-based business: chiropractors, salons, HVAC companies, personal trainers, dentists. If your team spends more than 30 minutes a day managing the calendar manually, AI scheduling has a clear ROI.</p>
    </div>
    <div class="faq-item">
      <h3>What does AI scheduling cost?</h3>
      <p>Basic tools like Calendly start under $20/month. Industry-specific tools with intake forms, CRM sync, and revenue recovery typically run $50–$200/month.</p>
    </div>
  </div>

  <div class="cta-card">
    <h2>Want help picking a scheduling tool for your business?</h2>
    <p>Text PJ. Plain answer about what fits your workflow — no upselling.</p>
    <a class="btn" href="sms:+17735441231">Text PJ · 773-544-1231</a>
  </div>

{RELATED}

  <div class="microFooter">
    <a href="/clusters/ai-customer-service.html">← AI Customer Service</a> &nbsp;·&nbsp;
    <a href="/clusters/ai-marketing-automation.html">AI Marketing Automation →</a>
  </div>
</main>
{FLOAT_BTN}
</body>
</html>"""

with open(os.path.join(CLUSTERS_DIR, "ai-scheduling.html"), "w") as f:
    f.write(sched_html)
print(f"✓ ai-scheduling.html ({len(sched_industries)} industry links)")


# ── 3–7: Guide-style cluster pages ───────────────────────────────────────────
guide_clusters = [
    {
        "slug": "ai-marketing-automation",
        "title": "AI Marketing Automation for Small Business",
        "tag": "Cluster Hub",
        "desc": "How AI marketing automation actually works — email sequences, lead scoring, content scheduling, and ad optimization. What saves time and what creates overhead.",
        "icon": "📣",
        "intro": "Marketing automation has a reputation for being either transformative or a massive time sink. The difference is almost always whether the underlying strategy is solid before automation is applied.",
        "h2_1": "What AI Marketing Automation Actually Covers",
        "body_1": "The term covers a range of tools: email drip campaigns, social media schedulers, lead scoring in your CRM, ad bid management, and content repurposing. The useful parts depend entirely on where your bottleneck is.",
        "checks": ["Automated email sequences for leads who don't convert immediately", "Social media post scheduling (not AI-written copy — that still needs a human)", "Lead scoring — flagging hot leads so sales doesn't waste time on tire-kickers", "Ad bid management on Google/Meta — saves hours of manual adjustment"],
        "h2_2": "What to Be Careful About",
        "body_2": "Generic AI-written marketing content reads exactly like generic AI-written marketing content. Your customers notice. Use automation to scale distribution of good content — not to generate mediocre content at scale.",
        "faqs": [
            ("Does AI marketing automation actually work for small businesses?", "For email sequences and lead nurturing, yes — these are well-proven. For AI-generated ad copy and social content, results are mixed. The tools that work best handle the timing and distribution of your content, not the creation of it."),
            ("What is lead scoring in marketing automation?", "Lead scoring assigns a numeric value to leads based on behavior — pages visited, emails opened, forms filled. It helps you prioritize which leads to contact first. Most CRMs with automation tiers (HubSpot, ActiveCampaign) include this."),
            ("How much does marketing automation cost?", "Entry-level: Mailchimp or ConvertKit at $20–$50/month for email only. Mid-tier: ActiveCampaign or Klaviyo at $50–$200/month with CRM integration. Full platforms: HubSpot Pro+ at $500+/month."),
        ],
        "prev": ("/clusters/ai-scheduling.html", "← AI Scheduling"),
        "next": ("/clusters/ai-workflow-automation.html", "AI Workflow Automation →"),
        "canonical": "https://sideguysolutions.com/clusters/ai-marketing-automation.html",
    },
    {
        "slug": "ai-workflow-automation",
        "title": "AI Workflow Automation — Connecting Your Business Tools",
        "tag": "Cluster Hub",
        "desc": "How AI workflow automation connects your apps and eliminates manual data entry. When automation platforms like Zapier, Make, and n8n actually help — and when they become maintenance overhead.",
        "icon": "⚙️",
        "intro": "Most small business workflow problems are not AI problems — they are integration problems. The same task gets done in three separate tools because no one connected them. Workflow automation fixes that.",
        "h2_1": "The Core Problem Workflow Automation Solves",
        "body_1": "When a new customer books an appointment, does your CRM update automatically? When an invoice is paid, does your project tracker close the job? If the answer is 'someone does that manually,' workflow automation is the right tool.",
        "checks": ["New form submission → CRM entry + Slack notification + welcome email, all automatic", "Invoice paid → project marked complete + client record updated", "New review posted → owner notified + response drafted for review", "Appointment booked → calendar blocked + intake form sent + reminder scheduled"],
        "h2_2": "The Maintenance Problem Nobody Talks About",
        "body_2": "Workflow automations break when the underlying apps update their APIs. A workflow that ran for 6 months without issues can silently fail after a software update. Build in monitoring — even just a weekly sanity check — or you will miss failures until a customer complains.",
        "faqs": [
            ("What is workflow automation?", "Workflow automation connects apps so data flows between them automatically — no manual copy-paste. Tools like Zapier, Make (formerly Integromat), and n8n are the most common platforms."),
            ("Is Zapier worth it for a small business?", "For simple two-step automations (trigger → action), Zapier's free or starter tier is often enough. For complex multi-step workflows with logic and filters, Make tends to be cheaper and more capable at scale."),
            ("What workflows break most often?", "Anything involving a third-party app that updates frequently — especially social media platforms and newer SaaS tools. Google Workspace and Stripe integrations tend to be the most stable."),
        ],
        "prev": ("/clusters/ai-marketing-automation.html", "← AI Marketing Automation"),
        "next": ("/clusters/ai-sales-automation.html", "AI Sales Automation →"),
        "canonical": "https://sideguysolutions.com/clusters/ai-workflow-automation.html",
    },
    {
        "slug": "ai-sales-automation",
        "title": "AI Sales Automation — Lead Follow-Up Without the Friction",
        "tag": "Cluster Hub",
        "desc": "How AI sales automation handles lead follow-up, pipeline tracking, and outreach sequences — so sales happens consistently without relying on memory or manual effort.",
        "icon": "📈",
        "intro": "Most small business sales problems are not strategy problems — they are consistency problems. The follow-up didn't happen because someone forgot, got busy, or felt awkward reaching out again. Automation solves consistency without solving judgment.",
        "h2_1": "Where AI Sales Automation Earns Its Keep",
        "body_1": "The highest-value use is automated follow-up sequences for leads that went quiet. A prospect who didn't respond to your first message often converts on the third or fourth touch — which almost never happens manually.",
        "checks": ["Automated follow-up sequences for non-responsive leads (day 2, day 5, day 10)", "Pipeline stage updates triggered by customer actions (opened email, clicked link, booked call)", "Meeting scheduling links embedded in outreach — no back-and-forth to book a call", "Deal close probability scoring based on engagement history"],
        "h2_2": "What AI Sales Automation Cannot Do",
        "body_2": "It cannot replace the human who actually understands the customer's situation and can adapt the pitch in real time. Automated sequences sent to the wrong person at the wrong time are worse than no outreach — they burn the relationship. Build in list hygiene and opt-out handling from day one.",
        "faqs": [
            ("What is AI sales automation?", "AI sales automation handles the repetitive parts of follow-up — sending timed email or SMS sequences, updating pipeline stages, and flagging high-intent leads — so salespeople focus on conversations that need human judgment."),
            ("What CRMs have the best built-in automation?", "HubSpot (free tier has basics), Pipedrive (affordable, strong automation), Close.io (built for outbound), and Salesforce (powerful but complex). For small service businesses, HubSpot Free or Pipedrive usually covers 90% of needs."),
            ("Is cold outreach automation worth it?", "Only with strong list segmentation and genuinely relevant messaging. Bulk cold email automation with generic copy has very low conversion rates and risks deliverability damage. Targeted sequences to warm or semi-warm leads are a different story."),
        ],
        "prev": ("/clusters/ai-workflow-automation.html", "← AI Workflow Automation"),
        "next": ("/clusters/ai-email-automation.html", "AI Email Automation →"),
        "canonical": "https://sideguysolutions.com/clusters/ai-sales-automation.html",
    },
    {
        "slug": "ai-email-automation",
        "title": "AI Email Automation — Sequences, Triggers, and Deliverability",
        "tag": "Cluster Hub",
        "desc": "How email automation actually works — triggered sequences, broadcast campaigns, deliverability basics, and where AI writing tools help versus hurt your open rates.",
        "icon": "✉️",
        "intro": "Email is still the highest-ROI marketing channel for most small businesses. The gap between businesses that use it well and businesses that don't is almost always automation — not the quality of the product.",
        "h2_1": "The Two Types of Email Automation",
        "body_1": "Behavioral triggers fire when a customer does something — books an appointment, abandons a cart, hasn't visited in 90 days. Scheduled sequences fire on a time-based cadence after a customer is added to a list. Both are useful. Triggers tend to convert better because they are timely.",
        "checks": ["Welcome sequence — 3–5 emails over 2 weeks when a new contact opts in", "Re-engagement sequence — triggered when a customer goes quiet for 60–90 days", "Post-purchase follow-up — review request + upsell 7 days after service", "Appointment reminders — 24 hours and 1 hour before"],
        "h2_2": "The Deliverability Issue Nobody Explains",
        "body_2": "Sending volume, list quality, and engagement rates all affect whether your emails land in the inbox or spam. A list of 1,000 engaged subscribers is worth more than 10,000 unverified cold contacts. Clean your list quarterly. Remove addresses that haven't opened in 6+ months.",
        "faqs": [
            ("What email tools are best for small businesses?", "Mailchimp and ConvertKit for simple lists and broadcasts. ActiveCampaign or Klaviyo for behavioral triggers and deep segmentation. Most businesses should start simple and scale tools only when they hit actual limits."),
            ("Does AI-written email copy work?", "As a first draft, yes. As a final send without human review, no. AI email copy tends toward generic phrases that reduce open rates over time. Use it to beat blank page paralysis, then rewrite in your own voice."),
            ("How often should a small business email its list?", "At minimum, once a month — enough to stay top of mind without being forgotten. The optimal frequency depends on your industry and how much genuinely useful content you can produce. Quality beats volume every time."),
        ],
        "prev": ("/clusters/ai-sales-automation.html", "← AI Sales Automation"),
        "next": ("/clusters/ai-productivity-tools.html", "AI Productivity Tools →"),
        "canonical": "https://sideguysolutions.com/clusters/ai-email-automation.html",
    },
    {
        "slug": "ai-productivity-tools",
        "title": "AI Productivity Tools for Small Business Operators",
        "tag": "Cluster Hub",
        "desc": "The AI tools that actually save operator time — transcription, meeting summaries, document drafting, research, and task management. Honest breakdown of what's worth paying for.",
        "icon": "⚡",
        "intro": "The most useful AI productivity tools are not the flashiest ones. They are the ones that remove a specific recurring friction from your actual workday — quietly, reliably, without requiring a new workflow.",
        "h2_1": "The Tools That Earn Their Subscription",
        "body_1": "These categories consistently save real time for small business operators, regardless of industry.",
        "checks": ["Meeting transcription and summary (Otter.ai, Fireflies) — no more taking notes while trying to listen", "AI dictation for quick replies and documents (faster than typing for most people)", "Document first drafts — proposals, SOPs, job descriptions (edit don't generate)", "Research and competitive intel — summarizing long documents or finding specific data fast", "Image and social media assets — Canva AI, Adobe Firefly for business owners without designers"],
        "h2_2": "What to Skip",
        "body_2": "AI task management tools that predict your next action are mostly noise at the small business level. AI scheduling assistants that email on your behalf cause more confusion than they save. And AI-generated business strategy content is consistently too generic to be actionable. Stick to tools that do one specific thing better than you currently do it manually.",
        "faqs": [
            ("What AI tools are worth paying for as a small business owner?", "Meeting transcription (Otter.ai or Fireflies), a solid AI writing assistant (Claude or ChatGPT Plus), and Canva Pro if you create any visual content. Beyond that, evaluate based on your specific time holes — not general productivity hype."),
            ("Is ChatGPT useful for running a small business?", "Yes for specific tasks: drafting communications, summarizing long documents, generating checklists and SOPs, and brainstorming. It is not useful as a replacement for expertise, local knowledge, or judgment about your specific customers."),
            ("How do I figure out which tasks to use AI for?", "Track your time for one week. Identify the tasks that took the longest and felt the most mechanical. Those are your automation candidates. Ignore anything that requires context only you have."),
        ],
        "prev": ("/clusters/ai-email-automation.html", "← AI Email Automation"),
        "next": ("/intelligence/problem-index.html", "Problem Index →"),
        "canonical": "https://sideguysolutions.com/clusters/ai-productivity-tools.html",
    },
]

for c in guide_clusters:
    faq_html = "\n".join(
        f"""    <div class="faq-item">
      <h3>{q}</h3>
      <p>{a}</p>
    </div>""" for q, a in c["faqs"]
    )
    check_html = "\n".join(f"      <li>{x}</li>" for x in c["checks"])
    bc = schema_breadcrumb([
        ("SideGuy Solutions", "https://sideguysolutions.com"),
        ("AI Automation Hub", "https://sideguysolutions.com/hubs/category-ai-automation.html"),
        (c["title"], c["canonical"]),
    ])
    faq_schema = schema_faq([(q, a) for q, a in c["faqs"]])
    prev_href, prev_label = c["prev"]
    next_href, next_label = c["next"]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{c["title"]} | SideGuy Solutions</title>
<link rel="canonical" href="{c["canonical"]}"/>
<meta name="description" content="{c["desc"]}"/>
<meta property="og:title" content="{c["title"]}"/>
<meta property="og:description" content="{c["desc"]}"/>
<meta property="og:url" content="{c["canonical"]}"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="SideGuy Solutions"/>
<meta property="og:locale" content="en_US"/>
<meta name="twitter:card" content="summary"/>
<script type="application/ld+json">
{bc}
</script>
<script type="application/ld+json">
{faq_schema}
</script>
<style>
{SHARED_STYLE}
</style>
</head>
<body>
<main>
  <nav class="bc">
    <a href="/">SideGuy Solutions</a>
    <span>/</span>
    <a href="/hubs/category-ai-automation.html">AI Automation Hub</a>
    <span>/</span>
    <span>{c["title"].split("—")[0].strip()}</span>
  </nav>

  <span class="tag">{c["tag"]}</span>
  <h1>{c["title"]}</h1>
  <p class="intro">{c["intro"]}</p>

  <div class="card">
    <h2>{c["icon"]} {c["h2_1"]}</h2>
    <p>{c["body_1"]}</p>
    <ul class="checklist">
{check_html}
    </ul>
  </div>

  <div class="card">
    <h2>⚠️ {c["h2_2"]}</h2>
    <p>{c["body_2"]}</p>
  </div>

  <div class="card">
    <h2>Honest Answers</h2>
{faq_html}
  </div>

  <div class="cta-card">
    <h2>Not sure where to start?</h2>
    <p>Text PJ. Describe the friction you are trying to remove and get a plain answer — no product pitch.</p>
    <a class="btn" href="sms:+17735441231">Text PJ · 773-544-1231</a>
  </div>

{RELATED}

  <div class="microFooter">
    <a href="{prev_href}">{prev_label}</a> &nbsp;·&nbsp;
    <a href="{next_href}">{next_label}</a>
  </div>
</main>
{FLOAT_BTN}
</body>
</html>"""

    out = os.path.join(CLUSTERS_DIR, f"{c['slug']}.html")
    with open(out, "w") as f:
        f.write(html)
    print(f"✓ {c['slug']}.html")

print("\nAll cluster pages built.")
