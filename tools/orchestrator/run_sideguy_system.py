import os
import subprocess

def run(cmd):
    print("\nRunning:", cmd)
    subprocess.run(cmd, shell=True)

print("\nSIDEGUY SYSTEM ORCHESTRATOR\n")

# 1 Radar
if os.path.exists("tools/future-radar/future_problem_radar.py"):
    run("python3 tools/future-radar/future_problem_radar.py")

# 2 Growth engine
if os.path.exists("tools/growth-engine/cluster_builder.py"):
    run("python3 tools/growth-engine/cluster_builder.py")

# 3 Query capture
if os.path.exists("tools/query-capture/query_capture.py"):
    run("python3 tools/query-capture/query_capture.py")

# 4 Page inventory
if os.path.exists("tools/recursive-builder/page_inventory.py"):
    run("python3 tools/recursive-builder/page_inventory.py")

# 5 Gap detection
if os.path.exists("tools/recursive-builder/gap_detector.py"):
    run("python3 tools/recursive-builder/gap_detector.py")

# 6 Priority builder
if os.path.exists("tools/recursive-builder/priority_builder.py"):
    run("python3 tools/recursive-builder/priority_builder.py")

# 7 Cluster injector
if os.path.exists("tools/cluster-injector/cluster_grouper.py"):
    run("python3 tools/cluster-injector/cluster_grouper.py")

if os.path.exists("tools/cluster-injector/card_builder.py"):
    run("python3 tools/cluster-injector/card_builder.py")

if os.path.exists("tools/cluster-injector/hub_injector.py"):
    run("python3 tools/cluster-injector/hub_injector.py")

print("\nSYSTEM COMPLETE\n")
