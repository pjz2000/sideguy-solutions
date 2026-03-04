#!/usr/bin/env python3
import os, re, json, html, datetime
from collections import defaultdict, Counter

PHONE_DISPLAY = "773-544-1231"
PHONE_SMS = "sms:+17735441231"

# Where to scan for content pages (keep it tight + safe)
SCAN_DIRS = [
  ".",             # root pages (index.html etc)
  "problems",
  "concepts",
  "generated",
  "auto",
  "longtail",
  "decisions",
  "prediction-markets",
  "knowledge",
  "fresh",
  "gravity",
  "authority",     # include existing authority (idempotent updates)
]

# Skip junk / huge artifacts
SKIP_PREFIXES = (
  ".git/", "node_modules/", ".next/", "dist/", "build/", "out/",
  "reports/", "radar/raw/", "radar/", "sitemaps/", "public/",
)
SKIP_FILES = set([
  "sitemap.xml", "sitemap-index.xml", "robots.txt",
])

# Authority settings
MIN_PAGES_PER_HUB = int(os.environ.get("AUTH_MIN_PAGES", "12"))      # threshold to mint a hub
TOP_N_LINKS = int(os.environ.get("AUTH_TOP_N", "60"))               # links shown per hub
MAX_HUBS = int(os.environ.get("AUTH_MAX_HUBS", "24"))               # cap minted per run
MODE = os.environ.get("AUTH_MODE", "smart")                         # smart | aggressive
DRY_RUN = os.environ.get("AUTH_DRY_RUN", "0") == "1"

AUTH_DIR = "authority"
AUTH_INDEX = os.path.join(AUTH_DIR, "index.html")
REPORT_JSON = os.path.join("reports", "authority-autopilot.json")
REPORT_MD = os.path.join("reports", "authority-autopilot-report.md")

MARKER_HOME = "<!-- SG_AUTHORITY_AUTOPILOT_CARD_START -->"
MARKER_HOME_END = "<!-- SG_AUTHORITY_AUTOPILOT_CARD_END -->"

MARKER_KMAP = "<!-- SG_AUTHORITY_AUTOPILOT_SECTION_START -->"
MARKER_KMAP_END = "<!-- SG_AUTHORITY_AUTOPILOT_SECTION_END -->"

MARKER_KHUB = "<!-- SG_AUTHORITY_AUTOPILOT_SECTION_START -->"
MARKER_KHUB_END = "<!-- SG_AUTHORITY_AUTOPILOT_SECTION_END -->"


def now_iso():
  return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_html_file(path: str) -> bool:
  return path.endswith(".html") and (os.path.basename(path) not in SKIP_FILES)


def skip_path(path: str) -> bool:
  norm = path.replace("\\", "/")
  for p in SKIP_PREFIXES:
    if norm.startswith(p):
      return True
  return False


def read_file(path: str) -> str:
  try:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
      return f.read()
  except Exception:
    return ""


def extract_title_h1(text: str):
  title = ""
  h1 = ""
  m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
  if m:
    title = re.sub(r"\s+", " ", m.group(1)).strip()
  m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
  if m:
    h1 = re.sub(r"<.*?>", "", m.group(1))
    h1 = re.sub(r"\s+", " ", h1).strip()
  return title, h1


def normalize_slug(path: str) -> str:
  p = path.replace("\\", "/")
  if p.startswith("./"):
    p = p[2:]
  p = re.sub(r"^/+", "", p)
  return p


def slug_tokens(slug: str):
  # "stripe-webhook-not-working.html" => ["stripe","webhook","not","working"]
  base = os.path.basename(slug).replace(".html","")
  base = base.replace("_","-")
  toks = [t for t in base.split("-") if t and len(t) > 1]
  return toks


def bucket_for(slug: str) -> str:
  # top-level folder bucket
  parts = slug.split("/")
  if len(parts) == 1:
    return "root"
  return parts[0]


def safe(text: str) -> str:
  return html.escape(str(text or ""))


