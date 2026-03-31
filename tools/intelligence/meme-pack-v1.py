#!/usr/bin/env python3
import os
import re
import random
from pathlib import Path

ROOT = Path(".")
LIMIT = int(os.environ.get("LIMIT", "100"))
TARGET_FILE = os.environ.get("TARGET_FILE", "")
LOG_FILE = os.environ.get("LOG_FILE", "")
MODE = os.environ.get("MODE", "money")

PHONE = "773-544-1231"
SMS = "7735441231"

MEME_BLOCK = """
<!-- SIDEGUY MEME PACK V1 START -->
<section class="sideguy-meme-pack" aria-label="SideGuy human relief layer">
  <div class="sideguy-meme-wrap">
    <div class="sideguy-meme-kicker">SideGuy Reality Check</div>
    <h2 class="sideguy-meme-headline">A little internet truth before you spend real money.</h2>
    <div class="sideguy-meme-grid">
      {cards}
    </div>
    <div class="sideguy-meme-cta-row">
      <a class="sideguy-meme-cta" href="sms:{sms}">Text PJ</a>
      <span class="sideguy-meme-sub">Clarity before cost · {phone}</span>
    </div>
  </div>
</section>
<style>
.sideguy-meme-pack {{
  margin: 32px auto;
  max-width: 1100px;
  padding: 0 16px;
}}
.sideguy-meme-wrap {{
  border: 1px solid rgba(255,255,255,.14);
  background:
    linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,.03)),
    radial-gradient(circle at top left, rgba(88,166,255,.16), transparent 34%),
    radial-gradient(circle at bottom right, rgba(0,255,200,.10), transparent 30%);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 20px;
  box-shadow: 0 16px 60px rgba(0,0,0,.18);
}}
.sideguy-meme-kicker {{
  display: inline-block;
  font-size: 12px;
  letter-spacing: .12em;
  text-transform: uppercase;
  opacity: .8;
  margin-bottom: 10px;
}}
.sideguy-meme-headline {{
  margin: 0 0 14px;
  font-size: clamp(22px, 3vw, 34px);
  line-height: 1.1;
}}
.sideguy-meme-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}}
.sideguy-meme-card {{
  border-radius: 18px;
  padding: 16px;
  border: 1px solid rgba(255,255,255,.12);
  background: rgba(255,255,255,.05);
}}
.sideguy-meme-card strong {{
  display: block;
  margin-bottom: 8px;
  font-size: 15px;
}}
.sideguy-meme-card p {{
  margin: 0;
  line-height: 1.45;
  font-size: 15px;
}}
.sideguy-meme-cta-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  margin-top: 16px;
}}
.sideguy-meme-cta {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 18px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
  border: 1px solid rgba(255,255,255,.18);
  background: rgba(255,255,255,.10);
}}
.sideguy-meme-sub {{
  font-size: 14px;
  opacity: .82;
}}
</style>
<!-- SIDEGUY MEME PACK V1 END -->
""".strip()

CARD_MAP = {
    "payments": [
        ("Processing Truth", "Stripe keeps the float. You should keep more of the customer."),
        ("Middleman Tax", "Middlemen are expensive roommates."),
        ("Fast Money", "0.4 seconds feels faster when it's your margin."),
        ("Operator Mode", "Own a piece of your processing, not just the headache.")
    ],
    "betting": [
        ("Lab Rules", "We don't predict. We structure."),
        ("Signal > Sweat", "The payout matrix is the meme."),
        ("Truth Layer", "Kalshi truth. Flex upside. No emotional bankruptcy."),
        ("System First", "Signals over sweating.")
    ],
    "hvac": [
        ("Quote Reality", "Sometimes the $12 part is hiding behind a $12,000 quote."),
        ("Truck Roll Check", "Text before truck roll."),
        ("Human Layer", "Clarity beats commission."),
        ("Operator Advice", "Before buying the expensive version, ask a human.")
    ],
    "homepage": [
        ("Internet Truth", "Google found the confusion. SideGuy found the fix."),
        ("Forum Fatigue", "Forums debate. SideGuy decides."),
        ("Approved Copy", "Clarity before cost."),
        ("Best CTA", "Text PJ before buying the expensive version.")
    ],
    "general": [
        ("SideGuy Truth", "The internet gives opinions. We help you move."),
        ("Human Relief", "A real person is still the unlock."),
        ("No Chaos", "Clarity before cost."),
        ("Problem Intake", "Text PJ before the rabbit hole gets expensive.")
    ],
}

