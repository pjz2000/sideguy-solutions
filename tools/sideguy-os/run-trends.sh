#!/usr/bin/env bash
PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

bash tools/trend-radar/run_trend_pipeline.sh
