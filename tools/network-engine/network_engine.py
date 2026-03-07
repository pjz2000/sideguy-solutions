import os
import re
import csv
import html
import json
import datetime
from collections import defaultdict
from pathlib import Path

RADAR_FILE = Path("docs/problem-radar/radar-signals.tsv")
LEADERBOARD_FILE = Path("docs/traffic-engine/problem-leaderboard.md")
OUT_DIR = Path("public/network")
DOCS_DIR = Path("docs/network")
MANIFEST_FILE = DOCS_DIR / "network-manifest.md"
JSON_FILE = DOCS_DIR / "network-map.json"
INDEX_FILE = OUT_DIR / "index.html"

OUT_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

PRIMARY_BUCKET_RULES = {
    "payments":           ["payment","payments","merchant","processor","processing","chargeback","stripe","square","pos","terminal"],
    "automation":         ["ai","automation","chatbot","crm","software","workflow","assistant"],
    "marketing":          ["seo","google ads","ads","website","leads","ranking","ppc","traffic"],
    "local-services":     ["hvac","plumbing","electrical","contractor","repair","install","service business"],
    "energy":             ["solar","energy","battery","utility","clean tech","charger"],
    "compliance-medical": ["medical","compliance","device","regulated","validation","quality"],
    "general":            [],
}

