"""
map.py — SideGuy Map Mode
Groups expansion pages into hub clusters, generates card HTML,
and injects cards into hub pages at <!--CLUSTER_CARDS--> markers.
"""
import os
import subprocess

print("\nSIDEGUY MAP MODE\n")

if os.path.exists("tools/cluster-injector/cluster_grouper.py"):
    subprocess.run("python3 tools/cluster-injector/cluster_grouper.py", shell=True)
else:
    print("  [skip] cluster_grouper not found")

if os.path.exists("tools/cluster-injector/card_builder.py"):
    subprocess.run("python3 tools/cluster-injector/card_builder.py", shell=True)
else:
    print("  [skip] card_builder not found")

if os.path.exists("tools/cluster-injector/hub_injector.py"):
    subprocess.run("python3 tools/cluster-injector/hub_injector.py", shell=True)
else:
    print("  [skip] hub_injector not found")

print("\nHub map updated\n")
