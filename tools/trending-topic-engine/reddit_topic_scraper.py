#!/usr/bin/env python3
"""
Reddit Topic Scraper — SideGuy Solutions
=======================================
Fetches trending topics from Reddit (e.g., r/sandiego, r/smallbusiness, r/hvac, r/plumbing, r/automation).
Appends new topics to docs/trending-topic-engine/expansion_queue.txt for auto-builder.

Note: For demo, uses static sample data. For production, integrate Reddit API or Pushshift.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

# Sample trending Reddit posts (replace with API fetch for production)
reddit_posts = [
    "Best HVAC troubleshooting tips for San Diego",
    "How to automate payment processing for small businesses",
    "San Diego plumbing emergency advice",
    "AI tools for contractors",
    "Home repair automation recommendations",
    "Water pressure issues in San Diego homes",
    "Marketing automation for local businesses",
    "Mini split AC repair experiences",
    "Battery backup installation questions",
    "Ecommerce payment solutions discussion"
]

new_topics = set()
for post in reddit_posts:
    topic = re.sub(r'[^\w\s\-]', '', post).strip().lower()
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
print(f"Reddit topics added: {len(new_topics - existing)}")
