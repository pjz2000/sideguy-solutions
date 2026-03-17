#!/bin/bash

echo "Running SideGuy Cluster Radar"

IDEAS="docs/radar/cluster-ideas.txt"
MANIFEST="manifests/factory/radar-manifest-$(date +%s).csv"

echo "Cluster Radar Scan $(date)" > $IDEAS
echo "" >> $IDEAS

echo "page_type,slug,title,parent,category,intent" > $MANIFEST

# Extract keywords from filenames
KEYWORDS=$(find . -name "*.html" \
 | sed 's#.*/##' \
 | sed 's/.html//' \
 | tr '-' '\n' \
 | tr '[:upper:]' '[:lower:]' \
 | sort | uniq -c | sort -rn | head -30 | awk '{print $2}')

echo "Top detected keywords:" >> $IDEAS
echo "$KEYWORDS" >> $IDEAS
echo "" >> $IDEAS

# Generate cluster ideas
for topic in $KEYWORDS
do

if [[ ${#topic} -gt 4 ]]; then

echo "Suggested cluster: $topic" >> $IDEAS

echo "guide,$topic-guide,$topic Guide,root,technology,info" >> $MANIFEST
echo "faq,$topic-faq,$topic FAQ,$topic,technology,faq" >> $MANIFEST
echo "cost,$topic-cost,$topic Cost,$topic,technology,pricing" >> $MANIFEST
echo "comparison,$topic-vs-alternatives,$topic Alternatives,$topic,technology,comparison" >> $MANIFEST
echo "future,future-of-$topic,Future of $topic,$topic,technology,future" >> $MANIFEST

echo "" >> $IDEAS

fi

done

echo ""
echo "Cluster ideas saved to:"
echo $IDEAS

echo ""
echo "Factory manifest created:"
echo $MANIFEST

echo ""
echo "To build clusters run:"
echo "bash tools/factory/page-factory.sh $MANIFEST"
