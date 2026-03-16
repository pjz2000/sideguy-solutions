#!/bin/bash

echo "Running SideGuy Trend Radar"

REPORT="docs/radar/trend-report.txt"
MANIFEST="manifests/factory/trend-manifest-$(date +%s).csv"

echo "SideGuy Trend Radar $(date)" > "$REPORT"
echo "" >> "$REPORT"

echo "page_type,slug,title,parent,category,intent" > "$MANIFEST"

TRENDS=(
  "ai-agents"
  "robotics-production"
  "autonomous-energy"
  "home-battery-systems"
  "machine-to-machine-payments"
  "stablecoin-commerce"
  "solana-business-payments"
  "crypto-payroll"
  "robotic-manufacturing"
  "distributed-energy-grid"
  "ai-customer-service-agents"
  "business-ai-automation"
  "robot-kitchens"
  "ai-repair-diagnostics"
  "self-driving-delivery"
  "energy-storage-business"
)

for trend in "${TRENDS[@]}"; do
  echo "Trend detected: $trend" >> "$REPORT"

  echo "guide,$trend-guide,$trend Guide,root,technology,info"                        >> "$MANIFEST"
  echo "faq,$trend-faq,$trend FAQ,$trend,technology,faq"                             >> "$MANIFEST"
  echo "cost,$trend-cost,$trend Cost,$trend,technology,pricing"                      >> "$MANIFEST"
  echo "comparison,$trend-vs-alternatives,$trend Alternatives,$trend,technology,comparison" >> "$MANIFEST"
  echo "future,future-of-$trend,Future of $trend,$trend,technology,future"           >> "$MANIFEST"

  echo "" >> "$REPORT"
done

ROWS=$(( ${#TRENDS[@]} * 5 ))

echo "" >> "$REPORT"
echo "Trends scanned: ${#TRENDS[@]}" >> "$REPORT"
echo "Manifest rows:  $ROWS" >> "$REPORT"
echo "Manifest:       $MANIFEST" >> "$REPORT"

echo ""
echo "Trend radar report:       $REPORT"
echo "Cluster manifest:         $MANIFEST"
echo "Trends detected:          ${#TRENDS[@]}"
echo "Pages queued:             $ROWS"
echo ""
echo "To build pages run:"
echo "bash tools/factory/page-factory.sh $MANIFEST"
