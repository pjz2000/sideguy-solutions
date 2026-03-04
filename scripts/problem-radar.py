#!/usr/bin/env python3
# ==============================================================
# SIDEGUY PROBLEM RADAR
# Pulls real-time "what's broken" signals from public sources:
#   - Google Suggest (unofficial, no key)
#   - StackOverflow API (public, no key)
#   - GitHub Issues search (public, no key)
#   - Reddit RSS search (public, no key)
# Outputs: radar/problem-radar.csv (all), radar/problem-radar-new.csv (unbuilt)
#          radar/top-100-slugs.txt
# ==============================================================

import csv, json, os, re, time, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

ROOT    = Path(__file__).parent.parent
OUT_DIR = ROOT / "radar"
RAW_DIR = ROOT / "radar" / "raw"
OUT_DIR.mkdir(exist_ok=True)
RAW_DIR.mkdir(exist_ok=True)

UA      = "SideGuyProblemRadar/1.0 (+https://sideguysolutions.com)"
TIMEOUT = 15

MAX_SUGGEST = 12
MAX_SO      = 40
MAX_GH      = 40
MAX_REDDIT  = 30

SEEDS = [
    # Payments / ops
    "payment processing not working",
    "chargeback payment declined",
    "stripe webhook not working",
    "square payout missing",
    "merchant account frozen",
    "ACH deposit not showing",
    # AI automation / ops
    "zapier not triggering",
    "make.com scenario not running",
    "ai agent not working",
    "gmail automation not sending",
    "hubspot workflow not firing",
    "google ads conversion not tracking",
    # Tech ops
    "dns not propagating",
    "ssl certificate error",
    "site indexing not working",
    "sitemap not found",
    # Prediction markets
    "kalshi order not filling",
    "polymarket price spread",
    "prediction market hedge",
]

PATTERNS = [
    "not working", "error", "failed", "declined", "stuck",
    "not triggering", "not sending", "not updating", "not showing", "how to fix",
]

SCORE_TERMS = {
    3: ["not working","error","declined","failed","stuck","won't","cant","can't","missing","not showing","not triggering","not sending"],
    2: ["stripe","chargeback","webhook","zapier","hubspot","quickbooks","dns","ssl","sitemap","indexing","kalshi","polymarket","merchant","payout","ach","invoice"],
}


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    return s[:90].strip("-")

def score_text(t: str) -> int:
    t = t.lower()
    sc = 0
    for pts, terms in SCORE_TERMS.items():
        for term in terms:
            if term in t:
                sc += pts
    if 25 <= len(t) <= 90:
        sc += 1
    return sc

def save_raw(name: str, data):
    path = RAW_DIR / f"{name}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def load_existing_slugs() -> set:
    dirs = [
        "problems","auto","concepts","clusters","pillars","generated",
        "longtail","prediction-markets","betting-lab","knowledge","hubs",
    ]
    slugs = set()
    for d in dirs:
        p = ROOT / d
        if not p.is_dir():
            continue
        for f in p.rglob("*.html"):
            slugs.add(f.stem)
    return slugs

def google_suggest(seed: str) -> list:
    q = urllib.parse.quote(seed)
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={q}"
    try:
        data = json.loads(http_get(url).decode("utf-8", errors="ignore"))
        return [s for s in (data[1] if isinstance(data, list) and len(data) > 1 else []) if isinstance(s, str)]
    except Exception:
        return []

def stackoverflow_questions(term: str) -> tuple:
    q = urllib.parse.quote(term)
    url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={q}&site=stackoverflow&pagesize={MAX_SO}"
    try:
        data = json.loads(http_get(url).decode("utf-8", errors="ignore"))
        titles = [it.get("title","").strip() for it in data.get("items",[]) if it.get("title","").strip()]
        return titles, data
    except Exception:
        return [], {}

def github_issues(term: str) -> tuple:
    q = urllib.parse.quote(term + " is:issue")
    url = f"https://api.github.com/search/issues?q={q}&per_page={MAX_GH}"
    try:
        data = json.loads(http_get(url).decode("utf-8", errors="ignore"))
        titles = [(it.get("title") or "").strip() for it in data.get("items",[]) if it.get("title","").strip()]
        return titles, data
    except Exception:
        return [], {}

