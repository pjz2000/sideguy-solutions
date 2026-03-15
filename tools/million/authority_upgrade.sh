#!/usr/bin/env bash
INPUT="docs/signal-miner/reports/signal-report.csv"
tail -n +2 "$INPUT" | head -20 | while IFS=, read -r score page
do
echo "Upgrading $page"
done
echo "Authority upgrades simulated"
