#!/usr/bin/env python3
"""
Auto-Upgrade Weak Pages — SideGuy Solutions
===========================================
Reads docs/quality-loop/needs_upgrade.txt and runs context injector + uniqueness engine
on each flagged page. Idempotent: skips pages already upgraded.

Run after quality scorer for maximum improvement.
"""
from pathlib import Path
import subprocess

ROOT = Path("/workspaces/sideguy-solutions")
UPGRADE_LIST = ROOT / "docs" / "quality-loop" / "needs_upgrade.txt"

if not UPGRADE_LIST.exists():
    print("No upgrade queue found.")
    exit(0)

pages = [line.strip() for line in UPGRADE_LIST.read_text().splitlines() if line.strip()]
if not pages:
    print("Upgrade queue empty.")
    exit(0)

print(f"Auto-upgrading {len(pages)} weak pages…")

for rel_path in pages:
    abs_path = ROOT / rel_path
    # Run context injector
    subprocess.run(["python3", str(ROOT / "tools" / "context-engine" / "context_injector.py"), str(abs_path)], check=False)
    # Run uniqueness engine
    subprocess.run(["python3", str(ROOT / "tools" / "uniqueness-engine" / "unique_paragraphs.py"), str(abs_path)], check=False)

print("Auto-upgrade complete.")
