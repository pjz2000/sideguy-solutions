import os
import re
import json
from collections import defaultdict

ROOT = "."
OUT_TSV = "docs/upgrade-queues/agent-readiness-upgrade-queue.tsv"
OUT_JSON = "docs/audits/agent-readiness-audit.json"


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""


def visible_text_score(html):
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.S|re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S|re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())


def count_links(html):
    return len(re.findall(r'<a\s[^>]*href=', html, flags=re.I))


def has(pattern, text):
    return re.search(pattern, text, flags=re.I|re.S) is not None


def classify(path, html):
    p = path.lower()
    title = ""
    m = re.search(r"<title>(.*?)</title>", html, flags=re.I|re.S)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()

    if "payments" in p or "payment" in title.lower():
        return "payments"
    if "seo" in p or "search" in title.lower():
        return "seo"
    if "hvac" in p or "plumb" in p or "electric" in p or "roof" in p or "repair" in p:
        return "services"
    if "ai" in p or "automation" in p or "agent" in p:
        return "ai"
    if "money" in p or "bet" in p or "kalshi" in p:
        return "money"
    return "general"


def score_page(path, html):
    words = visible_text_score(html)
    links = count_links(html)

    score = 0
    reasons = []

    if has(r"<h1[^>]*>.*?</h1>", html):
        score += 8
    else:
        reasons.append("missing_h1")

    if words >= 700:
        score += 16
    elif words >= 400:
        score += 10
    elif words >= 250:
        score += 5
    else:
        reasons.append("thin_content")

    if links >= 12:
        score += 16
    elif links >= 6:
        score += 10
    elif links >= 3:
        score += 5
    else:
        reasons.append("weak_internal_links")

    if has(r"faq|frequently asked", html):
        score += 12
    else:
        reasons.append("missing_faq")

    if has(r'application/ld\+json', html):
        score += 10
    else:
        reasons.append("missing_schema")

    if has(r'last updated|updated|build version|timestamp', html):
        score += 8
    else:
        reasons.append("missing_freshness_signal")

    if has(r'text pj|773-544-1231', html):
        score += 14
    else:
        reasons.append("missing_human_cta")

    if has(r'clarity before cost|real human|human help|talk to a human|operator', html):
        score += 10
    else:
        reasons.append("weak_human_positioning")

    if has(r'san diego|coronado|north county|encinitas|carlsbad|del mar|la jolla', html):
        score += 8
    else:
        reasons.append("weak_local_signal")

    if has(r'how it works|what happens next|our process|process', html):
        score += 8
    else:
        reasons.append("missing_process_block")

    if has(r'case study|example|scenario|common situation', html):
        score += 6
    else:
        reasons.append("missing_examples")

    if has(r'back to home|home', html):
        score += 4

    return score, reasons, words, links


rows = []
for name in os.listdir(ROOT):
    if not name.endswith(".html"):
        continue
    if name.startswith("."):
        continue
    html = read_file(name)
    if not html.strip():
        continue

    score, reasons, words, links = score_page(name, html)
    bucket = classify(name, html)

    upgrade_priority = 100 - score
    if "missing_human_cta" in reasons:
        upgrade_priority += 12
    if "missing_faq" in reasons:
        upgrade_priority += 8
    if "weak_internal_links" in reasons:
        upgrade_priority += 8
    if "missing_freshness_signal" in reasons:
        upgrade_priority += 6
    if "thin_content" in reasons:
        upgrade_priority += 10

    rows.append({
        "file": name,
        "bucket": bucket,
        "score": score,
        "priority": upgrade_priority,
        "words": words,
        "links": links,
        "reasons": reasons[:]
    })

rows.sort(key=lambda x: (-x["priority"], x["score"], x["file"]))

with open(OUT_TSV, "w", encoding="utf-8") as f:
    f.write("rank\tpriority\tscore\tbucket\twords\tlinks\tfile\tupgrade_reasons\n")
    for i, row in enumerate(rows, 1):
        f.write(
            f'{i}\t{row["priority"]}\t{row["score"]}\t{row["bucket"]}\t{row["words"]}\t{row["links"]}\t{row["file"]}\t{",".join(row["reasons"])}\n'
        )

summary = defaultdict(int)
reason_counts = defaultdict(int)
for row in rows:
    summary[row["bucket"]] += 1
    for r in row["reasons"]:
        reason_counts[r] += 1

payload = {
    "page_count": len(rows),
    "bucket_counts": dict(summary),
    "top_missing_signals": dict(sorted(reason_counts.items(), key=lambda x: (-x[1], x[0]))[:20]),
    "top_25_pages": rows[:25]
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

print(f"Wrote {OUT_TSV}")
print(f"Wrote {OUT_JSON}")
print(f"Audited {len(rows)} root HTML files")
