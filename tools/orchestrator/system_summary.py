import os

pages = 0

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".html"):
            pages += 1

print("\nSIDEGUY SYSTEM STATUS\n")
print("Total HTML pages:", pages)

if os.path.exists("docs/growth-engine/page-expansion.txt"):
    print("Expansion matrix ready")

if os.path.exists("docs/recursive-builder/priority-pages.txt"):
    print("Priority build queue ready")

if os.path.exists("docs/cluster-injector"):
    print("Hub cluster injector ready")

print("\nCommand Center Online\n")
