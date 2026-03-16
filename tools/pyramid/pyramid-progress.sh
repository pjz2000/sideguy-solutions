#!/usr/bin/env bash

PROBLEMS=$(wc -l < manifests/pyramid/problem-layer.txt)
SYSTEMS=$(wc -l < manifests/pyramid/system-layer.txt)
RESOLUTIONS=$(wc -l < manifests/pyramid/resolution-layer.txt)

TOTAL=$((PROBLEMS + SYSTEMS + RESOLUTIONS))

echo ""
echo "SideGuy Clarity Pyramid Status"
echo "--------------------------------"

echo "Problem nodes: $PROBLEMS"
echo "System nodes: $SYSTEMS"
echo "Resolution nodes: $RESOLUTIONS"
echo ""

echo "Total nodes: $TOTAL"
echo ""

echo "Architecture:"
echo "Problems → Systems → Human Decisions"
echo ""
