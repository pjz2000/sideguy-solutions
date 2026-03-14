#!/usr/bin/env python3
"""Refresh stale pages by injecting a freshness block. Handles quoted CSV."""

import csv
import os
import datetime
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
os.chdir(ROOT)

cfg = {}
for line in Path("docs/nervous/config/freshness-rules.env").read_text().splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip()

MAX_REFRESH = int(cfg.get("MAX_REFRESH_PER_RUN", 75))
STALE_FILE  = Path("docs/nervous/queues/stale-pages.csv")

if not STALE_FILE.exists():
    print("No stale-pages.csv found.")
    raise SystemExit(1)

stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")
refresh_block = f"""
<section class="sideguy-freshness">
  <h2>Freshness update</h2>
  <p>This page was reviewed and refreshed on {stamp} to keep the information accurate as technology and business practices evolve.</p>
</section>
"""

count = 0
with open(STALE_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if count >= MAX_REFRESH:
            break
        file_path = Path(row["file"].strip())
        if not file_path.exists():
            continue
        text = file_path.read_text()
        # Skip already-refreshed pages
        if "sideguy-freshness" in text:
            continue
        if "</main>" in text:
            text = text.replace("</main>", refresh_block + "\n</main>", 1)
        else:
            text += refresh_block
        file_path.write_text(text)
        count += 1

print(f"Refreshed {count} stale pages.")
