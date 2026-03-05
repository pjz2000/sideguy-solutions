#!/usr/bin/env python3
"""
SideGuy Topic Map Builder
--------------------------
Groups all HTML pages in the repo by their first slug token (the word before
the first hyphen) and writes a Markdown index to docs/topic-map/topic-map.md.

Also writes a TSV summary: docs/topic-map/topic-map-summary.tsv
  topic  page_count  sample_page
"""

import glob
import os
from collections import defaultdict
from pathlib import Path

ROOT     = Path(__file__).parent.parent.parent.resolve()
OUT_DIR  = ROOT / "docs" / "topic-map"
OUT_MD   = OUT_DIR / "topic-map.md"
OUT_TSV  = OUT_DIR / "topic-map-summary.tsv"

SKIP_DIRS = {".git", "node_modules", "_quarantine_backups", "dist", "build"}

def skip(path: str) -> bool:
    return any(f"/{d}/" in f"/{path.replace(os.sep, '/')}/" for d in SKIP_DIRS)

# Collect all HTML files
pages = [
    p for p in glob.glob(str(ROOT / "**" / "*.html"), recursive=True)
    if not skip(p)
]

topics: dict[str, list[str]] = defaultdict(list)
for p in sorted(pages):
    name = os.path.basename(p).replace(".html", "")
    parts = name.split("-")
    # Use first meaningful token (skip single-char tokens like "a")
    token = parts[0] if parts[0] else name
    topics[token].append(os.path.relpath(p, ROOT))

OUT_DIR.mkdir(parents=True, exist_ok=True)

# Write Markdown index
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# SideGuy Topic Map\n\n")
    f.write(f"Total pages: {len(pages)} | Topics: {len(topics)}\n\n---\n\n")
    for topic in sorted(topics):
        f.write(f"## {topic} ({len(topics[topic])} pages)\n")
        for p in topics[topic]:
            f.write(f"- {p}\n")
        f.write("\n")

# Write TSV summary
with open(OUT_TSV, "w", encoding="utf-8") as f:
    f.write("topic\tpage_count\tsample_page\n")
    for topic in sorted(topics, key=lambda t: -len(topics[t])):
        sample = topics[topic][0]
        f.write(f"{topic}\t{len(topics[topic])}\t{sample}\n")

print(f"Topic map created: {OUT_MD.relative_to(ROOT)}")
print(f"Topics : {len(topics)}")
print(f"Pages  : {len(pages)}")
print(f"Summary: {OUT_TSV.relative_to(ROOT)}")
