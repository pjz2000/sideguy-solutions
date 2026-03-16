#!/bin/bash

TOPICS="${1:-20}"
PAGES_PER_TOPIC="${2:-5}"

TOTAL=$((TOPICS * PAGES_PER_TOPIC))

echo ""
echo "Trend Radar Expansion Math"
echo "--------------------------"
echo "Topics detected: $TOPICS"
echo "Pages per topic: $PAGES_PER_TOPIC"
echo ""
echo "Potential pages: $TOTAL"
echo ""
