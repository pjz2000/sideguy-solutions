#!/bin/bash

echo "⚡ SIDEGUY WINNER UPGRADE MACHINE"
echo "================================"

TS=$(date +"%Y-%m-%d %H:%M:%S")
LOG="logs/winner-upgrade-$(date +%Y%m%d-%H%M%S).log"

echo "[$TS] starting winner loop" | tee -a "$LOG"

COUNT=0

find . -maxdepth 1 -name "*.html" | while read FILE; do
  if grep -q "FAQPage" "$FILE"; then
    if ! grep -q "Winner Upgrade Stamp" "$FILE"; then
      perl -0pi -e 's#</body>#<section style="padding:40px 20px;max-width:900px;margin:auto;"><h2>Why this page keeps getting stronger</h2><p>Every useful question visitors ask helps this page become clearer, more local, and more actionable over time.</p><p><strong>Winner Upgrade Stamp:</strong> machine-refined for crawl velocity, clarity, and trust.</p></section></body>#s' "$FILE"
        echo "UPGRADED $FILE" | tee -a "$LOG"
        COUNT=$((COUNT+1))
    fi
  fi
done

echo ""
echo "✅ Winner loop complete"
echo "📈 upgraded pages: $COUNT" | tee -a "$LOG"

cat > docs/machine/winner-loop.md <<DOC
# Winner Upgrade Loop

Last Run: $TS

Purpose:
- strengthen already-crawled pages
- improve clarity and CTR
- compound trust on impression winners
- prep pages for next crawl cycle
DOC

echo "🧠 machine docs updated"
