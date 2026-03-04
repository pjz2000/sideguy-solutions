#!/usr/bin/env python3
# ==============================================================
# SIDEGUY TRAFFIC MULTIPLIER
# Builds 6 crawler hub pages in hubs/ — each with up to 500
# links drawn from all content directories. Helps crawlers
# and internal link equity flow across the whole site.
# Ocean light CSS. Idempotent — rebuilds on every run.
# ==============================================================

import os, random, datetime
from pathlib import Path

ROOT        = Path(__file__).parent.parent
OUT_DIR     = ROOT / "hubs"
OUT_DIR.mkdir(exist_ok=True)

CONTENT_DIRS = ["problems", "auto", "concepts", "clusters", "pillars", "generated", "prediction-markets"]
MAX_LINKS    = 500
DOMAIN       = "https://sideguysolutions.com"
PHONE_D      = "773-544-1231"
PHONE_S      = "+17735441231"
TODAY        = datetime.date.today().isoformat()

HUBS = [
    ("top-guides",                "Top Operator Guides",             "📋", "Most-referenced guides across payments, AI automation, and operator systems."),
    ("operator-problems",         "Operator Problem Library",        "🗂️", "Real-world problems small businesses deal with every day — payments, systems, and ops."),
    ("ai-automation-guides",      "AI Automation Guides",            "🤖", "Where AI actually helps operators: scheduling, follow-up, intake, and more."),
    ("payments-guides",           "Payments & Fees Guides",          "💳", "Interchange, chargebacks, processor fees, settlement — the full payments knowledge base."),
    ("prediction-markets-guides", "Prediction Markets Guides",       "📈", "Kalshi, Polymarket, hedging strategies, and structured probability trading."),
    ("operator-playbooks",        "Operator Playbooks",              "🏆", "Step-by-step systems for common business operations — built for the working owner."),
]

# Per-hub slug token filters (empty = all pages)
HUB_FILTERS = {
    "ai-automation-guides":      ["ai","agent","automation","workflow","schedule","sop","crm","invoice","bot","gpt"],
    "payments-guides":           ["payment","fee","fees","interchange","chargeback","fraud","stripe","square","pci","settlement","processor","merchant"],
    "prediction-markets-guides": ["prediction","kalshi","polymarket","market","hedge","hedging","sports","betting","dfs"],
}

CSS = """  :root{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--mint:#21d3a1;--blue2:#1f7cff;--r:18px;--pill:999px}
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;background:radial-gradient(ellipse at 60% 0%,#c5f4ff 0%,#eefcff 55%,#fff 100%);color:var(--ink);min-height:100vh}
  a{color:var(--blue2);text-decoration:none}a:hover{text-decoration:underline}
  nav.bc{padding:11px 24px;font-size:.8rem;color:var(--muted);border-bottom:1px solid rgba(0,0,0,.06);background:rgba(255,255,255,.6);backdrop-filter:blur(6px);position:sticky;top:0;z-index:10}
  nav.bc a{color:var(--muted)}
  .wrap{max-width:1100px;margin:0 auto;padding:40px 24px 80px}
  .badge{display:inline-block;background:var(--mint);color:#073044;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 12px;border-radius:var(--pill);margin-bottom:10px}
  h1{font-size:clamp(1.5rem,4vw,2.3rem);font-weight:800;margin-bottom:6px}
  .sub{color:var(--muted);font-size:.95rem;margin-bottom:28px}
  .link-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:6px;margin-bottom:32px}
  .link-card{background:rgba(255,255,255,.78);border:1px solid rgba(0,0,0,.07);border-radius:12px;padding:10px 14px;font-size:.87rem;font-weight:500;color:var(--ink);display:block;line-height:1.35}
  .link-card:hover{background:var(--bg1);text-decoration:none}
  .hub-nav{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:30px}
  .hub-pill{background:rgba(255,255,255,.8);border:1px solid rgba(0,0,0,.08);border-radius:var(--pill);padding:7px 14px;font-size:.83rem;font-weight:500;color:var(--ink)}
  .hub-pill:hover{background:var(--mint);color:#073044;text-decoration:none}
  .floating{position:fixed;bottom:22px;right:22px;z-index:999}
  .floatBtn{display:flex;align-items:center;gap:8px;background:linear-gradient(135deg,#0e3d58,#073044);color:#fff;padding:11px 18px;border-radius:var(--pill);font-size:.88rem;font-weight:600;text-decoration:none;box-shadow:0 4px 18px rgba(0,0,0,.2)}
  footer{text-align:center;padding:16px;font-size:.75rem;color:var(--muted);border-top:1px solid rgba(0,0,0,.06);margin-top:28px}"""

