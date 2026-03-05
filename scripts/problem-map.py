#!/usr/bin/env python3
import os, re, json, math, datetime
from collections import defaultdict, Counter

PHONE_SMS = "sms:+17735441231"
SITE = "https://sideguysolutions.com"

# Buckets (dirs) we care about for maps
BUCKET_DIRS = [
  "problems", "concepts", "clusters", "pillars", "generated", "auto",
  "decisions", "prediction-markets", "authority", "knowledge", "fresh", "gravity", "multiplied"
]

# Prefer these summary paths if they exist (from your knowledge-graph engine)
SUMMARY_CANDIDATES = [
  "knowledge-graph-summary.json",
  "data/knowledge-graph-summary.json",
  "knowledge/knowledge-graph-summary.json",
  "reports/knowledge-graph-summary.json",
]


def read(path):
  with open(path, "r", encoding="utf-8", errors="ignore") as f:
    return f.read()


def write(path, s):
  os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    f.write(s)


def slug_bucket(path):
  # normalize bucket based on first folder
  p = path.replace("\\", "/").lstrip("./")
  parts = p.split("/")
  if len(parts) >= 2:
    b = parts[0]
    if b in BUCKET_DIRS:
      return b
  return "root"


def title_from_html(html):
  m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
  if m:
    return re.sub(r"\s+", " ", m.group(1)).strip()
  h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
  if h1:
    return re.sub(r"<[^>]+>", "", h1.group(1)).strip()
  return None


def extract_links(html):
  # only internal-ish hrefs
  hrefs = re.findall(r'href="([^"]+)"', html, re.I)
  out = []
  for h in hrefs:
    if h.startswith("http"):
      if "sideguysolutions.com" in h:
        out.append(h.replace(SITE, ""))
    elif h.startswith("/"):
      out.append(h)
    elif h.endswith(".html") or "/" in h:
      out.append(h if h.startswith("/") else "/" + h)
  return out


def load_graph_summary():
  for p in SUMMARY_CANDIDATES:
    if os.path.exists(p):
      try:
        return json.loads(read(p)), p
      except Exception:
        pass
  return None, None


def scan_html_fallback():
  pages = []
  outbound = defaultdict(set)
  titles = {}

  for root, dirs, files in os.walk("."):
    # skip huge irrelevant dirs
    skip = {"node_modules", ".git", ".next", "dist", "build", "__pycache__"}
    dirs[:] = [d for d in dirs if d not in skip]
    for f in files:
      if not f.endswith(".html"):
        continue
      p = os.path.join(root, f).replace("\\", "/")
      # ignore link-dump hubs (keep them on site but avoid map blowups)
      if "/hubs/" in p:
        continue
      try:
        html = read(p)
      except Exception:
        continue
      t = title_from_html(html) or os.path.basename(p)
      titles[p] = t
      pages.append(p)

      for link in extract_links(html):
        outbound[p].add(link)

  # inbound count using best-effort match (path suffix)
  inbound = Counter()
  pathset = set(p.replace("\\", "/") for p in pages)

  # index by suffix for faster matching
  suffix_index = defaultdict(list)
  for p in pages:
    suf = "/" + p.lstrip("./")
    suffix_index[suf].append(p)

  for src, links in outbound.items():
    for l in links:
      # normalize link to probable file path
      l2 = l.split("#")[0].split("?")[0]
      if l2 == "/":
        if os.path.exists("./index.html"):
          inbound["./index.html"] += 1
        continue
      # direct match to a page path
      candidate = "." + l2 if l2.startswith("/") else l2
      candidate = candidate.replace("//", "/")
      if candidate in pathset:
        inbound[candidate] += 1
      else:
        # try suffix match
        suf = l2 if l2.startswith("/") else "/" + l2
        if suf in suffix_index:
          for target in suffix_index[suf]:
            inbound[target] += 1

  return pages, titles, inbound