def reddit_rss(term: str) -> tuple:
    q = urllib.parse.quote(term)
    url = f"https://www.reddit.com/search.rss?q={q}&sort=new"
    try:
        raw = http_get(url).decode("utf-8", errors="ignore")
        titles = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>", raw)[1:]
        return titles[:MAX_REDDIT], {"rss_bytes": len(raw)}
    except Exception:
        return [], {}


if __name__ == "__main__":
    print("=== Problem Radar ===\n")
    ts       = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    existing = load_existing_slugs()
    rows     = []

    # Build query list (seeds + seed×pattern combos, capped at 40)
    queries = []
    for s in SEEDS:
        queries.append(s)
    for s in SEEDS[:10]:
        for p in PATTERNS:
            queries.append(f"{s} {p}")
    queries = list(dict.fromkeys(q.strip() for q in queries if q.strip()))[:40]

    # Google Suggest
    print(f"  Google Suggest: running {len(queries)} queries…")
    g_raw = {}
    for q in queries:
        sugg = google_suggest(q)[:MAX_SUGGEST]
        g_raw[q] = sugg
        for s in sugg:
            slug = slugify(s)
            if slug:
                rows.append({"ts": ts, "source": "google_suggest", "query": q, "title": s, "slug": slug, "score": score_text(s)})
        time.sleep(0.25)
    save_raw("google_suggest", g_raw)
    print(f"    {sum(len(v) for v in g_raw.values())} suggestions")

    # StackOverflow
    print("  StackOverflow: searching…")
    so_titles, so_raw = stackoverflow_questions(" ".join(SEEDS[:3]))
    save_raw("stackoverflow", so_raw)
    for t in so_titles:
        slug = slugify(t)
        if slug:
            rows.append({"ts": ts, "source": "stackoverflow", "query": "seed_mix", "title": t, "slug": slug, "score": score_text(t)})
    print(f"    {len(so_titles)} results")

    # GitHub Issues
    print("  GitHub Issues: searching…")
    gh_titles, gh_raw = github_issues(" ".join(SEEDS[:3]))
    save_raw("github_issues", gh_raw)
    for t in gh_titles:
        slug = slugify(t)
        if slug:
            rows.append({"ts": ts, "source": "github_issues", "query": "seed_mix", "title": t, "slug": slug, "score": score_text(t)})
    print(f"    {len(gh_titles)} results")

    # Reddit RSS
    print("  Reddit RSS: fetching…")
    rr_titles, rr_raw = reddit_rss(" ".join(SEEDS[:3]))
    save_raw("reddit_rss", rr_raw)
    for t in rr_titles:
        slug = slugify(t)
        if slug:
            rows.append({"ts": ts, "source": "reddit_rss", "query": "seed_mix", "title": t, "slug": slug, "score": score_text(t)})
    print(f"    {len(rr_titles)} results")

    # Dedup by slug (keep best score)
    best = {}
    for r in rows:
        slug = r["slug"]
        if slug not in best or r["score"] > best[slug]["score"]:
            best[slug] = r
    all_rows = sorted(best.values(), key=lambda r: (-r["score"], r["slug"]))

    # Write all
    f_all = OUT_DIR / "problem-radar.csv"
    with open(f_all, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ts","source","query","title","slug","score"])
        w.writeheader(); w.writerows(all_rows)

    # Write new-only
    new_rows = [r for r in all_rows if r["slug"] not in existing]
    f_new = OUT_DIR / "problem-radar-new.csv"
    with open(f_new, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ts","source","query","title","slug","score"])
        w.writeheader(); w.writerows(new_rows)

    # Top-100 slugs
    f_top = OUT_DIR / "top-100-slugs.txt"
    f_top.write_text("\n".join(r["slug"] for r in new_rows[:100]) + "\n", encoding="utf-8")

    print(f"\n  Candidates : {len(all_rows)}")
    print(f"  New only   : {len(new_rows)}")
    print(f"  Wrote: radar/problem-radar.csv")
    print(f"  Wrote: radar/problem-radar-new.csv")
    print(f"  Wrote: radar/top-100-slugs.txt")
