# Skill: Hero WOW Upgrade
**Version:** 1.0 · Append-only doctrine
**Purpose:** Safe, repeatable rules for premium hero upgrades — ocean aesthetic, split-pane, animations — without triggering the black-box rendering bug.

---

## THE CARDINAL RULE — Read Before Touching Anything

**NEVER apply `backdrop-filter` to a parent element that also has `overflow:hidden` children.**

This causes black-box rendering in Safari and Chrome. It has burned us multiple times. The safe pattern:
- `backdrop-filter` only on leaf elements (no children with overflow constraints)
- `overflow:hidden` and `backdrop-filter` must NEVER coexist in the same element
- If you need both effects, split them into sibling elements

---

## Current Hero Architecture (LOCKED — do not restructure)

```html
<section class="sgHero">                          <!-- full-bleed, no backdrop-filter here -->
  <div class="sgHeroLeft">                        <!-- transparent background, no overflow:hidden -->
    <p class="sgHeroEye">...</p>                  <!-- eyebrow line -->
    <p class="sgHeroSub">...</p>                  <!-- hero body copy -->
    <p class="sgHeroSub" micro-line>...</p>       <!-- micro trust line -->
    <div class="cmdHeroCtas">                     <!-- CTA group -->
      <a class="cmdPjOrb">Text PJ</a>             <!-- primary orb CTA -->
      <div class="cmdIconGroup">                  <!-- icon CTAs -->
    </div>
    <div class="sg-trust-badge">...</div>         <!-- live operator signal badge -->
    <div class="sg-signal-panel">...</div>        <!-- borderless telemetry strip -->
  </div>
  <div class="sgHeroVisual">...</div>             <!-- ocean panel — NEVER TOUCH -->
</section>
```

**What is locked:**
- `.sgHeroVisual` — the ocean panel. Never modify its content, background, or animation.
- `.sgHeroLeft` background must stay `transparent` — any card/gradient here creates a blue rectangle bug
- `.sg-signal-panel` must stay borderless — any border creates a box artifact inside the hero

---

## Ocean Gradient Rules

The ocean aesthetic lives in `.sgHeroVisual` and the overall page background. Rules:

**Safe gradient pattern:**
```css
background: linear-gradient(135deg, #0c2d48 0%, #0a1e34 60%, #073044 100%);
```

**Safe overlay for depth (on `.sgHeroVisual::after`):**
```css
background: linear-gradient(to right, transparent, rgba(255,255,255,.055) 48%, transparent);
animation: sgOceanSweep 10s ease-in-out infinite;
```

**Never use:**
- `background-clip: text` on any `h1` inside the hero — causes solid blue rectangle in Firefox/Safari
- `opacity < 0.15` on text — becomes unreadable on mobile
- `mix-blend-mode` on hero children — unpredictable cross-browser rendering

---

## Safe Opacity Standards

| Element | Min opacity | Notes |
|---|---|---|
| Hero body copy | 1.0 | Never reduce |
| Muted sub-copy | 0.75 | `.sgHeroSub` secondary lines |
| Trust/telemetry labels | 0.6 | Signal panel values |
| Decorative dots/particles | 0.3–0.5 | `.sg-cs-dot`, `.sg-rt-bead` |
| Ocean sweep overlay | 0.055 peak | `sgOceanSweep` keyframe |

---

## Split-Pane Architecture Rules

The hero is a CSS Grid split-pane. Left = text/CTAs. Right = ocean visual.

**Safe split ratios:**
```css
.sgHero { display: grid; grid-template-columns: 1fr 1fr; }  /* 50/50 */
.sgHero { display: grid; grid-template-columns: 55fr 45fr; } /* text-heavy */
```

**Full-bleed rule:**
```css
.sgHero {
  margin-left: -22px !important;
  margin-right: -22px !important;
  /* negates .wrap padding: 26px 22px */
}
```

**Never use `overflow:hidden` on `.sgHero` or `.sgHeroLeft`** — this is what triggers the black-box bug when combined with backdrop-filter on child elements.

---

## Particle / Animation Rules

**Safe animations (confirmed working):**

