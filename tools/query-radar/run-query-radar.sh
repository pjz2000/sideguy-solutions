#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

INDEX="$ROOT/docs/index/page-metadata.tsv"
OUTPUT="$ROOT/docs/radar/query-opportunities.txt"

echo "Running SideGuy Query Radar..."

STOPS="^(for|the|and|with|san|diego|in|a|to|my|i|is|do|on|of|or|at|it|be|if|no|we|us|so|as|an|by|up|how|who|why|are|was|not|can|get|has|but|our|your|this|that|from|what|will|does|did|have|into|been|you|they|their|its|also|any|all|one|two|three|when|where|which|just|more|than|then|there|would|about|after|before|else|out|go|am|much|both|each|him|her|his|she|he|me|may|let|per|via|new|old|big|top|best|good|bad|now|yet|too|very|many|some|few|most|last|next|same|own|back|over|re|non|pre|mid|off|down|un|ex|anyone|keeps|using|really|should|sure|losing|fake|constantly|brain|saying|quit|year|keep|says|los|angeles|austin|portland|phoenix|miami|denver|dallas|chicago|seattle|ever|still|never|always|already|even|say|tell|ask|know|think|feel|want|need|make|take|give|see|look|come|going|been|done|getting|saying|trying|looking|putting|taking|making|breaking|leaving|trying|working|running|building|handling|paying)$"

tail -n +2 "$INDEX" | awk -F'\t' '{print $1}' | \
sed 's/\.html//' | tr '-' '\n' | \
grep -vE "$STOPS" | \
grep -E '^[a-z]{3,}$' | \
sort | uniq -c | sort -rn | head -50 > /tmp/top-terms.txt

echo "" > "$OUTPUT"

while read count term
do
echo "ai-$term-for-small-business.html" >> "$OUTPUT"
echo "automation-$term-tools.html" >> "$OUTPUT"
echo "future-$term-systems.html" >> "$OUTPUT"
echo "$term-software-platforms.html" >> "$OUTPUT"
done < /tmp/top-terms.txt

echo "Query radar output:"
echo "$OUTPUT"

wc -l "$OUTPUT"

