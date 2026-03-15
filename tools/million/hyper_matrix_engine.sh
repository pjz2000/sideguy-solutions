#!/usr/bin/env bash
TOPICS=(ai-automation hvac-repair plumbing-problems workflow-automation solana-payments)
MODIFIERS=(guide faq pricing troubleshooting benefits risks examples)
LOCATIONS=(san-diego los-angeles phoenix austin miami chicago)
INDUSTRIES=(restaurants contractors real-estate logistics ecommerce)
COUNT=0
for t in "${TOPICS[@]}"; do
for m in "${MODIFIERS[@]}"; do
for l in "${LOCATIONS[@]}"; do
for i in "${INDUSTRIES[@]}"; do
slug="$t-$m-$l-$i"
echo "$slug"
COUNT=$((COUNT+1))
done
done
done
done
echo ""
echo "Total pages generated: $COUNT"
