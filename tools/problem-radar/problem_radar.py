#!/usr/bin/env python3
"""
SideGuy Problem Radar — Seed Collector
----------------------------------------
Appends new seed problems to docs/problem-radar/radar-signals.tsv.
Skips seeds already present (deduplicates on topic text).

Output: docs/problem-radar/radar-signals.tsv
"""

import datetime, os
from pathlib import Path

ROOT   = Path(__file__).parent.parent.parent.resolve()
OUTPUT = ROOT / "docs" / "problem-radar" / "radar-signals.tsv"
NOW    = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")

SEED_PROBLEMS = [
    # payments
    "payment processor fees too high",
    "chargeback prevention tools",
    "reduce stripe fees",
    "restaurant payment processing rates",
    "how to reduce credit card processing fees",
    "reduce payment processing chargebacks",
    # ai-automation
    "ai automation for small business",
    "small business ai customer support",
    "ai scheduling software for contractors",
    "how to automate small business tasks",
    "best ai tools for local business",
    "ai chatbots for customer service",
    "ai automation consulting cost",
    "small business workflow automation",
    # energy-ev
    "ev charger install cost",
    "electric vehicle charger installation permit",
    # crypto
    "how to accept crypto payments",
    "solana payments for merchants",
    # home-systems
    "hvac service pricing confusion",
    # local-seo
    "local seo for contractors",
    # new seeds
    "ai receptionist for local businesses",
    "how to accept stablecoin payments",
    "restaurant ai ordering systems",
    "ai appointment scheduling",
    "prediction markets explained",
    "kalshi trading strategy",
    "hvac ai call answering",
    "solar battery backup cost",
    "heat pump vs furnace cost",
    "ai agent for customer service",
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Load existing topics to avoid duplicates
existing_topics: set[str] = set()
header_written = False
if OUTPUT.exists():
    lines = OUTPUT.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if i == 0 and line.startswith("source\t"):
            header_written = True
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            existing_topics.add(parts[2].strip().lower())

# Append new seeds
added = 0
with open(OUTPUT, "a", encoding="utf-8") as f:
    if not header_written:
        f.write("source\tpillar\ttopic\ttimestamp\n")
    for topic in SEED_PROBLEMS:
        if topic.lower() not in existing_topics:
            f.write(f"seed\t\t{topic}\t{NOW}\n")
            existing_topics.add(topic.lower())
            added += 1

total = sum(1 for l in OUTPUT.read_text().splitlines() if not l.startswith("source\t") and l.strip())
print(f"Problem Radar: added {added} new seeds ({total} total in {OUTPUT.relative_to(ROOT)})")
