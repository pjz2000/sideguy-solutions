#!/usr/bin/env python3
"""
Meme Content Injector — SideGuy Solutions
=========================================
Injects a meme block into public/ pages for office/AI topics.
Idempotent: skips pages already containing a meme block.

Run after builder/context steps for maximum fun and engagement.
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions/public")
MEME_MARKER = "<!-- SideGuy Meme Block -->"

MEMES = [
    "When the AI says 'I'm sorry, I can't help with that.' — but you know it could if it wanted to.",
    "Office meme: 'When you automate your job and your boss asks what you do all day.'",
    "AI meme: 'Me: I need help. AI: Have you tried turning yourself off and on again?'",
    "Office meme: 'When the coffee machine is smarter than your manager.'",
    "AI meme: 'When you ask the AI for a joke and it gives you your quarterly report.'",
    "Office meme: 'When the printer jams and the AI says it’s a feature, not a bug.'",
    "AI meme: 'When you automate your reminders and still forget your meeting.'",
    "Office meme: 'When the AI schedules a meeting for Friday at 4pm.'",
        "Office meme: 'When the AI generates a meme about itself.'",
]

pages = list(ROOT.rglob("*.html"))
updated = 0
skipped = 0

for page in pages:
    text = page.read_text(errors="ignore")
    if MEME_MARKER in text:
        skipped += 1
        continue
    meme = random.choice(MEMES)
    block = f"\n{MEME_MARKER}\n<div class=\"sideguy-meme\" style=\"background:#f0faff;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;text-align:center;\">\n  <strong>Office/AI Meme:</strong> {meme}\n</div>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>", 1)
        page.write_text(text)
        updated += 1

print(f"Meme injector: {updated} pages updated, {skipped} already marked.")
