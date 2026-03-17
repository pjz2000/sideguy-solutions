#!/bin/bash

echo "Boosting CTAs..."

FILES=$(find . -name "*.html")

for file in $FILES
do

sed -i "/<\/body>/i \
<div style=\"position:fixed;bottom:20px;right:20px;background:#00ffcc;padding:14px 18px;border-radius:30px;font-weight:bold;\">\
📱 Text PJ\
</div>" "$file"

done

echo "CTA boost complete."
