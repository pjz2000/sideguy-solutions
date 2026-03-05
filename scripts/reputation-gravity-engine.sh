#!/usr/bin/env bash
# SIDEGUY REPUTATION GRAVITY ENGINE
# Turns strong pages into authority flywheels
# Output: data/reputation-gravity.json

set -euo pipefail
cd "$(dirname "$0")/.."

echo "================================"
echo " SIDEGUY REPUTATION GRAVITY ENGINE"
echo "================================"
echo ""

python3 scripts/reputation-gravity.py

echo ""
echo "Generating authority report…"
python3 - << 'PY'
import json
data = json.load(open("data/reputation-gravity.json"))
print(f"Total pages : {data['total_pages']}")
print(f"Top nodes   : {len(data['top_pages'])}")
print("")
print("Top 20 authority nodes:")
for p in data["top_pages"][:20]:
    print(f"  {p['inbound']:5}  {p['path']}")
PY

echo ""
echo "Gravity engine complete."
