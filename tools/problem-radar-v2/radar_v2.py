import os
import csv
import re
import datetime
from collections import OrderedDict, defaultdict

OUT_TSV = "docs/problem-radar/radar-signals.tsv"
OUT_MD = "docs/problem-radar/radar-summary.md"
ARCHIVE_DIR = "docs/problem-radar/archive"

SEED_PROBLEMS = [
    "payment processor fees too high",
    "chargeback prevention tools",
    "ai automation for small business",
    "hvac repair cost",
    "solar install cost",
    "website not getting leads",
    "google ads not converting",
    "seo agency too expensive",
    "merchant services pricing",
    "square vs stripe fees",
    "restaurant payment processing",
    "medical office software setup",
    "contractor leads too expensive",
    "crm setup for small business",
    "bookkeeping automation for contractors",
    "plumbing website not ranking",
    "electrical contractor seo",
    "vacation rental automation",
    "energy company payment systems",
    "compliance software explained",
    "medical device software support",
    "pos system for restaurants",
    "ai chatbot for local business",
    "stripe fees for small business",
    "how to lower payment processing fees",
]

LOCAL_CITIES = [
    "san diego", "encinitas", "carlsbad", "oceanside", "vista",
    "san marcos", "escondido", "del mar", "la jolla", "coronado", "chula vista",
]

MONEY_MODS = ["cost", "pricing", "fees", "quote", "cheaper options", "save money", "roi", "worth it"]

URGENCY_MODS = [
    "not working", "broken", "stopped working", "troubleshooting",
    "fix", "urgent help", "problem", "issue",
]

INTENT_MODS = [
    "explained", "how it works", "checklist", "setup guide",
    "for small business", "for contractors", "for restaurants",
    "for medical offices", "near me", "best options",
]

COMPARE_MODS = [
    "vs stripe", "vs square", "vs quickbooks",
    "vs manual process", "alternative", "alternatives",
]

QUESTION_TEMPLATES = [
    "what is {topic}",
    "how does {topic} work",
    "is {topic} worth it",
    "who helps with {topic}",
    "how much does {topic} cost",
    "why is {topic} so expensive",
    "how do i fix {topic}",
]

