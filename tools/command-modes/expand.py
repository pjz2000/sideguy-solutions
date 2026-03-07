"""
expand.py — SideGuy Expand Mode
Regenerates the page matrix, detects gaps, and scores the build queue.
"""
import os
import subprocess

print("\nSIDEGUY EXPAND MODE\n")

if os.path.exists("tools/growth-engine/cluster_builder.py"):
    subprocess.run("python3 tools/growth-engine/cluster_builder.py", shell=True)
else:
    print("  [skip] growth-engine not found")

if os.path.exists("tools/recursive-builder/page_inventory.py"):
    subprocess.run("python3 tools/recursive-builder/page_inventory.py", shell=True)
else:
    print("  [skip] page_inventory not found")

if os.path.exists("tools/recursive-builder/gap_detector.py"):
    subprocess.run("python3 tools/recursive-builder/gap_detector.py", shell=True)
else:
    print("  [skip] gap_detector not found")

if os.path.exists("tools/recursive-builder/priority_builder.py"):
    subprocess.run("python3 tools/recursive-builder/priority_builder.py", shell=True)
else:
    print("  [skip] priority_builder not found")

print("\nExpansion lists updated\n")
