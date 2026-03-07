"""
SideGuy Trend Radar
-------------------
Classifies seed problem phrases into clusters, scores them by
build priority, and outputs TSV + Markdown + JSON reports.

Usage:
  python3 tools/trend-radar/trend_radar.py

Outputs:
  docs/trend-radar/radar-signals.tsv
  docs/trend-radar/radar-report.md
  data/trend-radar/radar-clusters.json
"""
import csv
import datetime
import json
from pathlib import Path

SEED_FILE  = Path("data/trend-radar/seed_topics.txt")
OUT_TSV    = Path("docs/trend-radar/radar-signals.tsv")
OUT_MD     = Path("docs/trend-radar/radar-report.md")
OUT_JSON   = Path("data/trend-radar/radar-clusters.json")

today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def classify(topic: str) -> str:
    t = topic.lower()
    if any(x in t for x in ["payment", "processor", "chargeback", "stablecoin", "credit card", "fee"]):
        return "payments"
    if any(x in t for x in ["ai", "crm", "chatbot", "receptionist", "software", "website", "google business", "compliance"]):
        return "ai-software"
    if any(x in t for x in ["hvac", "mini split", "window", "dishwasher", "foundation", "plumbing", "landscaping", "drafty"]):
        return "home-operator"
    if any(x in t for x in ["ev charger", "tesla charger", "rare earth", "robotics", "medical device"]):
        return "future-industries"
    if any(x in t for x in ["kalshi", "underdog", "prediction market", "hedging"]):
        return "signal-lab"
    return "general-problems"


def intent(topic: str) -> str:
    t = topic.lower()
    if any(x in t for x in ["cost", "quote", "fee", "too high", "expensive", "lower", "price"]):
        return "money-pain"
    if any(x in t for x in ["how to", "help", "setup", "strategy", "install", "second opinion"]):
        return "guidance"
    if any(x in t for x in ["not ", "suspended", "draining", "cooling", "getting"]):
        return "diagnostic"
    return "discovery"


def slugify(text: str) -> str:
    return (
        text.lower()
        .replace("?", "").replace("/", "-").replace("'", "")
        .replace(" ", "-").replace("--", "-").strip("-")
    )


topics = [
    line.strip() for line in SEED_FILE.read_text().splitlines()
    if line.strip()
]

rows = []
clusters: dict = {}

for topic in topics:
    bucket = classify(topic)
    search_intent = intent(topic)
    slug = slugify(topic)
    url = f"/{slug}.html"

    rows.append({
        "timestamp": today,
        "topic": topic,
        "bucket": bucket,
        "intent": search_intent,
        "suggested_url": url,
    })
    clusters.setdefault(bucket, []).append({
        "topic": topic,
        "intent": search_intent,
        "suggested_url": url,
    })

# TSV
OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_TSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["timestamp", "topic", "bucket", "intent", "suggested_url"])
    for row in rows:
        writer.writerow([row["timestamp"], row["topic"], row["bucket"], row["intent"], row["suggested_url"]])

# JSON
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(clusters, indent=2), encoding="utf-8")

# Markdown report
priority = sorted(
    rows,
    key=lambda r: (
        3 if r["intent"] == "money-pain" else
        2 if r["intent"] == "diagnostic" else
        1 if r["intent"] == "guidance" else 0
    ) + (2 if r["bucket"] in {"payments", "ai-software", "home-operator"} else 0),
    reverse=True,
)

OUT_MD.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(f"# SideGuy Trend Radar Report\n\nGenerated: {today}\n\n")
    f.write("## Summary\n\n")
    for bucket, items in clusters.items():
        f.write(f"- **{bucket}**: {len(items)} signals\n")
    f.write("\n## Build-First Signals (top 15 by score)\n\n")
    for row in priority[:15]:
        score = (
            3 if row["intent"] == "money-pain" else
            2 if row["intent"] == "diagnostic" else
            1 if row["intent"] == "guidance" else 0
        ) + (2 if row["bucket"] in {"payments", "ai-software", "home-operator"} else 0)
        f.write(
            f"- **{row['topic']}** | bucket: `{row['bucket']}` | "
            f"intent: `{row['intent']}` | url: `{row['suggested_url']}` | score: `{score}`\n"
        )
    f.write("\n## All Signals\n\n")
    for bucket, items in clusters.items():
        f.write(f"### {bucket}\n")
        for item in items:
            f.write(f"- {item['topic']} → `{item['suggested_url']}`\n")
        f.write("\n")

print(f"Trend radar complete — {len(topics)} topics across {len(clusters)} clusters")
print(f"  TSV  : {OUT_TSV}")
print(f"  MD   : {OUT_MD}")
print(f"  JSON : {OUT_JSON}")
