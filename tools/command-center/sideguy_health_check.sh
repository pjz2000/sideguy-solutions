#!/bin/bash


echo ""
echo "====================================="
echo "SideGuy Command Center Diagnostics"
echo "====================================="
echo ""

echo "Workspace:"
pwd
echo ""

echo "---- PUBLIC SITE STATUS ----"

PAGE_COUNT=$(find public -name "*.html" 2>/dev/null | wc -l)

echo "Total HTML pages:"
echo $PAGE_COUNT
echo ""

echo "Sample pages:"
find public -name "*.html" | head -10
echo ""

echo "---- SITEMAP STATUS ----"

if [ -f public/sitemap.xml ]; then
    URL_COUNT=$(grep -o "<loc>" public/sitemap.xml | wc -l)
    echo "URLs in sitemap:"
    echo $URL_COUNT
else
    echo "No sitemap found"
fi

echo ""
echo "---- TREND SIGNAL QUEUE ----"

if [ -f docs/problem-radar/radar-signals.tsv ]; then
    SIGNAL_COUNT=$(wc -l < docs/problem-radar/radar-signals.tsv)
    echo "Radar signals queued:"
    echo $SIGNAL_COUNT
else
    echo "No radar signals file found"
fi

echo ""
echo "---- TRENDING TOPIC QUEUE ----"

if [ -f docs/trending-topics/topics_queue.txt ]; then
    TOPIC_COUNT=$(wc -l < docs/trending-topics/topics_queue.txt)
    echo "Trending topics queued:"
    echo $TOPIC_COUNT
else
    echo "No trending topic queue found"
fi

echo ""
echo "---- CLUSTER STATUS ----"

CLUSTER_FILES=$(find docs -name "*cluster*" 2>/dev/null | wc -l)

echo "Cluster-related files:"
echo $CLUSTER_FILES

echo ""
echo "---- MEME ENGINE ----"

MEME_FILES=$(grep -R "meme" tools 2>/dev/null | wc -l)

echo "Meme references in tools:"
echo $MEME_FILES

echo ""
echo "---- GIT STATUS ----"

git status --short

echo ""
echo "---- RECENT COMMITS ----"

git log --oneline -5

echo ""
echo "====================================="
echo "Diagnostics Complete"
echo "====================================="
echo ""