#!/usr/bin/env python3
"""
SideGuy Problem Radar Engine
-------------------------------
Thin wrapper that runs the full traffic-radar.py engine and
also writes the legacy flat-path outputs expected by older scripts:
  docs/problem-radar/RADAR_QUEUE.md
  docs/problem-radar/seeds_classified.tsv

Usage:
  python3 scripts/problem-radar-engine.py

All seed inputs live in:
  docs/problem-radar/trends_notes.txt
  docs/problem-radar/manual_seeds.txt

Add new seeds to those files, then re-run.
"""

import subprocess, sys, shutil, os
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()

# ── Run the full radar engine ─────────────────────────────────────────────────
print("=" * 42)
print("SIDEGUY ADVANCED PROBLEM RADAR ENGINE")
print("=" * 42)
print()

result = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "traffic-radar.py")],
    cwd=str(ROOT),
)

if result.returncode != 0:
    print("ERROR: traffic-radar.py exited with errors.")
    sys.exit(result.returncode)

# ── Copy generated outputs to flat paths ─────────────────────────────────────
GENERATED = ROOT / "docs" / "problem-radar" / "generated"
FLAT      = ROOT / "docs" / "problem-radar"

copies = [
    (GENERATED / "RADAR_QUEUE.md",        FLAT / "RADAR_QUEUE.md"),
    (GENERATED / "seeds_classified.tsv",  FLAT / "seeds_classified.tsv"),
]

for src, dst in copies:
    if src.exists():
        shutil.copy2(src, dst)
        print(f"✓ Copied {src.name} → {dst.relative_to(ROOT)}")

# ── Summary ───────────────────────────────────────────────────────────────────
radar_queue = FLAT / "RADAR_QUEUE.md"
if radar_queue.exists():
    lines = radar_queue.read_text(encoding="utf-8").splitlines()
    # find signal summary table
    for i, line in enumerate(lines[:30]):
        if "Total unique" in line:
            print()
            print(line.strip())
            break

print()
print("Radar outputs:")
print("  docs/problem-radar/RADAR_QUEUE.md")
print("  docs/problem-radar/seeds_classified.tsv")
print("  docs/problem-radar/generated/CLAUDE_PROMPT.md")
print("  docs/problem-radar/generated/NEXT_ACTIONS.md")
print()
print("Add new topics → docs/problem-radar/trends_notes.txt")
print("Add priority items → docs/problem-radar/manual_seeds.txt")
print("Re-run: python3 scripts/problem-radar-engine.py")
