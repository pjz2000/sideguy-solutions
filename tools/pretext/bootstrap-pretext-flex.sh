#!/bin/bash

echo "🌊⚡ SIDEGUY PRETEXT FLEX INTEGRATION"
echo "===================================="

STAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG="logs/pretext-flex-$(date +%Y%m%d-%H%M%S).log"

echo "[$STAMP] bootstrapping pretext integration" | tee -a "$LOG"

# install dependency for Claude / repo terminal
npm install @chenglou/pretext

cat > assets/js/pretext-gravity.js <<'JS'
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

export function flowTextAroundOrb(selector, width = 720, lineHeight = 30) {
  const el = document.querySelector(selector)
  if (!el) return

  const text = el.innerText.trim()
  const prepared = prepareWithSegments(text, '28px Inter')

  const { lines } = layoutWithLines(prepared, width, lineHeight)

  el.innerHTML = lines.map((line, i) => {
    const indent = i % 3 === 0 ? 48 : 0
    return `<div style="padding-left:${indent}px">${line.text}</div>`
  }).join('')
}
JS

cat > docs/pretext/pretext-flex-doctrine.md <<DOC
# SideGuy Pretext Flex Doctrine
Last Updated: $STAMP

Library:
@chenglou/pretext

Use Cases:
- cinematic hero text gravity
- memes wrapping around glow orbs
- score layers with adaptive line shaping
- curiosity bot radial input rings
- local trust names flowing around landmarks
- zero reflow measurement for premium typography

Claude Instructions:
1. Import assets/js/pretext-gravity.js on homepage and AI pages
2. Apply flowTextAroundOrb() to hero H1, meme truth stings, and score blocks
3. Preserve real DOM text for SEO and accessibility
4. Prefer prepare once + layout on resize only
DOC

echo "✅ pretext flex bootstrapped"
