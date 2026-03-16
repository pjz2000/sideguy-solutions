#!/bin/bash

AGENTS="${1:-1000000}"
PURCHASES_PER_AGENT="${2:-5}"

TOTAL=$((AGENTS * PURCHASES_PER_AGENT))

echo ""
echo "Autonomous Agent Economy Math"
echo "-----------------------------"
echo "Agents: $AGENTS"
echo "Purchases per agent: $PURCHASES_PER_AGENT"
echo ""
echo "Potential machine transactions: $TOTAL"
echo ""
