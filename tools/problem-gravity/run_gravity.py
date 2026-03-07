"""
run_gravity.py — Problem Gravity Pipeline Runner
Runs the engine and optionally merges output into the main build queue.
"""
import subprocess
import os

print("\nSIDEGUY PROBLEM GRAVITY ENGINE\n")

subprocess.run("python3 tools/problem-gravity/problem_gravity_engine.py", shell=True)

# Merge gravity pages into the recursive-builder signal pool if it exists
gravity_file = "docs/problem-gravity/gravity_pages.txt"
signals_file = "docs/recursive-builder/all-signals.txt"

if os.path.exists(gravity_file) and os.path.exists(signals_file):
    gravity = set(open(gravity_file).read().splitlines())
    existing = set(open(signals_file).read().splitlines())
    new_signals = gravity - existing
    if new_signals:
        with open(signals_file, "a") as f:
            for s in sorted(new_signals):
                f.write(s + "\n")
        print(f"  Merged {len(new_signals)} new signals into all-signals.txt")
    else:
        print("  All gravity signals already in all-signals.txt")

print("\nGravity run complete\n")
