#!/usr/bin/env python3
"""
SideGuy Trend Seismograph Engine
Predicts rising search demand from radar signals.
Scores each term on: radar score + hot-word presence + query-cluster depth.
Outputs: trends/seismograph.html + reports/trend-seismograph.json
"""
import csv, json, os, re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".").resolve()

RADAR_FILES = [
    "radar/problem-radar.csv",
    "radar/problem-radar-new.csv",
    "data/problem-ideas-new.csv",
    "data/problem-ideas.csv",
    "multiplier/problem-seeds.csv",
]

OUT_JSON = ROOT / "reports" / "trend-seismograph.json"
OUT_HTML = ROOT / "trends"  / "seismograph.html"
OUT_HTML.parent.mkdir(parents=True, exist_ok=True)

PHONE_SMS  = "sms:+17735441231"
PHONE_DISP = "773-544-1231"
DOMAIN     = "https://sideguysolutions.com"

HOT_WORDS = {
    "ai":3, "agent":3, "automation":3, "gpt":3, "llm":3, "claude":3,
    "crypto":3, "solana":3, "bitcoin":3, "prediction":3, "kalshi":3,
    "polymarket":3, "trading":3, "market":3,
    "payment":2, "stripe":2, "webhook":2, "api":2, "compliance":2,
    "software":2, "build":2, "automate":2,
    "how":1, "why":1, "fix":1, "error":1, "problem":1,
    "cost":1, "vs":1, "compare":1, "setup":1,
}

