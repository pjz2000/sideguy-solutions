#!/usr/bin/env bash

cd /workspaces/sideguy-solutions

echo ""
echo "=================================="
echo "SIDEGUY OPPORTUNITY ENGINE"
echo "=================================="
echo ""

python3 tools/opportunity-engine/build_priority_queue.py

echo ""
echo "Running builder..."
python3 tools/auto-builder/run_builder.py

echo ""
echo "Refreshing context..."
if [ -f tools/context-engine/context_injector.py ]; then
  python3 tools/context-engine/context_injector.py
fi

echo ""
echo "Refreshing links..."
if [ -f tools/internal-links/link_engine.py ]; then
  python3 tools/internal-links/link_engine.py
fi

echo ""
echo "Refreshing sitemap..."
if [ -f tools/page-upgrader/generate_sitemap_xml.py ]; then
  python3 tools/page-upgrader/generate_sitemap_xml.py
fi

echo ""
echo "Done."
echo "Queue: docs/opportunity-engine/priority_queue.txt"
echo "Report: docs/opportunity-engine/priority_report.tsv"