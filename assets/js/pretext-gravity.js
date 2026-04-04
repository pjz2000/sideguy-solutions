import { prepareWithSegments, layoutWithLines } from './vendor/pretext-layout.js'

/**
 * flowTextAroundOrb
 * Flows text using canvas-measured layout — no DOM reflow.
 * Safe for hero sub-copy, meme stings, and score blocks.
 *
 * @param {string} selector   CSS selector for target element
 * @param {number} width      Max line width in px (default 680)
 * @param {number} lineHeight Line height in px (default 28)
 * @param {string} font       Canvas font string
 */
export function flowTextAroundOrb(selector, width = 680, lineHeight = 28, font = '17px Inter, system-ui, sans-serif') {
  const el = document.querySelector(selector)
  if (!el) return

  const text = el.innerText.trim()
  if (!text) return

  const prepared = prepareWithSegments(text, font)
  const { lines } = layoutWithLines(prepared, width, lineHeight)

  // Render lines — indent rhythm: 0 / 16 / 8 cycling for cinematic flow
  el.innerHTML = lines.map((line, i) => {
    const indent = i % 3 === 0 ? 0 : i % 3 === 1 ? 16 : 8
    return `<span style="display:block;padding-left:${indent}px;line-height:${lineHeight}px">${line.text}</span>`
  }).join('')
}

/**
 * initHeroGravity
 * Wires pretext flow to SideGuy hero sub-copy (.sgHeroSub).
 * Call once on DOMContentLoaded. Re-runs on resize (debounced 120ms).
 */
export function initHeroGravity() {
  function apply() {
    const w = Math.min(window.innerWidth - 48, 680)
    flowTextAroundOrb('.sgHeroSub', w, 28, '17px Inter, system-ui, sans-serif')
  }

  apply()

  let timer
  window.addEventListener('resize', () => {
    clearTimeout(timer)
    timer = setTimeout(apply, 120)
  })
}
