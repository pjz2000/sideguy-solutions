import os, re, json, datetime
from pathlib import Path

DOMAIN       = "https://sideguysolutions.com"
PHONE_E164   = "+17735441231"
PHONE_PRETTY = "773-544-1231"

CATEGORIES = [
    {
        "key":       "payments",
        "title":     "Payments Authority",
        "desc":      "Merchant fees, chargebacks, payout timing, settlement, Stripe/Square/PayPal, and payment system decisions.",
        "match_any": ["payment","payments","processor","processing","stripe","square","paypal","chargeback","payout","settlement","interchange","merchant"],
    },
    {
        "key":       "ai-automation",
        "title":     "AI Automation Authority",
        "desc":      "AI tools, agents, workflows, Zapier/webhooks, and operator automation patterns that save time.",
        "match_any": ["ai","automation","agents","agent","openai","anthropic","claude","gpt","zapier","webhook","workflow"],
    },
    {
        "key":       "google-ads",
        "title":     "Google Ads Authority",
        "desc":      "Suspensions, Merchant Center, tracking, conversions, policy issues, and ad account recovery steps.",
        "match_any": ["google-ads","ads","ad-account","merchant-center","suspended","conversion","gtm","analytics","tracking","policy"],
    },
    {
        "key":       "operator-tools",
        "title":     "Operator Tools Authority",
        "desc":      "CRMs, SOPs, scheduling, invoicing, QuickBooks, HubSpot, and small business operating systems.",
        "match_any": ["crm","sop","hubspot","quickbooks","invoice","invoicing","scheduling","operator","tools","customer-ops","process"],
    },
    {
        "key":       "prediction-markets",
        "title":     "Prediction Markets Authority",
        "desc":      "Kalshi/Polymarket basics, market mechanics, risk framing, and SideGuy's signal & performance lab.",
        "match_any": ["kalshi","polymarket","prediction","markets","prediction-markets","market","trading"],
    },
    {
        "key":       "infrastructure",
        "title":     "Infrastructure Authority",
        "desc":      "DNS, SSL, Cloudflare, outages, APIs, webhooks reliability, and the boring stuff that breaks everything.",
        "match_any": ["dns","ssl","cloudflare","outage","down","api","webhook","server","hosting","aws","latency"],
    },
]

SCAN_DIRS = ["problems","concepts","clusters","hubs","authority","generated","auto","longtail","."]

PATH_PRIORITY = [
    ("hubs/",      1),
    ("clusters/",  2),
    ("concepts/",  3),
    ("problems/",  4),
    ("generated/", 5),
    ("auto/",      6),
    ("longtail/",  7),
    ("/",          9),
]


def now_date():
    return datetime.date.today().isoformat()


def ocean_css():
    return """<style>
:root{--ink:#073044;--muted:#3f6173;--line:#cce8f0;--card:#fff;--accent:#1f7cff;--bg0:#eefcff;--mint:#21d3a1;}
body{font-family:-apple-system,system-ui,sans-serif;max-width:1160px;margin:auto;padding:34px 18px;background:var(--bg0);color:var(--ink);line-height:1.65;}
a{color:var(--accent);text-decoration:none} a:hover{text-decoration:underline}
h1{margin:10px 0 6px;font-size:34px;letter-spacing:-.02em}
h2{margin:22px 0 10px;font-size:18px}
.small{font-size:13px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:12px;margin:12px 0 18px}
.card{border:1px solid var(--line);border-radius:16px;background:var(--card);padding:14px}
.card h3{margin:0 0 8px;font-size:16px}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:8px 12px;margin:6px 8px 0 0;font-size:13px;color:var(--ink);background:var(--card)}
hr{border:none;border-top:1px solid var(--line);margin:18px 0}
ol{padding-left:18px} li{margin:8px 0}
.floatBtn{position:fixed;right:16px;bottom:16px;z-index:9999;background:#073044;color:#fff;border-radius:999px;padding:14px 18px;font-weight:700;text-decoration:none;font-size:14px;box-shadow:0 8px 24px rgba(7,48,68,.25)}
</style>"""


def cta():
    return (
        f'<a class="floatBtn" href="sms:{PHONE_E164}">'
        f"Text PJ &nbsp;·&nbsp; {PHONE_PRETTY}</a>"
    )