def collect_pages():
    pages = []
    for d in CONTENT_DIRS:
        if not (ROOT / d).is_dir():
            continue
        for f in os.listdir(ROOT / d):
            if f.endswith(".html"):
                pages.append((d, f))
    return pages

def matches_filter(fn: str, filters: list) -> bool:
    s = fn.lower()
    return any(k in s for k in filters)

def label(fn: str) -> str:
    return fn.replace(".html","").replace("-"," ").replace("_"," ").title()

def build_hub(slug, title, icon, desc, all_pages):
    filters = HUB_FILTERS.get(slug, [])
    if filters:
        pool = [(d, f) for d, f in all_pages if matches_filter(f, filters)]
        # pad with random pages if pool is too small
        if len(pool) < 50:
            others = [(d, f) for d, f in all_pages if (d, f) not in pool]
            pool += random.sample(others, min(50 - len(pool), len(others)))
    else:
        pool = all_pages

    selected = random.sample(pool, min(MAX_LINKS, len(pool)))

    # Build other-hub nav pills
    hub_pills = "".join(
        f'  <a class="hub-pill" href="/hubs/{h}.html">{ht}</a>\n'
        for h, ht, _, _ in HUBS if h != slug
    )

    # Build link grid
    link_cards = "".join(
        f'  <a class="link-card" href="/{d}/{f}">{label(f)}</a>\n'
        for d, f in selected
    )

    canonical = f"{DOMAIN}/hubs/{slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{icon} {title} | SideGuy Solutions</title>
  <meta name="description" content="{desc} {len(selected)} hand-picked operator guides from SideGuy Solutions."/>
  <link rel="canonical" href="{canonical}"/>
  <meta name="robots" content="index,follow"/>
  <style>
{CSS}
  </style>
</head>
<body>
<nav class="bc" aria-label="Breadcrumb">
  <a href="/">SideGuy</a> ›
  <a href="/knowledge-hub.html">Knowledge Hub</a> ›
  {title}
</nav>
<main class="wrap">
  <div class="badge">Crawler Hub · {len(selected)} Guides</div>
  <h1>{icon} {title}</h1>
  <p class="sub">{desc}</p>

  <nav class="hub-nav" aria-label="Other hubs">
{hub_pills}  </nav>

  <div class="link-grid">
{link_cards}  </div>

  <footer>
    <a href="/">SideGuy Solutions</a> ·
    <a href="/knowledge-hub.html">Knowledge Hub</a> ·
    <a href="/problems/">Problem Library</a> ·
    <a href="tel:{PHONE_S}">{PHONE_D}</a>
    <br><small>Updated {TODAY} · {len(selected)} guides listed</small>
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

if __name__ == "__main__":
    print("=== Traffic Multiplier ===\n")
    all_pages = collect_pages()
    print(f"  Pages found: {len(all_pages)}")

    for slug, title, icon, desc in HUBS:
        html = build_hub(slug, title, icon, desc, all_pages)
        out  = OUT_DIR / f"{slug}.html"
        out.write_text(html, encoding="utf-8")
        print(f"  BUILT hubs/{slug}.html")

    print(f"\n  {len(HUBS)} hub pages written to hubs/")
