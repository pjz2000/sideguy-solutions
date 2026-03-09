#!/usr/bin/env bash

cd /workspaces/sideguy-solutions

echo "Running Search Console Intelligence..."

python3 tools/gsc-intelligence/process_queries.py

echo "Query analysis complete"