def shell(title, desc, body):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{title} · SideGuy Solutions</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
{ocean_css()}
</head>
<body>
<a href="/">← SideGuy Home</a> &nbsp;•&nbsp; <a href="/authority/authority-hub.html">Authority Hub</a> &nbsp;•&nbsp; <a href="/fresh/gravity.html">Gravity</a>
{body}
<div class="small" style="margin-top:18px;">Last updated: {now_date()}</div>
{cta()}
</body></html>
"""


def normalize_url(path: str) -> str:
    path = path.replace("\\", "/")
    if path.startswith("./"):
        path = path[2:]
    if path == "index.html":
        return "/"
    return "/" + path


def path_rank(p: str) -> int:
    p = p.replace("\\", "/")
    for prefix, r in PATH_PRIORITY:
        if prefix == "/" and ("/" not in p or p.count("/") == 0):
            return r
        if p.startswith(prefix):
            return r
    return 50


def extract_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if m:
        t = re.sub(r"\s+", " ", m.group(1)).strip()
        t = re.sub(r"\s*[·|]\s*SideGuy.*$", "", t).strip()
        return t[:90]
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if m:
        t = re.sub(r"<.*?>", "", m.group(1))
        return re.sub(r"\s+", " ", t).strip()[:90]
    return ""


def scan_pages():
    pages = []
    for d in SCAN_DIRS:
        base = Path(d)
        if not base.exists():
            continue
        for p in base.rglob("*.html"):
            sp = str(p).replace("\\", "/")
            if "node_modules/" in sp or ".git/" in sp or "sitemaps/" in sp:
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            title = extract_title(txt) or p.stem.replace("-", " ").title()
            pages.append({
                "path":    sp,
                "url":     normalize_url(sp),
                "title":   title,
                "rank":    path_rank(sp),
                "content": txt[:12000].lower(),
            })
    # dedupe by URL, keep best rank
    best = {}
    for pg in pages:
        u = pg["url"]
        if u not in best or pg["rank"] < best[u]["rank"]:
            best[u] = pg
    return list(best.values())


def pick_for_category(pages, cat, limit=24):
    needles = [n.lower() for n in cat["match_any"]]
    hits    = []
    for pg in pages:
        hay = pg["url"].lower() + " " + pg["title"].lower()
        if any(n in hay for n in needles) or any(n in pg["content"] for n in needles):
            hits.append(pg)
    hits.sort(key=lambda x: (x["rank"], len(x["url"]), x["title"].lower()))
    out, seen = [], set()
    for h in hits:
        if h["url"] in seen:
            continue
        seen.add(h["url"])
        out.append(h)
        if len(out) >= limit:
            break
    return out


def render_cards(items):
    if not items:
        return '<div class="small">No matches found yet — generate more pages in this category and re-run.</div>'
    return "\n".join(
        f'<div class="card"><h3><a href="{it["url"]}">{it["title"]}</a></h3>'
        f'<div class="small">{it["url"]}</div></div>'
        for it in items
    )


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def build_category_hub(cat, items):
    body = (
        f'<h1>{cat["title"]}</h1>\n'
        f'<p class="small">{cat["desc"]}</p>\n\n'
        '<a class="pill" href="/authority/authority-hub.html">← Authority Hub</a>\n\n'
        "<hr>\n\n"
        '<h2>Best Pages (curated automatically)</h2>\n'
        f'<div class="grid">\n{render_cards(items)}\n</div>\n\n'
        '<h2>How SideGuy helps here</h2>\n'
        '<ol class="small">\n'
        "  <li><b>Clarity first:</b> explain the system in plain terms.</li>\n"
        "  <li><b>Safe steps:</b> confirm the symptom → check known patterns → take the next safe move.</li>\n"
        "  <li><b>Human layer:</b> text PJ when it's urgent or confusing.</li>\n"
        "</ol>"
    )
    out = f"authority/{cat['key']}.html"
    write(out, shell(cat["title"], cat["desc"], body))
    return out


def build_master_hub(cat_list):
    cards = "\n".join(
        f'<div class="card"><h3><a href="/authority/{c["key"]}.html">{c["title"]}</a></h3>'
        f'<div class="small">{c["desc"]}</div></div>'
        for c in cat_list
    )
    body = (
        "<h1>Authority Hub</h1>\n"
        '<p class="small">SideGuy\'s organized brain — clusters the site into authority '
        "categories so humans and Google can navigate it like a real system.</p>\n\n"
        '<a class="pill" href="/">Home</a>\n'
        '<a class="pill" href="/fresh/gravity.html">Traffic Gravity</a>\n'
        '<a class="pill" href="/fresh/index.html">Freshness Hub</a>\n\n'
        "<hr>\n\n"
        "<h2>Authority Categories</h2>\n"
        f'<div class="grid">\n{cards}\n</div>\n\n'
        '<h2>How this builds authority</h2>\n'
        '<ol class="small">\n'
        "  <li><b>Hub → cluster → pages</b> structure (clear topical architecture).</li>\n"
        "  <li><b>Internal links</b> that reinforce topic depth.</li>\n"
        "  <li><b>Operator intent</b> framing — not random blog posts.</li>\n"
        "</ol>"
    )
    write("authority/authority-hub.html", shell(
        "Authority Hub",
        "SideGuy authority navigation across payments, AI automation, ads, operator tools, prediction markets, and infrastructure.",
        body,
    ))


def safe_insert(file_path, marker, block):
    if not os.path.exists(file_path):
        return False, f"missing {file_path}"
    txt = Path(file_path).read_text(encoding="utf-8", errors="ignore")
    if marker in txt:
        return True, "already"
    if "</main>" in txt:
        insert_at = "</main>"
    elif "</body>" in txt:
        insert_at = "</body>"
    else:
        return False, "no insert point"
    Path(file_path).write_text(
        txt.replace(insert_at, block + "\n" + insert_at, 1),
        encoding="utf-8",
    )
    return True, "inserted"


def main():
    pages = scan_pages()
    os.makedirs("reports", exist_ok=True)
    with open("reports/authority-scan-count.json", "w", encoding="utf-8") as f:
        json.dump({"date": now_date(), "pages_scanned": len(pages)}, f, indent=2)

    for cat in CATEGORIES:
        items = pick_for_category(pages, cat, limit=24)
        build_category_hub(cat, items)

    build_master_hub(CATEGORIES)

    # Wire into knowledge map
    km_file = next(
        (p for p in ["sideguy-knowledge-map.html", "knowledge/sideguy-knowledge-map.html"]
         if os.path.exists(p)),
        None,
    )
    km_block = """<!-- SIDEGUY_AUTHORITY_ENGINE -->
