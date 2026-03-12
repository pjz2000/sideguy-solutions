#!/usr/bin/env python3
"""SideGuy Intelligence Engines — interactive runner."""
import subprocess, sys

MENU = """
SideGuy Intelligence Engines
-----------------------------
1  News radar (signal seeds → data/signals/news_signals.tsv)
2  Authority gravity (public/ pages by size → docs/intel-reports/authority_pages.txt)
3  Page 2 opportunity seeds (→ docs/intel-reports/page2_targets.txt)
4  Full authority scan (root-level, slow) → docs/authority-gravity/authority-gravity.tsv
5  GSC page-2 engine (requires data/gsc/search-console-pages.csv)
q  Quit
"""

COMMANDS = {
    "1": ["python3", "tools/intel-engines/news_radar.py"],
    "2": ["python3", "tools/intel-engines/authority_gravity.py"],
    "3": ["python3", "tools/intel-engines/page2_opportunities.py"],
    "4": ["python3", "tools/authority-gravity/authority_gravity.py"],
    "5": ["python3", "tools/gsc-opportunity/page2_opportunity_engine.py"],
}

print(MENU)
choice = input("Select engine: ").strip().lower()

if choice == "q":
    sys.exit(0)
elif choice in COMMANDS:
    subprocess.run(COMMANDS[choice])
else:
    print("Invalid choice.")