INTENT_BUCKETS = {
    "money":      ["cost","pricing","fees","quote","roi","worth it","save money","cheaper"],
    "comparison": [" vs ","alternative","alternatives","compared to"],
    "urgency":    ["broken","not working","stopped working","fix","problem","issue","troubleshooting","urgent"],
    "local":      ["san diego","encinitas","carlsbad","oceanside","vista","san marcos","escondido",
                   "del mar","la jolla","coronado","chula vista","near me"],
    "operator":   ["for small business","for contractors","for restaurants","for medical offices",
                   "for service business","for local business"],
    "education":  ["explained","how it works","what is","how do i","why is","checklist","setup guide"],
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def nice(text: str) -> str:
    return " ".join(w.capitalize() for w in text.replace("-", " ").split())


def detect_primary_bucket(topic: str) -> str:
    t = topic.lower()
    for bucket, keywords in PRIMARY_BUCKET_RULES.items():
        for kw in keywords:
            if kw in t:
                return bucket
    return "general"


def detect_intents(topic: str):
    t = topic.lower()
    found = [b for b, kws in INTENT_BUCKETS.items() if any(kw in t for kw in kws)]
    return found or ["core"]


def load_radar():
    if not RADAR_FILE.exists():
        return []
    rows = []
    with open(RADAR_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            topic = (row.get("topic") or "").strip()
            if not topic:
                continue
            try:
                score = int(row.get("score") or 0)
            except ValueError:
                score = 0
            rows.append({
                "topic": topic, "score": score,
                "source": row.get("source", "radar"),
                "bucket": row.get("bucket", ""),
                "signal_type": row.get("signal_type", ""),
            })
    return rows


def load_leaderboard():
    if not LEADERBOARD_FILE.exists():
        return []
    rows = []
    with open(LEADERBOARD_FILE, encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|") or "---" in line or "Rank" in line:
                continue
            parts = [x.strip() for x in line.split("|")]
            if len(parts) < 5:
                continue
            try:
                rows.append({"rank": int(parts[1]), "topic": parts[2],
                              "score": int(parts[3]), "cluster": parts[4], "source": "leaderboard"})
            except (ValueError, IndexError):
                continue
    return rows


def merge_sources(radar_rows, leaderboard_rows):
    merged = {}
    for row in radar_rows:
        slug = slugify(row["topic"])
        merged[slug] = {
            "topic": row["topic"], "score": row["score"], "source": row["source"],
            "bucket": row.get("bucket") or detect_primary_bucket(row["topic"]),
            "intents": detect_intents(row["topic"]),
        }
    for row in leaderboard_rows:
        slug = slugify(row["topic"])
        if slug in merged:
            merged[slug]["score"] = max(merged[slug]["score"], row["score"])
            merged[slug]["source"] = "radar+leaderboard"
        else:
            merged[slug] = {
                "topic": row["topic"], "score": row["score"], "source": row["source"],
                "bucket": detect_primary_bucket(row["topic"]),
                "intents": detect_intents(row["topic"]),
            }
    return list(merged.values())


def topic_url(topic: str) -> str:
    return f"/auto/problem-pages/{slugify(topic)}.html"


def network_url(slug: str) -> str:
    return f"/network/{slug}.html"


def _orb() -> str:
    return '<a class="orb" href="sms:+17735441231">Text PJ</a>'


def _styles() -> str:
    return """<style>
    :root{--mint:#21d3a1;--ink:#073044;--bg:#f7fbff}
    body{font-family:-apple-system,system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:40px 20px;line-height:1.6;background:radial-gradient(ellipse at 20% 40%,#b8f4f0 0%,#d6f5ff 35%,var(--bg) 70%,#fff8f0 100%);color:var(--ink)}
    .card{background:#fff;border:1px solid #d9e8f2;border-radius:18px;padding:22px;margin:20px 0;box-shadow:0 4px 20px rgba(7,48,68,.07)}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
    a{color:#0b5cad;text-decoration:none}
    a:hover{text-decoration:underline}
    .orb{position:fixed;right:18px;bottom:18px;background:var(--mint);color:#fff;padding:14px 18px;border-radius:999px;text-decoration:none;font-weight:700;box-shadow:0 6px 20px rgba(33,211,161,.4);animation:pulse 2.5s ease-in-out infinite}
    @keyframes pulse{0%,100%{box-shadow:0 6px 20px rgba(33,211,161,.4)}50%{box-shadow:0 6px 32px rgba(33,211,161,.7)}}
    .muted{opacity:.7;font-size:.85rem}
  </style>"""


def write_bucket_page(bucket, rows):
    slug = slugify(bucket)
    path = OUT_DIR / f"{slug}.html"
    top_rows = sorted(rows, key=lambda x: (-x["score"], x["topic"]))[:120]

    intent_map = defaultdict(list)
    for row in top_rows:
        for intent in row["intents"]:
            intent_map[intent].append(row)

    sections = []
    for intent, items in sorted(intent_map.items()):
        lis = "".join(
            f'<li><a href="{topic_url(r["topic"])}">{html.escape(r["topic"])}</a> · score {r["score"]}</li>'
            for r in items[:20]
        )
        sections.append(f'<section class="card"><h2>{html.escape(nice(intent))}</h2><ul>{lis}</ul></section>')

    all_links = "".join(
        f'<li><a href="{topic_url(r["topic"])}">{html.escape(r["topic"])}</a></li>'
        for r in top_rows[:60]
    )

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(nice(bucket))} Network | SideGuy Solutions</title>
  <meta name="description" content="Explore the SideGuy {html.escape(bucket)} network: money questions, urgency problems, local intent, and operator-grade pages.">
  <link rel="canonical" href="https://www.sideguysolutions.com{network_url(slug)}">
  {_styles()}
</head>
<body>
  <p><a href="/network/index.html">← Back to Network Index</a></p>
  <h1>{html.escape(nice(bucket))} Network</h1>
  <p class="muted">Updated {now} · {len(top_rows)} mapped topics</p>

  <div class="card">
    <p>This network page groups SideGuy topics in the <strong>{html.escape(bucket)}</strong> category so the site behaves more like an authority map.</p>
  </div>

  <div class="grid">{''.join(sections[:6])}</div>

  <div class="card">
    <h2>All Core Topics</h2>
    <ul>{all_links}</ul>
  </div>

  {_orb()}
</body>
</html>
"""
    path.write_text(page, encoding="utf-8")
    return {"bucket": bucket, "slug": slug, "count": len(top_rows)}


def write_index(bucket_pages, bucket_map):
    cards = "".join(
        f'<div class="card"><h2><a href="{network_url(p["slug"])}">{html.escape(nice(p["bucket"]))}</a></h2>'
        f'<p>{p["count"]} mapped topics in this bucket.</p></div>'
        for p in sorted(bucket_pages, key=lambda x: x["bucket"])
    )

    highlights = []
    for bucket, rows in sorted(bucket_map.items(), key=lambda kv: len(kv[1]), reverse=True)[:6]:
        top = sorted(rows, key=lambda x: (-x["score"], x["topic"]))[:8]
        lis = "".join(
            f'<li><a href="{topic_url(r["topic"])}">{html.escape(r["topic"])}</a> · score {r["score"]}</li>'
            for r in top
        )
        highlights.append(f'<section class="card"><h2>{html.escape(nice(bucket))}</h2><ul>{lis}</ul></section>')

    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>SideGuy Network Index</title>
  <meta name="description" content="SideGuy Network Index: a public map of problem clusters across payments, AI, local services, marketing, energy, and compliance.">
  <link rel="canonical" href="https://www.sideguysolutions.com/network/index.html">
  {_styles()}
</head>
<body>
  <p><a href="/">← Back to Home</a></p>
  <h1>SideGuy Network Index</h1>
  <p class="muted">Updated {now}</p>

  <div class="card">
    <p>Google discovers the problem. AI explains it. A real human resolves it.</p>
    <p>This index is the public-facing map of SideGuy's self-expanding problem network.</p>
  </div>

  <div class="grid">{cards}</div>

  {''.join(highlights)}

  {_orb()}
</body>
</html>
"""
    INDEX_FILE.write_text(page, encoding="utf-8")


def write_manifest(bucket_map):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        f.write(f"# SideGuy Network Manifest\n\nGenerated: {now}\n\n")
        for bucket, rows in sorted(bucket_map.items(), key=lambda kv: -len(kv[1])):
            f.write(f"## {nice(bucket)}\n\n")
            for row in sorted(rows, key=lambda x: (-x["score"], x["topic"]))[:40]:
                f.write(f"- {row['topic']} | score {row['score']} | intents: {', '.join(row['intents'])}\n")
            f.write("\n")


def write_json(bucket_map):
    out = {
        bucket: [
            {"topic": r["topic"], "score": r["score"], "source": r["source"],
             "intents": r["intents"], "url": topic_url(r["topic"])}
            for r in sorted(rows, key=lambda x: (-x["score"], x["topic"]))[:120]
        ]
        for bucket, rows in bucket_map.items()
    }
    JSON_FILE.write_text(json.dumps(out, indent=2), encoding="utf-8")


def main():
    radar_rows = load_radar()
    leaderboard_rows = load_leaderboard()
    merged = merge_sources(radar_rows, leaderboard_rows)

    bucket_map = defaultdict(list)
    for row in merged:
        bucket_map[row["bucket"] or detect_primary_bucket(row["topic"])].append(row)

    bucket_pages = []
    for bucket, rows in sorted(bucket_map.items(), key=lambda kv: -len(kv[1])):
        bucket_pages.append(write_bucket_page(bucket, rows))

    write_index(bucket_pages, bucket_map)
    write_manifest(bucket_map)
    write_json(bucket_map)

    print("Network engine complete.")
    print(f"Buckets built:  {len(bucket_pages)}")
    print(f"Network index:  {INDEX_FILE}")
    print(f"Manifest:       {MANIFEST_FILE}")
    print(f"JSON map:       {JSON_FILE}")


if __name__ == "__main__":
    main()
