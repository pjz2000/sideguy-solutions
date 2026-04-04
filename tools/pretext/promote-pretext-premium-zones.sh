#!/bin/bash
echo "⚡🌊 SIDEGUY PRETEXT PREMIUM ZONES"
echo "================================="

STAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG="logs/pretext-premium-$(date +%Y%m%d-%H%M%S).log"

cat > docs/pretext/premium-zones-v3.md <<DOC
# Pretext Premium Zones v3
Last Updated: $STAMP

Promote @chenglou/pretext as the default typography engine for:

1. Homepage Hero
2. Text PJ Orbital Trust
3. Decision Confidence Cards
4. Intent Meme Truth Strips
5. Johnny 5 Curiosity Bot Input Ring

Claude rules:
- use prepareWithSegments once
- rerun layoutWithLines on resize only
- keep semantic DOM text
- prioritize mobile wow factor
- text must feel spatial, orbital, and cinematic
- avoid old boxed paragraph feel
DOC

echo "✅ premium typography zones promoted" | tee "$LOG"
