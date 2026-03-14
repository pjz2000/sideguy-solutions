#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p public/auto
SAMPLE_SIZE="${1:-250}"

find docs/million-page/manifests -name "*.csv" | while read -r manifest; do
  tail -n +2 "$manifest" | head -n "$SAMPLE_SIZE" | while IFS=, read -r url title h1 theme audience use_case industry city state modifier page_type intent; do
    CLEAN_URL="$(echo "$url" | tr -d '"')"
    FILE_PATH="public${CLEAN_URL}"

    mkdir -p "$(dirname "$FILE_PATH")"

    CLEAN_TITLE="$(echo "$title" | sed 's/^"//; s/"$//')"
    CLEAN_H1="$(echo "$h1" | sed 's/^"//; s/"$//')"
    CLEAN_THEME="$(echo "$theme" | sed 's/^"//; s/"$//')"
    CLEAN_AUDIENCE="$(echo "$audience" | sed 's/^"//; s/"$//')"
    CLEAN_USE_CASE="$(echo "$use_case" | sed 's/^"//; s/"$//')"
    CLEAN_INDUSTRY="$(echo "$industry" | sed 's/^"//; s/"$//')"
    CLEAN_CITY="$(echo "$city" | sed 's/^"//; s/"$//')"
    CLEAN_STATE="$(echo "$state" | sed 's/^"//; s/"$//')"
    CLEAN_MODIFIER="$(echo "$modifier" | sed 's/^"//; s/"$//')"
    CLEAN_PAGE_TYPE="$(echo "$page_type" | sed 's/^"//; s/"$//')"
    CLEAN_INTENT="$(echo "$intent" | sed 's/^"//; s/"$//')"

    cat > "$FILE_PATH" <<HTML
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>${CLEAN_TITLE}</title>
  <meta name="description" content="${CLEAN_H1}. Human-first explanation from SideGuy Solutions.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com${CLEAN_URL}">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <p><strong>Build:</strong> Million Page Reserve Sample</p>
    <h1>${CLEAN_H1}</h1>
    <p>SideGuy is where Google discovers the problem, AI explains it, and a real human resolves it.</p>

    <h2>Why this page exists</h2>
    <p>This page is part of the SideGuy million-page reserve architecture. It focuses on <strong>${CLEAN_THEME}</strong> for <strong>${CLEAN_INDUSTRY}</strong> in <strong>${CLEAN_CITY}, ${CLEAN_STATE}</strong>.</p>

    <h2>Audience</h2>
    <p>${CLEAN_AUDIENCE}</p>

    <h2>Use case</h2>
    <p>${CLEAN_USE_CASE}</p>

    <h2>Search intent</h2>
    <p>${CLEAN_INTENT}</p>

    <h2>Local relevance</h2>
    <p>Businesses in ${CLEAN_CITY}, ${CLEAN_STATE} searching for ${CLEAN_THEME} often want clarity around implementation, pricing, security, and whether the technology actually solves a real business problem.</p>

    <h2>SideGuy angle</h2>
    <p>Clarity before cost. Calm explanation first. Then implementation help if needed.</p>

    <h2>Related themes</h2>
    <ul>
      <li><a href="/machine-to-machine-payments.html">Machine-to-Machine Payments</a></li>
      <li><a href="/ai-automation.html">AI Automation</a></li>
      <li><a href="/solana-payments.html">Solana Payments</a></li>
      <li><a href="/usdc-merchant-payments.html">USDC Merchant Payments</a></li>
    </ul>

    <div style="margin-top:48px;padding:20px;border:1px solid #ddd;border-radius:18px;">
      <strong>Text PJ</strong>
      <p>Real human help when you want clarity on technology, payments, automation, or implementation.</p>
      <p><a href="sms:+17735441231">Text PJ: 773-544-1231</a></p>
    </div>
  </main>
</body>
</html>
HTML

  done
done
