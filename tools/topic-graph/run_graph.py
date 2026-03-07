"""
run_graph.py
------------
Runs the full topic-graph pipeline:
  1. build_graph.py   — scan pages, bin into topics
  2. build_related.py — write per-topic related-page lists
"""
import subprocess

print("\nSIDEGUY TOPIC GRAPH ENGINE\n")

subprocess.run("python3 tools/topic-graph/build_graph.py", shell=True)
subprocess.run("python3 tools/topic-graph/build_related.py", shell=True)

print("\nTopic graph generation complete\n")