def build_map_data():
  graph, graph_path = load_graph_summary()

  if graph:
    top = []
    try:
      if "top_nodes" in graph:
        top = graph["top_nodes"]
      elif "top100" in graph:
        top = graph["top100"]
      elif "top_pages" in graph:
        top = graph["top_pages"]
    except Exception:
      top = []

    # Normalize top entries into (path, score)
    norm = []
    for row in top:
      if isinstance(row, list) and len(row) >= 2:
        norm.append((row[0], float(row[1])))
      elif isinstance(row, dict) and "path" in row:
        norm.append((row["path"], float(row.get("score", row.get("inbound", 0)))))
      elif isinstance(row, str):
        norm.append((row, 0.0))

    if len(norm) < 10:
      pages, titles, inbound = scan_html_fallback()
      return {"mode": "fallback-scan", "pages": pages, "titles": titles, "inbound": inbound}

    pages, titles, inbound = scan_html_fallback()

    # boost inbound using norm scores if we have them
    for p, score in norm:
      pp = p.replace(SITE, "").replace("\\", "/")
      if pp.startswith("/"):
        pp = "." + pp
      if pp in inbound:
        inbound[pp] = max(inbound[pp], int(score))

    return {"mode": f"graph-summary:{graph_path}", "pages": pages, "titles": titles, "inbound": inbound}

  pages, titles, inbound = scan_html_fallback()
  return {"mode": "fallback-scan", "pages": pages, "titles": titles, "inbound": inbound}


def ocean_css(dark=True):
  bg     = "#06121f" if dark else "#f2fbff"
  card   = "rgba(255,255,255,0.06)" if dark else "rgba(0,40,70,0.06)"
  text   = "#eaf6ff" if dark else "#062033"
  muted  = "rgba(234,246,255,0.72)" if dark else "rgba(6,32,51,0.72)"
  line   = "rgba(255,255,255,0.12)" if dark else "rgba(0,40,70,0.12)"
  return f"""
  <style>
    :root {{
      --bg: {bg};
      --card: {card};
      --text: {text};
      --muted: {muted};
      --line: {line};
      --glow: rgba(0,255,200,0.35);
    }}
    body {{
      margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      background: radial-gradient(1200px 700px at 20% 10%, rgba(0,255,200,0.10), transparent 55%),
                  radial-gradient(900px 500px at 80% 0%, rgba(0,160,255,0.12), transparent 55%),
                  var(--bg);
      color: var(--text);
    }}
    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 28px 18px 90px; }}
    .top {{ display:flex; gap:14px; align-items:flex-end; justify-content:space-between; flex-wrap:wrap; }}
    h1 {{ margin:0; font-size: 28px; letter-spacing:0.2px; }}
    .meta {{ color: var(--muted); font-size: 13px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 16px; }}
    .card {{
      background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px;
      box-shadow: 0 18px 50px rgba(0,0,0,0.25);
    }}
    .card h2 {{ margin:0 0 8px; font-size: 14px; letter-spacing:0.2px; color: var(--muted); }}
    a {{ color: inherit; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .pillrow {{ display:flex; flex-wrap:wrap; gap:8px; margin-top: 10px; }}
    .pill {{
      display:inline-flex; align-items:center; gap:8px;
      padding: 8px 10px; border-radius: 999px; border: 1px solid var(--line);
      background: rgba(0,0,0,0.10);
      font-size: 12px; color: var(--muted);
    }}
    .list {{ margin: 0; padding-left: 18px; }}
    .list li {{ margin: 6px 0; color: var(--muted); }}
    .kpi {{ display:flex; gap:10px; flex-wrap:wrap; margin-top: 10px; }}
    .k {{ padding: 8px 10px; border: 1px solid var(--line); border-radius: 12px; background: rgba(0,0,0,0.12); font-size: 12px; color: var(--muted); }}
    .float {{
      position: fixed; right: 16px; bottom: 16px; z-index: 9999;
      padding: 12px 14px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.18);
      background: rgba(0,0,0,0.45);
      box-shadow: 0 0 0 0 var(--glow);
      animation: pulse 1.4s infinite;
      backdrop-filter: blur(8px);
    }}
    @keyframes pulse {{
      0% {{ box-shadow: 0 0 0 0 var(--glow); }}
      70% {{ box-shadow: 0 0 0 18px rgba(0,255,200,0.0); }}
      100% {{ box-shadow: 0 0 0 0 rgba(0,255,200,0.0); }}
    }}
    .float span {{ font-size: 13px; color: #eafffb; }}
    .table {{ width:100%; border-collapse: collapse; margin-top: 10px; }}
    .table th, .table td {{ border-bottom: 1px solid var(--line); padding: 10px 8px; text-align:left; }}
    .table th {{ font-size: 12px; color: var(--muted); font-weight:600; }}
    .score {{ font-variant-numeric: tabular-nums; color: var(--muted); }}
    .bar {{ height: 10px; border-radius: 999px; background: rgba(0,255,200,0.18); overflow:hidden; }}
    .bar > i {{ display:block; height:100%; background: rgba(0,255,200,0.55); width:0%; }}
    .jump {{ display:flex; flex-wrap:wrap; gap:8px; margin-top: 12px; }}
    .jump a {{ border:1px solid var(--line); border-radius: 999px; padding: 8px 10px; font-size: 12px; color: var(--muted); background: rgba(0,0,0,0.10); }}
  </style>
  """


