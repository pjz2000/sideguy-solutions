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
echo "====================================="
echo "SIDEGUY RUN COMPLETE"
echo "====================================="