def ensure_marker_block(doc: str, start: str, end: str, block_html: str) -> str:
  if start in doc and end in doc:
    pre = doc.split(start)[0]
    post = doc.split(end)[1]
    return pre + start + "\n" + block_html.strip() + "\n" + end + post
  # If markers missing, append near end before </body> if possible
  if "</body>" in doc:
    return doc.replace("</body>", f"\n{start}\n{block_html.strip()}\n{end}\n</body>", 1)
  return doc + f"\n{start}\n{block_html.strip()}\n{end}\n"


def ocean_css():
  return """
  <style>
    :root {
      --bg1:#071a2a; --bg2:#06101a; --card:#0b2236; --line:rgba(255,255,255,.10);
      --txt:rgba(255,255,255,.92); --mut:rgba(255,255,255,.70);
      --mint:#7fffd4; --aqua:#60a5fa; --glow:rgba(127,255,212,.35);
    }
    body {
      margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
      color:var(--txt);
      background: radial-gradient(1000px 600px at 20% 10%, rgba(96,165,250,.18), transparent 60%),
                  radial-gradient(900px 600px at 80% 20%, rgba(127,255,212,.12), transparent 60%),
                  linear-gradient(180deg, var(--bg1), var(--bg2));
    }
    a{ color: var(--mint); text-decoration:none; }
    a:hover{ text-decoration:underline; }
    .wrap{ max-width:1100px; margin:0 auto; padding:34px 18px 70px; }
    .topline{ display:flex; gap:10px; align-items:center; justify-content:space-between; flex-wrap:wrap; }
    .badge{ display:inline-flex; gap:8px; align-items:center; padding:8px 12px; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.04); }
    .grid{ display:grid; grid-template-columns: repeat(12, 1fr); gap:14px; margin-top:16px; }
    .card{ grid-column: span 6; border:1px solid var(--line); border-radius:16px; background:rgba(255,255,255,.04); padding:16px; }
    .card h3{ margin:0 0 6px; font-size:16px; }
    .meta{ color:var(--mut); font-size:13px; }
    .pills{ display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; }
    .pill{ font-size:12px; padding:7px 10px; border-radius:999px; border:1px solid var(--line); background:rgba(255,255,255,.03); }
    .links{ margin-top:12px; display:grid; grid-template-columns: 1fr; gap:6px; }
    .links a{ display:block; padding:8px 10px; border:1px solid var(--line); border-radius:12px; background:rgba(0,0,0,.12); }
    .links a:hover{ box-shadow: 0 0 0 3px rgba(127,255,212,.08); }
    .kicker{ color:var(--mut); font-size:13px; margin-top:6px; }
    .h1{ font-size:28px; line-height:1.15; margin:10px 0 0; }
    .sub{ color:var(--mut); font-size:14px; max-width:72ch; margin-top:10px; }
    .footer{ margin-top:28px; color:var(--mut); font-size:13px; }
    .float {
      position: fixed; right: 18px; bottom: 18px; z-index: 9999;
      display:flex; align-items:center; gap:10px;
      padding: 12px 14px; border-radius: 999px;
      border: 1px solid rgba(127,255,212,.30);
      background: rgba(3, 12, 18, .72);
      backdrop-filter: blur(10px);
      box-shadow: 0 0 0 2px rgba(127,255,212,.08), 0 18px 55px rgba(0,0,0,.45);
      animation: pulse 1.9s ease-in-out infinite;
    }
    .dot {
      width: 12px; height: 12px; border-radius: 99px;
      background: var(--mint);
      box-shadow: 0 0 0 6px rgba(127,255,212,.12), 0 0 24px rgba(127,255,212,.35);
    }
    @keyframes pulse {
      0%,100% { transform: translateY(0); box-shadow: 0 0 0 2px rgba(127,255,212,.08), 0 18px 55px rgba(0,0,0,.45); }
      50% { transform: translateY(-2px); box-shadow: 0 0 0 6px rgba(127,255,212,.10), 0 26px 65px rgba(0,0,0,.52); }
    }
    .float .t1{ font-weight:700; }
    .float .t2{ font-size:12px; color:var(--mut); margin-top:2px; }
    .float .txt{ display:flex; flex-direction:column; line-height:1.05; }
    .float svg{ width:18px; height:18px; opacity:.92; }
    .float:hover{ text-decoration:none; }
    .table{ width:100%; border-collapse: collapse; margin-top:18px; }
    .table th,.table td{ border-bottom:1px solid var(--line); padding:10px 8px; text-align:left; font-size:13px; }
    .table th{ color:var(--mut); font-weight:600; }
    @media(max-width:640px){ .card{ grid-column: span 12; } }
  </style>
  """


