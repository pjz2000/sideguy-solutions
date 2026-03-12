import os
import re
import glob
import json
import datetime
from collections import Counter

ROOT = "."
OUT_TSV = "docs/monetization/monetization-radar.tsv"
OUT_MD = "docs/monetization/monetization-radar.md"
OUT_JSON = "data/monetization/monetization-radar.json"

PAGES = glob.glob("*.html")

MONEY_KEYWORDS = {
    "payments": [
        "payment", "payments", "merchant", "processing", "processor",
        "stripe", "square", "pos", "transaction", "interchange",
        "chargeback", "fees", "settlement", "terminal"
    ],
    "ai_services": [
        "ai", "automation", "agent", "workflow", "chatbot", "bot",
        "crm", "lead capture", "voice ai", "answering service",
        "assistant", "integrations"
    ],
    "local_services": [
        "hvac", "plumber", "plumbing", "electrician", "solar",
        "roofing", "landscaping", "contractor", "repair", "replace",
        "install", "installation", "san diego", "near me"
    ],
    "software_affiliate": [
        "software", "saas", "platform", "tool", "tools", "best",
        "compare", "comparison", "reviews", "pricing", "hubspot",
        "quickbooks", "shopify", "gusto"
    ],
    "consulting": [
        "help", "support", "guide", "decision", "clarity",
        "cost", "quote", "diagnostic", "audit", "consult"
    ]
}

CTA_PATTERNS = [
    r"text\s*pj",
    r"call\s*pj",
    r"contact",
    r"get help",
    r"book",
    r"schedule",
    r"request a quote",
    r"free estimate",
    r"start here"
]

FAQ_PATTERNS = [
    r"faq",
    r"frequently asked questions",
    r"questions we hear",
    r"common questions"
]

AFFILIATE_HINTS = [
    "best", "compare", "comparison", "review", "reviews",
    "pricing", "software", "tool", "platform"
]

LOCAL_HINTS = [
    "san diego", "carlsbad", "encinitas", "coronado",
    "north county", "del mar", "la jolla", "oceanside"
]

SERVICE_HINTS = [
    "repair", "replace", "install", "cost", "quote",
    "emergency", "service", "contractor", "company"
]

def slug_to_title(path):
    slug = os.path.basename(path).replace(".html", "")
    return slug.replace("-", " ").strip()

def clean_text(html):
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip().lower()

def count_matches(text, patterns):
    total = 0
    for p in patterns:
        total += len(re.findall(re.escape(p), text))
    return total

def count_regex(text, patterns):
    total = 0
    for p in patterns:
        total += len(re.findall(p, text, re.I))
    return total

def detect_category(text, filename):
    scores = Counter()
    for category, keywords in MONEY_KEYWORDS.items():
        for kw in keywords:
            scores[category] += len(re.findall(re.escape(kw), text))
    fname = filename.lower()
    if "payment" in fname or "merchant" in fname:
        scores["payments"] += 4
    if "ai" in fname or "automation" in fname:
        scores["ai_services"] += 4
    if any(x in fname for x in ["hvac","plumb","electric","solar","roof","repair","install"]):
        scores["local_services"] += 4
    if any(x in fname for x in ["software","compare","best","review","pricing"]):
        scores["software_affiliate"] += 4
    if any(x in fname for x in ["help","guide","decision","cost","quote"]):
        scores["consulting"] += 3
    if not scores:
        return "general"
    return scores.most_common(1)[0][0]

