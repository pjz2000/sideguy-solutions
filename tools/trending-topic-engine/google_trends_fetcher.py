#!/usr/bin/env python3
"""
Google News RSS Fetcher — SideGuy Solutions
============================================
Fetches live headlines from Google News RSS (no API key needed).
Filters for San Diego + service industry relevance.
Appends new topics to docs/trending-topic-engine/expansion_queue.txt.
"""
from pathlib import Path
import re
import feedparser

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

# Google News RSS feeds — no API key, completely free
FEEDS = [
    # San Diego local news
    "https://news.google.com/rss/search?q=san+diego+repair&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=san+diego+home+service&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=san+diego+small+business&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=san+diego+HVAC+plumbing+electrical&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=AI+automation+small+business&hl=en-US&gl=US&ceid=US:en",
    "https://news.google.com/rss/search?q=payment+processing+small+business&hl=en-US&gl=US&ceid=US:en",
]

# Keywords that signal relevance to SideGuy topics
KEYWORDS = [
    "repair", "hvac", "plumbing", "electrical", "roofing", "solar",
    "payment", "automation", "ai", "contractor", "business", "service",
    "san diego", "installation", "leak", "water", "internet", "wifi",
    "software", "accounting", "insurance", "legal", "tax",
]

def clean_topic(text):
    text = re.sub(r'\s*[-|].*$', '', text)  # remove source suffix like " - NBC San Diego"
    text = re.sub(r'[^\w\s\-]', '', text).strip().lower()
    return text

new_topics = set()
for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:15]:
            title = entry.get('title', '')
            topic = clean_topic(title)
            if len(topic.split()) < 3:
                continue
            if any(kw in topic for kw in KEYWORDS):
                new_topics.add(topic)
    except Exception as e:
        print(f"Feed error ({feed_url[:60]}...): {e}")

if QUEUE.exists():
    existing = set(QUEUE.read_text().splitlines())
else:
    existing = set()
    QUEUE.parent.mkdir(parents=True, exist_ok=True)

added = new_topics - existing
with QUEUE.open("a") as f:
    for topic in sorted(added):
        f.write(topic + "\n")
print(f"Google News RSS topics added: {len(added)} (from {len(new_topics)} fetched)")
