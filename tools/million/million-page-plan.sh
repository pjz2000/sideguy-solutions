#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo "== Building million-page reserve manifests =="
bash tools/million/build-million-manifests.sh

echo ""
echo "== Counting total page space =="
bash tools/million/count-million-space.sh

echo ""
echo "== Building top hub pages from the screenshot themes =="
bash tools/million/build-million-hub-pages.sh

echo ""
echo "== Building small sample pages =="
bash tools/million/build-million-sample-pages.sh 100

echo ""
echo "Done."
echo "Next step: selectively wire sitemap/index ingestion instead of mass publishing everything."
