#!/usr/bin/env python3
"""
Uniqueness Engine — SideGuy Solutions
Injects an industry-specific operational context paragraph into each public/ page.

Fixes applied vs. original spec:
  - Re-injection guard uses the marker string that actually appears in the injected block
    ("SideGuy Unique Context") so re-running is idempotent.
  - Industry is extracted from the first meaningful URL segment (not the last, which is
    usually "san-diego" or "diego" on most longtail slugs).
"""
from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions/public")

PARAGRAPH_TEMPLATES = [
    "Many {industry} businesses struggle with manual scheduling, missed inquiries, and inconsistent follow-ups. AI automation can streamline customer communication and reduce administrative workload.",
    "For modern {industry} operators, automation tools can improve lead response times and reduce repetitive tasks such as appointment scheduling, reminders, and invoicing.",
    "Small {industry} businesses often lose revenue due to delayed responses or manual coordination. AI systems can automatically capture inquiries, qualify leads, and route requests to the right staff member.",
    "In the {industry} industry, automation is increasingly used to handle customer intake, service scheduling, and follow-up communications.",
]

# Segments to ignore when picking an industry word from the slug
_SKIP = {
    "san", "diego", "los", "angeles", "new", "york", "las", "vegas",
    "for", "the", "and", "with", "how", "what", "why", "who",
    "html", "auto", "ai", "in", "a", "of",
}


def _industry_from_slug(slug: str) -> str:
    """Return the first non-noise word from the slug as a rough industry label."""
    parts = [p for p in slug.split("-") if p and p not in _SKIP]
    return parts[0] if parts else "business"


MARKER = "SideGuy Unique Context"

pages = list(ROOT.rglob("*.html"))
updated = 0
skipped = 0

for page in pages:
    text = page.read_text(errors="ignore")

    if MARKER in text:
        skipped += 1
        continue

    slug     = page.stem
    industry = _industry_from_slug(slug)
    para     = random.choice(PARAGRAPH_TEMPLATES).replace("{industry}", industry)

    block = f"""
<!-- {MARKER} -->
<div class="sideguy-unique">
  <h2>Operational Context</h2>
  <p>{para}</p>
</div>
"""

    if "</body>" in text:
        text = text.replace("</body>", block + "</body>", 1)
        page.write_text(text)
        updated += 1

print(f"Unique context added — {updated} updated, {skipped} already marked")
