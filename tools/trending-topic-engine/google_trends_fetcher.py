#!/usr/bin/env python3
"""
Google Trends Fetcher — SideGuy Solutions
=========================================
Fetches trending topics from Google Trends for San Diego and relevant industries.
Appends new topics to docs/trending-topic-engine/expansion_queue.txt for auto-builder.

Note: For demo, uses static sample data. For production, integrate pytrends or Google Trends API.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

# Sample trending Google Trends topics (replace with API fetch for production)
google_trends = [
    "hvac repair san diego",
    "plumbing emergency san diego",
    "ai automation for contractors",
    "payment processing solutions",
    "mini split ac repair",
    "battery backup installation",
    "marketing automation san diego",
    "home repair automation",
    "water pressure issues san diego",
    "ecommerce payment solutions"
]

new_topics = set()
for topic in google_trends:
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
print(f"Google Trends topics added: {len(new_topics - existing)}")