```css
/* Ocean sweep — .sgHeroVisual::after */
@keyframes sgOceanSweep {
  0%,100% { opacity:0; transform:translateX(-80%) skewX(-16deg); }
  5%       { opacity:1; }
  20%      { opacity:0; transform:translateX(160%) skewX(-16deg); }
}

/* Pulse dot */
@keyframes sgOsDotPulse {
  0%,100% { opacity:.7 }
  50%     { opacity:1; }
}

/* Float (trust badge) */
@keyframes sgFloat {
  0%,100% { transform:translateY(0); }    /* NOTE: semicolon required — missing it breaks keyframe */
  50%     { transform:translateY(-4px); }
}

/* Traveling bead (signal route) */
@keyframes sgBeadTravel {
  0%   { left: 0%; opacity:0; }
  5%   { opacity:1; }
  95%  { opacity:1; }
  100% { left:100%; opacity:0; }
}
```

**Rules:**
- Keep animation durations 6–12s for ambient loops — faster feels cheap
- Use `ease-in-out` not `linear` for organic feel
- Always add `animation-delay` offsets when stacking multiple pulses (0s, .6s, 1.2s)
- Never animate `background-color` — GPU performance hit on mobile

---

## PJ Orb Glow Standards

The `.cmdPjOrb` is the primary conversion CTA. Keep its glow consistent:

```css
/* Default state */
.cmdPjOrb {
  background: linear-gradient(135deg, #0ea5e9, #0891b2);
  box-shadow: 0 8px 32px rgba(8,145,178,.35);
}

/* Hover state */
.cmdPjOrb:hover {
  transform: scale(1.09) translateY(-3px) !important;
  box-shadow: 0 0 0 5px rgba(8,145,178,.22), 0 22px 60px rgba(8,145,178,.55) !important;
}
```

**Rules:**
- Never remove the `!important` on hover — other rules will override without it
- Keep the dual box-shadow on hover: inner ring + outer glow
- Scale max: 1.09 — beyond this it clips adjacent elements on mobile
- Color stays on the `#0891b2` / `#0ea5e9` spectrum — do not go purple or green

---

## Mobile WOW Rules

- Below 768px: hero stack vertically, ocean visual goes below text (or hides)
- Font size: use `clamp(min, preferred, max)` — never fixed px for hero headings
- Touch targets: all CTAs minimum 44px height
- Animation: reduce or remove sweep/particle animations on mobile (`@media (prefers-reduced-motion)`)
- Proof strip: reduce to 2 columns or single column on mobile

**Mobile-safe media query pattern:**
```css
@media(max-width:768px) {
  .sgHero { grid-template-columns: 1fr; }
  .sgHeroVisual { display: none; } /* or order: -1 */
}
```

---

## Style Block Naming Convention

Each hero upgrade gets its own named `<style>` block with an ID:
```html
<style id="sg-fullbleed-trust">  ... </style>
<style id="sg-hero-polish-v1">   ... </style>
<style id="sg-os-upgrade">       ... </style>
```

Append new blocks — never edit existing ones. This preserves rollback safety.

---

## Known Bugs + Fixes

| Bug | Cause | Fix |
|---|---|---|
| Black rectangle in hero left | `backdrop-filter` + `overflow:hidden` on same element | Remove `overflow:hidden` from `.sgHeroLeft` |
| H1 renders as solid blue block | `background: linear-gradient` + `background-clip:text` fails in some browsers | Delete the gradient background from h1 entirely |
| Blue card appears inside hero | A section with `background:#f0f9ff` or border sits directly above transparent hero | Delete or move the section |
| Keyframe breaks entirely | Missing semicolon in `transform: translateY(0)` | Add the semicolon |
| Signal panel creates box | `.sg-signal-panel` has `background` or `border` | Set `background:transparent!important; border:none!important` |

---

## Hero Upgrade Checklist

```
[ ] Read existing hero structure before touching anything
[ ] Identify which style block to append to (never edit existing)
[ ] Confirm no backdrop-filter + overflow:hidden collision
[ ] Add new CSS in a named <style id="sg-hero-pass-vN"> block
[ ] Test copy changes with grep before editing (confirm exact string)
[ ] Bump version timestamp after hero edit
[ ] Commit: feat: hero upgrade pass vN — [what changed]
```
