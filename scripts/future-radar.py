#!/usr/bin/env python3
"""
SIDEGUY FUTURE RADAR (SEO Time Travel)
- Pulls fresh "future problems" from multiple signal sources (HN, Reddit, status feeds, SO)
- Scores + clusters them by hot-word + depth
- Outputs: future/radar.html + future/future-radar.csv + future/future-radar.json + future/top-topics.txt
- Produces a build list you can feed into problem-multiplier (TOPICS)
"""

import os, re, json, csv, time, hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError

PHONE_SMS  = "sms:+17735441231"
OUT_CSV    = "future/future-radar.csv"
OUT_JSON   = "future/future-radar.json"
OUT_HTML   = "future/radar.html"
OUT_TOPICS = "future/top-topics.txt"
RAW_DIR    = "future/raw"

SOURCES = [
  # Hacker News
  ("hn_new",        "https://hnrss.org/newest?points=20"),
  ("hn_front",      "https://hnrss.org/frontpage"),
  # Status feeds (real incidents = real pain = real SEO demand)
  ("stripe_status", "https://status.stripe.com/history.rss"),
  ("vercel_status", "https://www.vercel-status.com/history.rss"),
  ("openai_status", "https://status.openai.com/history.rss"),
  # Stack Overflow hot questions
  ("so_hot",            "https://stackoverflow.com/feeds"),
  # Reddit operator/dev subreddits
  ("reddit_smallbiz",   "https://www.reddit.com/r/smallbusiness/.rss"),
  ("reddit_sysadmin",   "https://www.reddit.com/r/sysadmin/.rss"),
  ("reddit_webdev",     "https://www.reddit.com/r/webdev/.rss"),
  ("reddit_stripe",     "https://www.reddit.com/r/stripe/.rss"),
]

HOT_WORDS = [
  ("not working",   6.0),
  ("down",          5.5),
  ("declined",      5.0),
  ("chargeback",    5.0),
  ("webhook",       4.8),
  ("api",           4.2),
  ("error",         4.0),
  ("timeout",       4.0),
  ("refund",        4.0),
  ("payout",        4.0),
  ("verification",  3.8),
  ("dispute",       3.8),
  ("fraud",         3.6),
  ("compliance",    3.4),
  ("killed",        3.4),
  ("blocked",       3.4),
  ("broken",        3.2),
  ("cancelled",     3.2),
  ("pricing",       2.8),
  ("fees",          2.8),
  ("migration",     2.8),
  ("rate limit",    2.8),
]

TOPIC_BUCKETS = [
  ("payments",          ["stripe","square","payment","card","chargeback","payout","refund","interchange","merchant","processor","invoice","ach"]),
  ("ai-automation",     ["ai","agent","gpt","prompt","automation","workflow","zapier","make.com","n8n","webhook"]),
  ("operator-tools",    ["crm","hubspot","quickbooks","scheduling","no-show","appointment","invoice","bookkeeping","email","domain","dns"]),
  ("prediction-markets",["kalshi","polymarket","prediction","market","odds","hedge","arb","spread","moneyline"]),
  ("small-business-tech",["website","seo","vercel","hosting","shopify","checkout","analytics","tracking","pixel"]),
]


def fetch(url, ua="SideGuyFutureRadar/1.0"):
  try:
    req = Request(url, headers={"User-Agent": ua})
    return urlopen(req, timeout=20).read().decode("utf-8", errors="ignore")
  except (URLError, Exception):
    return ""


def slugify(s):
  s = s.lower()
  s = re.sub(r"[^a-z0-9\s\-]+", " ", s)
  s = re.sub(r"\s+", "-", s).strip("-")
  s = re.sub(r"-+", "-", s)
  return (s or "untitled")[:90]


def extract_items(rss_text):
  items = []
  for m in re.finditer(r"<item>(.*?)</item>", rss_text, flags=re.S | re.I):
    blk = m.group(1)
    t = re.search(r"<title>(.*?)</title>", blk, flags=re.S | re.I)
    l = re.search(r"<link>(.*?)</link>", blk, flags=re.S | re.I)
    if not t or not l:
      continue
    title = re.sub(r"\s+", " ", re.sub(r"<.*?>", "", t.group(1))).strip()
    link  = re.sub(r"\s+", " ", re.sub(r"<.*?>", "", l.group(1))).strip()
    if title and link:
      items.append((title, link))
  # Atom fallback
  if not items:
    for m in re.finditer(r"<entry>(.*?)</entry>", rss_text, flags=re.S | re.I):
      blk = m.group(1)
      t = re.search(r"<title.*?>(.*?)</title>", blk, flags=re.S | re.I)
      l = re.search(r"<link[^>]*href=[\"']([^\"']+)[\"']", blk, flags=re.S | re.I)
      if not t or not l:
        continue
      title = re.sub(r"\s+", " ", re.sub(r"<.*?>", "", t.group(1))).strip()
      link  = l.group(1).strip()
      if title and link:
        items.append((title, link))
  return items


