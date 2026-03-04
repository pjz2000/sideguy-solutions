#!/usr/bin/env python3
import csv, os, re, glob, datetime
from collections import defaultdict

PHONE_E164   = os.environ.get("SIDEGUY_PHONE_E164",   "+17735441231")
PHONE_PRETTY = os.environ.get("SIDEGUY_PHONE_PRETTY", "773-544-1231")

CANDIDATES = [
    "radar/problem-radar-new.csv",
    "radar/problem-radar.csv",
    "data/problem-ideas-new.csv",
    "data/problem-ideas.csv",
    "problem-ideas-new.csv",
    "problem-ideas.csv",
    "scripts/problem-ideas-new.csv",
    "scripts/problem-ideas.csv",
]


def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_rows(path):
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        for r in reader:
            rows.append({k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()})
    return rows


def slugify(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:120] if s else "unknown"


def to_float(x, default=0.0):
    try:
        return float(str(x).strip())
    except Exception:
        return default


def pick_best_csv():
    for p in CANDIDATES:
        if os.path.exists(p):
            return p
    for p in glob.glob("**/*problem-ideas*.csv", recursive=True):
        if os.path.isfile(p):
            return p
    return None


def extract_fields(r):
    q      = r.get("q") or r.get("query") or r.get("question") or r.get("title") or r.get("problem") or ""
    topic  = r.get("topic") or r.get("cluster") or r.get("category") or r.get("route") or r.get("source") or ""
    score  = (r.get("priority_score") or r.get("score") or r.get("priority") or r.get("rank") or "")
    already = r.get("already_exists") or r.get("exists") or r.get("built") or ""
    slug   = r.get("slug") or r.get("path") or ""
    return q, topic, score, already, slug


def guess_problem_url(q, slug_hint):
    if slug_hint:
        s = slug_hint.strip().replace("\\", "/")
        if s.endswith(".html"):
            return "/" + s.lstrip("/")
        if s:
            return "/problems/" + s.strip("/") + ".html"
    return "/problems/" + slugify(q) + ".html"


