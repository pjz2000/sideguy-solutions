import csv
import os
import re
import html
import datetime
from collections import defaultdict, Counter
from pathlib import Path

PAGES_CSV = Path("data/gsc/pages.csv")
QUERIES_CSV = Path("data/gsc/queries.csv")

DOCS_DIR = Path("docs/learning-loop")
INCLUDES_DIR = Path("public/includes")

REPORT_FILE = DOCS_DIR / "learning-loop-report.md"
MANIFEST_FILE = DOCS_DIR / "next-build-manifest.md"
WINNERS_INCLUDE = INCLUDES_DIR / "learning-loop-winners.html"

DOCS_DIR.mkdir(parents=True, exist_ok=True)
INCLUDES_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"[^a-z0-9\s/-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def parse_float(v):
    s = str(v or "").strip().replace(",", "").replace("%", "")
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def normalize_row_keys(row):
    return {str(k).strip().lower(): v for k, v in row.items()}


def first_present(row, names, default=""):
    for n in names:
        if n in row and str(row[n]).strip():
            return str(row[n]).strip()
    return default


def load_csv(path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [normalize_row_keys(r) for r in csv.DictReader(f)]


def read_pages():
    out = []
    for row in load_csv(PAGES_CSV):
        page = first_present(row, ["page", "top pages", "url", "link", "address"])
        if not page:
            continue
        out.append({
            "page":        page,
            "clicks":      parse_float(first_present(row, ["clicks"])),
            "impressions": parse_float(first_present(row, ["impressions"])),
            "ctr":         parse_float(first_present(row, ["ctr", "site ctr"])),
            "position":    parse_float(first_present(row, ["position", "average position"])),
        })
    return out


def read_queries():
    out = []
    for row in load_csv(QUERIES_CSV):
        query = first_present(row, ["query", "top queries", "search query"])
        if not query:
            continue
        out.append({
            "query":       query,
            "clicks":      parse_float(first_present(row, ["clicks"])),
            "impressions": parse_float(first_present(row, ["impressions"])),
            "ctr":         parse_float(first_present(row, ["ctr", "site ctr"])),
            "position":    parse_float(first_present(row, ["position", "average position"])),
        })
    return out


def classify_page(url: str) -> str:
    u = url.lower()
    if "/auto/problem-pages/" in u: return "problem-page"
    if "/auto/problem-hubs/" in u:  return "problem-hub"
    if "/network/" in u:            return "network"
    if "/discovery/" in u:          return "discovery"
    if any(x in u for x in ["payment", "merchant", "stripe", "square"]): return "payments"
    if any(x in u for x in ["seo", "google-ads", "ppc", "website", "lead"]): return "marketing"
    if any(x in u for x in ["ai", "automation", "chatbot", "crm", "software"]): return "automation"
    if any(x in u for x in ["hvac", "plumbing", "electrical", "contractor", "repair"]): return "local-services"
    return "general"


def classify_query(query: str) -> dict:
    q = query.lower()
    bucket = "general"
    intent = "core"

    if any(x in q for x in ["payment","merchant","processor","stripe","square","chargeback","pos"]):
        bucket = "payments"
    elif any(x in q for x in ["ai","automation","chatbot","crm","software"]):
        bucket = "automation"
    elif any(x in q for x in ["seo","google ads","ppc","website","lead","ranking"]):
        bucket = "marketing"
    elif any(x in q for x in ["hvac","plumbing","electrical","contractor","repair","install"]):
        bucket = "local-services"
    elif any(x in q for x in ["solar","energy","battery","utility"]):
        bucket = "energy"
    elif any(x in q for x in ["medical","compliance","device"]):
        bucket = "compliance-medical"

    if " vs " in q or "alternative" in q:
        intent = "comparison"
    elif any(x in q for x in ["cost","pricing","fees","quote","worth it","roi"]):
        intent = "money"
    elif any(x in q for x in ["near me","san diego","encinitas","carlsbad","oceanside","vista","coronado","la jolla"]):
        intent = "local"
    elif any(x in q for x in ["broken","not working","fix","troubleshooting","problem","issue"]):
        intent = "urgency"
    elif any(x in q for x in ["what is","how","why","explained","guide","checklist"]):
        intent = "education"
    elif any(x in q for x in ["for small business","for contractors","for restaurants","for medical offices"]):
        intent = "operator"

    return {"bucket": bucket, "intent": intent}


def page_score(row) -> float:
    pos = row["position"] if row["position"] > 0 else 100.0
    return round(
        row["clicks"] * 8.0
        + min(row["impressions"], 5000) * 0.08
        + row["ctr"] * 2.0
        + max(0, 25.0 - pos) * 1.5,
        2,
    )


def query_score(row) -> float:
    pos = row["position"] if row["position"] > 0 else 100.0
    imp = row["impressions"]
    opportunity = 0.0
    if imp >= 20 and row["clicks"] < max(1, imp * 0.02):
        opportunity += imp * 0.12
    opportunity += max(0, 18.0 - pos) * 1.1
    opportunity += row["ctr"] * 1.2
    opportunity += row["clicks"] * 4.0
    return round(opportunity, 2)


def top_patterns(queries):
    bucket_counter, intent_counter = Counter(), Counter()
    bucket_weight, intent_weight = defaultdict(float), defaultdict(float)
    for row in queries:
        c = classify_query(row["query"])
        s = query_score(row)
        bucket_counter[c["bucket"]] += 1
        intent_counter[c["intent"]] += 1
        bucket_weight[c["bucket"]] += s
        intent_weight[c["intent"]] += s
    return {
        "bucket_counter": bucket_counter, "intent_counter": intent_counter,
        "bucket_weight": bucket_weight,   "intent_weight": intent_weight,
    }


def recommend_builds(queries):
    recs, seen = [], set()
    for row in sorted(queries, key=lambda x: (-query_score(x), -x["impressions"], x["query"])):
        q = row["query"].strip()
        key = slugify(q)
        if not key or key in seen:
            continue
        seen.add(key)
        c = classify_query(q)
        recs.append({
            "query": q, "bucket": c["bucket"], "intent": c["intent"],
            "score": query_score(row), "impressions": row["impressions"],
            "clicks": row["clicks"], "position": row["position"],
        })
        if len(recs) >= 40:
            break
    return recs


def build_include(top_pages):
    cards = []
    for row in top_pages[:6]:
        label = classify_page(row["page"])
        title = row["page"].replace("https://www.sideguysolutions.com", "").strip("/") or "home"
        cards.append(
            f'\n      <div class="sg-ll-card">'
            f'\n        <div class="sg-ll-kicker">Live Winner · {html.escape(label)}</div>'
            f'\n        <h3><a href="{html.escape(row["page"])}">{html.escape(title)}</a></h3>'
            f'\n        <p>{int(row["clicks"])} clicks · {int(row["impressions"])} impressions · position {row["position"]:.1f}</p>'
            f'\n      </div>'
        )

    block = f"""<!-- SideGuy Learning Loop Winners -->
<section class="sg-learning-loop">
  <div class="sg-learning-loop-inner">
    <p class="sg-ll-eyebrow">Learning Loop</p>
    <h2>Pages already pulling signal from reality.</h2>
    <p>Current winners based on clicks, impressions, and search visibility. Build around what is already getting traction.</p>
    <div class="sg-ll-grid">
      {''.join(cards) if cards else '<p>No GSC data yet — drop pages.csv into data/gsc/</p>'}
    </div>
  </div>
</section>
<style>
.sg-learning-loop{{padding:48px 20px}}
.sg-learning-loop-inner{{max-width:1200px;margin:0 auto}}
.sg-ll-eyebrow{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin:0 0 10px}}
.sg-ll-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:24px}}
.sg-ll-card{{background:rgba(255,255,255,.85);border:1px solid rgba(120,160,200,.25);border-radius:18px;padding:18px;box-shadow:0 10px 30px rgba(0,0,0,.05)}}
.sg-ll-kicker{{font-size:11px;text-transform:uppercase;letter-spacing:.14em;opacity:.65;margin-bottom:8px}}
.sg-ll-card h3{{margin:0 0 10px;font-size:19px;line-height:1.15}}
.sg-ll-card p{{margin:0;opacity:.8}}
.sg-ll-card a{{color:inherit;text-decoration:none}}
</style>
"""
    WINNERS_INCLUDE.write_text(block, encoding="utf-8")


def write_report(pages, queries, recs, patterns):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    top_pages   = sorted(pages,   key=lambda x: (-page_score(x),  -x["clicks"],      -x["impressions"]))[:20]
    top_queries = sorted(queries, key=lambda x: (-query_score(x), -x["impressions"]))[:30]

    lines = [
        "# SideGuy Learning Loop Report", "",
        f"Generated: {now}", "",
        f"Pages loaded: **{len(pages)}**",
        f"Queries loaded: **{len(queries)}**", "",
        "## Top Winning Pages", "",
    ]
    for row in top_pages:
        lines.append(
            f"- {row['page']} | score {page_score(row)} | clicks {int(row['clicks'])} "
            f"| impressions {int(row['impressions'])} | ctr {row['ctr']:.2f} | position {row['position']:.1f}"
        )
    lines += ["", "## Top Opportunity Queries", ""]
    for row in top_queries:
        c = classify_query(row["query"])
        lines.append(
            f"- {row['query']} | score {query_score(row)} | bucket {c['bucket']} | intent {c['intent']} "
            f"| clicks {int(row['clicks'])} | impressions {int(row['impressions'])} | position {row['position']:.1f}"
        )
    lines += ["", "## Strongest Buckets", ""]
    for bucket, weight in sorted(patterns["bucket_weight"].items(), key=lambda kv: -kv[1])[:12]:
        lines.append(f"- {bucket} | weighted opportunity {weight:.2f} | query count {patterns['bucket_counter'][bucket]}")
    lines += ["", "## Strongest Intents", ""]
    for intent, weight in sorted(patterns["intent_weight"].items(), key=lambda kv: -kv[1])[:12]:
        lines.append(f"- {intent} | weighted opportunity {weight:.2f} | query count {patterns['intent_counter'][intent]}")
    lines += [
        "", "## Build Logic", "",
        "- Double down on buckets with both impressions and multiple related queries.",
        "- Expand pages that are already getting impressions but weak clicks.",
        "- Turn strong query patterns into cluster pages, comparison pages, and local variants.",
        "- Promote live winners into visible homepage or discovery slots.", "",
    ]
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(recs):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    lines = [
        "# SideGuy Next Build Manifest", "",
        f"Generated: {now}", "",
        "## Recommended Next Pages", "",
    ]
    for r in recs:
        lines.append(
            f"- {r['query']} | bucket {r['bucket']} | intent {r['intent']} | score {r['score']} "
            f"| impressions {int(r['impressions'])} | clicks {int(r['clicks'])} | position {r['position']:.1f}"
        )
    lines += [
        "", "## Notes", "",
        "- Build adjacent long-tail pages around the highest-scoring queries.",
        "- Prefer clusters over isolated one-off pages.",
        "- Where impressions are high and clicks are low, improve title/meta and page match.",
        "- Where a bucket repeats, create stronger hubs and internal links.",
    ]
    MANIFEST_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    pages = read_pages()
    queries = read_queries()

    if not pages and not queries:
        print("No GSC CSV data found.")
        print("  → Add Google Search Console exports to:")
        print("      data/gsc/pages.csv")
        print("      data/gsc/queries.csv")
        print("  Writing empty placeholder files...")

    ranked_pages = sorted(pages, key=lambda x: (-page_score(x), -x["clicks"], -x["impressions"]))
    patterns = top_patterns(queries)
    recs = recommend_builds(queries)

    write_report(pages, queries, recs, patterns)
    write_manifest(recs)
    build_include(ranked_pages)

    print("Learning loop complete.")
    print(f"Pages loaded:       {len(pages)}")
    print(f"Queries loaded:     {len(queries)}")
    print(f"Report:             {REPORT_FILE}")
    print(f"Manifest:           {MANIFEST_FILE}")
    print(f"Winners include:    {WINNERS_INCLUDE}")


if __name__ == "__main__":
    main()