def bucket_for(text):
  t = text.lower()
  best, best_hits = None, 0
  for name, keys in TOPIC_BUCKETS:
    hits = sum(1 for k in keys if k in t)
    if hits > best_hits:
      best_hits, best = hits, name
  return best or "general"


def hot_score(text):
  t = text.lower()
  score = 0.0
  for w, val in HOT_WORDS:
    if w in t:
      score += val
  if any(x in t for x in ["how to","why","fix","solution","help","error code"]):
    score += 2.0
  return score


def cluster_key(title):
  t = title.lower()
  t = re.sub(r"\b(stripe|square|vercel|openai|hubspot|quickbooks|kalshi|polymarket|shopify|zapier|make\.com|n8n)\b", "", t)
  t = re.sub(r"\b\d+(\.\d+)?\b", "", t)
  t = re.sub(r"[^a-z\s]", " ", t)
  t = re.sub(r"\s+", " ", t).strip()
  toks = t.split()[:6]
  return " ".join(toks) if toks else "misc"


def safe_write(path, s):
  os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
  with open(path, "w", encoding="utf-8") as f:
    f.write(s)


def esc(s):
  return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")


def main():
  os.makedirs(RAW_DIR, exist_ok=True)
  all_rows = []

  for name, url in SOURCES:
    print(f"  fetching {name}…", end=" ", flush=True)
    txt = fetch(url)
    safe_write(os.path.join(RAW_DIR, f"{name}.xml"), txt[:200000])
    items = extract_items(txt)
    print(f"{len(items)} items")
    for title, link in items[:120]:
      b  = bucket_for(title + " " + link)
      hs = hot_score(title)
      ck = cluster_key(title)
      sid = hashlib.md5((title + "|" + link).encode("utf-8")).hexdigest()[:10]
      all_rows.append({
        "id":       sid,
        "source":   name,
        "bucket":   b,
        "cluster":  ck,
        "title":    title,
        "link":     link,
        "hot_score": round(hs, 2),
        "slug":     slugify(title),
        "ts":       int(time.time()),
      })

  # Deduplicate by (title, link)
  seen, dedup = set(), []
  for r in all_rows:
    key = (r["title"].lower(), r["link"].lower())
    if key in seen:
      continue
    seen.add(key)
    dedup.append(r)

  # Cluster depth bonus
  clusters = {}
  for r in dedup:
    clusters.setdefault(r["cluster"], []).append(r)
  for ck, items in clusters.items():
    depth = len(items)
    for r in items:
      r["depth"] = depth
      r["radar_score"] = round(r["hot_score"] * 1.5 + min(10, depth) * 0.8, 2)

  dedup.sort(key=lambda r: r["radar_score"], reverse=True)

  # Top topics for build list
  top_topics = []
  for r in dedup[:60]:
    t = r["title"].lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    topic = slugify(
      t.replace(" how to "," ").replace(" why "," ")
       .replace(" fix "," ").replace(" error "," ")
    )
    if topic not in top_topics:
      top_topics.append(topic)
  safe_write(OUT_TOPICS, "\n".join(top_topics[:60]) + "\n")

  # CSV
  os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
  with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["radar_score","depth","hot_score","bucket","source","cluster","title","slug","link"])
    for r in dedup[:400]:
      w.writerow([r["radar_score"],r["depth"],r["hot_score"],r["bucket"],r["source"],r["cluster"],r["title"],r["slug"],r["link"]])

  # JSON
  safe_write(OUT_JSON, json.dumps({
    "generated_at": int(time.time()),
    "phone_sms":    PHONE_SMS,
    "count":        len(dedup),
    "top":          dedup[:200],
    "topics":       top_topics[:60],
  }, indent=2))

  # ── HTML ──
  top10 = dedup[:10]
  cards = ""
  for r in top10:
    cards += f"""
  <div class="card">
    <div class="meta">{esc(r['bucket'])} &bull; {esc(r['source'])} &bull; depth {r['depth']}</div>
    <div class="score">Radar {r['radar_score']}</div>
    <a class="title" href="{esc(r['link'])}" target="_blank" rel="noopener">{esc(r['title'])}</a>
    <div class="cluster">{esc(r['cluster'])}</div>
  </div>"""

  rows = ""
  for r in dedup[:100]:
    rows += f"""
  <tr>
    <td>{r['radar_score']}</td>
    <td>{r['depth']}</td>
    <td><span class="pill">{esc(r['bucket'])}</span></td>
    <td><a href="{esc(r['link'])}" target="_blank" rel="noopener">{esc(r['title'])}</a></td>
    <td class="muted">{esc(r['source'])}</td>
  </tr>"""

  topics_html = "".join([f"<li><code>{esc(t)}</code></li>" for t in top_topics[:30]])

  html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>SideGuy Future Radar</title>
