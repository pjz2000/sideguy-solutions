import os, re, csv, datetime, collections

PHONE      = "773-544-1231"
PHONE_HREF = "+17735441231"
DOMAIN     = "https://sideguysolutions.com"

MAP_PATH = "authority/authority-map.tsv"
OUT_DIR  = "authority"

SCAN_DIRS = [
    "problems", "auto", "concepts", "prediction-markets",
    "betting-lab", "generated", "longtail", "hubs",
]

MAX_PAGES_PER_CLUSTER = 80
MAX_TOP_PAGES         = 60


def list_html_pages():
    pages = []
    for d in SCAN_DIRS:
        if not os.path.isdir(d):
            continue
        for root, _, files in os.walk(d):
            for fn in files:
                if fn.endswith(".html"):
                    rel = os.path.join(root, fn).replace("\\", "/")
                    pages.append(rel)
    return sorted(set(pages))


def file_tokens(path):
    fn   = os.path.basename(path).replace(".html", "")
    stop = {
        "for", "and", "the", "a", "an", "to", "of",
        "in", "on", "with", "without", "my", "your",
        "business", "guide", "explained",
    }
    return [p for p in fn.split("-") if p and p not in stop]


def score_page(path, keywords):
    toks = set(file_tokens(path))
    sc   = 0
    for k in keywords:
        if k in toks:
            sc += 3
        if any(k in t for t in toks):
            sc += 1
    if path.startswith("problems/"):
        sc += 2
    if path.startswith("concepts/"):
        sc += 2
    if "index" in os.path.basename(path):
        sc += 1
    return sc


def title_from_path(path):
    fn = os.path.basename(path).replace(".html", "").replace("-", " ")
    return " ".join(w.capitalize() for w in fn.split())


def href_from_path(path):
    return "/" + path.replace("\\", "/")


