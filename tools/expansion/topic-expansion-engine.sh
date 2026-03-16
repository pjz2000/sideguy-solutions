#!/bin/bash

SEEDS="data/topic-seeds/service-topics.txt"
OUTDIR="pages/expansion"
SITEMAP="sitemap.xml"
LOG="logs/expansion/expansion.log"

echo "Expansion run $(date)" >> $LOG

while read topic
do

slug=$(echo $topic | tr ' ' '-')

pages=(
"$slug-cost-guide"
"$slug-repair-vs-replace"
"$slug-warning-signs"
"$slug-checklist"
"$slug-common-mistakes"
"$slug-questions-to-ask"
"$slug-scam-red-flags"
"$slug-inspection-cost"
"$slug-upgrade-options"
"$slug-future-tech"
)

for p in "${pages[@]}"
do

FILE="$OUTDIR/$p.html"

cat > "$FILE" <<HTML
<!DOCTYPE html>
<html>
<head>
<title>${p//-/ } | SideGuy</title>
<meta name="description" content="Learn about $topic including costs, warning signs, and decision checklists.">
<link rel="canonical" href="https://sideguysolutions.com/expansion/$p.html">
</head>

<body>

<h1>${p//-/ }</h1>

<p>
This guide explains important things to understand about $topic including common mistakes, warning signs, and what to check before making decisions.
</p>

<h2>Why This Matters</h2>

<p>
Many homeowners and business operators make expensive mistakes when dealing with $topic. Understanding the basics helps avoid unnecessary costs.
</p>

<h2>Checklist</h2>

<ul>
<li>Research typical pricing</li>
<li>Get multiple quotes</li>
<li>Understand scope of work</li>
<li>Verify contractor credentials</li>
</ul>

<p>
Need a second opinion? Text PJ at <strong>773-544-1231</strong>.
</p>

</body>
</html>
HTML

echo "$p built" >> $LOG

if [ -f "$SITEMAP" ]; then
sed -i "/<\/urlset>/i \
<url><loc>https://sideguysolutions.com/expansion/$p.html</loc></url>" "$SITEMAP"
fi

done

done < "$SEEDS"

echo "Expansion complete" >> $LOG

echo "Pages generated."
