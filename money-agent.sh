#!/usr/bin/env bash

########################################
# SIDEGUY MONEY AGENT v1
# Injects conversion-focused CTA blocks
# on money-intent queries
########################################

INPUT="docs/gsc/query-pages.csv"
LOG="docs/money/money-log.txt"

mkdir -p "docs/money"

echo "---------------------------------------"
echo "💰 MONEY AGENT"
echo "---------------------------------------"

normalize() {
  url="$1"
  url="${url#https://www.sideguysolutions.com/}"
  url="${url%%\?*}"
  url="${url%%\#*}"
  [[ "$url" != *.html ]] && url="$url.html"
  [ -z "$url" ] && url="index.html"
  echo "$url"
}

is_money_query() {
  q=$(echo "$1" | tr '[:upper:]' '[:lower:]')

  if [[ "$q" =~ cost|price|quote|install|repair|near|who|best ]]; then
    return 0
  else
    return 1
  fi
}

########################################
# MONEY BLOCK
########################################

build_money_block() {
cat <<EOF
<section data-sg-money="v1" style="background:#eafff3;padding:18px;border-radius:14px;margin:20px 0;">
<h2>💰 Get a Real Answer Fast</h2>
<p>At this point, most people just want a clear number and the right next step.</p>

<ul>
<li>✔ Quick estimate based on your situation</li>
<li>✔ Who to call (and who to avoid)</li>
<li>✔ What actually matters vs upsells</li>
</ul>

<p><strong>Text PJ → 773-544-1231</strong></p>
</section>
EOF
}

########################################
# PROCESS
########################################

tail -n +2 "$INPUT" | while IFS=, read -r page query clicks impressions ctr position; do

FILE=$(normalize "$page")
[ ! -f "$FILE" ] && continue

is_money_query "$query" || continue

grep -q "data-sg-money" "$FILE" && continue

BLOCK="docs/money/block.html"
build_money_block > "$BLOCK"

awk -v block="$(cat $BLOCK)" '
BEGIN{added=0}
{
print $0
if(!added && $0 ~ /<h1/){
print block
added=1
}
}' "$FILE" > "$FILE.tmp" && mv "$FILE.tmp" "$FILE"

echo "MONEY|$FILE|$query" >> "$LOG"

done

echo "✅ Money blocks injected"
