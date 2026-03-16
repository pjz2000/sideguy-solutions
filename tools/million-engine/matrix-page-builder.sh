#!/bin/bash
# SideGuy Matrix Page Builder wrapper
# Full build: bash tools/million-engine/matrix-page-builder.sh
# Dry run:    bash tools/million-engine/matrix-page-builder.sh --dry-run
# Subset:     bash tools/million-engine/matrix-page-builder.sh --service=hvac --location="san diego"
python3 tools/million-engine/matrix-page-builder.py "$@"
