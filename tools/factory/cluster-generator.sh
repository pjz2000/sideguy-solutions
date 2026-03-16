#!/bin/bash

TOPIC="$1"

if [ -z "$TOPIC" ]; then
  echo "Usage: bash tools/factory/cluster-generator.sh topic-name"
  echo "Example: bash tools/factory/cluster-generator.sh machine-payments"
  exit 1
fi

OUTPUT="manifests/factory/cluster-$TOPIC-$(date +%s).csv"
mkdir -p manifests/factory

echo "page_type,slug,title,parent,category,intent" > "$OUTPUT"
echo "guide,$TOPIC,$TOPIC Guide,root,technology,info"                     >> "$OUTPUT"
echo "faq,$TOPIC-faq,$TOPIC FAQ,$TOPIC,technology,faq"                   >> "$OUTPUT"
echo "cost,$TOPIC-cost,$TOPIC Cost,$TOPIC,technology,pricing"            >> "$OUTPUT"
echo "comparison,$TOPIC-vs-alternatives,$TOPIC Alternatives,$TOPIC,technology,comparison" >> "$OUTPUT"
echo "future,future-of-$TOPIC,Future of $TOPIC,$TOPIC,technology,future" >> "$OUTPUT"
echo "problems,$TOPIC-problems,$TOPIC Problems,$TOPIC,technology,troubleshooting" >> "$OUTPUT"
echo "tools,$TOPIC-tools,$TOPIC Tools,$TOPIC,technology,tools"           >> "$OUTPUT"
echo "automation,$TOPIC-automation,$TOPIC Automation,$TOPIC,technology,automation" >> "$OUTPUT"

echo ""
echo "Cluster manifest created: $OUTPUT"
echo "Rows: 8"
echo ""
echo "Next step:"
echo "bash tools/factory/page-factory.sh $OUTPUT"
