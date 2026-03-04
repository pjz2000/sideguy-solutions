#!/usr/bin/env python3
"""
SideGuy Decision Engine — builds /decisions/<slug>.html comparison pages.
Ocean CSS theme, proper sms:+E164 links, topic buckets, idempotent.
"""
import json, os, datetime

PHONE      = "773-544-1231"
PHONE_SMS  = "sms:+17735441231"
PHONE_TEL  = "tel:+17735441231"
DOMAIN     = "https://sideguysolutions.com"

INPUT  = "data/decision_topics.json"
OUT    = "decisions"
INDEX  = f"{OUT}/index.html"

# Talking-points per topic bucket — makes pages non-boilerplate
BUCKET_ROWS = {
    "payments": [
        ("Fee structure",         "Interchange / flat-rate / custom", "Interchange / flat-rate / custom"),
        ("Payout speed",          "Instant, same-day, or next-day options", "Instant, same-day, or next-day options"),
        ("Chargeback process",    "Dispute portal + automated rules", "Dispute portal + automated rules"),
        ("International support", "140+ currencies", "Varies by platform"),
        ("Integration effort",    "API-first, dev-friendly", "SDK / no-code options available"),
    ],
    "ai-automation": [
        ("Model strength",        "Best for structured reasoning / code", "Best for creative + chat tasks"),
        ("API cost",              "Usage-based; varies by model tier",  "Usage-based; varies by model tier"),
        ("No-code options",       "Varies by plan",                     "Native drag-and-drop builder"),
        ("Webhook reliability",   "Near-real-time with retries",        "Near-real-time with retries"),
        ("Operator fit",          "Deep integrations, complex flows",   "Quick setup, easy for small teams"),
    ],
    "prediction-markets": [
        ("Regulatory status",     "CFTC-regulated",                     "Varies / offshore options"),
        ("Available markets",     "Binary + conditional contracts",     "Wide range including crypto"),
        ("Liquidity",             "Growing US user base",               "Global liquidity pool"),
        ("Minimum bet size",      "Varies by contract",                 "Varies by market"),
        ("Withdrawal speed",      "1–3 business days typical",         "Varies; often faster offshore"),
    ],
    "small-business-tech": [
        ("Setup time",            "Hours to days",                      "Hours to days"),
        ("CRM integration",       "Native or via Zapier",               "Native or via API"),
        ("Pricing model",         "Subscription / seats",               "Free tier + paid upgrades"),
        ("Mobile app",            "Available",                          "Available"),
        ("Operator learning curve","Moderate",                          "Low to moderate"),
    ],
}
DEFAULT_ROWS = [
    ("Ease of use",     "Moderate learning curve",    "Moderate learning curve"),
    ("Flexibility",     "High",                       "High"),
    ("Pricing",         "Subscription / usage-based", "Subscription / usage-based"),
    ("Support quality", "Email + docs",               "Email + docs"),
    ("Best for",        "Established workflows",      "Teams wanting alternatives"),
]


def css():
    return """<style>
:root{--bg0:#eefcff;--bg1:#d7f5ff;--ink:#073044;--muted:#3f6173;--line:#cce8f0;
--card:#fff;--mint:#21d3a1;--blue2:#1f7cff;}
*{box-sizing:border-box;}
body{font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,sans-serif;
  background:radial-gradient(ellipse 160% 60% at 50% -10%,var(--bg1),var(--bg0));
  color:var(--ink);max-width:940px;margin:auto;padding:36px 20px 100px;line-height:1.65;}
h1{font-size:clamp(22px,4vw,36px);margin:8px 0 4px;letter-spacing:-.02em;}
h2{font-size:20px;margin:28px 0 10px;}
a{color:var(--blue2);text-decoration:none;} a:hover{text-decoration:underline;}
.breadcrumb{font-size:13px;color:var(--muted);margin-bottom:18px;}
.verdict{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 0 28px;}
@media(max-width:600px){.verdict{grid-template-columns:1fr;}}
.vcard{border:1px solid var(--line);border-radius:16px;background:var(--card);padding:18px;}
.vcard h3{margin:0 0 8px;font-size:16px;}
.vcard p{margin:0;font-size:14px;color:var(--muted);}
table{width:100%;border-collapse:collapse;margin:14px 0 24px;font-size:14px;}
th{background:var(--bg1);text-align:left;padding:10px 12px;border-bottom:2px solid var(--line);}
td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;}
tr:last-child td{border-bottom:none;}
.note{background:var(--bg1);border-left:4px solid var(--mint);border-radius:0 12px 12px 0;
  padding:14px 16px;font-size:14px;margin:24px 0;}
.pills{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0 20px;}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;
  padding:8px 14px;font-size:13px;color:var(--ink);background:var(--card);}
.floatBtn{position:fixed;right:16px;bottom:16px;z-index:9999;background:#073044;
  color:#fff;border-radius:999px;padding:14px 20px;font-weight:700;
  text-decoration:none;font-size:14px;box-shadow:0 8px 24px rgba(7,48,68,.25);}
</style>"""


def shell(title, desc, slug, body):
    today = datetime.date.today().isoformat()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{title} · SideGuy Solutions</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/decisions/{slug}.html">
<meta name="viewport" content="width=device-width,initial-scale=1">
{css()}
</head>
<body>
<div class="breadcrumb">
  <a href="/">SideGuy</a> › <a href="/decisions/index.html">Decisions</a> › {title}
