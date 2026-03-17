#!/bin/bash

echo "================================="
echo "SIDEGUY MONETIZATION LOOP"
echo "================================="

echo "1. Find money pages"
bash tools/monetization/money-page-detector.sh

echo ""
echo "2. Inject decision blocks"
bash tools/monetization/decision-injector.sh

echo ""
echo "3. Boost CTAs"
bash tools/monetization/cta-booster.sh

echo ""
echo "Monetization layer complete."
