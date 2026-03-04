#!/usr/bin/env python3
"""
SideGuy Knowledge Graph Engine (Wiki Brain)
- Walks all content dirs, extracts page metadata + internal links
- Outputs: knowledge/knowledge-graph.html + reports/knowledge-graph.json
- Injects a card into knowledge map, knowledge hub, and homepage (marker-based, idempotent)
- Uses sms:+17735441231 (no dashes in href)
"""
import os, re, json, hashlib, datetime
from urllib.parse import urlparse

SITE_HOST = "sideguysolutions.com"
SITE_BASE = f"https://{SITE_HOST}"
SMS_HREF  = "sms:+17735441231"

INCLUDE_DIRS = [
    ".", "pillars", "clusters", "concepts", "problems", "generated",
    "longtail", "decisions", "authority", "auto", "prediction-markets",
    "fresh", "gravity", "katie", "knowledge",
]

EXCLUDE_DIRS  = {".git", ".github", "node_modules", "dist", "build",
                 "__pycache__", "sitemaps", "radar", "reports"}
EXCLUDE_FILES = {"sitemap.xml", "sitemap-index.xml", "robots.txt"}

KG_CARD_START = "<!-- SG_KNOWLEDGE_GRAPH_CARD_START -->"
KG_CARD_END   = "<!-- SG_KNOWLEDGE_GRAPH_CARD_END -->"


def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def rel_to_url(rel: str) -> str:
    return f"{SITE_BASE}/{rel.lstrip('./')}"


def url_to_rel(url: str) -> str:
    try:
        u = urlparse(url)
        if u.netloc and u.netloc != SITE_HOST:
            return ""
        p = u.path.lstrip("/")
        if not p:
            return "index.html"
        if p.endswith("/"):
            p += "index.html"
        return p
    except Exception:
        return ""


def bucket_for_path(rel: str) -> str:
    if rel == "index.html":
        return "root"
    top = rel.split("/")[0]
    if top in {"pillars", "clusters", "concepts", "problems", "generated",
               "longtail", "decisions", "authority", "auto", "knowledge",
               "prediction-markets", "fresh", "gravity", "katie"}:
        return top
    return "other"


TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
H1_RE    = re.compile(r"<h1[^>]*>(.*?)</h1>",  re.I | re.S)
A_RE     = re.compile(r'<a\s[^>]*href=["\']([^"\']+)["\']', re.I)


def extract_meta(html: str):
    title = h1 = ""
    m = TITLE_RE.search(html)
    if m:
        title = clean_text(re.sub("<.*?>", "", m.group(1)))
    m = H1_RE.search(html)
    if m:
        h1 = clean_text(re.sub("<.*?>", "", m.group(1)))
    return title, h1


def extract_links(html: str) -> list[str]:
    out, seen = [], set()
    for href in A_RE.findall(html):
        href = href.strip()
        if not href or href.startswith("#"):
            continue
        if any(href.startswith(p) for p in ("mailto:", "tel:", "sms:")):
            continue
        if href.startswith(("http://", "https://")):
            rel = url_to_rel(href)
        elif href.startswith("/"):
            rel = href.lstrip("/")
            if rel.endswith("/"):
                rel += "index.html"
        else:
            rel = href.split("#")[0].split("?")[0]
            if rel.endswith("/"):
                rel += "index.html"
        rel = rel.split("#")[0].split("?")[0]
        if rel and rel not in seen:
            seen.add(rel)
            out.append(rel)
    return out


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()[:12]


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def walk_pages() -> list[str]:
    pages = set()
    for base in INCLUDE_DIRS:
        if base in EXCLUDE_DIRS or not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for fn in files:
                if fn in EXCLUDE_FILES or not fn.endswith(".html"):
                    continue
                path = os.path.join(root, fn)
                if os.path.isfile(path):
                    pages.add(path)
    return sorted(pages)


