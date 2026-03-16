#!/usr/bin/env bash

VERTICAL="${1:-payments}"
HUB="${2:-machine-to-machine-payments}"
CITY="${3:-san-diego}"

OUT="manifests/plans/${VERTICAL}-${HUB}-plan.csv"

mkdir -p manifests/plans

cat > "$OUT" <<EOF2
page_type,slug,title,parent_hub,vertical,locality,intent,notes
hub,$HUB,$HUB,$HUB.html,$VERTICAL,global,authority,manual hub
problem,what-is-$VERTICAL,What is $VERTICAL,$HUB.html,$VERTICAL,global,long-tail,definition page
problem,how-does-$VERTICAL-work,How $VERTICAL Works,$HUB.html,$VERTICAL,global,long-tail,explanation
comparison,$VERTICAL-vs-traditional,$VERTICAL vs traditional,$HUB.html,$VERTICAL,global,decision,comparison
local,$VERTICAL-$CITY,$VERTICAL in $CITY,$HUB.html,$VERTICAL,$CITY,local,local intent
EOF2

echo "Cluster plan created:"
echo "$OUT"
