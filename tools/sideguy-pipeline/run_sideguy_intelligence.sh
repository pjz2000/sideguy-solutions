#!/usr/bin/env bash

echo ""
echo "==============================="
echo "SIDEGUY INTELLIGENCE PIPELINE"
echo "==============================="
echo ""

cd /workspaces/sideguy-solutions

echo "1️⃣  Market Radar Discovery"
echo "--------------------------------"
if [ -f tools/market-radar/market_radar.py ]; then
  python3 tools/market-radar/market_radar.py
else
  echo "Market radar not installed"
fi

echo ""
echo "2️⃣  Inventory Intelligence"
echo "--------------------------------"
if [ -f tools/inventory-intelligence/run_inventory_intelligence.sh ]; then
  bash tools/inventory-intelligence/run_inventory_intelligence.sh
else
  echo "Inventory intelligence not installed"
fi

echo ""
echo "3️⃣  Gravity Page Builder"
echo "--------------------------------"
if [ -f tools/auto-builder/run_builder.py ]; then
  python3 tools/auto-builder/run_builder.py
else
  echo "Gravity builder not installed"
fi

echo ""
echo "4️⃣  Context Differentiation"
echo "--------------------------------"
if [ -f tools/context-engine/context_injector.py ]; then
  python3 tools/context-engine/context_injector.py
else
  echo "Context engine missing"
fi

echo ""
echo "5️⃣  Crawl Accelerator"
echo "--------------------------------"
if [ -f tools/crawl-accelerator/run_accelerator.sh ]; then
  bash tools/crawl-accelerator/run_accelerator.sh
else
  echo "Crawl accelerator not installed"
fi

echo ""
echo "6️⃣  Sitemap Refresh"
echo "--------------------------------"
if [ -f public/sitemap.xml ]; then
  echo "Sitemap present — re-generating..."
  python3 tools/page-upgrader/generate_sitemap_xml.py
else
  echo "WARNING: sitemap.xml missing — run generate_sitemap_xml.py"
fi

echo ""
echo "==============================="
echo "PIPELINE COMPLETE"
echo "==============================="
echo ""
