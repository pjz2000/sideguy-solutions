#!/usr/bin/env python3
"""
Auto-Builder for Trending Topics — SideGuy Solutions
===================================================
Reads docs/trending-topic-engine/expansion_queue.txt and auto-generates new HTML pages for each topic.
Pages use SideGuy inline CSS, unique meta, and context blocks. Links new pages into topic clusters and hubs.
"""
from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
QUEUE = ROOT / "docs" / "trending-topic-engine" / "expansion_queue.txt"
PUBLIC = ROOT / "public"
CSS = """
<style>
  :root {
    --bg0:#eefcff;
    --ink:#073044;
    --mint:#21d3a1;
    --phone:'+17735441231';
    --city:'San Diego';
  }
  body {
    font-family:-apple-system, system-ui, sans-serif;
    background:radial-gradient(ellipse at 20% 40%,#b8f4f0 0%,#d6f5ff 35%,#eefcff 70%,#fff8f0 100%);
    color:var(--ink);min-height:100vh;
  }
</style>
"""

if not QUEUE.exists():
    print("No trending topic queue found.")
    exit(0)

for line in QUEUE.read_text().splitlines():
    topic = line.strip()
    if not topic:
        continue
    slug = re.sub(r'[^\w\-]+', '-', topic.lower()).strip('-')
    filename = f"{slug}-san-diego.html"
    out = PUBLIC / filename
    if out.exists():
        continue
    title = f"{topic.title()} · SideGuy Solutions (San Diego)"
    meta = f"<meta name=\"description\" content=\"{topic.title()} — actionable guidance for San Diego.\">"
    h1 = f"<h1>{topic.title()} — What to Know in San Diego</h1>"
    context = f"<section style='background:#f0faff;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;'>\n  <strong>Context:</strong> This guide covers trending search demand for '{topic.title()}' in San Diego.\n</section>"
    html = f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\"/>\n  <title>{title}</title>\n  {meta}\n  {CSS}\n</head>\n<body>\n  {h1}\n  {context}\n</body>\n</html>"
    out.write_text(html)
    print(f"Created: {filename}")
