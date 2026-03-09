#!/bin/bash

echo "====================================="
echo "SIDEGUY COMMAND CENTER"
echo "====================================="

echo ""
echo "Step 1: Radar Signals"
python3 tools/problem-radar-v2/radar_v2.py || true

echo ""
echo "Step 2: Traffic Engine"
python3 tools/traffic-engine/traffic_engine.py || true

echo ""
echo "Step 3: Network Engine"
python3 tools/network-engine/network_engine.py || true

echo ""
echo "Step 4: Surface Engine"
python3 tools/surface-engine/surface_engine.py || true

echo ""
echo "Step 5: Trend Engine"
python3 tools/trend-engine/trend_engine.py || true

echo ""
echo "Step 6: Learning Loop"
python3 tools/learning-loop/learning_loop.py || true

echo ""
echo "Step 7: Learning Builder"
python3 tools/learning-builder/learning_builder.py || true

echo ""
echo "Step 8: Gravity Engine"
python3 tools/problem-gravity/gravity_engine.py || true

echo ""
echo "Step 9: Cluster Intelligence"
python3 tools/cluster-intelligence/cluster_intelligence.py || true

echo ""
echo "Step 10: Hub Router"
python3 tools/hub-router/hub_router.py || true

echo ""
echo "Step 11: Signal Scanner  ←— curated query ingestion"
python3 tools/signal-scanner/signal_scanner.py || true

echo ""
echo "Step 12: Inventory Intelligence"
if [ -f tools/inventory-intelligence/build_inventory_signals.py ]; then
  python3 tools/inventory-intelligence/build_inventory_signals.py || true
fi

echo ""
echo "Step 13: Gravity Page Builder"
if [ -f tools/auto-builder/run_builder.py ]; then
  python3 tools/auto-builder/run_builder.py || true
fi

echo ""
echo "Step 14: Context Injector"
python3 tools/context-engine/context_injector.py || true

echo ""
echo "Step 15: Uniqueness Engine"
python3 tools/uniqueness-engine/unique_paragraphs.py || true

echo ""
echo "Step 16: Crawl Accelerator  ←— hub index + sitemap"
python3 tools/crawl-accelerator/crawl_accelerator.py || true

echo ""
echo "Step 17: Signal Extractor  ←— seeds next run"
python3 tools/expansion-engine/signal_extractor.py || true

echo ""
echo "Step 18: Quality Scorer  ←— flags weak pages"
python3 tools/quality-loop/page_scorer.py || true

echo ""
echo "Step 19: Meme Injector"
python3 tools/page-upgrader/meme_injector.py || true

echo ""
echo "Step 20: FAQ/Schema Injector"
python3 tools/page-upgrader/faq_schema_injector.py || true

echo ""
echo "Step 21: Lead Magnet Injector"
python3 tools/page-upgrader/lead_magnet_injector.py || true

echo ""
echo "Step 22: Sitemap Refresh"
if [ -f tools/page-upgrader/generate_sitemap_xml.py ]; then
  python3 tools/page-upgrader/generate_sitemap_xml.py || true
fi

echo ""
echo "Step 23: Topic Cluster Builder"
python3 tools/topic-cluster-engine/topic_cluster_builder.py || true

echo ""
echo "Step 24: Semantic Link Injector"
python3 tools/topic-cluster-engine/semantic_link_injector.py || true

echo ""
echo "Step 25: Trending Topic Detector"
python3 tools/trending-topic-engine/trending_topic_detector.py || true

echo ""
echo "Step 26: Freshness Upgrader"
python3 tools/freshness-engine/freshness_upgrader.py || true

echo ""
echo "Step 27: Schema Expander"
python3 tools/schema-expander/schema_expander.py || true

echo ""
echo "Step 28: Engagement Injector"
python3 tools/engagement-engine/engagement_injector.py || true

echo ""
echo "Step 29: Trust Injector"
python3 tools/trust-engine/trust_injector.py || true

echo ""
echo "Step 30: Auto-Builder for Trending Topics"
python3 tools/trending-topic-engine/auto_builder.py || true

echo ""
echo "Step 31: Reddit Topic Scraper"
python3 tools/trending-topic-engine/reddit_topic_scraper.py || true

echo ""
echo "Step 32: Google Trends Fetcher"
python3 tools/trending-topic-engine/google_trends_fetcher.py || true

echo ""
echo "Step 33: Reddit API Fetcher"
python3 tools/trending-topic-engine/reddit_api_fetcher.py || true

echo ""
echo "Step 34: Twitter API Fetcher"
python3 tools/trending-topic-engine/twitter_api_fetcher.py || true

echo ""
echo "Step 35: News API Fetcher"
python3 tools/trending-topic-engine/news_api_fetcher.py || true

echo ""
echo "Step 36: Stack Overflow API Fetcher"
python3 tools/trending-topic-engine/stackoverflow_api_fetcher.py || true

echo ""
echo "Step 37: Quora API Fetcher"
python3 tools/trending-topic-engine/quora_api_fetcher.py || true

echo ""
echo "====================================="
echo "SIDEGUY RUN COMPLETE"
echo "====================================="
echo ""
echo "Loop status:"
grep -c "" docs/problem-gravity/gravity_pages.txt 2>/dev/null | xargs -I{} echo "  Gravity queue : {} slugs"
cat docs/quality-loop/summary.txt 2>/dev/null | grep -E "Needs upgrade|Average score" | sed 's/^/  /'
echo ""
