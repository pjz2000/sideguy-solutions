#!/usr/bin/env python3
"""
Auto Commit — SideGuy Solutions
==============================
Stages and commits all new pages after each build for instant source control updates.
"""
import os
os.system('git add public/')
os.system('git commit -m "Add: real-time trending pages - auto-builder output" || true')
print("Auto commit complete.")
