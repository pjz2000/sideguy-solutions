#!/usr/bin/env python3
# ==============================================================
# SIDEGUY PROBLEM HUB BUILDER
# Creates problems/index.html — categorized index of all
# problem guide pages in problems/ directory.
# Ocean light CSS theme. Phone 773-544-1231.
# ==============================================================

import os, datetime

PHONE_D  = "773-544-1231"
PHONE_S  = "+17735441231"
DOMAIN   = "https://sideguysolutions.com"
DIR      = "problems"
OUT      = os.path.join(DIR, "index.html")
TODAY    = datetime.date.today().isoformat()

BUCKET_ORDER = [
    "Payments",
    "Customer Ops",
    "Systems & Automation",
    "AI & Tools",
    "Crypto & Payments",
    "Prediction Markets",
    "General Operator Problems",
]

BUCKET_ICONS = {
    "Payments":               "💳",
    "Customer Ops":           "📞",
    "Systems & Automation":   "⚙️",
    "AI & Tools":             "🤖",
    "Crypto & Payments":      "🔗",
    "Prediction Markets":     "📈",
    "General Operator Problems": "🗂️",
}

BUCKET_DESCS = {
    "Payments":               "Fees, chargebacks, fraud, settlement, processor choice.",
    "Customer Ops":           "Missed calls, reviews, reply templates, lead capture.",
    "Systems & Automation":   "Scheduling, SOPs, CRM, invoicing, workflows.",
    "AI & Tools":             "Agents, AI workflows — where AI helps, where it doesn't.",
    "Crypto & Payments":      "Stablecoins, Solana, crypto-rail settlements.",
    "Prediction Markets":     "Kalshi, Polymarket, hedging, betting strategy.",
    "General Operator Problems": "Broader small-business guides that span categories.",
}

def guess_bucket(slug: str) -> str:
    s = slug.lower()
    if any(k in s for k in ["payment","fee","fees","interchange","chargeback","fraud","processor","processing","settlement","pci","markup","stripe","square"]):
        return "Payments"
    if any(k in s for k in ["missed-call","missed_call","customer","review","reply","text","sms","lead","follow","support","intake","call-summary","call_summary"]):
        return "Customer Ops"
    if any(k in s for k in ["schedule","scheduling","booking","appointment","crm","invoic","workflow","sop","process","automation","system","systems","dashboard","ops"]):
        return "Systems & Automation"
    if any(k in s for k in ["ai","agent","gpt","bot","copilot","ml","machine-learning","machine_learning"]):
        return "AI & Tools"
    if any(k in s for k in ["crypto","wallet","stablecoin","solana","token","blockchain"]):
        return "Crypto & Payments"
    if any(k in s for k in ["prediction","kalshi","polymarket","market","bet","hedge","hedging"]):
        return "Prediction Markets"
    return "General Operator Problems"

def title_from_filename(fn: str) -> str:
    base = fn.replace(".html","").replace("-"," ").replace("_"," ")
    return " ".join(w.capitalize() for w in base.split())

