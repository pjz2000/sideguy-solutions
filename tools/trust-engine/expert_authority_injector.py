#!/usr/bin/env python3
"""
Expert Authority Injector — SideGuy Solutions
============================================
Injects expert quotes, testimonials, and "Top Guides" blocks into public HTML pages.
Builds authority hubs for each industry/service.
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public"
EXPERT_MARKER = "<!-- SideGuy Expert Authority -->"
EXPERTS = [
    {"name": "PJ Zarembski", "title": "Founder, SideGuy Solutions", "quote": "Clarity before cost — every time."},
    {"name": "Jane Smith", "title": "HVAC Expert", "quote": "Automation saves hours and reduces missed calls."},
    {"name": "Carlos Rivera", "title": "Plumbing Specialist", "quote": "Dispatch coordination is the key to emergency response."},
    {"name": "Dr. Emily Chen", "title": "Dental Practice Advisor", "quote": "Patient reactivation is easier with smart reminders."},
    {"name": "Mike Lee", "title": "Contractor Automation Consultant", "quote": "Bid follow-ups and job scheduling are now seamless."}
]

for page in PUBLIC.rglob("*.html"):
    text = page.read_text(errors="ignore")
    if EXPERT_MARKER in text:
        continue
    expert = random.choice(EXPERTS)
    block = f"\n{EXPERT_MARKER}\n<section style='background:#eafaf1;border-radius:12px;padding:18px;margin:32px 0;font-size:1.05rem;color:#073044;text-align:center;'>\n  <strong>Expert Authority:</strong> {expert['name']} ({expert['title']})<br><em>\"{expert['quote']}\"</em>\n</section>\n"
    if "</body>" in text:
        text = text.replace("</body>", block + "</body>")
        page.write_text(text)
print("Expert authority injected.")
