#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

echo "== Phase 2 :: building state packs =="
bash tools/million/build-state-packs.sh

echo ""
echo "== Phase 2 :: scoring reserve pages =="
bash tools/million/score-million-pages.sh

echo ""
echo "== Phase 2 :: deduping reserve pages =="
bash tools/million/dedupe-million-pages.sh

echo ""
echo "== Phase 2 :: selecting controlled publish wave =="
bash tools/million/select-wave-pages.sh

echo ""
echo "== Phase 2 :: building selected wave pages =="
bash tools/million/build-wave-pages.sh

echo ""
echo "== Phase 2 :: building category sitemaps =="
bash tools/million/build-category-sitemaps.sh

echo ""
echo "== Phase 2 :: building sitemap index =="
bash tools/million/build-sitemap-index.sh

echo ""
echo "== Phase 2 :: appending links to homepage =="
bash tools/million/append-wave-to-index.sh

echo ""
echo "== Phase 2 :: logging summary =="
bash tools/million/log-wave-summary.sh

echo ""
echo "Done."
echo "Main outputs:"
echo "  docs/million-page/state-packs/"
echo "  docs/million-page/scored/"
echo "  docs/million-page/scored-deduped/"
echo "  docs/million-page/selected/wave-selection.csv"
echo "  public/sitemaps/*.xml"
echo "  public/sitemaps/sitemap-million-index.xml"