def main():
    csv_path = pick_best_csv()
    if not csv_path:
        raise SystemExit("No problem-ideas CSV found.")

    rows = read_rows(csv_path)

    items = []
    for r in rows:
        q, topic, score, already, slug = extract_fields(r)
        if not q:
            continue
        s      = to_float(score)
        exists = str(already).strip().lower() in ("yes", "true", "1", "y")
        url    = guess_problem_url(q, slug)
        items.append({"q": q, "topic": topic.strip() or "General", "score": s, "exists": exists, "url": url})

    items.sort(key=lambda x: (x["exists"], -x["score"], x["q"].lower()))

    total       = len(items)
    top_unbuilt = [x for x in items if not x["exists"]][:200]
    top_built   = [x for x in items if     x["exists"]][:60]

    bucket = defaultdict(list)
    for x in top_unbuilt[:160]:
        bucket[x["topic"]].append(x)
    top_topics = sorted(bucket.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))[:14]

    out_path = os.path.join("radar", "index.html")
    os.makedirs("radar", exist_ok=True)
    built_ts = now_iso()

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>SideGuy Discovery Radar — Next Problems to Build</title>
  <meta name="description" content="SideGuy Discovery Radar: a living list of high-intent problems to build next, scored and grouped for fast ranking."/>
  <link rel="canonical" href="https://sideguysolutions.com/radar/"/>
  <meta property="og:title" content="SideGuy Discovery Radar"/>
  <meta property="og:description" content="High-intent problems detected + prioritized. Build the next pages automatically."/>
  <meta property="og:type" content="website"/>
  <style>
    :root {{
      --bg0:#04121c; --bg1:#062737;
      --card:rgba(255,255,255,.06); --line:rgba(255,255,255,.10);
      --txt:rgba(255,255,255,.92); --muted:rgba(255,255,255,.70);
      --mint:#54f7c7; --blue:#59b6ff; --good:#9cffc2;
      --shadow:0 18px 60px rgba(0,0,0,.45); --radius:18px;
      --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;
      --sans:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
    }}
    *{{box-sizing:border-box;}}
    body{{margin:0;font-family:var(--sans);color:var(--txt);
      background:radial-gradient(1200px 600px at 10% 10%,rgba(84,247,199,.14),transparent 55%),
        radial-gradient(900px 600px at 90% 0%,rgba(89,182,255,.14),transparent 55%),
        linear-gradient(180deg,var(--bg0),var(--bg1));min-height:100vh;overflow-x:hidden;}}
    a{{color:var(--mint);text-decoration:none;}} a:hover{{text-decoration:underline;}}
    .wrap{{max-width:1120px;margin:0 auto;padding:26px 18px 120px;}}
    .top{{display:flex;gap:14px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;
      padding:18px;border:1px solid var(--line);
      background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.03));
      border-radius:var(--radius);box-shadow:var(--shadow);}}
    .brand{{display:flex;gap:12px;align-items:center;}}
    .orb{{width:44px;height:44px;border-radius:999px;
      background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.9),rgba(84,247,199,.55) 30%,rgba(89,182,255,.35) 55%,rgba(0,0,0,.0) 72%);
      box-shadow:0 0 0 1px rgba(255,255,255,.12),0 18px 40px rgba(0,0,0,.45),0 0 24px rgba(84,247,199,.16);}}
    h1{{margin:0;font-size:18px;}}
    .sub{{color:var(--muted);font-size:13px;line-height:1.35;margin-top:4px;}}
    .meta{{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;font-family:var(--mono);font-size:12px;color:rgba(255,255,255,.72);}}
    .pill{{padding:7px 10px;border:1px solid var(--line);border-radius:999px;background:rgba(0,0,0,.20);white-space:nowrap;}}
    .grid{{display:grid;grid-template-columns:1.2fr .8fr;gap:14px;margin-top:14px;}}
    @media(max-width:920px){{.grid{{grid-template-columns:1fr;}}}}
    .card{{border:1px solid var(--line);background:rgba(255,255,255,.05);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;}}
    .card .hd{{padding:14px 14px 10px;border-bottom:1px solid rgba(255,255,255,.06);display:flex;gap:10px;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;}}
    .card .hd b{{font-size:14px;}} .card .hd span{{color:var(--muted);font-size:12px;}}
    .card .bd{{padding:14px;}}
    .kpi{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}}
    .kpi .box{{border:1px solid rgba(255,255,255,.09);background:rgba(0,0,0,.18);border-radius:14px;padding:10px;}}
    .kpi .num{{font-family:var(--mono);font-size:18px;color:var(--mint);}}
    .kpi .lab{{color:var(--muted);font-size:12px;margin-top:4px;}}
    .list{{display:flex;flex-direction:column;gap:10px;}}
    .row{{border:1px solid rgba(255,255,255,.08);background:rgba(0,0,0,.16);border-radius:14px;
      padding:10px;display:flex;gap:10px;align-items:flex-start;justify-content:space-between;}}
    .row .q{{font-size:13px;line-height:1.3;}} .row .t{{color:var(--muted);font-size:12px;margin-top:4px;}}
    .row .right{{text-align:right;flex:0 0 auto;font-family:var(--mono);font-size:12px;color:rgba(255,255,255,.75);}}
    .score{{display:inline-block;padding:6px 8px;border-radius:999px;border:1px solid rgba(255,255,255,.12);
      background:rgba(84,247,199,.10);color:var(--mint);}}
    .btns{{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px;}}
    .btn{{display:inline-flex;align-items:center;justify-content:center;padding:10px 12px;border-radius:12px;
      border:1px solid rgba(255,255,255,.12);background:rgba(0,0,0,.20);color:rgba(255,255,255,.92);
      text-decoration:none;font-size:13px;}}
    .btn:hover{{background:rgba(255,255,255,.06);text-decoration:none;}}
    .btn.primary{{border-color:rgba(84,247,199,.35);background:rgba(84,247,199,.10);}}
    .btn.primary:hover{{background:rgba(84,247,199,.14);}}
    .note{{margin-top:10px;color:var(--muted);font-size:12px;line-height:1.4;}}
    .topics{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;}}
    @media(max-width:720px){{.topics{{grid-template-columns:1fr;}}}}
    .topic{{border:1px solid rgba(255,255,255,.08);background:rgba(0,0,0,.16);border-radius:14px;padding:10px;}}
    .topic .name{{font-size:13px;}} .topic .count{{font-family:var(--mono);color:var(--mint);font-size:12px;margin-top:4px;}}
    .topic ul{{margin:8px 0 0;padding-left:16px;}} .topic li{{margin:6px 0;color:rgba(255,255,255,.86);font-size:12.5px;}}
    .textpj{{position:fixed;right:18px;bottom:18px;z-index:9999;display:flex;align-items:center;gap:10px;
      padding:12px 14px;border-radius:999px;border:1px solid rgba(84,247,199,.35);
      background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.18));
      box-shadow:0 16px 50px rgba(0,0,0,.55),0 0 26px rgba(84,247,199,.20);
      text-decoration:none;color:rgba(255,255,255,.95);backdrop-filter:blur(10px);}}
    .textpj .bubble{{width:40px;height:40px;border-radius:999px;
      background:radial-gradient(circle at 30% 30%,rgba(255,255,255,.9),rgba(84,247,199,.55) 34%,rgba(89,182,255,.30) 58%,rgba(0,0,0,0) 74%);}}
    .textpj .label{{display:flex;flex-direction:column;line-height:1.1;}}
    .textpj .label b{{font-size:13px;letter-spacing:.2px;}}
    .textpj .label span{{font-size:11px;color:rgba(255,255,255,.75);font-family:var(--mono);}}
  </style>
  <script type="application/ld+json">
  {{
    "@context":"https://schema.org",
    "@type":"CollectionPage",
    "name":"SideGuy Discovery Radar",
    "url":"https://sideguysolutions.com/radar/",
    "description":"A prioritized discovery feed of problems to build next (SideGuy Operator Intelligence).",
    "dateModified":"{built_ts}"
  }}
  </script>
