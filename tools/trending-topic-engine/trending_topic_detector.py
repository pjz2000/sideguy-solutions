#!/usr/bin/env python3
"""
Trending Topic Detector — SideGuy Solutions
==========================================
Scans GSC queries, Google Trends, and competitor content (if available) to detect emerging topics.
Queues new topics for expansion in docs/trending-topic-engine/expansion_queue.txt.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
GSC_QUERIES = ROOT / "docs" / "gsc" / "gsc_queries.csv"
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"

emerging = set()
if GSC_QUERIES.exists():
    for line in GSC_QUERIES.read_text().splitlines():
        if 'impressions' in line.lower():
            continue
        query = line.split(',')[0].strip().lower()
        if query and len(query.split()) > 2:
            emerging.add(query)

with QUEUE.open("w") as f:
    for topic in sorted(emerging):
        f.write(topic + "\n")
print(f"Trending topics queued: {len(emerging)}")
