#!/usr/bin/env bash
# SideGuy Solutions — Daily Update Pipeline
# Runs: topic fetchers → auto-builder → meme injector → sitemap → commit + push
set -e

REPO="/workspaces/sideguy-solutions"
cd "$REPO"

echo "[pipeline] $(date) — starting"

# 1. Fetch trending topics (static curated for now; swap in live API when key is ready)
python3 tools/trending-topic-engine/google_trends_fetcher.py
python3 tools/trending-topic-engine/reddit_topic_scraper.py

# 2. Build any new pages from queue
python3 tools/trending-topic-engine/auto_builder.py

# 3. Inject memes into any pages that don't have one yet
python3 tools/page-upgrader/meme_injector.py

# 4. Regenerate public sitemap
python3 - <<'EOF'
import os
from datetime import date
today = date.today().isoformat()
base = "https://sideguysolutions.com"
pages = []
for root, dirs, files in os.walk("public"):
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    for f in files:
        if f.endswith(".html"):
            path = os.path.join(root, f)
            url_path = "/" + path.replace("public/", "", 1)
            pages.append(url_path)
pages.sort()
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages:
    lines.append(f'<url><loc>{base}{p}</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>')
lines.append('</urlset>')
with open("public/sitemap.xml", "w") as fh:
    fh.write("\n".join(lines))
print(f"Sitemap: {len(pages)} URLs")
EOF

# 5. Commit and push if there are changes
if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard public/)" ]; then
    git add public/ docs/trending-topic-engine/expansion_queue.txt
    git commit -m "Auto: daily pipeline — memes, trending pages, sitemap ($(date +%Y-%m-%d))"
    git push
    echo "[pipeline] committed and pushed"
else
    echo "[pipeline] nothing changed, skipping commit"
fi

echo "[pipeline] done"
