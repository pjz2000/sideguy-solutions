import json, os, datetime
import feedparser

RSS_SOURCES = [
    "https://www.reddit.com/r/smallbusiness/top.rss",
    "https://www.reddit.com/r/Entrepreneur/top.rss",
]

# Fallback seeds used when RSS is unavailable (no network in CI, etc.)
FALLBACK = [
    "how to automate small business",
    "AI tools for restaurants",
    "AI for plumbers",
    "AI bookkeeping small business",
    "automate HVAC scheduling",
    "AI automation for contractors",
    "AI CRM for real estate",
    "AI call answering for dentists",
    "AI scheduling for gyms",
    "AI marketing for restaurants",
    "san diego hvac automation",
    "san diego ai bookkeeping",
    "san diego ai marketing",
    "san diego crypto payments",
    "san diego ai customer service",
]

os.makedirs("signals", exist_ok=True)

signals = []
now = datetime.datetime.now(datetime.UTC).isoformat()

for url in RSS_SOURCES:
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            signals.append({"topic": entry.title, "source": url, "timestamp": now})
        print(f"  {url}: {min(10, len(feed.entries))} entries")
    except Exception as e:
        print(f"  {url}: fetch failed ({e})")

if not signals:
    print("RSS unavailable — using fallback seed topics")
    for t in FALLBACK:
        signals.append({"topic": t, "source": "fallback", "timestamp": now})

with open("signals/signals.json", "w") as f:
    json.dump(signals, f, indent=2)

print(f"Generated {len(signals)} signal topics")
