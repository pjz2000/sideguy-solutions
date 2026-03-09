#!/usr/bin/env bash

echo ""
echo "==============================="
echo "SIDEGUY INTELLIGENCE PIPELINE"
echo "==============================="
echo ""

cd /workspaces/sideguy-solutions

echo "0️⃣  Signal Scanner  ←— ingest curated queries first"
echo "--------------------------------"
if [ -f tools/signal-scanner/signal_scanner.py ]; then
  python3 tools/signal-scanner/signal_scanner.py
else
  echo "Signal scanner not installed"
fi

echo ""
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
echo "7️⃣  Signal Extractor  ←— feeds NEXT run"
echo "--------------------------------"
if [ -f tools/expansion-engine/signal_extractor.py ]; then
  python3 tools/expansion-engine/signal_extractor.py
else
  echo "Signal extractor not installed"
fi

echo ""
echo "8️⃣  Quality Scorer  ←— improves weak pages"
echo "--------------------------------"
if [ -f tools/quality-loop/page_scorer.py ]; then
  python3 tools/quality-loop/page_scorer.py
else
  echo "Quality scorer not installed"
fi

echo ""
echo "9️⃣  Self-Improving SEO  ←— GSC winner injection"
echo "--------------------------------"
if [ -f tools/self-improving-seo/self_improving_seo.py ]; then
  python3 tools/self-improving-seo/self_improving_seo.py
else
  echo "Self-improving SEO not installed (needs docs/gsc/gsc_pages.csv)"
fi

echo ""
echo "==============================="
echo "PIPELINE COMPLETE"
echo "==============================="
echo ""
echo "Loop status:"
grep -c "" docs/problem-gravity/gravity_pages.txt 2>/dev/null | xargs -I{} echo "  Gravity queue : {} slugs"
cat docs/quality-loop/summary.txt 2>/dev/null | grep -E "Needs upgrade|Average score" | sed 's/^/  /'
echo "  Run again to process new signals ↑"
echo ""
