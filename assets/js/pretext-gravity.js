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
