import os, re, json, datetime, urllib.request
from xml.etree import ElementTree as ET

DOMAIN       = "https://sideguysolutions.com"
PHONE_E164   = "+17735441231"
PHONE_PRETTY = "773-544-1231"

# --- Sources (RSS) ---
SOURCES = [
    ("GoogleTrendsDaily", "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"),
    ("HackerNews",        "https://hnrss.org/frontpage"),
]

MUST_MATCH = [
    "stripe", "payment", "processor", "chargeback", "payout",
    "zapier", "webhook", "api", "openai", "claude", "gpt",
    "quickbooks", "invoice", "google ads", "suspended",
    "shopify", "square", "paypal",
    "outage", "down", "cloudflare", "aws", "dns", "ssl",
    "kalshi", "polymarket", "prediction",
]

MAX_ITEMS = 40


def fetch(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": "SideGuyBot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s\-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"\-+", "-", s)
    return s[:80].strip("-") or "trend"


def now_date():
    return datetime.date.today().isoformat()


def ocean_css():
    return """<style>
:root{--ink:#073044;--muted:#3f6173;--line:#cce8f0;--card:#fff;--accent:#1f7cff;--bg0:#eefcff;}
body{font-family:-apple-system,system-ui,sans-serif;max-width:1100px;margin:auto;padding:34px 20px;background:var(--bg0);color:var(--ink);line-height:1.6;}
a{color:var(--accent);text-decoration:none} a:hover{text-decoration:underline}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:14px 0 18px}
.card{border:1px solid var(--line);border-radius:14px;background:var(--card);padding:14px}
.card h2{margin:0 0 8px;font-size:16px}
.small{font-size:13px;color:var(--muted)}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:8px 12px;margin:6px 8px 0 0;font-size:13px;color:var(--ink);background:var(--card)}
hr{border:none;border-top:1px solid var(--line);margin:18px 0}
ol{padding-left:18px} li{margin:8px 0}
code{background:#d7f5ff;padding:2px 6px;border-radius:8px}
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
<a href="/">← SideGuy Home</a> &nbsp;•&nbsp; <a href="/fresh/index.html">Fresh</a> &nbsp;•&nbsp; <a href="/fresh/gravity.html">Gravity</a> &nbsp;•&nbsp; <a href="/authority/authority-hub.html">Authority</a>
{body}
<div class="small" style="margin-top:18px;">Last updated: {now_date()}</div>
{cta()}
</body></html>
"""


def parse_rss(xml_bytes):
    root  = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link  = (item.findtext("link")  or "").strip()
        if title:
            items.append((title, link))
    return items


def is_signal(title):
    t = title.lower()
    return any(k in t for k in MUST_MATCH)


def exists_anywhere(slug):
    targets = [
        f"gravity/{slug}.html",
        f"problems/{slug}.html",
        f"concepts/{slug}.html",
        f"generated/{slug}.html",
        f"auto/{slug}.html",
        f"longtail/{slug}.html",
    ]
    for p in targets:
        if os.path.exists(p):
            return p
    return None


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def build_trend_page(title, link):
    slug  = "gravity-" + slugify(title)
    prior = exists_anywhere(slug)
    if prior:
        return None  # idempotent

    source_pill = f'<a class="pill" href="{link}">Source →</a>' if link else ""

    body = f"""
<h1>{title}</h1>
<p class="small">Traffic Gravity: built from a live trend signal. Routes operators into the right SideGuy help path fast.</p>

<a class="pill" href="/fresh/gravity.html">← Today's Gravity</a>
{source_pill}

<hr>

<h2>What this usually means</h2>
<ol>
  <li><b>Spike in confusion</b> around this topic — something broke or changed.</li>
  <li><b>Operators are searching</b> for the fastest fix, not a tutorial.</li>
  <li><b>SideGuy's job:</b> explain clearly, list safe moves, escalate to a human if needed.</li>
</ol>

<h2>Fast path (SideGuy style)</h2>
<div class="grid">
  <div class="card"><h2>1) Confirm the symptom</h2>
    <div class="small">Error message, payout status, webhook attempts, chargeback reason code, etc.</div></div>
  <div class="card"><h2>2) Check known patterns</h2>
    <div class="small">Outage vs config issue vs provider policy vs timing window.</div></div>
  <div class="card"><h2>3) Take the safe next step</h2>
    <div class="small">Retry logic, idempotency keys, payout schedule, dispute timeline, account verification.</div></div>
</div>

<h2>Related SideGuy hubs</h2>
<ul>
  <li><a href="/authority/payments.html">Payments Authority</a></li>
  <li><a href="/authority/ai-automation.html">AI Automation Authority</a></li>
  <li><a href="/authority/prediction-markets.html">Prediction Markets</a></li>
  <li><a href="/authority/operator-tools.html">Operator Tools</a></li>
</ul>
""".strip()

    html = shell(title, f"Live trend page: {title}. SideGuy quick explanation and safe next steps.", body)
    out  = f"gravity/{slug}.html"
    write(out, html)
    return (title, out)


def build_gravity_hub(built_items):
    cards = [
        f'<div class="card"><h2><a href="/{p.replace(chr(92), "/")}">{t}</a></h2>'
        f'<div class="small">/{p.replace(chr(92), "/")}</div></div>'
        for t, p in built_items
    ]

    body = f"""
<h1>Traffic Gravity</h1>
<p class="small">This page updates when the internet spikes. It's the "be there when the problems arrive" engine.</p>

<a class="pill" href="/fresh/index.html">Freshness Hub</a>
<a class="pill" href="/fresh/radar.html">Fresh Radar</a>

<hr>

<h2>Today's Builds</h2>
<div class="grid">
{"".join(cards) if cards else '<div class="small">No new high-signal trends found today. Re-run later.</div>'}
</div>

<h2>How to use this</h2>
<ol class="small">
  <li>Re-run this script daily or when you notice a spike.</li>
  <li>Pick 3 pages that look like real operator pain.</li>
  <li>Do a quick 2-pass upgrade: Claude adds the operator checklist; GPT polishes clarity + SEO.</li>
</ol>
""".strip()

    write("fresh/gravity.html", shell(
        "Traffic Gravity",
        "Trending operator problems and fresh SideGuy pages built from live signals.",
        body,
    ))


def main():
    all_items = []
    for name, url in SOURCES:
        try:
            xml   = fetch(url)
            items = parse_rss(xml)
            for t, l in items:
                all_items.append((name, t, l))
        except Exception as e:
            print(f"  [warn] {name}: {e}")

    seen   = set()
    signal = []
    for src, title, link in all_items:
        key = title.lower().strip()
        if key in seen:
            continue
        seen.add(key)
        if is_signal(title):
            signal.append((src, title, link))

    signal = signal[:MAX_ITEMS]

    built = []
    for src, title, link in signal:
        r = build_trend_page(title, link)
        if r:
            built.append(r)

    build_gravity_hub(built)

    os.makedirs("reports", exist_ok=True)
    rep = {
        "date":         now_date(),
        "total_signal": len(signal),
        "built_new":    len(built),
        "built_paths":  [p for _, p in built],
    }
    with open("reports/traffic-gravity.json", "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2)

    print("=== Traffic Gravity Done ===")
    print(f"  Signal items : {len(signal)}")
    print(f"  New pages    : {len(built)}")
    print("  fresh/gravity.html")
    print("  reports/traffic-gravity.json")


if __name__ == "__main__":
    main()
