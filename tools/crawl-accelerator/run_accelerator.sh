#!/usr/bin/env bash
cd /workspaces/sideguy-solutions
echo "Running crawl accelerator..."
python3 tools/crawl-accelerator/crawl_accelerator.py
echo "Hub + sitemap updated"
