#!/usr/bin/env bash

cd /workspaces/sideguy-solutions

echo "Running SideGuy Inventory Intelligence..."
python3 tools/inventory-intelligence/build_inventory_signals.py
python3 tools/inventory-intelligence/append_to_gravity.py

echo "Done."
echo "Next step:"
echo "python3 tools/auto-builder/run_builder.py"
