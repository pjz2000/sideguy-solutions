"""
scale_dashboard.py
------------------
Full SideGuy scale monitor — page counts, cluster distribution,
gap analysis status, and priority build queue summary.
"""
import subprocess
import os

SEP = "-" * 45

def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

print("SIDEGUY SCALE MONITOR")
print("=" * 45)

section("Page Count")
subprocess.run(["python3", "tools/scale-monitor/page_scan.py"])

section("Cluster Distribution")
subprocess.run(["python3", "tools/scale-monitor/cluster_scan.py"])

section("Growth Engine Status")
gap_file = "docs/recursive-builder/pages-to-build.txt"
priority_file = "docs/recursive-builder/priority-pages.txt"
expansion_file = "docs/growth-engine/page-expansion.txt"

if os.path.exists(expansion_file):
    n = len(open(expansion_file).read().splitlines())
    print(f"  Expansion matrix:    {n} target slugs")

if os.path.exists(gap_file):
    gaps = [l for l in open(gap_file).read().splitlines() if l.strip()]
    print(f"  Pages still to build: {len(gaps)}")

if os.path.exists(priority_file):
    top = open(priority_file).read().splitlines()[:5]
    print(f"  Top 5 priority pages:")
    for t in top:
        print(f"    {t}")

section("Signal Sources")
signals_file = "docs/recursive-builder/all-signals.txt"
query_file = "data/query-capture/page-ideas.txt"
future_file = "data/future-signals/future-problems.tsv"

for label, path in [
    ("All signals merged", signals_file),
    ("Query capture ideas", query_file),
    ("Future radar signals", future_file),
]:
    if os.path.exists(path):
        n = len(open(path).read().splitlines())
        print(f"  {label:<26} {n}")
    else:
        print(f"  {label:<26} (not found)")

section("Hub Pages")
hubs = ["ai-automation.html", "payments.html", "lead-generation.html",
        "business-operations.html", "technology-decisions.html"]
for h in hubs:
    status = "OK" if os.path.exists(h) else "MISSING"
    size = f"{os.path.getsize(h):,} bytes" if os.path.exists(h) else ""
    print(f"  {h:<36} {status}  {size}")

print(f"\n{'=' * 45}")
print("  Command Center Online")
print("=" * 45)
