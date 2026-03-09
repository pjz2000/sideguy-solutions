#!/usr/bin/env bash

cd /workspaces/sideguy-solutions

echo "Building SideGuy Authority Pages..."

python3 tools/authority-engine/build_authority_pages.py

echo "Authority pages generated"
