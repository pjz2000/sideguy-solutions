"""
sideguy.py — SideGuy Command Line Interface
============================================
Usage:
  python3 tools/command-modes/sideguy.py <mode> [options]

Modes:
  discover   Find new operator problems (future-radar + query-capture)
  expand     Generate page matrix, detect gaps, score build queue
  build      Show next pages to build  [optional: count, e.g. build 10]
  map        Update hub cluster cards and inject into hub pages
  monitor    Run scale dashboard (page count + cluster distribution)
  status     Quick system health check (file/tool presence only)
"""
import sys
import subprocess
import os

MODES = {
    "discover": ("tools/command-modes/discover.py",       "Find new operator problems"),
    "expand":   ("tools/command-modes/expand.py",         "Generate page matrix + gap list"),
    "build":    ("tools/command-modes/build.py",          "Show next pages to build"),
    "map":      ("tools/command-modes/map.py",            "Update hub cluster cards"),
    "graph":    ("tools/command-modes/graph.py",          "Rebuild topic graph"),
    "gravity":  ("tools/command-modes/gravity.py",        "Detect emerging problems"),
    "monitor":  ("tools/scale-monitor/scale_dashboard.py","Scale dashboard"),
}

def print_help():
    print("\nSideGuy Command Modes\n")
    print(f"  {'Command':<12}  Description")
    print(f"  {'-'*12}  {'-'*38}")
    for cmd, (_, desc) in MODES.items():
        print(f"  {cmd:<12}  {desc}")
    print("\n  status     Quick system health check")
    print("\nExample:  python3 tools/command-modes/sideguy.py build 10\n")

def run_status():
    print("\nSIDEGUY SYSTEM STATUS\n")
    checks = [
        ("Future radar",      "tools/future-radar/future_problem_radar.py"),
        ("Query capture",     "tools/query-capture/query_capture.py"),
        ("Growth engine",     "tools/growth-engine/cluster_builder.py"),
        ("Recursive builder", "tools/recursive-builder/priority_builder.py"),
        ("Cluster injector",  "tools/cluster-injector/hub_injector.py"),
        ("Scale monitor",     "tools/scale-monitor/scale_dashboard.py"),
        ("Expansion matrix",  "docs/growth-engine/page-expansion.txt"),
        ("Build queue",       "docs/recursive-builder/priority-pages.txt"),
        ("All signals",       "docs/recursive-builder/all-signals.txt"),
    ]
    for label, path in checks:
        status = "OK" if os.path.exists(path) else "MISSING"
        print(f"  {'OK' if status=='OK' else '!!'} {label:<22} {path}")
    print()

cmd = sys.argv[1] if len(sys.argv) > 1 else ""
extra = sys.argv[2] if len(sys.argv) > 2 else ""

if cmd in MODES:
    script = MODES[cmd][0]
    run_cmd = f"python3 {script} {extra}".strip()
    subprocess.run(run_cmd, shell=True)
elif cmd == "status":
    run_status()
else:
    print_help()
