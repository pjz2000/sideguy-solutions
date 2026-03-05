# Friendly Intelligence Block — Template & Guide

## What it is
A standard content block that appears on every SideGuy leaf page.
Sounds like a smart friend explaining things calmly — not a sales page, not a manual.

---

## Block Structure (copy this into every page)

### 1. Quick Answer
_1–3 sentences. Direct. No hedging._

Example: "Your AC isn't cooling because the refrigerant is low or the compressor is struggling. It won't fix itself — but there are two things to check before calling anyone."

### 2. Why This Happens
_Short, plain-language root cause. No jargon._

Example: "Most chargebacks happen because the customer doesn't recognize the charge on their statement — not because they're trying to scam you."

### 3. What People Misunderstand
_3 bullets. Correct the most common wrong assumptions._

- "Most people think X, but actually Y."
- "It's not usually Z — it's almost always Q."
- "The fix is simpler than it sounds."

### 4. Simple Next Steps
_5 steps max. Numbered. Action-oriented._

1. Check [specific thing]
2. Try [specific action]
3. If that doesn't work, try [alternative]
4. If still broken, you probably need [professional/tool]
5. Text PJ if you want a second opinion before spending money

### 5. When to Text PJ
_1–2 sentences. Non-salesy. Honest._

Example: "Text PJ if you want a human to sanity-check your situation before you commit to a repair or a vendor."

---

## Tone Rules

| Wrong | Right |
|-------|-------|
| "Thermodynamic systems operate at..." | "Your AC compressor is basically the heart of the system..." |
| "Payment rail velocity impacts settlement latency..." | "The money usually takes 1–2 business days to land." |
| "Leverage AI paradigms to optimize..." | "You can set this up once and it runs itself." |
| "Consult a qualified professional..." | "If it's tripped twice this week, call an electrician — don't reset it again." |
| "This varies depending on many factors..." | "Usually $200–400. More if the capacitor is also dead." |

---

## HTML Snippet (paste into leaf pages)

```html
<section class="sideguy-intelligence" style="background:#f0fbf6;border-left:4px solid #21d3a1;padding:1.5rem 2rem;margin:2rem 0;border-radius:8px">
  <h2 style="margin-top:0;color:#073044">Quick Answer</h2>
  <p><!-- 1–3 sentence direct answer --></p>

  <h3 style="color:#073044">Why This Happens</h3>
  <p><!-- plain language root cause --></p>

  <h3 style="color:#073044">What People Get Wrong</h3>
  <ul>
    <li><!-- misconception 1 --></li>
    <li><!-- misconception 2 --></li>
    <li><!-- misconception 3 --></li>
  </ul>

  <h3 style="color:#073044">Simple Next Steps</h3>
  <ol>
    <li><!-- step 1 --></li>
    <li><!-- step 2 --></li>
    <li><!-- step 3 --></li>
    <li><!-- step 4 --></li>
    <li><!-- step 5 --></li>
  </ol>
</section>

<div class="text-pj-cta" style="text-align:center;padding:1.5rem;background:#073044;color:#fff;border-radius:8px;margin:2rem 0">
  <p style="margin:0 0 0.5rem">Still unsure? Get calm clarity from a real human.</p>
  <a href="sms:+17735441231" style="color:#21d3a1;font-weight:700;font-size:1.1rem">Text PJ: 773-544-1231</a>
</div>
```

---

## Pyramid Nav Snippet (required on every leaf page)

```html
<nav class="pyramid-nav" aria-label="Site hierarchy" style="font-size:0.85rem;color:#666;margin-bottom:1.5rem">
  <a href="/">SideGuy</a> →
  <a href="<!-- pillar hub URL -->"><!-- Pillar Name --></a> →
  <span><!-- Cluster Name --></span>
</nav>
```
