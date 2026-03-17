#!/bin/bash

echo "================================="
echo "SIDEGUY AUTO RESPONDER LOOP"
echo "================================="

echo "1. Capture message"
bash tools/responder/inbox.sh

echo ""
echo "2. Classify"
bash tools/responder/classify.sh

echo ""
echo "3. Respond"
bash tools/responder/respond.sh

echo ""
echo "Response output:"
cat logs/responder/outbox.txt

echo ""
echo "Done."