def html_page(title, body, dark=True):
  now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
  return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title} | SideGuy Map</title>
  <link rel="canonical" href="{SITE}/map/"/>
  {ocean_css(dark=dark)}
</head>
<body>
  <a class="float" href="{PHONE_SMS}"><span>💬 Text PJ · 773-544-1231</span></a>
  <div class="wrap">
    <div class="top">
      <div>
        <h1>{title}</h1>
        <div class="meta">Generated {now} &nbsp;•&nbsp; Wikipedia-mode navigation &nbsp;•&nbsp; <a href="{PHONE_SMS}">Text PJ</a></div>
      </div>
      <div class="meta"><a href="{SITE}/">← Home</a></div>
    </div>
    {body}
  </div>
</body>
</html>"""


def normalize_path(p):
  p = p.replace("\\", "/").lstrip("./")
  if p == "index.html":
    return "/"
  return "/" + p


def main():
  print("[problem-map] Building map data…")
  data = build_map_data()
  pages = data["pages"]
  titles = data["titles"]
  inbound = data["inbound"]
  print(f"[problem-map] Scanned {len(pages)} pages  mode={data['mode']}")

  # bucket grouping
  bucket_pages = defaultdict(list)
  for p in pages:
    b = slug_bucket(p)
    bucket_pages[b].append(p)

  # rank pages within each bucket by inbound count
  ranked_bucket = {}
  for b, arr in bucket_pages.items():
    ranked_bucket[b] = sorted(arr, key=lambda x: inbound.get(x, 0), reverse=True)

  # overall top nodes
  overall = sorted(pages, key=lambda x: inbound.get(x, 0), reverse=True)[:120]

  os.makedirs("map", exist_ok=True)

  # build per-bucket pages
  for b in sorted(ranked_bucket.keys()):
    top = ranked_bucket[b][:250]
    if not top:
      continue

    max_in = max([inbound.get(p, 0) for p in top] + [1])
    rows = []
    for p in top[:150]:
      t = titles.get(p, os.path.basename(p))
      sc = inbound.get(p, 0)
      pct = int((sc / max_in) * 100) if max_in else 0
      url = normalize_path(p)
      rows.append(f"""
      <tr>
        <td><a href="{url}">{t}</a><div class="meta">{url}</div></td>
        <td class="score">{sc}</td>
        <td style="width:40%">
          <div class="bar"><i style="width:{pct}%"></i></div>
        </td>
      </tr>
      """)

    body = f"""
    <div class="kpi">
      <div class="k">Bucket: <b>{b}</b></div>
      <div class="k">Pages: <b>{len(ranked_bucket[b])}</b></div>
      <div class="k">Mode: <b>{data["mode"]}</b></div>
    </div>

    <div class="card" style="margin-top:14px">
      <h2>Top pages in this bucket (ranked by inbound links)</h2>
      <table class="table">
        <thead><tr><th>Page</th><th>Inbound</th><th>Gravity</th></tr></thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </div>

    <div class="pillrow">
      <span class="pill">Tip: top inbound pages are your "Wikipedia nodes"</span>
      <span class="pill">Next move: wire "Top Guides" blocks to push traffic into these nodes</span>
      <span class="pill"><a href="/map/index.html">← Back to Map Index</a></span>
    </div>
    """
    write(f"map/{b}.html", html_page(f"Bucket Map: {b}", body, dark=True))
    print(f"  ✓ map/{b}.html  ({len(ranked_bucket[b])} pages)")

  # build master index — jump links to bucket pages
  jumps = []
  for b in sorted(ranked_bucket.keys()):
    if not ranked_bucket[b]:
      continue
    jumps.append(f'<a href="/map/{b}.html">🧭 {b} ({len(ranked_bucket[b])})</a>')

  # top overall table
  max_all = max([inbound.get(p, 0) for p in overall] + [1])
  rows = []
  for p in overall[:80]:
    t = titles.get(p, os.path.basename(p))
    sc = inbound.get(p, 0)
    pct = int((sc / max_all) * 100) if max_all else 0
    url = normalize_path(p)
    b = slug_bucket(p)
    rows.append(f"""
    <tr>
      <td><a href="{url}">{t}</a><div class="meta">{url}</div></td>
      <td class="score">{b}</td>
      <td class="score">{sc}</td>
      <td style="width:35%"><div class="bar"><i style="width:{pct}%"></i></div></td>
    </tr>
    """)

  body = f"""
  <div class="grid">
    <div class="card">
      <h2>What this is</h2>
      <ul class="list">
        <li>A Wikipedia-style map of SideGuy built from real internal link gravity.</li>
        <li>Top pages here are your "authority nodes" that Google trusts fastest.</li>
        <li>Use this to decide what to improve, wire, and promote.</li>
      </ul>
    </div>

    <div class="card">
      <h2>System status</h2>
      <div class="kpi">
        <div class="k">Total pages scanned: <b>{len(pages)}</b></div>
        <div class="k">Buckets detected: <b>{len([b for b in ranked_bucket if ranked_bucket[b]])}</b></div>
        <div class="k">Mode: <b>{data["mode"]}</b></div>
      </div>
      <div class="pillrow" style="margin-top:12px">
        <span class="pill">sms:+17735441231 everywhere</span>
        <span class="pill">Re-run anytime</span>
      </div>
    </div>

    <div class="card">
      <h2>Jump to bucket maps</h2>
      <div class="jump">
        {''.join(jumps)}
      </div>
    </div>
  </div>

  <div class="card" style="margin-top:14px">
    <h2>Top authority nodes site-wide (ranked by inbound links)</h2>
    <table class="table">
      <thead><tr><th>Page</th><th>Bucket</th><th>Inbound</th><th>Gravity</th></tr></thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>

  <div class="pillrow">
    <span class="pill">Hidden Rule #1: inbound links = trust</span>
    <span class="pill">Hidden Rule #2: hubs make everything crawl faster</span>
    <span class="pill">Hidden Rule #3: link loops compound</span>
  </div>
  """

  write("map/index.html", html_page("SideGuy Internet Problem Map", body, dark=True))
  print("[problem-map] Written map/index.html")

  # export machine-readable
  export = {
    "mode": data["mode"],
    "pages_scanned": len(pages),
    "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "buckets": {b: len(ranked_bucket[b]) for b in ranked_bucket},
    "top_nodes": [
      {
        "path": normalize_path(p),
        "bucket": slug_bucket(p),
        "inbound": inbound.get(p, 0),
        "title": titles.get(p, ""),
      }
      for p in overall[:120]
    ],
  }
  os.makedirs("data", exist_ok=True)
  with open("data/problem-map.json", "w", encoding="utf-8") as f:
    json.dump(export, f, indent=2)
  print("[problem-map] Written data/problem-map.json")
  print(f"\n[problem-map] DONE — {len(ranked_bucket)} bucket maps + master index")


if __name__ == "__main__":
  main()
