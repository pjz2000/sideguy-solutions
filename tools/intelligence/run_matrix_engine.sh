#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo ""
echo "SIDEGUY MATRIX COMMAND CENTER"
echo "================================"
echo ""
echo "1) Generate full slug matrix"
echo "2) Build page batch from queue"
echo "3) Show queue stats"
echo ""
read -rp "Select (1/2/3): " CHOICE

case "$CHOICE" in
  1)
    bash tools/intelligence/hyper-matrix-engine.sh
    ;;
  2)
    read -rp "How many pages to build? " NUM
    bash tools/page-builder/build_batch.sh "$NUM"
    ;;
  3)
    if [ -f data/matrix-queue/all-slugs.txt ]; then
      TOTAL=$(wc -l < data/matrix-queue/all-slugs.txt)
      BUILT=$(ls public/*.html 2>/dev/null | wc -l)
      echo ""
      echo "Queue:  $TOTAL slugs"
      echo "Built:  $BUILT pages in public/"
      echo ""
    else
      echo "No queue found. Run option 1 first."
    fi
    ;;
  *)
    echo "Invalid option."
    ;;
esac
