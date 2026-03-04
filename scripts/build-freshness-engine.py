import os, re, datetime, collections

DOMAIN     = "https://sideguysolutions.com"
PHONE      = "773-544-1231"
PHONE_HREF = "+17735441231"

SCAN_DIRS = [
    "authority", "hubs", "concepts", "problems",
    "auto", "generated", "clusters", "longtail",
]
EXCLUDE_PARTS = [
    "/node_modules/", "/.git/", "/dist/", "/build/",
    "/out/", "/tmp/", "/reports/", "/sitemaps/",
]

MAX_NEW   = 120
MAX_TREND = 120


def ok_path(p):
    p = p.replace("\\", "/")
    if not p.endswith(".html"):
        return False
    for x in EXCLUDE_PARTS:
        if x in p:
            return False
    return True


def href(path):
    return "/" + path.replace("\\", "/")


def title_from_path(path):
    fn = os.path.basename(path).replace(".html", "").replace("-", " ")
    return " ".join(w.capitalize() for w in fn.split())


def style():
    return """<style>
:root{--ink:#073044;--muted:#3f6173;--line:#cce8f0;--card:#fff;--accent:#1f7cff;--bg0:#eefcff;}
body{font-family:-apple-system,system-ui,sans-serif;max-width:1100px;margin:auto;padding:34px 20px;background:var(--bg0);color:var(--ink);line-height:1.6;}
a{color:var(--accent);text-decoration:none} a:hover{text-decoration:underline}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:8px 12px;margin:6px 8px 0 0;font-size:13px;color:var(--ink);background:var(--card)}
.small{font-size:13px;color:var(--muted)}
hr{border:none;border-top:1px solid var(--line);margin:18px 0}
ol{padding-left:18px} li{margin:8px 0}
.floatBtn{position:fixed;right:16px;bottom:16px;z-index:9999;background:#073044;color:#fff;border-radius:999px;padding:14px 18px;font-weight:700;text-decoration:none;font-size:14px;box-shadow:0 8px 24px rgba(7,48,68,.25)}
</style>"""


def cta():
    return f'<a class="floatBtn" href="sms:{PHONE_HREF}">Text PJ &nbsp;·&nbsp; {PHONE}</a>'


def shell(title, desc, body):
    today = datetime.date.today().isoformat()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{title} · SideGuy Solutions</title>
<meta name="description" content="{desc}">
<meta name="viewport" content="width=device-width, initial-scale=1">
{style()}
</head>
<body>
<a href="/">← SideGuy Home</a> &nbsp;•&nbsp; <a href="/fresh/index.html">Fresh</a> &nbsp;•&nbsp; <a href="/authority/index.html">Authority</a> &nbsp;•&nbsp; <a href="/sideguy-knowledge-map.html">Knowledge Map</a>
{body}
<div class="small" style="margin-top:18px;">Last updated: {today}</div>
{cta()}
</body></html>
"""


def list_pages():
    pages = []
    for d in SCAN_DIRS:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for fn in files:
                p = os.path.join(root, fn).replace("\\", "/")
                if ok_path(p):
                    pages.append(p)
    return sorted(set(pages))


def newest_pages(pages):
    items = []
    for p in pages:
        try:
            m = os.path.getmtime(p)
        except Exception:
            continue
        items.append((m, p))
    items.sort(key=lambda x: -x[0])
    return items[:MAX_NEW]


LINK_RE = re.compile(r'href="([^"]+\.html)"')


def trending_pages(pages):
    counts = collections.Counter()
    known  = set(href(p) for p in pages)
    for p in pages:
        try:
            html = open(p, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for h in LINK_RE.findall(html):
            if h.startswith("http"):
                continue
            h = ("/" + h) if not h.startswith("/") else h
            h = h.split("#")[0].split("?")[0]
            if h in known:
                counts[h] += 1
    return counts.most_common(MAX_TREND)


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)


def build():
    pages = list_pages()
    new   = newest_pages(pages)
    trend = trending_pages(pages)

    # fresh/index.html
    new_list = [
        f'<li><a href="{href(p)}">{title_from_path(p)}</a> '
        f'<span class="small">({datetime.datetime.fromtimestamp(m).strftime("%Y-%m-%d %H:%M")})</span></li>'
        for m, p in new
    ]
    body = (
        "<h1>Freshness Hub</h1>\n"
        '<p class="small">This page is intentionally updated often to encourage frequent crawling. '
        "It highlights recently updated SideGuy guides and the most-referenced pages inside the site.</p>\n"
        '<a class="pill" href="/fresh/trending.html">View Trending →</a>\n'
        '<a class="pill" href="/authority/index.html">Authority Engine →</a>\n'
        "<hr>\n"
        "<h2>Recently Updated</h2>\n<ol>\n"
        + ("\n".join(new_list) if new_list else '<li class="small">No pages found yet.</li>')
        + "\n</ol>"
    )
    write("fresh/index.html", shell(
        "Freshness Hub",
        "Recently updated SideGuy pages and trending internal guides.",
        body,
    ))

    # fresh/trending.html
    trend_list = [
        f'<li><a href="{h}">{h}</a> <span class="small">({c} internal links)</span></li>'
        for h, c in trend
    ]
    body2 = (
        "<h1>Trending Inside SideGuy</h1>\n"
        '<p class="small">Pages most referenced inside the site — a strong crawl + authority signal.</p>\n'
        '<a class="pill" href="/fresh/index.html">← Back to Fresh</a>\n'
        "<hr>\n"
        "<h2>Top Linked Pages</h2>\n<ol>\n"
        + ("\n".join(trend_list) if trend_list else '<li class="small">No link data yet.</li>')
        + "\n</ol>"
    )
    write("fresh/trending.html", shell(
        "Trending",
        "Pages most linked inside SideGuy.",
        body2,
    ))

    print("=== Freshness Engine Built ===")
    print("  fresh/index.html")
    print("  fresh/trending.html")
    print(f"  New entries  : {len(new)}")
    print(f"  Trend entries: {len(trend)}")


if __name__ == "__main__":
    build()
