#!/usr/bin/env python3
"""
Topic Cluster Builder — SideGuy Solutions
========================================
Scans all public HTML pages, extracts main topics/intents using simple NLP,
groups pages into clusters, and writes cluster maps to docs/topic-clusters/clusters.json.

Run after page/context steps for maximum coverage.
"""
from pathlib import Path
import re, json

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
OUT = ROOT / "docs" / "topic-clusters" / "clusters.json"

# Simple topic extraction: from H1, title, meta description
TOPIC_PATTERNS = [
    re.compile(r'<h1[^>]*>(.*?)</h1>', re.I),
    re.compile(r'<title[^>]*>(.*?)</title>', re.I),
    re.compile(r'<meta name="description"[^>]*content="([^"]+)"', re.I),
]

clusters = {}

for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    topics = set()
    for pat in TOPIC_PATTERNS:
        for match in pat.findall(text):
            # Clean up topic text
            topic = re.sub(r'[^\w\s\-]', '', match).strip().lower()
            if topic:
                topics.add(topic)
    for topic in topics:
        clusters.setdefault(topic, []).append(str(page.relative_to(ROOT)))

with OUT.open("w") as f:
    json.dump(clusters, f, indent=2)

print(f"Topic clusters written: {len(clusters)} topics, {sum(len(v) for v in clusters.values())} pages.")
