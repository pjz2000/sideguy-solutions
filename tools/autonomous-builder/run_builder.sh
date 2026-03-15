#!/usr/bin/env bash
PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0
BATCH="${1:-docs/autonomous-builder/queues/batch-0001.tsv}"
python3 tools/autonomous-builder/build_batch.py "$BATCH"
