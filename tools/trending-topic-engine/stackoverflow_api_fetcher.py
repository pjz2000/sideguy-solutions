#!/usr/bin/env python3
"""
Stack Overflow API Fetcher — SideGuy Solutions
==============================================
Fetches trending questions and issues from Stack Overflow for relevant tags.
Appends new topics to docs/trending-topic-engine/expansion_queue.txt for auto-builder.

Note: For demo, uses static sample data. For production, integrate Stack Overflow API credentials and fetch live data.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

# Sample Stack Overflow API topics (replace with live fetch for production)
stackoverflow_api_topics = [
    "hvac troubleshooting",
    "plumbing automation",
    "ai tools for contractors",
    "home repair automation",
    "water pressure problems",
    "marketing automation tools",
    "mini split ac repair",
    "battery backup installation",
    "payment processing hardware",
    "ecommerce payment solutions"
]

new_topics = set()
for topic in stackoverflow_api_topics:
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
print(f"Stack Overflow API topics added: {len(new_topics - existing)}")