def float_btn():
  return f"""
  <a class="float" href="{PHONE_SMS}">
    <span class="dot"></span>
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M7 10h10M7 14h7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      <path d="M21 12c0 4.5-4 8-9 8-1.3 0-2.6-.2-3.7-.7L3 21l1.7-4.6C4.2 15.2 4 13.6 4 12c0-4.5 4-8 9-8s8 3.5 8 8Z"
            stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
    </svg>
    <span class="txt">
      <span class="t1">Text PJ</span>
      <span class="t2">{PHONE_DISPLAY}</span>
    </span>
  </a>
  """


def canonical_for(path: str) -> str:
  return "https://sideguysolutions.com/" + path.replace("\\","/")


def build_hub_page(hub_slug: str, hub_title: str, hub_desc: str, items: list, buckets: Counter, tokens: list):
  rows = []
  for it in items[:TOP_N_LINKS]:
    label = it["h1"] or it["title"] or it["slug"]
    rows.append(f'<a href="/{safe(it["slug"])}">{safe(label)}</a>')

  bucket_pills = "".join([f'<span class="pill">{safe(k)}: {v}</span>' for k,v in buckets.most_common(10)])
  token_pills = "".join([f'<span class="pill">{safe(t)}</span>' for t in tokens[:12]])

  page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{safe(hub_title)} | SideGuy Authority Hub</title>
  <meta name="description" content="{safe(hub_desc)}"/>
  <link rel="canonical" href="{canonical_for(hub_slug)}"/>
  <meta property="og:title" content="{safe(hub_title)}"/>
  <meta property="og:description" content="{safe(hub_desc)}"/>
  <meta property="og:type" content="website"/>
  {ocean_css()}
  <script type="application/ld+json">
  {json.dumps({
    "@context":"https://schema.org",
    "@type":"CollectionPage",
    "name": hub_title,
    "description": hub_desc,
    "url": canonical_for(hub_slug),
    "isPartOf": {"@type":"WebSite","name":"SideGuy Solutions","url":"https://sideguysolutions.com/"},
  }, indent=2)}
  </script>
</head>
<body>
  <div class="wrap">
    <div class="topline">
      <div class="badge">🌊 <strong>Authority Autopilot</strong> <span class="meta">Generated {now_iso()}</span></div>
      <div class="badge"><a href="/">← Home</a> <span class="meta">/</span> <a href="/authority/index.html">Authority Index</a></div>
    </div>

    <h1 class="h1">{safe(hub_title)}</h1>
    <div class="sub">{safe(hub_desc)}</div>

    <div class="grid">
      <div class="card">
        <h3>Cluster signals</h3>
        <div class="meta">Tokens + bucket distribution from live site inventory.</div>
        <div class="pills">{token_pills}</div>
        <div class="pills" style="margin-top:12px">{bucket_pills}</div>
      </div>

      <div class="card">
        <h3>Best pages in this cluster</h3>
        <div class="meta">Top {min(TOP_N_LINKS, len(items))} pages detected for this topic.</div>
        <div class="links">
          {''.join(rows)}
        </div>
      </div>
    </div>

    <div class="footer">
      <div><strong>SideGuy</strong> is where Google discovers the problem, AI explains it, and a real human resolves it.</div>
      <div class="kicker">Clarity before cost. Text PJ if you want the fastest path to a clean fix.</div>
    </div>
  </div>

  {float_btn()}
