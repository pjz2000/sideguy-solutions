#!/bin/bash

REL_FILE="manifests/wiki-graph/relationships.csv"

echo ""
echo "SideGuy Orphan Page Detector"
echo "----------------------------"

cut -d',' -f1 "$REL_FILE" | sort | uniq > /tmp/source_pages.txt
cut -d',' -f2 "$REL_FILE" | sort | uniq > /tmp/target_pages.txt

echo "Pages that link out:"
wc -l /tmp/source_pages.txt

echo "Pages that receive links:"
wc -l /tmp/target_pages.txt

echo ""
echo "If counts diverge heavily, some pages may be orphaned."
