#!/usr/bin/env python3
"""
Authority Gravity (public/ variant) — read-only.
Ranks pages in public/ by file size as a quick content-depth proxy.
For the full root-level scan, use tools/authority-gravity/authority_gravity.py.
"""
import os

ROOT = "public"
report = []

for root_dir, dirs, files in os.walk(ROOT):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root_dir, file)
            size = os.path.getsize(path)
            report.append((size, path))

report.sort(reverse=True)

os.makedirs("docs/intel-reports", exist_ok=True)
out = "docs/intel-reports/authority_pages.txt"

with open(out, "w") as f:
    f.write("size_bytes\tpath\n")
    for size, path in report[:50]:
        f.write(f"{size}\t{path}\n")

print(f"Authority report written to {out} ({len(report)} pages total)")
