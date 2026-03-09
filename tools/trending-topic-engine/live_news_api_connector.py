#!/usr/bin/env python3
"""
Live News API Connector — SideGuy Solutions
==========================================
Fetches live headlines from NewsAPI (or similar) and queues topics for auto-builder.
Note: Replace 'YOUR_API_KEY' with a real key for production.
"""
from pathlib import Path
import requests, re

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"
API_KEY = 'YOUR_API_KEY'
NEWS_URL = f'https://newsapi.org/v2/top-headlines?country=us&q=san+diego&apiKey={API_KEY}'

try:
    resp = requests.get(NEWS_URL)
    articles = resp.json().get('articles', [])
except Exception:
    articles = []

new_topics = set()
for article in articles:
    title = article.get('title', '')
    topic = re.sub(r'[^\w\s\-]', '', title).strip().lower()
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
print(f"Live news topics added: {len(new_topics - existing)}")
