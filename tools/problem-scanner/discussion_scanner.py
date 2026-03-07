"""
discussion_scanner.py
---------------------
Fetches recent HN discussions via Algolia API and collects titles
as raw problem signals → docs/problem-scanner/discussion-signals.txt.
"""
import urllib.request
import json
import os

sources = [
    ("ai",            "https://hn.algolia.com/api/v1/search?query=ai+small+business"),
    ("automation",    "https://hn.algolia.com/api/v1/search?query=automation+tools"),
    ("payments",      "https://hn.algolia.com/api/v1/search?query=payment+processing+fees"),
    ("crm",           "https://hn.algolia.com/api/v1/search?query=crm+software"),
    ("small business","https://hn.algolia.com/api/v1/search?query=small+business+problems"),
]

signals = []

for tag, url in sources:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SideGuy/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        hits = data.get("hits", [])
        collected = 0
        for hit in hits[:15]:
            title = (hit.get("title") or hit.get("story_title") or "").strip()
            if title:
                signals.append(title.lower())
                collected += 1
        print(f"  [{tag}] {collected} signals")
    except Exception as e:
        print(f"  [{tag}] fetch failed: {e}")

os.makedirs("docs/problem-scanner", exist_ok=True)
with open("docs/problem-scanner/discussion-signals.txt", "w") as f:
    for s in signals:
        f.write(s + "\n")

print(f"\nSignals collected: {len(signals)}")