OPERATOR_TEMPLATES = [
    "{topic} for owner operators",
    "{topic} for local business",
    "{topic} for service business",
    "{topic} for high ticket service business",
]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def slugify(text: str) -> str:
    text = clean(text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def detect_bucket(topic: str) -> str:
    t = topic.lower()
    if any(x in t for x in ["payment", "processor", "merchant", "stripe", "square", "chargeback", "pos"]):
        return "payments"
    if any(x in t for x in ["ai", "automation", "chatbot", "crm", "software"]):
        return "automation"
    if any(x in t for x in ["hvac", "plumbing", "electrical", "contractor", "repair", "install"]):
        return "local-services"
    if any(x in t for x in ["seo", "google ads", "website", "leads", "ranking"]):
        return "marketing"
    if any(x in t for x in ["medical", "compliance", "device"]):
        return "compliance-medical"
    if any(x in t for x in ["energy", "solar"]):
        return "energy"
    return "general"


def detect_signal_type(topic: str) -> str:
    t = topic.lower()
    if " vs " in t or "alternative" in t:
        return "comparison"
    if any(x in t for x in ["cost", "pricing", "fees", "quote", "worth it", "save money", "roi"]):
        return "money"
    if any(x in t for x in ["broken", "not working", "stopped working", "fix", "troubleshooting", "urgent", "issue", "problem"]):
        return "urgency"
    if any(city in t for city in LOCAL_CITIES) or "near me" in t:
        return "local"
    if any(t.startswith(p) for p in ["what is ", "how ", "why ", "who "]):
        return "question"
    return "intent"


def score_topic(topic: str) -> int:
    t = topic.lower()
    score = 0
    high_value = [
        "payment", "payments", "processor", "merchant", "fees", "chargeback",
        "software", "ai", "automation", "crm", "seo", "google ads", "leads",
        "hvac", "plumbing", "electrical", "solar", "energy", "medical",
        "compliance", "device", "pos",
    ]
    for w in high_value:
        if w in t: score += 5
    for w in ["cost", "pricing", "fees", "quote", "save money", "roi", "worth it"]:
        if w in t: score += 4
    for w in ["broken", "not working", "stopped working", "troubleshooting", "fix", "urgent", "issue", "problem"]:
        if w in t: score += 4
    for w in LOCAL_CITIES + ["near me"]:
        if w in t: score += 6
    for w in [" vs ", "alternative", "alternatives"]:
        if w in t: score += 3
    score += min(len(t.split()), 10)
    return score


def expand_seed(seed: str):
    seed = clean(seed)
    out = [seed]
    for mod in MONEY_MODS:      out.append(f"{seed} {mod}")
    for mod in URGENCY_MODS:    out.append(f"{seed} {mod}")
    for mod in INTENT_MODS:     out.append(f"{seed} {mod}")
    for mod in COMPARE_MODS:    out.append(f"{seed} {mod}")
    for q in QUESTION_TEMPLATES:  out.append(q.format(topic=seed))
    for q in OPERATOR_TEMPLATES:  out.append(q.format(topic=seed))
    for city in LOCAL_CITIES:
        out.append(f"{seed} {city}")
        out.append(f"{seed} cost {city}")
        out.append(f"{seed} for small business {city}")
        out.append(f"{seed} near me {city}")
    # variant swaps
    for old, new in [("cost","pricing"),("pricing","cost"),("fees","pricing"),("fees","cost")]:
        if old in seed:
            out.append(seed.replace(old, new))
    if "too high" in seed:
        out.append(seed.replace("too high", "explained"))
        out.append(seed.replace("too high", "how to lower"))

    seen, deduped = set(), []
    for item in out:
        item = clean(item)
        s = slugify(item)
        if item and s and s not in seen:
            seen.add(s)
            deduped.append(item)
    return deduped


def main():
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    today = datetime.date.today().isoformat()

    rows = []
    seen = set()
    for seed in SEED_PROBLEMS:
        for topic in expand_seed(seed):
            slug = slugify(topic)
            if slug in seen:
                continue
            seen.add(slug)
            rows.append({
                "source": "radar-v2",
                "topic": topic,
                "slug": slug,
                "bucket": detect_bucket(topic),
                "signal_type": detect_signal_type(topic),
                "score": score_topic(topic),
                "seed": seed,
                "generated_at": generated_at,
            })

    rows.sort(key=lambda r: (-r["score"], r["bucket"], r["topic"]))

    fieldnames = ["source", "topic", "slug", "bucket", "signal_type", "score", "seed", "generated_at"]
    for path in [OUT_TSV, os.path.join(ARCHIVE_DIR, f"radar-signals-{today}.tsv")]:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)

    bucket_counts = defaultdict(int)
    type_counts = defaultdict(int)
    for row in rows:
        bucket_counts[row["bucket"]] += 1
        type_counts[row["signal_type"]] += 1

    top_by_bucket = OrderedDict()
    for bucket in sorted(bucket_counts.keys()):
        top_by_bucket[bucket] = [r for r in rows if r["bucket"] == bucket][:12]

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# SideGuy Radar Summary\n\n")
        f.write(f"Generated: {generated_at}\n\n")
        f.write(f"Total signals: **{len(rows)}**\n\n")

        f.write("## Bucket Counts\n\n")
        for bucket, count in sorted(bucket_counts.items(), key=lambda kv: -kv[1]):
            f.write(f"- **{bucket}**: {count}\n")

        f.write("\n## Signal Type Counts\n\n")
        for sig_type, count in sorted(type_counts.items(), key=lambda kv: -kv[1]):
            f.write(f"- **{sig_type}**: {count}\n")

        f.write("\n## Top 40 Signals Overall\n\n")
        for row in rows[:40]:
            f.write(f"- {row['topic']} | score {row['score']} | {row['bucket']} | {row['signal_type']}\n")

        f.write("\n")
        for bucket, items in top_by_bucket.items():
            f.write(f"## {bucket.title()}\n\n")
            for row in items:
                f.write(f"- {row['topic']} | score {row['score']} | {row['signal_type']}\n")
            f.write("\n")

    archive_path = os.path.join(ARCHIVE_DIR, f"radar-signals-{today}.tsv")
    print("Radar v2 complete.")
    print(f"Signals generated: {len(rows)}")
    print(f"Main TSV:          {OUT_TSV}")
    print(f"Archive TSV:       {archive_path}")
    print(f"Summary MD:        {OUT_MD}")


if __name__ == "__main__":
    main()
