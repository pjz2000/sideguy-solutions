from pathlib import Path
import re
from datetime import datetime
from collections import defaultdict

ROOT = Path("/workspaces/sideguy-solutions")
SEARCH_DIRS = [
    ROOT,
    ROOT / "public",
    ROOT / "public" / "auto",
    ROOT / "public" / "auto" / "million",
    ROOT / "public" / "auto" / "clusters",
    ROOT / "pages",
]
OUT = ROOT / "docs" / "inventory-brain" / "reports" / "master-inventory.tsv"

TOPIC_KEYWORDS = {
    "hvac": ["hvac", "mini-split", "air-conditioning", "ac-", "furnace", "heat-pump"],
    "plumbing": ["plumbing", "sink", "drain", "water-pressure", "leak", "pipe"],
    "payments": ["payments", "payment", "merchant", "stripe", "square", "solana", "usdc", "stablecoin", "processing-fees"],
    "automation": ["automation", "workflow", "ai-agent", "ai-agents", "orchestration", "operator", "automation-tools"],
    "real-estate": ["real-estate", "realtor", "idx", "listing", "broker"],
    "software": ["software", "shopify", "crm", "api", "integration", "website", "saas"],
    "future-tech": ["machine-to-machine", "programmable-money", "compute", "gpu", "autonomous", "robot", "future-infrastructure"],
    "local-problems": ["wifi", "home-tech", "local-problem", "diagnostics", "payment-processing-problems", "small-business-tech"],
    "general": []
}

def all_html_files():
    seen = set()
    for base in SEARCH_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*.html"):
            try:
                rp = p.resolve()
            except Exception:
                rp = p
            if rp in seen:
                continue
            seen.add(rp)
            yield p

def read_file(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def detect_cluster(path_str):
    slug = path_str.lower().replace("\\", "/")
    best = "general"
    best_score = 0
    for cluster, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in slug)
        if score > best_score:
            best_score = score
            best = cluster
    return best

def title_from_html(html):
    m = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
    return m.group(1).strip() if m else ""

def count_links(html):
    return len(re.findall(r'href=["\']', html, flags=re.I))

def count_h2(html):
    return len(re.findall(r"<h2", html, flags=re.I))

def has_faq(html):
    low = html.lower()
    return int("faq" in low or "frequently asked" in low or '"@type":"faqpage"' in low.replace(" ", ""))

def has_text_pj(html):
    low = html.lower()
    return int("text pj" in low or "773-544-1231" in low)

def word_count(html):
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.findall(r"\w+", text))

def freshness_days(path):
    try:
        mtime = path.stat().st_mtime
        age = (datetime.now() - datetime.fromtimestamp(mtime)).days
        return age
    except Exception:
        return 9999

rows = []
for path in all_html_files():
    html = read_file(path)
    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    cluster = detect_cluster(rel)
    title = title_from_html(html)
    words = word_count(html)
    links = count_links(html)
    h2s = count_h2(html)
    faq = has_faq(html)
    textpj = has_text_pj(html)
    age_days = freshness_days(path)

    score = (
        (words // 150)
        + (links * 2)
        + (h2s * 3)
        + (faq * 10)
        + (textpj * 6)
    )

    rows.append({
        "path": rel,
        "cluster": cluster,
        "title": title,
        "words": words,
        "links": links,
        "h2s": h2s,
        "faq": faq,
        "textpj": textpj,
        "age_days": age_days,
        "score": score
    })

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("score\tcluster\tpath\twords\tlinks\th2s\tfaq\ttextpj\tage_days\ttitle\n")
    for r in sorted(rows, key=lambda x: (-x["score"], x["path"])):
        f.write(
            f'{r["score"]}\t{r["cluster"]}\t{r["path"]}\t{r["words"]}\t{r["links"]}\t{r["h2s"]}\t{r["faq"]}\t{r["textpj"]}\t{r["age_days"]}\t{r["title"]}\n'
        )

print(f"Wrote {OUT}")
print(f"Pages indexed: {len(rows)}")