KEYWORDS = {
    "payments": ["payment", "payments", "processing", "merchant", "solana", "usdc", "stripe", "checkout", "settlement", "pos"],
    "betting": ["betting", "kalshi", "underdog", "prizepicks", "signal", "money-index", "prop", "market"],
    "hvac": ["hvac", "mini-split", "air-conditioning", "furnace", "repair", "replace", "cooling", "heating"],
    "homepage": ["index.html", "home", "homepage"],
}

def load_targets():
    if TARGET_FILE and Path(TARGET_FILE).exists():
        return [line.strip() for line in Path(TARGET_FILE).read_text().splitlines() if line.strip()]
    files = []
    for p in ROOT.glob("*.html"):
        name = p.name.lower()
        score = 0
        if p.name == "index.html":
            score += 100
        for bucket, words in KEYWORDS.items():
            for w in words:
                if w in name:
                    score += 10
        if any(x in name for x in ["san-diego", "north-county", "solana-beach", "del-mar", "encinitas", "la-jolla", "cardiff"]):
            score += 4
        if any(x in name for x in ["payments", "money", "operator", "directory", "lab"]):
            score += 3
        if score > 0:
            files.append((score, p.name))
    files.sort(key=lambda x: (-x[0], x[1]))
    out = [name for _, name in files[:LIMIT]]
    return out

def choose_cards(filename):
    lower = filename.lower()
    if filename == "index.html":
        bucket = "homepage"
    elif any(k in lower for k in KEYWORDS["payments"]):
        bucket = "payments"
    elif any(k in lower for k in KEYWORDS["betting"]):
        bucket = "betting"
    elif any(k in lower for k in KEYWORDS["hvac"]):
        bucket = "hvac"
    else:
        bucket = "general"
    cards = CARD_MAP[bucket]
    return "\n".join(
        f'''<article class="sideguy-meme-card"><strong>{title}</strong><p>{body}</p></article>'''
        for title, body in cards
    )

def already_has_block(text):
    return "SIDEGUY MEME PACK V1 START" in text

def insert_block(text, block):
    lower = text.lower()
    idx = lower.rfind("</body>")
    if idx == -1:
        return None
    return text[:idx] + "\n\n" + block + "\n\n" + text[idx:]

def write_log(lines):
    if LOG_FILE:
        Path(LOG_FILE).write_text("\n".join(lines) + "\n")

targets = load_targets()
if TARGET_FILE:
    Path(TARGET_FILE).write_text("\n".join(targets) + "\n")

changed = []
skipped = []
missing = []

for name in targets[:LIMIT]:
    path = ROOT / name
    if not path.exists():
        missing.append(name)
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if already_has_block(text):
        skipped.append(name)
        continue
    cards = choose_cards(name)
    block = MEME_BLOCK.format(cards=cards, sms=SMS, phone=PHONE)
    new_text = insert_block(text, block)
    if new_text is None:
        skipped.append(name)
        continue
    path.write_text(new_text, encoding="utf-8")
    changed.append(name)

summary = []
summary.append(f"TARGET_COUNT={len(targets[:LIMIT])}")
summary.append(f"CHANGED_COUNT={len(changed)}")
summary.append(f"SKIPPED_COUNT={len(skipped)}")
summary.append(f"MISSING_COUNT={len(missing)}")
summary.append("")
summary.append("[CHANGED]")
summary.extend(changed)
summary.append("")
summary.append("[SKIPPED]")
summary.extend(skipped)
summary.append("")
summary.append("[MISSING]")
summary.extend(missing)
write_log(summary)

print(f"Targets: {len(targets[:LIMIT])}")
print(f"Changed: {len(changed)}")
print(f"Skipped: {len(skipped)}")
print(f"Missing: {len(missing)}")