# Topic buckets for grouping signals
BUCKETS = [
    ("ai-automation",       ["ai","agent","automation","llm","gpt","claude","zapier","make","n8n","workflow"]),
    ("payments",            ["payment","stripe","square","checkout","chargeback","payout","invoice","billing"]),
    ("prediction-markets",  ["kalshi","polymarket","predictit","prediction","market","trading","odds","bet"]),
    ("software",            ["software","app","api","webhook","build","code","deploy","cloud","saas"]),
    ("crypto",              ["crypto","solana","bitcoin","ethereum","wallet","defi","token"]),
    ("operations",          ["cost","pricing","setup","how","fix","error","problem","not working","guide"]),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def detect_bucket(term: str) -> str:
    tl = term.lower()
    for bucket, keywords in BUCKETS:
        if any(k in tl for k in keywords):
            return bucket
    return "other"


def score_term(title: str, query: str, radar_score: float) -> float:
    tl = (title + " " + query).lower()
    s = radar_score * 1.5  # weight the radar's own score
    for word, bonus in HOT_WORDS.items():
        if word in tl:
            s += bonus
    # longer titles = more specific = slight bonus
    s += len(title.split()) * 0.3
    return round(s, 2)


def read_radar() -> list[dict]:
    rows = []
    seen_slugs = set()

    for rf in RADAR_FILES:
        path = ROOT / rf
        if not path.exists():
            continue
        try:
            with path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    r = {k.strip(): v.strip() if isinstance(v, str) else v
                         for k, v in r.items()}
                    # normalize column names
                    title = r.get("title") or r.get("query") or r.get("keyword") or ""
                    query = r.get("query") or title
                    slug  = r.get("slug") or re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
                    ts    = r.get("ts", "")
                    radar_score = float(r.get("score", 5) or 5)

                    if not title or slug in seen_slugs:
                        continue
                    seen_slugs.add(slug)

                    rows.append({
                        "title":       title,
                        "query":       query,
                        "slug":        slug,
                        "ts":          ts,
                        "radar_score": radar_score,
                        "source_file": rf,
                    })
        except Exception as e:
            print(f"  [warn] {rf}: {e}")

    return rows


def build_signals(rows: list[dict]) -> list[dict]:
    # Group by query cluster to get depth (how many suggestions each query spawned)
    cluster_counts: dict[str, int] = {}
    for r in rows:
        q = r["query"].lower().strip()
        cluster_counts[q] = cluster_counts.get(q, 0) + 1

    results = []
    for r in rows:
        q     = r["query"].lower().strip()
        depth = cluster_counts.get(q, 1)
        sig   = score_term(r["title"], r["query"], r["radar_score"])
        sig  += min(depth * 0.5, 5.0)  # cluster depth bonus (capped)

        results.append({
            "term":          r["title"],
            "query_cluster": r["query"],
            "slug":          r["slug"],
            "bucket":        detect_bucket(r["title"]),
            "seis_score":    round(sig, 2),
            "radar_score":   r["radar_score"],
            "cluster_depth": depth,
            "ts":            r["ts"],
        })

    results.sort(key=lambda x: x["seis_score"], reverse=True)
    return results[:100]


def build_html(data: list[dict]) -> str:
    generated = now_iso()
    top10 = data[:10]

    # Bucket summary
    bucket_totals: dict[str, int] = {}
    for d in data:
        b = d["bucket"]
        bucket_totals[b] = bucket_totals.get(b, 0) + 1

    bucket_pills = "".join(
        f'<span class="pill"><b>{b}</b> {n}</span>'
        for b, n in sorted(bucket_totals.items(), key=lambda x: -x[1])
    )

    def bar(score: float, max_score: float = 40.0) -> str:
        pct = min(int(score / max_score * 100), 100)
        return (
            f'<div style="background:rgba(255,255,255,.08);border-radius:999px;height:6px;margin-top:4px;">'
            f'<div style="width:{pct}%;height:6px;border-radius:999px;'
            f'background:linear-gradient(90deg,#6ef3c5,#4ad7ff);"></div></div>'
        )

    rows_html = ""
    for i, d in enumerate(data):
        slug_href = f"/problems/multiplied/{d['slug']}.html"
        exists    = (ROOT / slug_href.lstrip("/")).exists()
        link      = f'<a href="{slug_href}">{d["term"]}</a>' if exists else d["term"]
        rows_html += f"""
        <tr>
          <td style="color:#9bc2d6;font-size:12px;">{i+1}</td>
          <td>{link}<br/>{bar(d['seis_score'])}</td>
          <td><span class="pill pill-{d['bucket']}">{d['bucket']}</span></td>
          <td style="font-weight:700;color:#6ef3c5;">{d['seis_score']}</td>
          <td style="color:#9bc2d6;font-size:13px;">{d['cluster_depth']}</td>
        </tr>"""

    top10_cards = ""
    for d in top10:
        top10_cards += f"""
        <div class="card" style="grid-column:span 6;">
          <div style="font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#9bc2d6;">{d['bucket']}</div>
          <div style="font-weight:800;margin:6px 0 4px;font-size:15px;">{d['term']}</div>
          <div style="font-size:13px;color:#9bc2d6;">Score: <b style="color:#6ef3c5;">{d['seis_score']}</b> · Cluster depth: {d['cluster_depth']}</div>
          {bar(d['seis_score'])}
        </div>"""

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>SideGuy Trend Seismograph — Rising Search Signals</title>
  <meta name="description" content="SideGuy Trend Seismograph: predicted rising search demand from Google Suggest radar signals. Top 100 terms scored by demand momentum."/>
  <link rel="canonical" href="{DOMAIN}/trends/seismograph.html"/>
  <style>
    :root{{--bg:#07121a;--panel:#0b1b25;--card:#0e2230;--line:#163548;
      --text:#eaf6ff;--muted:#9bc2d6;--mint:#6ef3c5;--aqua:#4ad7ff;}}
    *{{box-sizing:border-box}}
    body{{margin:0;background:
      radial-gradient(1200px 800px at 20% -10%,#0a2d40 0%,var(--bg) 55%);
      color:var(--text);font-family:ui-sans-serif,-apple-system,Segoe UI,Inter,Arial;}}
    a{{color:var(--aqua);text-decoration:none}}a:hover{{text-decoration:underline}}
    .wrap{{max-width:1100px;margin:0 auto;padding:28px 18px 120px}}
    .hero{{padding:18px;border:1px solid var(--line);border-radius:18px;
      background:linear-gradient(180deg,var(--panel),transparent);margin-bottom:14px;}}
    .kicker{{color:var(--muted);font-size:13px;letter-spacing:.08em;text-transform:uppercase}}
    h1{{margin:10px 0 8px;font-size:30px;letter-spacing:-.02em}}
    h3{{margin:0 0 10px}}
    .sub{{color:var(--muted);line-height:1.5;margin:0 0 12px;max-width:720px}}
    .grid{{display:grid;grid-template-columns:repeat(12,1fr);gap:12px;margin-bottom:14px}}
    .card{{grid-column:span 12;border:1px solid var(--line);border-radius:16px;
      padding:16px;background:rgba(14,34,48,.75);}}
    @media(min-width:700px){{.card[style*="span 6"]{{grid-column:span 6}}}}
    .pill{{display:inline-block;border:1px solid rgba(255,255,255,.14);border-radius:999px;
      padding:4px 10px;font-size:12px;background:rgba(0,0,0,.22);color:var(--text);margin:2px;}}
    .pillrow{{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}}
    .pill-ai-automation{{border-color:rgba(110,243,197,.4);color:#6ef3c5}}
    .pill-payments{{border-color:rgba(74,215,255,.4);color:#4ad7ff}}
    .pill-prediction-markets{{border-color:rgba(255,209,102,.4);color:#ffd166}}
    .pill-crypto{{border-color:rgba(255,150,100,.4);color:#ff9664}}
    .pill-software{{border-color:rgba(160,140,255,.4);color:#a08cff}}
    .pill-operations{{border-color:rgba(200,200,200,.2);color:#c0d8e8}}
    table{{width:100%;border-collapse:collapse;font-size:14px}}
    td,th{{border-bottom:1px solid rgba(255,255,255,.07);padding:10px 8px;text-align:left;vertical-align:middle;}}
    th{{color:var(--muted);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.05em}}
    .floatBtn{{position:fixed;right:16px;bottom:16px;z-index:9999;display:flex;
      align-items:center;gap:10px;padding:13px 16px;border-radius:999px;
      background:linear-gradient(135deg,rgba(110,243,197,.22),rgba(74,215,255,.18));
      border:1px solid rgba(110,243,197,.45);box-shadow:0 16px 40px rgba(0,0,0,.4);
      color:var(--text);font-weight:700;text-decoration:none;font-size:14px;}}
    .floatBtn:hover{{transform:translateY(-2px);text-decoration:none;}}
    .dot{{width:9px;height:9px;border-radius:50%;background:var(--mint);
      animation:pulse 1.6s infinite;box-shadow:0 0 0 0 rgba(110,243,197,.5);}}
    @keyframes pulse{{
      0%{{box-shadow:0 0 0 0 rgba(110,243,197,.5)}}
      70%{{box-shadow:0 0 0 14px rgba(110,243,197,0)}}
      100%{{box-shadow:0 0 0 0 rgba(110,243,197,0)}}
    }}
  </style>
</head>
<body>
<a class="floatBtn" href="{PHONE_SMS}">
  <span class="dot"></span> Text PJ &nbsp;·&nbsp; {PHONE_DISP}
</a>
<div class="wrap">
  <div class="hero">
    <div class="kicker">SideGuy Intelligence Layer</div>
    <h1>📡 Trend Seismograph</h1>
    <p class="sub">Predicted rising search demand scored from Google Suggest radar signals. Terms with high cluster depth = many related searches surfaced from a single root query — a leading indicator of demand momentum.</p>
    <div class="pillrow">
      <span class="pill">Signals: <b>{len(data)}</b></span>
      <span class="pill">Generated: <b>{generated}</b></span>
      {bucket_pills}
    </div>
  </div>

  <h3 style="margin:18px 0 10px;font-size:16px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;">Top 10 Hot Signals</h3>
  <div class="grid">
    {top10_cards}
  </div>

  <div class="card">
    <h3>Full Signal Table — Top 100</h3>
    <p style="color:var(--muted);font-size:13px;margin:0 0 12px;">
      Seismograph score = radar score × 1.5 + hot-word bonus + cluster depth bonus.
      Cluster depth = how many Google Suggest variants a single root query produced.
    </p>
    <table>
      <thead><tr>
        <th>#</th><th>Search Term</th><th>Bucket</th>
        <th>Score</th><th>Depth</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>

  <div style="margin-top:16px;font-size:13px;color:var(--muted);">
    <a href="/knowledge/knowledge-graph.html">Knowledge Graph</a> &nbsp;·&nbsp;
    <a href="/radar/index.html">Discovery Radar</a> &nbsp;·&nbsp;
    <a href="/decisions/index.html">Decisions</a> &nbsp;·&nbsp;
    <a href="/">SideGuy Home</a>
  </div>
</div>
</body>
</html>
"""


def main():
    os.makedirs("reports", exist_ok=True)
    os.makedirs("trends",  exist_ok=True)

    rows = read_radar()
    if not rows:
        print("[seismograph] No radar data found. Run problem-radar.py first.")
        return

    signals = build_signals(rows)

    OUT_JSON.write_text(json.dumps(signals, indent=2), encoding="utf-8")
    OUT_HTML.write_text(build_html(signals), encoding="utf-8")

    print(f"[seismograph] signals={len(signals)}")
    print(f"[seismograph] wrote: {OUT_HTML}")
    print(f"[seismograph] wrote: {OUT_JSON}")
    print("Top 5:")
    for s in signals[:5]:
        print(f"  {s['seis_score']:5.1f}  {s['term']}")


if __name__ == "__main__":
    main()