def score_page(filename, text, raw_html):
    word_count = len(text.split())
    cta_count = count_regex(text, CTA_PATTERNS)
    faq_count = count_regex(text, FAQ_PATTERNS)
    affiliate_count = count_matches(text, AFFILIATE_HINTS)
    local_count = count_matches(text, LOCAL_HINTS)
    service_count = count_matches(text, SERVICE_HINTS)

    has_schema = 1 if "application/ld+json" in raw_html.lower() else 0
    has_title = 1 if re.search(r"(?is)<title>.*?</title>", raw_html) else 0
    has_meta_desc = 1 if re.search(r'meta[^>]+name=["\']description["\']', raw_html, re.I) else 0
    has_h1 = 1 if re.search(r"(?is)<h1[^>]*>.*?</h1>", raw_html) else 0
    has_text_pj = 1 if re.search(r"text\s*pj", text, re.I) else 0

    category = detect_category(text, filename)

    monetization_fit = 0
    if category == "payments":
        monetization_fit += 30
    elif category == "local_services":
        monetization_fit += 28
    elif category == "ai_services":
        monetization_fit += 26
    elif category == "software_affiliate":
        monetization_fit += 22
    elif category == "consulting":
        monetization_fit += 20
    else:
        monetization_fit += 12

    intent_score = min(20, service_count * 3 + local_count * 2 + affiliate_count * 2)
    cta_score = min(15, cta_count * 4)
    faq_score = min(10, faq_count * 5)
    structure_score = (has_title * 3) + (has_meta_desc * 3) + (has_h1 * 4) + (has_schema * 3)
    depth_score = 0
    if word_count >= 1400:
        depth_score = 15
    elif word_count >= 900:
        depth_score = 12
    elif word_count >= 600:
        depth_score = 8
    elif word_count >= 300:
        depth_score = 4

    text_pj_bonus = 8 if has_text_pj else 0

    total = monetization_fit + intent_score + cta_score + faq_score + structure_score + depth_score + text_pj_bonus

    quick_win = []
    if not has_text_pj:
        quick_win.append("add Text PJ orb/CTA")
    if faq_count == 0:
        quick_win.append("add FAQ block")
    if not has_meta_desc:
        quick_win.append("add meta description")
    if not has_h1:
        quick_win.append("add H1")
    if word_count < 700:
        quick_win.append("expand helpful content depth")
    if category == "software_affiliate":
        quick_win.append("add compare/review affiliate block")
    if category == "local_services":
        quick_win.append("add verified operator / quote routing")
    if category == "payments":
        quick_win.append("add savings calculator + payments CTA")
    if category == "ai_services":
        quick_win.append("add AI audit / install CTA")
    if category == "consulting":
        quick_win.append("add paid clarity/decision CTA")

    return {
        "page": filename,
        "title_guess": slug_to_title(filename),
        "category": category,
        "word_count": word_count,
        "cta_count": cta_count,
        "faq_count": faq_count,
        "local_count": local_count,
        "service_count": service_count,
        "affiliate_count": affiliate_count,
        "has_schema": has_schema,
        "has_title": has_title,
        "has_meta_desc": has_meta_desc,
        "has_h1": has_h1,
        "has_text_pj": has_text_pj,
        "score": total,
        "quick_wins": quick_win[:5]
    }

rows = []
for page in PAGES:
    try:
        raw = open(page, "r", encoding="utf-8", errors="ignore").read()
        text = clean_text(raw)
        rows.append(score_page(page, text, raw))
    except Exception as e:
        rows.append({
            "page": page,
            "title_guess": slug_to_title(page),
            "category": "error",
            "word_count": 0,
            "cta_count": 0,
            "faq_count": 0,
            "local_count": 0,
            "service_count": 0,
            "affiliate_count": 0,
            "has_schema": 0,
            "has_title": 0,
            "has_meta_desc": 0,
            "has_h1": 0,
            "has_text_pj": 0,
            "score": 0,
            "quick_wins": [f"read error: {str(e)}"]
        })

rows = sorted(rows, key=lambda x: (-x["score"], x["page"]))

with open(OUT_TSV, "w", encoding="utf-8") as f:
    f.write("score\tcategory\tpage\tword_count\tcta_count\tfaq_count\thas_text_pj\thas_meta_desc\thas_h1\thas_schema\tquick_wins\n")
    for r in rows:
        f.write(
            f'{r["score"]}\t{r["category"]}\t{r["page"]}\t{r["word_count"]}\t{r["cta_count"]}\t{r["faq_count"]}\t{r["has_text_pj"]}\t{r["has_meta_desc"]}\t{r["has_h1"]}\t{r["has_schema"]}\t{" | ".join(r["quick_wins"])}\n'
        )

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({
        "generated_at": datetime.datetime.utcnow().isoformat(),
        "page_count": len(rows),
        "top_pages": rows[:50]
    }, f, indent=2)

top10 = rows[:10]
cat_counts = Counter([r["category"] for r in rows])

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# SideGuy Monetization Radar\n\n")
    f.write(f"Generated: {datetime.datetime.utcnow().isoformat()} UTC\n\n")
    f.write(f"Pages scanned: **{len(rows)}**\n\n")
    f.write("## Category Counts\n\n")
    for cat, count in sorted(cat_counts.items(), key=lambda x: (-x[1], x[0])):
        f.write(f"- **{cat}**: {count}\n")
    f.write("\n## Top 10 Pages To Upgrade For Money\n\n")
    for i, r in enumerate(top10, start=1):
        f.write(f"### {i}. `{r['page']}` — score {r['score']}\n")
        f.write(f"- Category: **{r['category']}**\n")
        f.write(f"- Words: {r['word_count']}\n")
        f.write(f"- CTA count: {r['cta_count']}\n")
        f.write(f"- FAQ count: {r['faq_count']}\n")
        f.write(f"- Text PJ present: {'yes' if r['has_text_pj'] else 'no'}\n")
        f.write(f"- Quick wins: {', '.join(r['quick_wins'])}\n\n")

print("")
print("SideGuy Monetization Radar complete")
print("----------------------------------")
print("Pages scanned:", len(rows))
print("Top page:", rows[0]["page"] if rows else "none")
print("Reports:")
print(" -", OUT_TSV)
print(" -", OUT_MD)
print(" -", OUT_JSON)
print("")
