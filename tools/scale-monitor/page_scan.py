import os

pages = []

for root, dirs, files in os.walk("."):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root, f))

print("Total HTML pages:", len(pages))

# Breakdown by top-level directory vs root
root_pages = [p for p in pages if p.count("/") <= 1]
sub_pages = [p for p in pages if p.count("/") > 1]
print("  Root-level pages:", len(root_pages))
print("  Subdirectory pages:", len(sub_pages))
