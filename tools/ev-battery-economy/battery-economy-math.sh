#!/usr/bin/env bash

EVS="${1:-80000000}"
BATTERIES_PER_EV=1

SECOND_LIFE=$((EVS * BATTERIES_PER_EV))

echo ""
echo "Second-Life Battery Market"
echo "--------------------------"

echo "EVs in circulation: $EVS"
echo "Potential second-life batteries: $SECOND_LIFE"

echo ""
echo "Each battery becomes future energy storage."
