"""
gravity.py — SideGuy Gravity Mode
Detects and maps emerging operator problems into page slugs.
"""
import subprocess

print("\nSIDEGUY GRAVITY MODE\n")

subprocess.run("python3 tools/problem-gravity/run_gravity.py", shell=True)
subprocess.run("python3 tools/gravity-ranking/gravity_ranker.py", shell=True)

print("\nGravity mode finished\n")
