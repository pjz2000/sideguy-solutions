#!/usr/bin/env python3
"""
Reddit RSS Scraper — SideGuy Solutions
=======================================
Fetches hot posts from relevant subreddits via their public RSS feeds.
No API key or OAuth needed — Reddit's .rss endpoint is public.
Appends new topics to docs/trending-topic-engine/expansion_queue.txt.
"""
from pathlib import Path
import re
import feedparser

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

# Public Reddit RSS feeds — no API key needed
SUBREDDITS = [
    "sandiego",
    "smallbusiness",
    "hvac",
    "plumbing",
    "electricians",
    "automation",
    "entrepreneur",
    "homeowners",
    "paymentprocessing",
    "AItools",
]

# Skip posts that are too generic or off-topic
SKIP_WORDS = ["meme", "rant", "oc:", "[oc]", "tell me", "unpopular opinion"]

def clean_topic(text):
    text = re.sub(r'\[.*?\]', '', text)  # remove [tags]
    text = re.sub(r'[^\w\s\-]', '', text).strip().lower()
    return text

new_topics = set()
for sub in SUBREDDITS:
    url = f"https://www.reddit.com/r/{sub}/hot.rss?limit=15"
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:15]:
            title = entry.get('title', '')
            topic = clean_topic(title)
            if len(topic.split()) < 3:
                continue
            if any(skip in topic for skip in SKIP_WORDS):
                continue
            new_topics.add(topic)
    except Exception as e:
        print(f"Reddit feed error (r/{sub}): {e}")

if QUEUE.exists():
    existing = set(QUEUE.read_text().splitlines())
else:
    existing = set()
    QUEUE.parent.mkdir(parents=True, exist_ok=True)

added = new_topics - existing
with QUEUE.open("a") as f:
    for topic in sorted(added):
        f.write(topic + "\n")
print(f"Reddit RSS topics added: {len(added)} (from {len(new_topics)} fetched)")