def build_graph():
    paths = walk_pages()
    nodes = {}
    edges = []

    rels = []
    for p in paths:
        rel = os.path.relpath(p, ".").replace("\\", "/")
        rels.append(rel)

    for rel in rels:
        html    = read_file(rel)
        title, h1 = extract_meta(html)
        nodes[rel] = {
            "id":      sha1(rel),
            "rel":     rel,
            "url":     rel_to_url(rel),
            "bucket":  bucket_for_path(rel),
            "title":   title or h1 or rel,
            "h1":      h1,
            "inbound": 0,
            "outbound": 0,
        }

    rel_set = set(nodes)

    for rel in rels:
        html     = read_file(rel)
        outlinks = extract_links(html)
        src_id   = nodes[rel]["id"]
        cnt      = 0
        for tgt_rel in outlinks:
            if tgt_rel in rel_set:
                edges.append({"src": src_id, "dst": nodes[tgt_rel]["id"],
                              "src_rel": rel, "dst_rel": tgt_rel})
                nodes[tgt_rel]["inbound"]  += 1
                cnt += 1
        nodes[rel]["outbound"] = cnt

    return nodes, edges


def top_nodes(nodes: dict, bucket: str | None = None, limit: int = 15) -> list:
    items = list(nodes.values())
    if bucket:
        items = [n for n in items if n["bucket"] == bucket]
    items.sort(key=lambda n: (n["inbound"], n["outbound"]), reverse=True)
    return items[:limit]


