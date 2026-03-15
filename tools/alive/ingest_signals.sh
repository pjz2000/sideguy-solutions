#!/usr/bin/env bash
cd /workspaces/sideguy-solutions || exit 0
mkdir -p docs/alive/signals
cat docs/alive/inbox/*.txt docs/trend-signals/*.tsv 2>/dev/null \
| awk 'NF' \
| sort \
| uniq > docs/alive/signals/combined-signals.txt
echo "Signals ingested"
