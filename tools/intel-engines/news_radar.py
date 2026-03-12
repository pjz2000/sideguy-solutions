#!/usr/bin/env python3
"""
News Radar — writes a static signal list to data/signals/news_signals.tsv.
Replace the signals list with real RSS/API data when ready.
"""
import datetime, os

signals = [
    "AI receptionist adoption rising",
    "Solana payment rails for merchants",
    "Stripe vs Square fee complaints",
    "Local service automation tools",
    "AI customer support for small business",
    "Zapier vs Make automation growth",
]

os.makedirs("data/signals", exist_ok=True)

now = datetime.datetime.utcnow().isoformat()
out = "data/signals/news_signals.tsv"

with open(out, "w") as f:
    f.write("timestamp\tsignal\n")
    for s in signals:
        f.write(f"{now}\t{s}\n")

print(f"News radar signals written to {out}")
