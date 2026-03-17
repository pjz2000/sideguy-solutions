#!/bin/bash

echo "================================="
echo "SIDEGUY FULL LOOP"
echo "================================="

echo "1. Priority scan"
bash tools/intelligence/priority-engine.sh

echo "2. Self improve"
bash tools/intelligence/self-improver.sh

echo "3. Auto link"
bash tools/link-engine/auto-link-injector.sh

echo "4. Gravity scan"
bash tools/gravity/gravity-engine.sh

echo ""
echo "Loop complete"
