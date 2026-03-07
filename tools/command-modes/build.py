"""
build.py — SideGuy Build Mode
Shows the next pages to build from the priority queue.
Pass an optional count: python3 tools/command-modes/build.py 10
"""
import os
import sys

queue = "docs/recursive-builder/priority-pages.txt"

print("\nSIDEGUY BUILD MODE\n")

if not os.path.exists(queue):
    print("No build queue found — run: python3 tools/command-modes/sideguy.py expand")
    exit(1)

limit = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 30
pages = [l for l in open(queue).read().splitlines() if l.strip()]

print(f"Next {min(limit, len(pages))} pages to build (of {len(pages)} total):\n")
for p in pages[:limit]:
    score, slug = p.split(" ", 1) if " " in p else ("?", p)
    print(f"  [{score:>3}]  {slug}")

print("\nTo build these pages, pass the list to the hub builder or page generator.\n")
