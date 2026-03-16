#!/usr/bin/env python3

import os
import re
import csv
import json
from collections import defaultdict

ROOT = "/workspaces/sideguy-solutions"
REPORT_DIR = os.path.join(ROOT, "docs/cluster-gravity/reports")

HTML_DIRS = [
    ROOT,
    os.path.join(ROOT, "public"),
    os.path.join(ROOT, "public", "auto"),
]

CLUSTER_RULES = {
    "hvac": ["hvac", "mini-split", "air-conditioning", "ac-", "heating", "furnace"],
    "plumbing": ["plumb", "sink", "drain", "water-pressure", "pipe", "toilet"],
    "electrical": ["electrical", "electric", "panel", "breaker", "wiring"],
    "payments": ["payment", "payments", "merchant", "stripe", "square", "usdc", "solana", "processing-fees"],
    "ai-automation": ["ai", "automation", "agent", "workflow", "orchestration", "operator"],
    "software": ["software", "shopify", "api", "integration", "crm", "saas"],
    "future-infra": ["machine-to-machine", "stablecoin", "future", "autonomous", "compute", "robot", "infrastructure"],
    "local-services": ["san-diego", "near-me", "emergency", "repair", "replacement", "contractor"],
}

def iter_html_files():
    seen = set()
    for base in HTML_DIRS:
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".next", "archive", "backups"}]
            for f in files:
                if not f.endswith(".html"):
                    continue
                path = os.path.join(root, f)
                if path in seen:
                    continue
                seen.add(path)
                yield path

def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return ""

def count_internal_links(text):
    return len(re.findall(r'href="/', text))

def count_words(text):
    return len(re.findall(r"\b[\w'-]+\b", text))

def detect_cluster(path):
    slug = os.path.basename(path).lower()
    best = "general"
    best_score = 0

    for cluster, keywords in CLUSTER_RULES.items():
        score = 0
        for kw in keywords:
            if kw in slug:
                score += 1
        if score > best_score:
            best_score = score
            best = cluster

    return best

def main():
    os.makedirs(REPORT_DIR, exist_ok=True)

    page_rows = []
    cluster_pages = defaultdict(list)
    cluster_totals = defaultdict(lambda: {"pages": 0, "words": 0, "links": 0, "score": 0})

    for path in iter_html_files():
        text = read_text(path)
        if not text.strip():
            continue

        cluster = detect_cluster(path)
        words = count_words(text)
        links = count_internal_links(text)
        score = words + (links * 250)

        row = {
            "page": os.path.relpath(path, ROOT),
            "cluster": cluster,
            "words": words,
            "links": links,
            "score": score,
        }

        page_rows.append(row)
        cluster_pages[cluster].append(row)

        cluster_totals[cluster]["pages"] += 1
        cluster_totals[cluster]["words"] += words
        cluster_totals[cluster]["links"] += links
        cluster_totals[cluster]["score"] += score

    page_rows.sort(key=lambda x: (-x["score"], x["page"]))

    cluster_summary = []
    for cluster, totals in cluster_totals.items():
        avg_score = round(totals["score"] / max(totals["pages"], 1), 2)
        cluster_summary.append({
            "cluster": cluster,
            "pages": totals["pages"],
            "words": totals["words"],
            "links": totals["links"],
            "total_score": totals["score"],
            "avg_score": avg_score,
        })

    cluster_summary.sort(key=lambda x: (-x["total_score"], -x["pages"], x["cluster"]))

    summary_csv = os.path.join(REPORT_DIR, "cluster-summary.csv")
    with open(summary_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cluster", "pages", "words", "links", "total_score", "avg_score"])
        writer.writeheader()
        writer.writerows(cluster_summary)

    pages_csv = os.path.join(REPORT_DIR, "cluster-pages.csv")
    with open(pages_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["page", "cluster", "words", "links", "score"])
        writer.writeheader()
        writer.writerows(page_rows)

    top_md = os.path.join(REPORT_DIR, "cluster-gravity-report.md")
    with open(top_md, "w", encoding="utf-8") as f:
        f.write("# SideGuy Cluster Gravity Report\n\n")
        f.write("This report shows where authority is forming across the site.\n\n")

        f.write("## Top Clusters\n\n")
        for i, row in enumerate(cluster_summary[:12], 1):
            f.write(f"### {i}. {row['cluster']}\n")
            f.write(f"- Pages: **{row['pages']}**\n")
            f.write(f"- Words: **{row['words']}**\n")
            f.write(f"- Internal Links: **{row['links']}**\n")
            f.write(f"- Total Gravity Score: **{row['total_score']}**\n")
            f.write(f"- Average Page Score: **{row['avg_score']}**\n\n")

            top_pages = sorted(cluster_pages[row["cluster"]], key=lambda x: (-x["score"], x["page"]))[:5]
            f.write("Top pages in cluster:\n")
            for p in top_pages:
                f.write(f"- `{p['page']}` — score {p['score']}, links {p['links']}, words {p['words']}\n")
            f.write("\n")

        f.write("## Upgrade Logic\n\n")
        f.write("- strengthen clusters with many pages but weak average scores\n")
        f.write("- add internal links into strong pages that already show authority\n")
        f.write("- improve thin pages inside promising clusters\n")
        f.write("- use clusters with strong gravity as hubs for new publishing\n")

    upgrades_md = os.path.join(REPORT_DIR, "upgrade-targets.md")
    with open(upgrades_md, "w", encoding="utf-8") as f:
        f.write("# SideGuy Upgrade Targets\n\n")
        f.write("Pages with good cluster fit but weaker gravity are strong upgrade candidates.\n\n")

        candidates = []
        for row in page_rows:
            if row["words"] < 900 or row["links"] < 8:
                candidates.append(row)

        candidates.sort(key=lambda x: (x["cluster"], -x["score"]))
        for row in candidates[:150]:
            f.write(f"- `{row['page']}` | cluster: **{row['cluster']}** | words: {row['words']} | links: {row['links']} | score: {row['score']}\n")

    state_json = os.path.join(REPORT_DIR, "cluster-gravity-state.json")
    with open(state_json, "w", encoding="utf-8") as f:
        json.dump({
            "clusters": cluster_summary,
            "top_pages": page_rows[:300],
        }, f, indent=2)

    print("Cluster Gravity Engine complete.")
    print("Wrote:", summary_csv)
    print("Wrote:", pages_csv)
    print("Wrote:", top_md)
    print("Wrote:", upgrades_md)
    print("Wrote:", state_json)

if __name__ == "__main__":
    main()