</div>
{body}
<div style="font-size:13px;color:var(--muted);margin-top:24px;">Last updated: {today}</div>
<a class="floatBtn" href="{PHONE_SMS}">Text PJ · {PHONE}</a>
</body></html>
"""


def build_page(t):
    a    = t["a"]
    b    = t["b"]
    slug = t["slug"]
    topic = t.get("topic", "small-business-tech")
    rows  = BUCKET_ROWS.get(topic, DEFAULT_ROWS)

    table_rows = "\n".join(
        f"<tr><td><b>{cat}</b></td><td>{va}</td><td>{vb}</td></tr>"
        for cat, va, vb in rows
    )

    body = f"""
<h1>{a} vs {b}</h1>
<p style="color:var(--muted);font-size:15px;">Operators comparing <strong>{a}</strong> and <strong>{b}</strong> usually want clarity fast — not a 3,000-word sponsored post. Here's the real breakdown.</p>

<div class="verdict">
  <div class="vcard">
    <h3>When to pick {a}</h3>
    <p>Best when you need a mature ecosystem, established integrations, and predictable behavior in production.</p>
  </div>
  <div class="vcard">
    <h3>When to pick {b}</h3>
    <p>Best when you want flexibility, lower cost at scale, or want to avoid vendor lock-in in your stack.</p>
  </div>
</div>

<h2>Side-by-Side Comparison</h2>
<table>
<thead><tr><th>Category</th><th>{a}</th><th>{b}</th></tr></thead>
<tbody>
{table_rows}
</tbody>
</table>

<div class="note">
<strong>SideGuy take:</strong> Neither option is universally "better." The right choice depends on your current stack, team size, and risk tolerance. If you're unsure, the fastest path is a 2-minute text.
</div>

<h2>Switching Costs to Consider</h2>
<ul>
<li><strong>Migration effort:</strong> Data export formats, API parity, downtime risk</li>
<li><strong>Team learning curve:</strong> How long before the new tool is faster than the old one</li>
<li><strong>Contract/lock-in:</strong> Annual commitments, data portability clauses</li>
<li><strong>Hidden fees:</strong> Per-seat, per-transaction, or overage charges at scale</li>
</ul>

<h2>Questions to Ask Before You Decide</h2>
<ol>
<li>What specific problem are you solving — is this a current pain or future-proofing?</li>
<li>Does your team have the capacity to migrate and test properly?</li>
<li>What happens if it doesn't work — is there a rollback plan?</li>
</ol>

<div class="pills">
  <a class="pill" href="/decisions/index.html">← All Comparisons</a>
  <a class="pill" href="/authority/authority-hub.html">Authority Hub</a>
  <a class="pill" href="/problems/">Problem Library</a>
  <a class="pill" href="{PHONE_SMS}">Text PJ for a human take</a>
</div>
"""

    title = f"{a} vs {b}"
    desc  = f"Real comparison of {a} vs {b} — features, pricing, switching costs, and operator insights from SideGuy."
    out   = os.path.join("decisions", f"{slug}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(shell(title, desc, slug, body))
    return out


def build_index(topics):
    cards = []
    for t in topics:
        a, b, slug = t["a"], t["b"], t["slug"]
        topic = t.get("topic", "general")
        cards.append(
            f'<a href="/decisions/{slug}.html" style="text-decoration:none;">'
            f'<div class="vcard" style="transition:box-shadow .15s;">'
            f'<h3 style="margin:0 0 4px;font-size:15px;">{a} vs {b}</h3>'
            f'<div style="font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.5px;">{topic}</div>'
            f"</div></a>"
        )
    grid = "\n".join(cards)
    today = datetime.date.today().isoformat()
    body = f"""
<h1>Decision Hub</h1>
<p style="color:var(--muted);">Clear comparisons for operators who need to choose between tools, platforms, and technologies — without the marketing spin.</p>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:16px;">
{grid}
</div>
<div style="font-size:13px;color:var(--muted);margin-top:24px;">Last updated: {today} · {len(topics)} comparisons</div>
<a class="floatBtn" href="{PHONE_SMS}">Text PJ · {PHONE}</a>
"""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Decision Hub — Tool &amp; Platform Comparisons · SideGuy Solutions</title>
<meta name="description" content="Clear comparisons for operators choosing between tools and platforms. Stripe vs Square, Kalshi vs Polymarket, Claude vs GPT, and more.">
<link rel="canonical" href="{DOMAIN}/decisions/index.html">
<meta name="viewport" content="width=device-width,initial-scale=1">
{css()}
</head>
<body>
<div class="breadcrumb"><a href="/">SideGuy</a> › Decisions</div>
{body}
</body></html>
"""
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(INPUT, encoding="utf-8") as f:
        topics = json.load(f)

    built = []
    skipped = 0
    for t in topics:
        out = os.path.join("decisions", f"{t['slug']}.html")
        if os.path.exists(out):
            skipped += 1
            continue
        build_page(t)
        built.append(t["slug"])

    # Always rebuild index so new topics appear
    build_index(topics)

    print(f"=== Decision Engine Done ===")
    print(f"  Built   : {len(built)}")
    print(f"  Skipped : {skipped} (already exist)")
    print(f"  Index   : {INDEX}")


if __name__ == "__main__":
    main()