def render_html(nodes: dict, edges: list) -> str:
    generated = now_iso()

    bucket_counts: dict[str, int] = {}
    for n in nodes.values():
        b = n["bucket"]
        bucket_counts[b] = bucket_counts.get(b, 0) + 1

    bucket_rows = "\n".join(
        f"<tr><td>{b}</td><td>{bucket_counts[b]}</td></tr>"
        for b in sorted(bucket_counts)
    )

    BUCKETS = [
        "root", "pillars", "clusters", "concepts", "problems", "generated",
        "longtail", "decisions", "authority", "auto", "knowledge",
        "prediction-markets", "fresh", "gravity", "katie", "other",
    ]
    tops_html = []
    for b in BUCKETS:
        t = top_nodes(nodes, bucket=b, limit=15)
        if not t:
            continue
        li = "".join(
            f'<li><a href="/{n["rel"]}">{n["title"]}</a> '
            f'<span class="muted">({n["inbound"]} in / {n["outbound"]} out)</span></li>'
            for n in t
        )
        tops_html.append(f"""
      <div class="card">
        <h3>{b} — Top pages by internal links</h3>
        <ol class="ol">{li}</ol>
      </div>""")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>SideGuy Knowledge Graph — Site Intelligence Map</title>
  <meta name="description" content="SideGuy Knowledge Graph: a site-wide intelligence map of pages and internal links, built automatically."/>
  <link rel="canonical" href="{SITE_BASE}/knowledge/knowledge-graph.html"/>
  <style>
    :root{{--bg:#07121a;--panel:#0b1b25;--card:#0e2230;--line:#163548;
      --text:#eaf6ff;--muted:#9bc2d6;--mint:#6ef3c5;--aqua:#4ad7ff;}}
    *{{box-sizing:border-box}}
    body{{margin:0;background:radial-gradient(1200px 800px at 20% -10%,#123a4a 0%,var(--bg) 55%);
      color:var(--text);font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,Segoe UI,Inter,Roboto,Arial;}}
    a{{color:var(--aqua);text-decoration:none}}a:hover{{text-decoration:underline}}
    .wrap{{max-width:1100px;margin:0 auto;padding:28px 18px 120px}}
    .hero{{padding:18px 18px 10px;border:1px solid var(--line);
      background:linear-gradient(180deg,var(--panel),transparent);border-radius:18px}}
    .kicker{{color:var(--muted);font-size:13px;letter-spacing:.08em;text-transform:uppercase}}
    h1{{margin:10px 0 8px;font-size:30px}}h3{{margin:0 0 10px}}
    .sub{{color:var(--muted);line-height:1.45;margin:0 0 12px}}
    .grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:14px;margin-top:14px}}
    .card{{grid-column:span 12;border:1px solid var(--line);
      background:rgba(14,34,48,.75);border-radius:16px;padding:16px}}
    @media(min-width:900px){{.half{{grid-column:span 6}}}}
    table{{width:100%;border-collapse:collapse;margin-top:10px}}
    td,th{{border-bottom:1px solid rgba(255,255,255,.08);padding:10px 8px;text-align:left}}
    th{{color:var(--muted);font-weight:600}}
    .muted{{color:var(--muted)}}
    .pillrow{{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}}
    .pill{{border:1px solid rgba(255,255,255,.14);padding:7px 10px;border-radius:999px;
      color:var(--text);background:rgba(0,0,0,.18);font-size:13px}}
    .ol{{margin:8px 0 0 18px}}
    .ol li{{margin:5px 0;font-size:14px}}
    .cta{{position:fixed;right:16px;bottom:16px;z-index:9999}}
    .cta a{{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:999px;
      background:linear-gradient(135deg,rgba(110,243,197,.22),rgba(74,215,255,.18));
      border:1px solid rgba(110,243,197,.45);box-shadow:0 18px 40px rgba(0,0,0,.35);
      color:var(--text);font-weight:700;text-decoration:none;}}
    .dot{{width:10px;height:10px;border-radius:50%;background:var(--mint);
      box-shadow:0 0 0 0 rgba(110,243,197,.55);animation:pulse 1.6s infinite}}
    @keyframes pulse{{0%{{box-shadow:0 0 0 0 rgba(110,243,197,.55)}}
      70%{{box-shadow:0 0 0 18px rgba(110,243,197,0)}}
      100%{{box-shadow:0 0 0 0 rgba(110,243,197,0)}}}}
    code{{background:rgba(0,0,0,.25);padding:2px 6px;border-radius:8px;border:1px solid rgba(255,255,255,.08)}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div class="kicker">SideGuy Intelligence Layer</div>
      <h1>Knowledge Graph</h1>
      <p class="sub">Wikipedia-style map of SideGuy: pages, buckets, and how everything links together. Built automatically on <b>{generated}</b>.</p>
      <div class="pillrow">
        <span class="pill">Nodes: <b>{len(nodes)}</b></span>
        <span class="pill">Edges: <b>{len(edges)}</b></span>
        <span class="pill">Export: <a href="/reports/knowledge-graph.json">knowledge-graph.json</a></span>
      </div>
    </div>

    <div class="grid">
      <div class="card half">
        <h3>Bucket counts</h3>
        <p class="muted">Pages in each directory bucket.</p>
        <table><thead><tr><th>Bucket</th><th>Pages</th></tr></thead>
        <tbody>{bucket_rows}</tbody></table>
      </div>

      <div class="card half">
        <h3>How to use this</h3>
        <ul>
          <li>Highest inbound pages are your internal "authorities".</li>
          <li>If a bucket looks thin, build more pages + wire them.</li>
          <li>After major builds: re-run engine + submit priority URLs in GSC.</li>
        </ul>
        <p class="muted">Run anytime:</p>
        <p><code>python3 scripts/knowledge-graph-engine.py</code></p>
        <p><a href="/">← SideGuy Home</a> &nbsp;·&nbsp; <a href="/knowledge/sideguy-knowledge-map.html">Knowledge Map</a></p>
      </div>

      <div class="card">
        <h3>Top pages per bucket (by inbound links)</h3>
        <p class="muted">Sorted by inbound links (then outbound). These are your highest-gravity pages.</p>
      </div>

      {''.join(tops_html)}
    </div>
  </div>

  <div class="cta">
    <a href="{SMS_HREF}">
      <span class="dot"></span>
      <span>Text PJ</span>
      <span class="muted">&nbsp;773-544-1231</span>
    </a>
  </div>
</body>
</html>
"""


def write(path: str, content: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def inject_card(target_file: str, card_html: str) -> bool:
    html = read_file(target_file)
    if not html:
        return False
    block = f"{KG_CARD_START}\n{card_html}\n{KG_CARD_END}"
    if KG_CARD_START in html and KG_CARD_END in html:
        html2 = re.sub(
            re.escape(KG_CARD_START) + r".*?" + re.escape(KG_CARD_END),
            block, html, flags=re.S,
        )
    elif "</body>" in html:
        html2 = html.replace("</body>", block + "\n</body>", 1)
    else:
        html2 = html + "\n" + block
    if html2 != html:
        write(target_file, html2)
        return True
    return False


def main():
    nodes, edges = build_graph()

    # Full JSON export (large — gitignored, regenerate locally as needed)
    graph = {
        "generated_at": now_iso(),
        "site":  SITE_BASE,
        "nodes": list(nodes.values()),
        "edges": edges,
    }
    write("reports/knowledge-graph.json", json.dumps(graph, indent=2))

    # Compact summary (committed — top 100 nodes by inbound + bucket counts)
    bucket_counts: dict[str, int] = {}
    for n in nodes.values():
        b = n["bucket"]
        bucket_counts[b] = bucket_counts.get(b, 0) + 1

    top100 = sorted(nodes.values(), key=lambda n: (n["inbound"], n["outbound"]), reverse=True)[:100]
    summary = {
        "generated_at":  now_iso(),
        "total_nodes":   len(nodes),
        "total_edges":   len(edges),
        "bucket_counts": bucket_counts,
        "top_100_nodes": [
            {"rel": n["rel"], "title": n["title"],
             "inbound": n["inbound"], "outbound": n["outbound"],
             "bucket": n["bucket"]}
            for n in top100
        ],
    }
    write("reports/knowledge-graph-summary.json", json.dumps(summary, indent=2))

    # HTML page
    write("knowledge/knowledge-graph.html", render_html(nodes, edges))

    # Card wiring (marker-based, idempotent)
    card = f"""  <section style="margin:22px 0;">
    <div style="border:1px solid rgba(255,255,255,.14);border-radius:16px;padding:16px;background:rgba(14,34,48,.55);">
      <div style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#9bc2d6;">Intelligence Layer</div>
      <h2 style="margin:8px 0 6px;">Knowledge Graph</h2>
      <p style="margin:0 0 10px;color:#9bc2d6;line-height:1.45;">
        Wikipedia-style map of SideGuy: buckets, authority pages, and internal link gravity.
        {len(nodes):,} nodes · {len(edges):,} edges.
      </p>
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <a href="/knowledge/knowledge-graph.html" style="padding:10px 12px;border-radius:12px;border:1px solid rgba(74,215,255,.35);background:rgba(0,0,0,.22);color:#eaf6ff;font-weight:700;">Open Knowledge Graph</a>
        <a href="/reports/knowledge-graph.json" style="padding:10px 12px;border-radius:12px;border:1px solid rgba(110,243,197,.35);background:rgba(0,0,0,.22);color:#eaf6ff;font-weight:700;">Download JSON</a>
      </div>
    </div>
  </section>"""

    patched = 0
    for f in ["knowledge/sideguy-knowledge-map.html", "knowledge-hub.html", "index.html"]:
        if os.path.isfile(f):
            if inject_card(f, card):
                patched += 1

    print(f"[KG] nodes={len(nodes):,}  edges={len(edges):,}")
    print(f"[KG] wrote: knowledge/knowledge-graph.html")
    print(f"[KG] wrote: reports/knowledge-graph.json  (gitignored — 64 MB full graph)")
    print(f"[KG] wrote: reports/knowledge-graph-summary.json  (committed — top 100 + counts)")
    print(f"[KG] patched files: {patched}")


if __name__ == "__main__":
    main()
