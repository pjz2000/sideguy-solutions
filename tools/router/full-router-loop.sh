#!/bin/bash

echo "================================="
echo "SIDEGUY ROUTER LOOP"
echo "================================="

echo "1. Intake"
bash tools/router/intake.sh

echo ""
echo "2. Classify"
bash tools/router/classifier.sh

echo ""
echo "3. Route"
bash tools/router/router.sh

echo ""
echo "4. Dashboard"
bash tools/router/dashboard.sh

echo ""
echo "5. Value"
bash tools/router/value-estimator.sh

echo ""
echo "Routing cycle complete."
