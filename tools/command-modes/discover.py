"""
discover.py — SideGuy Discover Mode
Runs future-radar and query-capture to surface new operator problems.
"""
import os
import subprocess

print("\nSIDEGUY DISCOVER MODE\n")

if os.path.exists("tools/future-radar/future_problem_radar.py"):
    subprocess.run("python3 tools/future-radar/future_problem_radar.py", shell=True)
else:
    print("  [skip] future-radar not found")

if os.path.exists("tools/query-capture/query_capture.py"):
    subprocess.run("python3 tools/query-capture/query_capture.py", shell=True)
else:
    print("  [skip] query-capture not found")

print("\nDiscovery complete\n")