def read_map():
    topics = collections.OrderedDict()
    with open(MAP_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            tslug = r["topic_slug"].strip()
            if not tslug:
                continue
            topics.setdefault(tslug, {
                "topic_title": r["topic_title"].strip(),
                "clusters":    [],
            })
            topics[tslug]["clusters"].append({
                "cluster_slug":  r["cluster_slug"].strip(),
                "cluster_title": r["cluster_title"].strip(),
                "keywords":      [k.strip() for k in r["keywords"].split() if k.strip()],
            })
    return topics


def style():
    return """<style>
:root{--ink:#073044;--muted:#3f6173;--line:#cce8f0;--card:#fff;--accent:#1f7cff;--bg0:#eefcff;--mint:#21d3a1;}
body{font-family:-apple-system,system-ui,sans-serif;max-width:1100px;margin:auto;padding:34px 20px;background:var(--bg0);color:var(--ink);line-height:1.6;}
a{color:var(--accent);text-decoration:none} a:hover{text-decoration:underline}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:14px 0 18px}
.card{border:1px solid var(--line);border-radius:14px;background:var(--card);padding:14px}
.card h2{margin:0 0 8px;font-size:16px;color:var(--ink)}
.small{font-size:13px;color:var(--muted)}
.pills a{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:8px 12px;margin:6px 8px 0 0;font-size:13px;color:var(--ink);background:var(--card)}
.floatBtn{position:fixed;right:16px;bottom:16px;z-index:9999;background:#073044;color:#fff;border-radius:999px;padding:14px 18px;font-weight:700;text-decoration:none;font-size:14px;box-shadow:0 8px 24px rgba(7,48,68,.25)}
</style>"""


def cta():
    return (
        f'<a class="floatBtn" href="sms:{PHONE_HREF}">Text PJ &nbsp;·&nbsp; {PHONE}</a>'
    )


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def page_shell(title, desc, body, canon_path=""):
    today = datetime.date.today().isoformat()
    canon = f'<link rel="canonical" href="{DOMAIN}/{canon_path}">' if canon_path else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{title} · SideGuy Solutions</title>
<meta name="description" content="{desc}">
{canon}
<meta name="viewport" content="width=device-width, initial-scale=1">
{style()}
</head>
<body>
<a href="/">← SideGuy Home</a> &nbsp;•&nbsp; <a href="/sideguy-knowledge-map.html">Knowledge Map</a> &nbsp;•&nbsp; <a href="/problems/">Problem Library</a>
{body}
<div class="small" style="margin-top:18px;">Last updated: {today}</div>
{cta()}
</body></html>
"""


def build():
    topics = read_map()
    pages  = list_html_pages()

    # Score pages per cluster
    cluster_best = {}
    for tslug, t in topics.items():
        for c in t["clusters"]:
            key    = (tslug, c["cluster_slug"])
            scored = []
            for p in pages:
                sc = score_page(p, c["keywords"])
                if sc > 0:
                    scored.append((sc, p))
            scored.sort(key=lambda x: (-x[0], x[1]))
            cluster_best[key] = [p for _, p in scored[:MAX_PAGES_PER_CLUSTER]]

    # /authority/index.html
    cards = []
    for tslug, t in topics.items():
        cards.append(
            f'<div class="card"><h2><a href="/authority/{tslug}.html">'
            f'{t["topic_title"]}</a></h2>'
            f'<div class="small">Clusters: {len(t["clusters"])}</div></div>'
        )
    body = (
        "<h1>SideGuy Authority Engine</h1>\n"
        '<p class="small">High-level topic hubs → cluster hubs → best guides. '
        "Built to help humans and help crawlers.</p>\n"
        f'<div class="grid">\n{"".join(cards)}\n</div>'
    )
    write(
        os.path.join(OUT_DIR, "index.html"),
        page_shell("Authority Engine", "SideGuy topic authority hubs.", body),
    )

    # Topic pages + cluster pages
    for tslug, t in topics.items():
        cl_cards = []
        for c in t["clusters"]:
            cl_cards.append(
                f'<div class="card"><h2>'
                f'<a href="/authority/{tslug}/{c["cluster_slug"]}.html">'
                f'{c["cluster_title"]}</a></h2>'
                f'<div class="small">Keywords: {" ".join(c["keywords"][:6])}</div>'
                f"</div>"
            )
        t_body = (
            f'<h1>{t["topic_title"]}</h1>\n'
            '<p class="small">Cluster hubs for this authority topic.</p>\n'
            f'<div class="grid">\n{"".join(cl_cards)}\n</div>'
        )
        write(
            os.path.join(OUT_DIR, f"{tslug}.html"),
            page_shell(t["topic_title"], f'{t["topic_title"]} hub and clusters.', t_body),
        )

        # Cluster pages
        for c in t["clusters"]:
            key  = (tslug, c["cluster_slug"])
            best = cluster_best.get(key, [])
            items = [
                f'<li><a href="{href_from_path(p)}">{title_from_path(p)}</a> '
                f'<span class="small">({p})</span></li>'
                for p in best[:MAX_TOP_PAGES]
            ]
            cl_body = (
                f'<h1>{c["cluster_title"]}</h1>\n'
                f'<p class="small"><a href="/authority/{tslug}.html">← Back to {t["topic_title"]}</a></p>\n'
                '<div class="pills">'
                '<a href="/authority/index.html">Authority Index</a>'
                '<a href="/concepts/index.html">Concepts</a>'
                '<a href="/problems/">Problems</a>'
                "</div>\n"
                '<h2 style="margin-top:18px;">Best Guides</h2>\n'
                "<ul>\n"
                + (
                    "\n".join(items)
                    if items
                    else '<li class="small">No matches yet — add keywords or generate more pages.</li>'
                )
                + "\n</ul>"
            )
            write(
                os.path.join(OUT_DIR, tslug, f'{c["cluster_slug"]}.html'),
                page_shell(
                    c["cluster_title"],
                    f'{c["cluster_title"]} guides and related pages.',
                    cl_body,
                ),
            )

    print("=== Authority Engine Built ===")
    print(f"  Topics   : {len(topics)}")
    total_clusters = sum(len(t['clusters']) for t in topics.values())
    print(f"  Clusters : {total_clusters}")
    print(f"  Pages    : 1 index + {len(topics)} topic + {total_clusters} cluster")
    print(f"  Written to: {OUT_DIR}/")


if __name__ == "__main__":
    build()
