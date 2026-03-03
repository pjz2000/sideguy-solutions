"""
Signal Connector — converts signals/signals.json into signals/signal-topics.txt
generate-topics.py reads that file as extra seed topics each run.
"""
import json, os, re

os.makedirs("signals", exist_ok=True)

try:
    with open("signals/signals.json") as f:
        signals = json.load(f)
except FileNotFoundError:
    signals = []

def clean(title):
    # strip punctuation, lowercase, basic normalise
    t = title.lower().strip()
    t = re.sub(r"[^\w\s-]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

seen = set()
topics = []
for s in signals:
    t = clean(s.get("topic", ""))
    if t and t not in seen and len(t) > 5:
        seen.add(t)
        topics.append(t)

with open("signals/signal-topics.txt", "w") as f:
    for t in topics:
        f.write(t + "\n")

print(f"Converted {len(topics)} signals → signals/signal-topics.txt")
