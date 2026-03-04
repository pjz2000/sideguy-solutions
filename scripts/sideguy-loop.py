#!/usr/bin/env python3
# ==============================================================
# SIDEGUY AUTONOMOUS LOOP
# One command runs the full intelligence pipeline in sequence:
#   1. Problem Radar (Google Suggest + SO + GH + Reddit)
#   2. Auto-build problems from data/problem-ideas-new.csv
#   3. Auto-build problems from radar/problem-radar-new.csv (new only)
#   4. Knowledge Graph cross-links
#   5. Traffic Multiplier hub pages
#   6. Sitemap regeneration
# ==============================================================

import os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

def run(label: str, cmd: str, env_extra: dict = None):
    print(f"\n{'─'*50}")
    print(f"  {label}")
    print(f"{'─'*50}")
    env = {**os.environ, **(env_extra or {})}
    result = subprocess.run(cmd, shell=True, cwd=ROOT, env=env)
    if result.returncode != 0:
        print(f"  ⚠  Non-zero exit code ({result.returncode}) — continuing.")

def script_exists(name: str) -> bool:
    p = ROOT / "scripts" / name
    if p.exists():
        return True
    print(f"  SKIP: scripts/{name} not found")
    return False

print("\n" + "═"*50)
print("  SIDEGUY AUTONOMOUS LOOP")
print("═"*50)

# 1 — Problem Radar
if script_exists("problem-radar.py"):
    run("1/6 Problem Radar", "python3 scripts/problem-radar.py")

# 2 — Auto-build from main CSV
if script_exists("auto-build-problems.py"):
    run("2/6 Auto-build: data/problem-ideas-new.csv", "python3 scripts/auto-build-problems.py")

# 3 — Auto-build from radar output
radar_csv = ROOT / "radar" / "problem-radar-new.csv"
if script_exists("auto-build-problems.py") and radar_csv.exists():
    run(
        "3/6 Auto-build: radar/problem-radar-new.csv",
        "python3 scripts/auto-build-problems.py",
        env_extra={"INPUT": str(radar_csv)},
    )
else:
    print("\n  3/6 Radar CSV not found yet — skipping radar auto-build")

# 4 — Knowledge Graph
if script_exists("knowledge-graph-builder.py"):
    run("4/6 Knowledge Graph Builder", "python3 scripts/knowledge-graph-builder.py")

# 5 — Traffic Multiplier
if script_exists("traffic-multiplier.py"):
    run("5/6 Traffic Multiplier", "python3 scripts/traffic-multiplier.py")

# 6 — Sitemap
if script_exists("generate-sitemap.py"):
    run("6/6 Sitemap Generator", "python3 scripts/generate-sitemap.py")

print("\n" + "═"*50)
print("  SIDEGUY LOOP COMPLETE")
print("═"*50 + "\n")
