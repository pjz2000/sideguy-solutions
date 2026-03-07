import os
import re
import json
import math
import datetime
from collections import Counter

INPUT_FILE = "docs/problem-page-ideas.txt"
OUT_JSON = "docs/problem-heatmap/problem-heatmap.json"
OUT_MD = "docs/problem-heatmap/problem-heatmap.md"
OUT_QUEUE = "docs/problem-heatmap/top-20-build-queue.txt"
OUT_CLAUDE = "docs/claude/problem-heatmap-execution-brief.md"

NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

MONEY_WORDS = {
    "payment","payments","processor","processing","merchant","chargeback","fee","fees","cost","costs",
    "roi","revenue","sales","settlement","invoice","invoicing","bookkeeping","automation","lead","leads",
    "ads","ppc","seo","rankings","ranking","software","crm","saas","compliance","payroll","fraud","billing"
}

URGENT_WORDS = {
    "broken","error","down","not working","fix","repair","stuck","urgent","issue","issues","problem","problems",
    "failing","declined","chargeback","refund","cancelled","late","slow","outage","scam","warning","emergency"
}

LOCAL_WORDS = {
    "san diego","carlsbad","encinitas","oceanside","del mar","la jolla","north county","southern california",
    "coronado","vista","escondido","poway","solana beach","rancho bernardo","california"
}

FUTURE_WORDS = {
    "ai","agent","agents","automation","robot","robotics","crypto","solana","stablecoin","llm","prediction market",
    "kalshi","polymarket","api","voice ai","autonomous","future","emerging","software","compliance software"
}

MEME_WORDS = {
    "meme","funny","weird","crazy","insane","vs","twitter","x ","reddit","tiktok","doom","collapse","hype",
    "viral","joke","panic","trend","drama"
}

BUYER_WORDS = {
    "best","cost","pricing","price","near me","company","service","help","consultant","agency","setup","install",
    "for small business","for business","for restaurants","for contractors","for homeowners","san diego"
}

def clean_line(line):
    line = line.strip()
    line = re.sub(r'^\s*[-*•]+\s*', '', line)
    line = re.sub(r'^\s*\d+[\.\)]\s*', '', line)
    return line.strip()

def load_topics(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = [clean_line(x) for x in f.readlines()]
    raw = [x for x in raw if x]
    deduped = []
    seen = set()
    for item in raw:
        k = item.lower()
        if k not in seen:
            deduped.append(item)
            seen.add(k)
    return deduped

def contains_any(text, words):
    t = text.lower()
    count = 0
    for w in words:
        if w in t:
            count += 1
    return count

def phrase_bonus(text):
    t = text.lower()
    bonus = 0
    if len(t.split()) >= 5:
        bonus += 1
    if "how to" in t:
        bonus += 1
    if "for " in t:
        bonus += 1
    if " near me" in t or t.endswith(" near me"):
        bonus += 2
    if "san diego" in t:
        bonus += 2
    if "vs" in t:
        bonus += 1
    return bonus

def bucket(score):
    if score >= 18:
        return "SHIP NOW"
    if score >= 13:
        return "HIGH PRIORITY"
    if score >= 9:
        return "GOOD BACKLOG"
    return "LOWER PRIORITY"

def classify(text):
    t = text.lower()

    money = contains_any(t, MONEY_WORDS)
    urgency = contains_any(t, URGENT_WORDS)
    local_fit = contains_any(t, LOCAL_WORDS)
    future_fit = contains_any(t, FUTURE_WORDS)
    meme = contains_any(t, MEME_WORDS)
    buyer = contains_any(t, BUYER_WORDS)
    bonus = phrase_bonus(t)

    score = (
        money * 3 +
        urgency * 3 +
        local_fit * 2 +
        future_fit * 2 +
        meme * 1 +
        buyer * 2 +
        bonus
    )

    tags = []
    if money: tags.append("money")
    if urgency: tags.append("urgent")
    if local_fit: tags.append("local")
    if future_fit: tags.append("future")
    if meme: tags.append("meme")
    if buyer: tags.append("buyer-intent")

    route = "general"
    if local_fit and money:
        route = "local-money"
    elif money and future_fit:
        route = "future-money"
    elif urgency and local_fit:
        route = "local-urgent"
    elif urgency:
        route = "urgent"
    elif meme and future_fit:
        route = "meme-future"
    elif meme:
        route = "meme"
    elif future_fit:
        route = "future"

    return {
        "topic": text,
        "score": score,
        "bucket": bucket(score),
        "route": route,
        "signals": {
            "money": money,
            "urgency": urgency,
            "local_fit": local_fit,
            "future_fit": future_fit,
            "memeability": meme,
            "buyer_intent": buyer,
            "phrase_bonus": bonus
        },
        "tags": tags
    }

def suggest_slug(topic):
    s = topic.lower().strip()
    s = s.replace("&", " and ")
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:90]

