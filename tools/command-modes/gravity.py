"""
gravity.py — SideGuy Gravity Mode
Detects and maps emerging operator problems into page slugs.
"""
import subprocess

print("\nSIDEGUY GRAVITY MODE\n")

subprocess.run("python3 tools/problem-gravity/run_gravity.py", shell=True)

print("\nGravity mode finished\n")
