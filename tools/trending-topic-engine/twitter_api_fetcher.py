#!/usr/bin/env python3
"""
Twitter API Fetcher — SideGuy Solutions
======================================
Fetches trending hashtags and keywords from Twitter/X for San Diego and relevant industries.
Appends new topics to docs/trending-topic-engine/expansion_queue.txt for auto-builder.

Note: For demo, uses static sample data. For production, integrate Twitter API credentials and fetch live data.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

# Sample Twitter API topics (replace with live fetch for production)
twitter_api_topics = [
    "#hvacrepair",
    "#plumbingemergency",
    "#automation",
    "#paymentprocessing",
    "#minisplit",
    "#marketingautomation",
    "#homeautomation",
    "#waterpressure",
    "#ecommercepayments"
]

new_topics = set()
for topic in twitter_api_topics:
    topic = re.sub(r'[^\w\s\-]', '', topic).strip().lower()
    if topic and len(topic.split()) > 2:
        new_topics.add(topic)

if QUEUE.exists():
    existing = set(QUEUE.read_text().splitlines())
else:
    existing = set()

with QUEUE.open("a") as f:
    for topic in sorted(new_topics):
        if topic not in existing:
            f.write(topic + "\n")
print(f"Twitter API topics added: {len(new_topics - existing)}")
