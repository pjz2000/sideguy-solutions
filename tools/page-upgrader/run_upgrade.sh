#!/usr/bin/env bash

cd /workspaces/sideguy-solutions

echo "Running SideGuy Page Upgrade Engine..."

python3 tools/page-upgrader/upgrade_pages.py

echo "Upgrade complete"