</body>
</html>
"""
  return page


def scan_pages():
  pages = []
  seen = set()
  for d in SCAN_DIRS:
    if not os.path.exists(d):
      continue
    for root, _, files in os.walk(d):
      for f in files:
        p = os.path.join(root, f)
        p = p.replace("\\","/")
        if skip_path(p):
          continue
        if not is_html_file(p):
          continue
        slug = normalize_slug(p)
        if slug in seen:
          continue
        seen.add(slug)
        txt = read_file(p)
        title, h1 = extract_title_h1(txt)
        pages.append({
          "slug": slug,
          "bucket": bucket_for(slug),
          "title": title,
          "h1": h1
        })
  return pages


def candidate_hubs(pages):
  """
  smart : build hubs from frequent 2-token slug stems that look intent-y
  aggressive : include 1-token hubs too (noisier, larger)
  """
  token_pairs = defaultdict(list)
  token_singles = defaultdict(list)

  NOISE = {"index","guide","how","to","best","top","vs","and","the","for",
           "with","from","your","not","working","san","diego","page","html"}

  for p in pages:
    toks = slug_tokens(p["slug"])
    toks = [t for t in toks if t not in NOISE]
    if not toks:
      continue

    # singles
    for t in set(toks[:6]):
      token_singles[t].append(p)

    # adjacent pairs
    for i in range(min(len(toks)-1, 6)):
      a, b = toks[i], toks[i+1]
      key = f"{a}-{b}"
      token_pairs[key].append(p)

  hubs = []

  # prefer pairs
  for key, items in token_pairs.items():
    if len(items) >= MIN_PAGES_PER_HUB:
      hubs.append((key, items))

  if MODE == "aggressive":
    for key, items in token_singles.items():
      if len(items) >= (MIN_PAGES_PER_HUB + 8):
        hubs.append((key, items))

  # sort by size desc, deduplicate by slug
  hubs.sort(key=lambda x: len(x[1]), reverse=True)
  return hubs[:MAX_HUBS]


def hub_title_from_key(key: str) -> str:
  return " ".join([w.capitalize() for w in key.split("-")])


def hub_desc_from_key(key: str, count: int) -> str:
  base = hub_title_from_key(key)
  return (f"A SideGuy Authority Hub for \u201c{base}\u201d \u2014 {count} related guides, fixes, "
          f"and operator pages detected across the site. Built automatically from real internal "
          f"link + slug signals.")


def write_file(path: str, content: str):
  os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    f.write(content)


def patch_home_card():
  home = "index.html"
  if not os.path.exists(home):
    return False
  doc = read_file(home)

  card = """
  <section style="margin-top:18px">
    <div style="border:1px solid rgba(255,255,255,.10); border-radius:18px; padding:16px; background:rgba(255,255,255,.04)">
      <div style="display:flex; gap:10px; align-items:center; justify-content:space-between; flex-wrap:wrap">
        <div style="display:flex; gap:10px; align-items:center">
          <span style="display:inline-flex; width:10px; height:10px; border-radius:99px; background:#7fffd4; box-shadow:0 0 0 6px rgba(127,255,212,.12)"></span>
          <strong>Authority Autopilot</strong>
          <span style="opacity:.72; font-size:13px">Auto-built topic hubs (Wikipedia-style) from live SideGuy inventory</span>
        </div>
        <a href="/authority/index.html" style="padding:8px 12px; border-radius:999px; border:1px solid rgba(255,255,255,.12); background:rgba(0,0,0,.15)">Open Authority Hubs \u2192</a>
      </div>
      <div style="opacity:.75; font-size:13px; margin-top:10px">
        Hubs update automatically as new pages ship \u2014 tighter internal linking, clearer navigation, and faster indexing paths.
      </div>
    </div>
  </section>
  """.strip()

  out = ensure_marker_block(doc, MARKER_HOME, MARKER_HOME_END, card)
  if out != doc and not DRY_RUN:
    write_file(home, out)
    return True
  return out != doc  # dry-run: return True if would-change


def patch_knowledge_map():
  candidates = [
    "knowledge/sideguy-knowledge-map.html",
    "sideguy-knowledge-map.html",
  ]
  target = None
  for c in candidates:
    if os.path.exists(c):
      target = c
      break
  if not target:
    return False

  doc = read_file(target)
  block = """
  <section style="margin-top:18px">
    <h2 style="margin:0 0 10px">Authority Autopilot</h2>
    <div style="opacity:.75; font-size:13px; margin-bottom:10px">
      Auto-built topic hubs based on real site inventory signals. Use these as crawler entry points.
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:10px">
      <a href="/authority/index.html" style="padding:10px 12px; border-radius:14px; border:1px solid rgba(255,255,255,.12); background:rgba(0,0,0,.14)">Authority Hub Index \u2192</a>
    </div>
  </section>
  """.strip()

  out = ensure_marker_block(doc, MARKER_KMAP, MARKER_KMAP_END, block)
  if out != doc and not DRY_RUN:
    write_file(target, out)
    return True
  return out != doc


def patch_knowledge_hub():
  candidates = [
    "knowledge-hub.html",
    "knowledge/knowledge-hub.html",
  ]
  target = None
  for c in candidates:
    if os.path.exists(c):
      target = c
      break
  if not target:
    return False

  doc = read_file(target)
  block = """
  <section style="margin-top:18px">
    <h2 style="margin:0 0 10px">Authority Hubs</h2>
    <div style="opacity:.75; font-size:13px; margin-bottom:10px">
      Wikipedia-style topic hubs built automatically from SideGuy\u2019s live page inventory.
    </div>
    <div style="display:flex; flex-wrap:wrap; gap:10px">
      <a href="/authority/index.html" style="padding:10px 12px; border-radius:14px; border:1px solid rgba(255,255,255,.12); background:rgba(0,0,0,.14)">Open Authority Index \u2192</a>
    </div>
  </section>
  """.strip()

  out = ensure_marker_block(doc, MARKER_KHUB, MARKER_KHUB_END, block)
  if out != doc and not DRY_RUN:
    write_file(target, out)
    return True
  return out != doc


def build_authority_index(hubs_meta):
  cards = []
  for h in hubs_meta:
    sample_links = "".join([
      f'<a href="/{safe(s)}">{safe(lbl)}</a>'
      for (s, lbl) in h["sample"]
    ])
    cards.append(f"""
    <div class="card">
      <h3><a href="/{safe(h['hub_slug'])}">{safe(h['hub_title'])}</a></h3>
      <div class="meta">{safe(h['hub_desc'])}</div>
      <div class="pills" style="margin-top:10px">
        <span class="pill">pages: {h['count']}</span>
        <span class="pill">top bucket: {safe(h['top_bucket'])}</span>
      </div>
      <div class="links" style="margin-top:12px">
        {sample_links}
      </div>
    </div>
    """.strip())

  page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Authority Hubs | SideGuy</title>
  <meta name="description" content="Auto-built topic hubs (Wikipedia-style) generated from SideGuy&#39;s live page inventory for faster crawling, tighter internal linking, and stronger authority."/>
  <link rel="canonical" href="{canonical_for('authority/index.html')}"/>
  {ocean_css()}
</head>
<body>
  <div class="wrap">
    <div class="topline">
      <div class="badge">🌊 <strong>Authority Autopilot</strong> <span class="meta">Generated {now_iso()}</span></div>
      <div class="badge"><a href="/">← Home</a></div>
    </div>

    <h1 class="h1">Authority Hubs</h1>
    <div class="sub">
      Wikipedia-style topic hubs built automatically from SideGuy's live inventory signals.
      These are crawler-friendly entry points + internal link concentrators.
    </div>

    <div class="grid">
      {''.join(cards)}
    </div>

    <div class="footer">
      <div><strong>SideGuy</strong> is where Google discovers the problem, AI explains it, and a real human resolves it.</div>
      <div class="kicker">Clarity before cost. Text PJ if you want the fastest path to a clean fix.</div>
    </div>
  </div>

  {float_btn()}
</body>
</html>
"""
  return page


