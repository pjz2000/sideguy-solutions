import os

expansion_file = "docs/growth-engine/page-expansion.txt"
existing_file = "docs/recursive-builder/site-pages.txt"

if not os.path.exists(expansion_file):
    print("Missing page-expansion.txt")
    exit()

expansion = set(open(expansion_file).read().split())
existing = set()

if os.path.exists(existing_file):
    existing = set(open(existing_file).read().split())

missing = expansion - existing

with open("docs/recursive-builder/pages-to-build.txt", "w") as f:
    for p in sorted(missing):
        f.write(p + "\n")

print("Missing pages:", len(missing))
