"""
graph.py — SideGuy Graph Mode
Rebuilds the topic graph and related-page lists.
"""
import subprocess

print("\nSIDEGUY GRAPH MODE\n")

subprocess.run("python3 tools/topic-graph/run_graph.py", shell=True)

print("\nGraph update finished\n")