<hr>
<h2>Authority Navigation</h2>
<p class="small">High-signal entry points into SideGuy's core categories.</p>
<div class="grid">
  <div class="card"><h3><a href="/authority/authority-hub.html">Authority Hub</a></h3><div class="small">Master navigation across core categories.</div></div>
  <div class="card"><h3><a href="/authority/payments.html">Payments</a></h3><div class="small">Fees, chargebacks, payouts, settlement.</div></div>
  <div class="card"><h3><a href="/authority/ai-automation.html">AI Automation</a></h3><div class="small">Agents, workflows, Zapier/webhooks.</div></div>
  <div class="card"><h3><a href="/authority/google-ads.html">Google Ads</a></h3><div class="small">Suspensions, tracking, recovery.</div></div>
  <div class="card"><h3><a href="/authority/operator-tools.html">Operator Tools</a></h3><div class="small">CRM, SOPs, scheduling, invoicing.</div></div>
  <div class="card"><h3><a href="/authority/prediction-markets.html">Prediction Markets</a></h3><div class="small">Kalshi/Polymarket reference + lab.</div></div>
</div>
<!-- /SIDEGUY_AUTHORITY_ENGINE -->"""
    km_status = "skipped (not found)"
    if km_file:
        _, msg = safe_insert(km_file, "<!-- SIDEGUY_AUTHORITY_ENGINE -->", km_block)
        km_status = f"{km_file}: {msg}"

    # Wire into homepage
    home_block = """<!-- SIDEGUY_AUTHORITY_ENGINE_HOME -->
<section style="margin:18px 0;">
  <div style="border:1px solid #cce8f0;border-radius:16px;background:#fff;padding:14px;">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
      <div>
        <div style="font-weight:900;letter-spacing:-.01em;">Authority Hub</div>
        <div style="font-size:13px;color:#3f6173;">Navigate SideGuy like a real OS — Payments, AI, Ads, Operator Tools, Prediction Markets, Infrastructure.</div>
      </div>
      <a href="/authority/authority-hub.html" style="display:inline-block;background:#073044;color:#fff;padding:10px 12px;border-radius:999px;text-decoration:none;font-weight:800;">Open Authority</a>
    </div>
  </div>
</section>
<!-- /SIDEGUY_AUTHORITY_ENGINE_HOME -->"""
    home_status = "skipped"
    if os.path.exists("index.html"):
        _, msg = safe_insert("index.html", "<!-- SIDEGUY_AUTHORITY_ENGINE_HOME -->", home_block)
        home_status = f"index.html: {msg}"

    rep = {
        "date":           now_date(),
        "pages_scanned":  len(pages),
        "authority_pages": ["authority/authority-hub.html"] + [f"authority/{c['key']}.html" for c in CATEGORIES],
        "wired":          {"knowledge_map": km_status, "homepage": home_status},
    }
    with open("reports/authority-engine.json", "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2)

    print("=== Authority Engine Done ===")
    print("  authority/authority-hub.html")
    for c in CATEGORIES:
        print(f"  authority/{c['key']}.html")
    print(f"  Wiring: {km_status} | {home_status}")
    print("  reports/authority-engine.json")


if __name__ == "__main__":
    main()
