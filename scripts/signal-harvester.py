import json
import random
from datetime import datetime

sources = {
    "reddit": [
        "how to automate small business",
        "AI tools for restaurants",
        "AI for plumbers",
        "AI bookkeeping small business",
        "automate HVAC scheduling"
    ],
    "trends": [
        "AI automation for contractors",
        "AI CRM for real estate",
        "AI call answering for dentists",
        "AI scheduling for gyms",
        "AI marketing for restaurants"
    ],
    "local": [
        "san diego hvac automation",
        "san diego ai bookkeeping",
        "san diego ai marketing",
        "san diego crypto payments",
        "san diego ai customer service"
    ]
}

signals = []

for category, items in sources.items():
    for item in items:
        signals.append({
            "topic": item,
            "source": category,
            "timestamp": datetime.utcnow().isoformat()
        })

random.shuffle(signals)

with open("signals/signals.json", "w") as f:
    json.dump(signals, f, indent=2)

print(f"Generated {len(signals)} signal topics")