def suggest_hub(item):
    tags = set(item["tags"])
    topic = item["topic"].lower()

    if "payment" in topic or "merchant" in topic or "processor" in topic or "settlement" in topic:
        return "payments"
    if "ai" in topic or "automation" in topic or "agent" in topic or "llm" in topic:
        return "ai"
    if "seo" in topic or "ads" in topic or "ppc" in topic or "lead" in topic:
        return "growth"
    if "crypto" in topic or "solana" in topic or "stablecoin" in topic:
        return "crypto"
    if "compliance" in topic or "software" in topic:
        return "software"
    if "san diego" in topic or "north county" in topic or "encinitas" in topic:
        return "san-diego"
    if "meme" in tags:
        return "meme-zone"
    if "future" in tags:
        return "future"
    return "operator-index"

topics = load_topics(INPUT_FILE)

results = []
for t in topics:
    item = classify(t)
    item["slug"] = suggest_slug(t)
    item["hub"] = suggest_hub(item)
    results.append(item)

results.sort(key=lambda x: (-x["score"], x["topic"].lower()))

summary = {
    "generated_at": NOW,
    "input_file": INPUT_FILE,
    "topic_count": len(results),
    "bucket_counts": dict(Counter([r["bucket"] for r in results])),
    "route_counts": dict(Counter([r["route"] for r in results])),
    "top_tags": dict(Counter(tag for r in results for tag in r["tags"]).most_common(12))
}

payload = {
    "summary": summary,
    "results": results
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

top20 = results[:20]

with open(OUT_QUEUE, "w", encoding="utf-8") as f:
    for i, r in enumerate(top20, 1):
        f.write(f"{i}. {r['topic']} | score={r['score']} | bucket={r['bucket']} | hub={r['hub']} | slug={r['slug']}\n")

md = []
md.append("# SideGuy Problem Heatmap")
md.append("")
md.append(f"- Generated: {NOW}")
md.append(f"- Source: `{INPUT_FILE}`")
md.append(f"- Topics scanned: **{len(results)}**")
md.append("")
md.append("## Summary")
md.append("")
for k, v in summary["bucket_counts"].items():
    md.append(f"- {k}: **{v}**")
md.append("")
md.append("## Top Routes")
md.append("")
for k, v in summary["route_counts"].items():
    md.append(f"- {k}: **{v}**")
md.append("")
md.append("## Top 20 Build Queue")
md.append("")
for i, r in enumerate(top20, 1):
    sig = r["signals"]
    md.append(f"### {i}. {r['topic']}")
    md.append(f"- Score: **{r['score']}**")
    md.append(f"- Bucket: **{r['bucket']}**")
    md.append(f"- Route: `{r['route']}`")
    md.append(f"- Hub: `{r['hub']}`")
    md.append(f"- Slug: `{r['slug']}`")
    md.append(f"- Signals: money={sig['money']} urgency={sig['urgency']} local={sig['local_fit']} future={sig['future_fit']} meme={sig['memeability']} buyer={sig['buyer_intent']} bonus={sig['phrase_bonus']}")
    md.append("")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

claude = []
claude.append("# Claude Execution Brief — Problem Heatmap")
claude.append("")
claude.append(f"Generated: {NOW}")
claude.append("")
claude.append("Use `docs/problem-heatmap/top-20-build-queue.txt` as the source queue.")
claude.append("")
claude.append("## Objective")
claude.append("")
claude.append("Build the first 20 highest-priority pages from the heatmap using the existing SideGuy page template.")
claude.append("")
claude.append("## Rules")
claude.append("")
claude.append("- append-only")
claude.append("- use existing SideGuy template")
claude.append("- create one page at a time")
claude.append("- add each page to sitemap after creation")
claude.append("- add each page to index.html after creation")
claude.append("- cross-link to the most relevant hub")
claude.append("- commit after each page")
claude.append("- no rewrites of existing pages unless exact slug conflict forces alternate slug")
claude.append("")
claude.append("## Output expectations")
claude.append("")
claude.append("- Each page should have a strong title, H1, intro, problem framing, SideGuy-style clarity copy, and a calm CTA")
claude.append("- Include Text PJ orb/footer pattern where applicable")
claude.append("- Use internal cross-links to hub pages and related pages")
claude.append("- Keep metadata clean and local-intent aware when relevant")
claude.append("")
claude.append("## Top 20 queue")
claude.append("")
for i, r in enumerate(top20, 1):
    claude.append(f"{i}. {r['topic']} | hub={r['hub']} | slug={r['slug']} | score={r['score']}")
claude.append("")

with open(OUT_CLAUDE, "w", encoding="utf-8") as f:
    f.write("\n".join(claude) + "\n")

print("Generated:")
print(f"- {OUT_JSON}")
print(f"- {OUT_MD}")
print(f"- {OUT_QUEUE}")
print(f"- {OUT_CLAUDE}")
print("")
print("Top 10:")
for i, r in enumerate(top20[:10], 1):
    print(f"{i}. {r['topic']} | score={r['score']} | hub={r['hub']} | slug={r['slug']}")
