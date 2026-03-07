import requests
import datetime

OUTPUT = "docs/future-radar/future-problems.tsv"

sources = [
    ("ai", "https://hn.algolia.com/api/v1/search?query=ai"),
    ("automation", "https://hn.algolia.com/api/v1/search?query=automation"),
    ("payments", "https://hn.algolia.com/api/v1/search?query=payments"),
    ("startup", "https://hn.algolia.com/api/v1/search?query=software")
]

signals = []

def add_signal(source, title):
    signals.append({
        "source": source,
        "title": title,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })

for tag, url in sources:
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        for hit in data.get("hits", [])[:10]:
            title = hit.get("title")
            if title:
                add_signal(tag, title)
    except Exception:
        pass

with open(OUTPUT, "w") as f:
    f.write("source\ttitle\ttimestamp\n")
    for s in signals:
        f.write(f"{s['source']}\t{s['title']}\t{s['timestamp']}\n")

print("Future problem signals collected:", len(signals))
