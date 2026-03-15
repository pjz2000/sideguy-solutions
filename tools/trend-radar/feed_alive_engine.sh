#!/usr/bin/env bash
PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 0

TREND_FILE="docs/trend-signals/trend-signals.tsv"
ALIVE_INBOX="docs/alive/inbox/trend-signals.txt"

[ -f "$TREND_FILE" ] || exit 0

cut -f2 "$TREND_FILE" >> "$ALIVE_INBOX"

echo "Trend signals fed into Alive Engine inbox"
