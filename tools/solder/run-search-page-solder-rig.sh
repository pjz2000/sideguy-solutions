#!/bin/bash

echo "🪛 SIDEGUY SEARCH → PAGE SOLDER RIG"
echo "==================================="

STAMP=$(date +"%Y-%m-%d_%H-%M-%S")
MAP="data/solder/search-page-map-$STAMP.tsv"
LOG="logs/search-solder-$STAMP.log"

echo -e "query\turl\tcluster\tconfidence\tnext_action" > "$MAP"

# seed known strong routing examples
echo -e "hvac repair vs replace\thvac-repair-vs-replace.html\thvac\t0.96\tspawn-cost-guide" >> "$MAP"
echo -e "san diego payment processing fees\tsolana-payments-san-diego.html\tpayments\t0.94\tspawn-toast-vs-stripe" >> "$MAP"
echo -e "who do i call airport terminal help\twho-do-i-call-airport-help.html\ttravel\t0.91\tspawn-airline-pages" >> "$MAP"
echo -e "north county ai automation help\tnorth-county-verified-operator-hub.html\tlocal-ai\t0.95\tspawn-industry-pages" >> "$MAP"
echo -e "mini split worth it san diego\tmini-split-san-diego.html\tenergy\t0.93\tspawn-cost-calculator" >> "$MAP"

echo "[$(date)] solder map created: $MAP" | tee "$LOG"

cat > docs/solder/search-page-soldering.md <<DOC
# Search → Page Soldering

Purpose:
- permanently stitch search demand to best destination pages
- reduce orphan intent
- improve crawl relevance
- create deterministic child spawn routes
- compound winners instead of creating noise

Flow:
search signal
→ best page
→ stronger intro / faq / local block
→ cluster child spawn
→ crawl reinforcement
DOC

echo ""
echo "✅ solder rig complete"
echo "📍 map file: $MAP"
echo "🧠 next step: auto route GSC winners into this map"