def main():
  print(f"[authority-autopilot] Scanning pages… (MIN_PAGES={MIN_PAGES_PER_HUB}, MAX_HUBS={MAX_HUBS}, MODE={MODE}, DRY_RUN={DRY_RUN})")
  pages = scan_pages()
  print(f"[authority-autopilot] Scanned {len(pages)} pages")

  hubs = candidate_hubs(pages)
  print(f"[authority-autopilot] {len(hubs)} hub candidates found")

  hubs_meta = []
  minted = 0
  skipped = 0

  for key, items in hubs:
    hub_slug = f"{AUTH_DIR}/{key}-hub.html"
    hub_title = f"{hub_title_from_key(key)} Hub"
    hub_desc = hub_desc_from_key(key, len(items))

    # Sort by bucket then slug for stable output
    items_sorted = sorted(items, key=lambda x: (x["bucket"], x["slug"]))

    # Build bucket counter
    buckets = Counter(it["bucket"] for it in items_sorted)
    top_bucket = buckets.most_common(1)[0][0] if buckets else "root"

    # Tokens for display pills
    tokens = key.split("-")

    if not DRY_RUN:
      page_html = build_hub_page(hub_slug, hub_title, hub_desc, items_sorted, buckets, tokens)
      os.makedirs(AUTH_DIR, exist_ok=True)
      with open(hub_slug, "w", encoding="utf-8") as f:
        f.write(page_html)
      minted += 1
      print(f"  ✓ {hub_slug}  ({len(items_sorted)} pages)")
    else:
      print(f"  [DRY] would mint {hub_slug}  ({len(items_sorted)} pages)")
      minted += 1

    # Sample 5 pages for the index card
    sample = []
    for it in items_sorted[:5]:
      lbl = it["h1"] or it["title"] or it["slug"]
      sample.append((it["slug"], lbl))

    hubs_meta.append({
      "key": key,
      "hub_slug": hub_slug,
      "hub_title": hub_title,
      "hub_desc": hub_desc,
      "count": len(items_sorted),
      "top_bucket": top_bucket,
      "buckets": dict(buckets),
      "tokens": tokens,
      "sample": sample,
    })

  # Build/update authority index
  if not DRY_RUN and hubs_meta:
    idx_html = build_authority_index(hubs_meta)
    os.makedirs(AUTH_DIR, exist_ok=True)
    with open(AUTH_INDEX, "w", encoding="utf-8") as f:
      f.write(idx_html)
    print(f"[authority-autopilot] Index written → {AUTH_INDEX}")

  # Wire into homepage
  patched_home = patch_home_card()
  print(f"[authority-autopilot] Homepage {'patched' if patched_home else 'skipped (already up to date)'}")

  # Wire into knowledge map
  patched_kmap = patch_knowledge_map()
  print(f"[authority-autopilot] Knowledge map {'patched' if patched_kmap else 'skipped'}")

  # Wire into knowledge hub
  patched_khub = patch_knowledge_hub()
  print(f"[authority-autopilot] Knowledge hub {'patched' if patched_khub else 'skipped'}")

  # Write reports
  report = {
    "generated": now_iso(),
    "pages_scanned": len(pages),
    "hubs_minted": minted,
    "dry_run": DRY_RUN,
    "settings": {
      "MIN_PAGES_PER_HUB": MIN_PAGES_PER_HUB,
      "TOP_N_LINKS": TOP_N_LINKS,
      "MAX_HUBS": MAX_HUBS,
      "MODE": MODE,
    },
    "hubs": [{
      "key": h["key"],
      "slug": h["hub_slug"],
      "title": h["hub_title"],
      "count": h["count"],
      "top_bucket": h["top_bucket"],
      "buckets": h["buckets"],
    } for h in hubs_meta],
  }

  os.makedirs("reports", exist_ok=True)
  with open(REPORT_JSON, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)
  print(f"[authority-autopilot] Report → {REPORT_JSON}")

  # Markdown summary
  lines = [
    f"# Authority Autopilot Report",
    f"",
    f"Generated: {now_iso()}",
    f"Pages scanned: {len(pages)}",
    f"Hubs minted: {minted}",
    f"Mode: {MODE} | DRY_RUN: {DRY_RUN}",
    f"",
    f"## Hubs",
    f"",
    f"| Hub | Count | Top Bucket |",
    f"|-----|-------|------------|",
  ]
  for h in hubs_meta:
    lines.append(f"| [{h['hub_title']}](/{h['hub_slug']}) | {h['count']} | {h['top_bucket']} |")

  with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
  print(f"[authority-autopilot] Markdown report → {REPORT_MD}")

  print(f"\n[authority-autopilot] DONE — {minted} hubs minted, {len(pages)} pages scanned")


if __name__ == "__main__":
  main()