<meta name="description" content="SideGuy Future Radar: live operator pain signals -&gt; scored targets -&gt; build list."/>
<link rel="canonical" href="https://sideguysolutions.com/future/radar.html"/>
<style>
  :root {{
    --bg:#06131f; --bg2:#071a2b; --txt:#d7f3ff; --mut:#86b7c7;
    --card:#0a2236; --line:#12344a; --glow:rgba(80,255,200,.22);
  }}
  body {{ margin:0; font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial;
    background:radial-gradient(1200px 700px at 20% 10%,#0b2b3d 0%,var(--bg) 55%),
               linear-gradient(180deg,var(--bg2),var(--bg));
    color:var(--txt); }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:26px 18px 90px; }}
  h1 {{ margin:0 0 8px; font-size:28px; letter-spacing:.2px; }}
  .sub {{ color:var(--mut); margin:0 0 18px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px; margin:16px 0 18px; }}
  .card {{ background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.01));
    border:1px solid var(--line); border-radius:14px; padding:14px;
    box-shadow:0 18px 40px rgba(0,0,0,.35); }}
  .meta {{ color:var(--mut); font-size:12px; margin-bottom:6px; }}
  .score {{ font-weight:800; font-size:14px; margin-bottom:6px; color:#b7ffef; text-shadow:0 0 18px var(--glow); }}
  .title {{ color:var(--txt); text-decoration:none; display:block; font-weight:700; line-height:1.25; }}
  .title:hover {{ text-decoration:underline; }}
  .cluster {{ margin-top:8px; color:var(--mut); font-size:12px; }}
  .panel {{ background:rgba(255,255,255,.03); border:1px solid var(--line); border-radius:14px; padding:14px; }}
  table {{ width:100%; border-collapse:collapse; margin-top:10px; }}
  th,td {{ border-bottom:1px solid rgba(255,255,255,.07); padding:10px 8px; font-size:13px; vertical-align:top; }}
  th {{ text-align:left; color:#bfefff; font-weight:800; }}
  .pill {{ display:inline-block; padding:3px 8px; border-radius:999px; border:1px solid rgba(255,255,255,.10); background:rgba(0,0,0,.20); color:#b7ffef; font-size:12px; }}
  .muted {{ color:var(--mut); font-size:12px; }}
  .split {{ display:grid; grid-template-columns:1.2fr .8fr; gap:12px; }}
  @media(max-width:900px) {{ .split {{ grid-template-columns:1fr; }} }}
  .cta {{
    position:fixed; right:18px; bottom:18px;
    background:rgba(5,25,35,.85); border:1px solid rgba(80,255,200,.35);
    box-shadow:0 0 0 6px rgba(80,255,200,.06),0 18px 50px rgba(0,0,0,.45);
    border-radius:999px; padding:12px 14px; display:flex; gap:10px; align-items:center;
    text-decoration:none; color:var(--txt); backdrop-filter:blur(10px);
    animation:pulse 1.8s infinite ease-in-out;
  }}
  .dot {{ width:12px; height:12px; border-radius:50%; background:#50ffc8; box-shadow:0 0 18px rgba(80,255,200,.45); }}
  @keyframes pulse {{ 0%{{transform:translateY(0)}} 50%{{transform:translateY(-2px)}} 100%{{transform:translateY(0)}} }}
  code {{ color:#b7ffef; }}
  a {{ color:#50ffc8; }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Future Radar</h1>
    <p class="sub">Live operator pain signals &rarr; scored targets &rarr; build list. (Auto-generated)</p>

    <div class="grid">
      {cards}
    </div>

    <div class="split">
      <div class="panel">
        <h2 style="margin:0 0 6px;font-size:18px;">Top 100 Signals</h2>
        <div class="muted">Scoring: hot_score &times; 1.5 + cluster depth bonus. Depth = how many variants echo the same pain.</div>
        <table>
          <thead><tr><th>Score</th><th>Depth</th><th>Bucket</th><th>Signal</th><th>Source</th></tr></thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <div class="panel">
        <h2 style="margin:0 0 6px;font-size:18px;">Build List (Top Topics)</h2>
        <div class="muted">Feed these into your generators (multiplier / auto-build). Updated on every run.</div>
        <ol style="margin:10px 0 0;padding-left:18px;line-height:1.35;">{topics_html}</ol>
        <div style="margin-top:14px" class="muted">
          Files:<br/>
          <code>future/future-radar.csv</code><br/>
          <code>future/future-radar.json</code><br/>
          <code>future/top-topics.txt</code>
        </div>
      </div>
    </div>
  </div>

  <a class="cta" href="{PHONE_SMS}">
    <span class="dot"></span>
    <span><strong>Text PJ</strong><br/><span class="muted">Future Radar &rarr; build it</span></span>
  </a>
</body>
</html>
"""
  safe_write(OUT_HTML, html)

  print("\nFuture Radar deployed:")
  print(f"  - {OUT_HTML}")
  print(f"  - {OUT_CSV}")
  print(f"  - {OUT_JSON}")
  print(f"  - {OUT_TOPICS}")
  print(f"  - Total signals: {len(dedup)}")
  if dedup:
    print(f"  - Top signal: {dedup[0]['title']} (score {dedup[0]['radar_score']})")


if __name__ == "__main__":
  main()
