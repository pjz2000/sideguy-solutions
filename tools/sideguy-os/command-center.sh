#!/usr/bin/env bash
cd /workspaces/sideguy-solutions || exit 0
echo ""
echo "SideGuy Command Center"
echo ""
echo "1 Trend Radar"
echo "2 Alive Discovery"
echo "3 Million Page Matrix"
echo "4 Signal Miner"
echo "5 Gravity Map"
echo "6 Authority Upgrade"
echo "7 Run Everything"
echo ""
read -p "Select option: " OPT
case $OPT in
1) bash tools/trend-radar/run_trend_radar.sh ;;
2) bash tools/alive/ingest_signals.sh ;;
3) bash tools/million/hyper_matrix_engine.sh ;;
4) python3 tools/signal-miner/signal_miner.py ;;
5) python3 tools/gravity-map/gravity_map.py ;;
6) bash tools/million/authority_upgrade.sh ;;
7)
bash tools/trend-radar/run_trend_radar.sh
bash tools/alive/ingest_signals.sh
bash tools/million/hyper_matrix_engine.sh
python3 tools/signal-miner/signal_miner.py
python3 tools/gravity-map/gravity_map.py
bash tools/million/authority_upgrade.sh
;;
esac
