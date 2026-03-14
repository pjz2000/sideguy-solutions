#!/usr/bin/env bash
# Delegates to Python builder (handles quoted CSV correctly)

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

python3 tools/million/build-wave-pages.py
exit $?

SELECTION="docs/million-page/selected/wave-selection.csv"
[ -f "$SELECTION" ] || { echo "No wave-selection.csv found. Run select-wave-pages.sh first."; exit 1; }

mkdir -p public public/auto
BUILT=0

tail -n +2 "$SELECTION" | while IFS=, read -r url title h1 theme audience use_case industry city state modifier page_type intent score; do
  CLEAN_URL="$(echo "$url"         | tr -d '"')"
  CLEAN_TITLE="$(echo "$title"     | sed 's/^"//;s/"$//')"
  CLEAN_H1="$(echo "$h1"           | sed 's/^"//;s/"$//')"
  CLEAN_THEME="$(echo "$theme"     | sed 's/^"//;s/"$//')"
  CLEAN_AUDIENCE="$(echo "$audience" | sed 's/^"//;s/"$//')"
  CLEAN_USE_CASE="$(echo "$use_case" | sed 's/^"//;s/"$//')"
  CLEAN_INDUSTRY="$(echo "$industry" | sed 's/^"//;s/"$//')"
  CLEAN_CITY="$(echo "$city"       | sed 's/^"//;s/"$//')"
  CLEAN_STATE="$(echo "$state"     | sed 's/^"//;s/"$//')"
  CLEAN_MODIFIER="$(echo "$modifier" | sed 's/^"//;s/"$//')"
  CLEAN_PAGE_TYPE="$(echo "$page_type" | sed 's/^"//;s/"$//')"
  CLEAN_INTENT="$(echo "$intent"   | sed 's/^"//;s/"$//')"
  CLEAN_SCORE="$(echo "$score"     | sed 's/^"//;s/"$//')"

  FILE_PATH="public${CLEAN_URL}"
  mkdir -p "$(dirname "$FILE_PATH")"

  cat > "$FILE_PATH" <<HTML
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>${CLEAN_TITLE}</title>
  <meta name="description" content="${CLEAN_H1}. Human-first clarity from SideGuy Solutions.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com${CLEAN_URL}">
  <meta name="robots" content="index,follow">
</head>
<body>
  <main style="max-width:940px;margin:0 auto;padding:40px 20px;font-family:-apple-system,system-ui,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>${CLEAN_H1}</h1>
    <p>SideGuy is where Google discovers the problem, AI explains it, and a real human resolves it.</p>

    <h2>What this page covers</h2>
    <p>This page focuses on <strong>${CLEAN_THEME}</strong> for <strong>${CLEAN_INDUSTRY}</strong> in <strong>${CLEAN_CITY}, ${CLEAN_STATE}</strong>, with emphasis on <strong>${CLEAN_PAGE_TYPE}</strong> and <strong>${CLEAN_USE_CASE}</strong>.</p>

    <h2>Why people search this</h2>
    <p>Usually they want clarity on whether the technology is useful, what it costs, how implementation works, what risks matter, and whether it fits their business or workflow.</p>

    <h2>Audience</h2>
    <p>${CLEAN_AUDIENCE}</p>

    <h2>Use case</h2>
    <p>${CLEAN_USE_CASE}</p>

    <h2>Industry angle</h2>
    <p>${CLEAN_INDUSTRY} teams often need practical explanations instead of hype. SideGuy keeps the tone calm, direct, and implementation-aware.</p>

    <h2>Local angle</h2>
    <p>Businesses in ${CLEAN_CITY}, ${CLEAN_STATE} often need help evaluating new systems without getting lost in vendor noise.</p>

    <h2>Search modifier</h2>
    <p>${CLEAN_MODIFIER}</p>

    <h2>FAQ</h2>
    <p><strong>What is this really about?</strong><br>This page helps explain the real-world use of ${CLEAN_THEME}.</p>
    <p><strong>Who is this for?</strong><br>${CLEAN_AUDIENCE}</p>
    <p><strong>What does SideGuy do?</strong><br>Clarity before cost. Calm explanation first, then human help if needed.</p>

    <h2>Related Pages</h2>
    <ul>
      <li><a href="/ai-agents-answer-engine-traffic.html">AI Agents &amp; Answer Engine Traffic</a></li>
      <li><a href="/machine-to-machine-payments.html">Machine-to-Machine Payments</a></li>
      <li><a href="/solana-payments.html">Solana Payments</a></li>
      <li><a href="/usdc-merchant-payments.html">USDC Merchant Payments</a></li>
    </ul>

    <div style="margin-top:48px;padding:22px;border:1px solid #ddd;border-radius:20px;">
      <strong>Text PJ</strong>
      <p>Need a real human to help you sort through the noise?</p>
      <p><a href="sms:+17735441231">Text PJ: 773-544-1231</a></p>
    </div>
  </main>
</body>
</html>
HTML

  echo "Built $FILE_PATH"
done

echo "Done building wave pages."
