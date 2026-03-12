#!/bin/bash

cd /workspaces/sideguy-solutions || exit 1

python3 tools/intelligence/agent_readiness_audit.py

echo
echo "Top 20 pages to upgrade next:"
echo "----------------------------------------"
head -21 docs/upgrade-queues/agent-readiness-upgrade-queue.tsv | column -t -s $'\t'
echo "----------------------------------------"
echo
echo "Audit JSON: docs/audits/agent-readiness-audit.json"
echo "Queue TSV : docs/upgrade-queues/agent-readiness-upgrade-queue.tsv"