def build():
    if not os.path.isdir(DIR):
        print(f"ERROR: {DIR}/ not found"); return

    pages = sorted(f for f in os.listdir(DIR) if f.endswith(".html") and f != "index.html")
    buckets = {}
    for fn in pages:
        b = guess_bucket(fn.replace(".html",""))
        buckets.setdefault(b, []).append((fn, title_from_filename(fn)))

    # stat cards
    stat_cards = "".join(
        f"""  <div style="background:rgba(255,255,255,.8);border:1px solid rgba(0,0,0,.08);border-radius:18px;padding:18px 22px;text-align:center">
    <div style="font-size:1.6rem">{BUCKET_ICONS.get(b,'📄')}</div>
    <div style="font-weight:700;margin:6px 0 3px">{b}</div>
    <div style="font-size:.82rem;color:#3f6173">{BUCKET_DESCS.get(b,'')}</div>
  </div>\n"""
        for b in BUCKET_ORDER if b in buckets
    )

    # bucket sections
    sections_html = ""
    for b in BUCKET_ORDER:
        if b not in buckets:
            continue
        icon = BUCKET_ICONS.get(b, "📄")
        items = buckets[b]
        links = "".join(
            f'      <li><a href="/problems/{fn}" style="color:#1f7cff">{title}</a></li>\n'
            for fn, title in items
        )
        sections_html += f"""<section style="margin-bottom:36px">
  <h2 style="font-size:1.2rem;font-weight:800;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #d7f5ff">{icon} {b}</h2>
  <ul style="columns:2;column-gap:28px;list-style:disc;padding-left:20px;font-size:.92rem;line-height:1.9">
{links}  </ul>
</section>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Operator Problem Guides | SideGuy Solutions</title>
  <meta name="description" content="{len(pages)}+ operator problem guides covering payments, customer ops, AI tools, scheduling & automation. Clarity before cost — SideGuy Solutions San Diego."/>
  <link rel="canonical" href="{DOMAIN}/problems/"/>
  <meta name="robots" content="index,follow"/>
  <style>
  :root{{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--blue2:#1f7cff;--r:18px;--pill:999px}}
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;background:radial-gradient(ellipse at 60% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);color:var(--ink);min-height:100vh}}
  a{{color:var(--blue2);text-decoration:none}}a:hover{{text-decoration:underline}}
  nav.bc{{padding:11px 24px;font-size:.8rem;color:var(--muted);border-bottom:1px solid rgba(0,0,0,.06);background:rgba(255,255,255,.6);backdrop-filter:blur(6px);position:sticky;top:0;z-index:10}}
  nav.bc a{{color:var(--muted)}}
  .wrap{{max-width:940px;margin:0 auto;padding:44px 24px 100px}}
  h1{{font-size:clamp(1.7rem,5vw,2.6rem);font-weight:800;margin-bottom:8px}}
  .sub{{color:var(--muted);margin-bottom:28px;font-size:1rem}}
  .grid3{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;margin-bottom:40px}}
  .floating{{position:fixed;bottom:22px;right:22px;z-index:999}}
  .floatBtn{{display:flex;align-items:center;gap:8px;background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.2)}}
  .floatBtn:hover{{opacity:.92;text-decoration:none}}
  footer{{text-align:center;padding:18px;font-size:.76rem;color:var(--muted);border-top:1px solid rgba(0,0,0,.06);margin-top:36px}}
  @media(max-width:640px){{ul[style*="columns:2"]{{columns:1!important}}}}
  </style>
</head>
<body>
<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> ›
  <a href="/knowledge-hub.html">Knowledge Hub</a> ›
  Problem Guides
</nav>
<main class="wrap">
  <h1>Operator Problem Guides</h1>
  <p class="sub">If Google discovers the problem, SideGuy explains it — and a real human can help resolve it. {len(pages)} guides across {len(buckets)} categories.</p>

  <div class="grid3">
{stat_cards}  </div>

{sections_html}
  <div style="background:linear-gradient(135deg,#073044,#0e3d58);border-radius:18px;padding:26px 30px;color:#fff;display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin-top:28px">
    <div>
      <div style="font-weight:700;font-size:1.1rem;margin-bottom:4px">Don't see your problem?</div>
      <div style="font-size:.9rem;opacity:.8">Text PJ a quick description. Real human, San Diego. No pitch.</div>
    </div>
    <a href="sms:{PHONE_S}" style="flex-shrink:0;background:#21d3a1;color:#073044;font-weight:700;padding:11px 20px;border-radius:999px;text-decoration:none">💬 Text {PHONE_D}</a>
  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/knowledge-hub.html">Knowledge Hub</a> ·
    <a href="/payments.html">Payments</a> ·
    <a href="/ai-automation-hub.html">AI Automation</a>
    <br><small>Updated {TODAY} · {len(pages)} problem guides</small>
  </footer>
</main>
<div class="floating">
  <a class="floatBtn" href="sms:{PHONE_S}">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
    Text PJ · {PHONE_D}
  </a>
</div>
</body>
</html>
"""
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"  Built {OUT}  ({len(pages)} pages across {len(buckets)} buckets)")

if __name__ == "__main__":
    print("=== Problem Hub Builder ===\n")
    build()
