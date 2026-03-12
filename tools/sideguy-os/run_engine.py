#!/usr/bin/env python3
"""
SideGuy Command Center — interactive tool launcher.
All options produce reports or stubs only. No pages are auto-published.
"""
import subprocess, sys

MENU = """
SideGuy Command Center
----------------------
1  Run intelligence engines   (analysis reports)
2  Run authority gravity scan (full root scan)
3  View cluster roadmap       (docs/cluster-plans/cluster_outline.json)
4  Build new page stub        (requires human content before publishing)
5  Validate page families     (read-only audit)
q  Quit
"""

print(MENU)
choice = input("Select option: ").strip().lower()

if choice == "q":
    sys.exit(0)

elif choice == "1":
    subprocess.run(["python3", "tools/intel-engines/run_intel.py"])

elif choice == "2":
    subprocess.run(["python3", "tools/authority-gravity/authority_gravity.py"])

elif choice == "3":
    import json, os
    path = "docs/cluster-plans/cluster_outline.json"
    if os.path.exists(path):
        data = json.load(open(path))
        print()
        for cluster, pages in data.items():
            print(f"[{cluster}]")
            for p in pages:
                print(f"  {p}")
            print()
    else:
        print("No cluster outline found. Run tools/cluster-planner/build_clusters.py first.")

elif choice == "4":
    slug = input("Page slug (e.g. ai-receptionist-cost-san-diego): ").strip()
    if slug:
        subprocess.run(["python3", "tools/page-builder/build_page.py", slug])
    else:
        print("No slug provided.")

elif choice == "5":
    subprocess.run(["python3", "tools/differentiation/page_family_validator.py"])

else:
    print("Invalid option.")
