#!/bin/bash

SIGNALS="${1:-20}"
MODIFIERS="${2:-12}"

TOTAL=$((SIGNALS * MODIFIERS))

echo ""
echo "SideGuy Future Math"
echo "--------------------"
echo "Signals: $SIGNALS"
echo "Modifiers per signal: $MODIFIERS"
echo ""
echo "Future topic pages: $TOTAL"
echo ""