</head>
<body>
  <div class="wrap">
    <div class="top">
      <div>
        <div class="brand">
          <div class="orb"></div>
          <div>
            <h1>SideGuy Discovery Radar</h1>
            <div class="sub">High-intent problems detected + prioritized. Auto-built from problem discovery CSV so you always know what to build next.</div>
          </div>
        </div>
        <div class="btns">
          <a class="btn" href="/">← Home</a>
          <a class="btn" href="/knowledge-hub.html">Knowledge Hub</a>
          <a class="btn" href="/operator-tools-hub.html">Operator Tools Hub</a>
          <a class="btn" href="/fresh/radar.html">Fresh Radar</a>
          <a class="btn primary" href="sms:{PHONE_E164}?body=SideGuy%20Radar%3A%20I%20need%20help%20routing%20a%20problem">Text PJ</a>
        </div>
        <div class="note">Built from: <span style="font-family:var(--mono);">{csv_path}</span> • Updated: <span style="font-family:var(--mono);">{built_ts}</span></div>
      </div>
      <div class="meta">
        <div class="pill">signal_rows={total}</div>
        <div class="pill">unbuilt_top={len(top_unbuilt)}</div>
        <div class="pill">built_seen={len(top_built)}</div>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <div class="hd"><b>Top Unbuilt Problems</b><span>highest score first</span></div>
        <div class="bd">
          <div class="kpi">
            <div class="box"><div class="num">{total}</div><div class="lab">signals in CSV</div></div>
            <div class="box"><div class="num">{len(top_unbuilt)}</div><div class="lab">top unbuilt candidates</div></div>
            <div class="box"><div class="num">{len(top_topics)}</div><div class="lab">topic buckets</div></div>
          </div>
          <div class="note">Use this like a "problem market." Build 10/day from the top and your site compounds forever.</div>
          <div class="list" style="margin-top:12px;">
"""

    for x in top_unbuilt[:40]:
        q     = x["q"]
        t     = x["topic"]
        score = f"{x['score']:.1f}" if x["score"] else "0.0"
        url   = x["url"]
        html += f"""
            <div class="row">
              <div class="left">
                <div class="q"><a href="{url}">{q}</a></div>
                <div class="t">{t}</div>
              </div>
              <div class="right"><div class="score">score {score}</div></div>
            </div>
"""

    html += """
          </div>
          <div class="note">After building a batch, re-run this script — the radar reshuffles automatically.</div>
        </div>
      </div>

      <div class="card">
        <div class="hd"><b>Topic Buckets</b><span>fast clustering</span></div>
        <div class="bd">
          <div class="topics">
"""

    for topic, arr in top_topics:
        html += f"""
            <div class="topic">
              <div class="name"><b>{topic}</b></div>
              <div class="count">{len(arr)} unbuilt candidates</div>
              <ul>
"""
        for y in arr[:5]:
            html += f'                <li><a href="{y["url"]}">{y["q"]}</a></li>\n'
        html += "              </ul>\n            </div>\n"

    html += f"""
          </div>

          <div class="card" style="margin-top:12px;">
            <div class="hd"><b>What to do next</b><span>Operator Mode</span></div>
            <div class="bd">
              <ol style="margin:0;padding-left:18px;color:rgba(255,255,255,.86);font-size:13px;line-height:1.5;">
                <li><b>Build 10</b> pages/day from "Top Unbuilt Problems".</li>
                <li>Wire each into <code style="font-family:var(--mono);">Related Problems</code> + <code style="font-family:var(--mono);">Best Next Pages</code>.</li>
                <li>Re-run sitemap generator after batches.</li>
                <li><b>Clarity before cost</b> + human help layer.</li>
              </ol>
            </div>
          </div>

          <div class="card" style="margin-top:12px;">
            <div class="hd"><b>Built Examples</b><span>already exists</span></div>
            <div class="bd">
              <div class="list">
"""

    for x in top_built[:12]:
        q     = x["q"]
        t     = x["topic"]
        score = f"{x['score']:.1f}" if x["score"] else "0.0"
        url   = x["url"]
        html += f"""
                <div class="row">
                  <div class="left">
                    <div class="q"><a href="{url}">{q}</a></div>
                    <div class="t">{t}</div>
                  </div>
                  <div class="right"><div class="score" style="background:rgba(156,255,194,.10);color:var(--good);border-color:rgba(156,255,194,.25);">built</div></div>
                </div>
"""

    html += f"""
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>

  <a class="textpj" href="sms:{PHONE_E164}?body=SideGuy%20Radar%3A%20I%20need%20help%20with%20a%20problem" aria-label="Text PJ">
    <div class="bubble"></div>
    <div class="label">
      <b>Text PJ</b>
      <span>{PHONE_PRETTY}</span>
    </div>
  </a>
</body>
</html>
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[OK] Wrote {out_path} from {csv_path} ({total} rows).")


if __name__ == "__main__":
    main()
