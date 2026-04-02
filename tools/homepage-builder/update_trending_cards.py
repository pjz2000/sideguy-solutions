#!/usr/bin/env python3
"""
Homepage Trending Cards Updater
Reads data/gsc-winners.json and rewrites the trending section in index.html.

Usage:
  python3 tools/homepage-builder/update_trending_cards.py

Run after gsc_query_puller.py. Safe to run standalone with existing JSON.
"""

import json
import re
from datetime import date
from pathlib import Path
from html import escape

REPO_ROOT   = Path(__file__).parent.parent.parent
DATA_FILE   = REPO_ROOT / "data" / "gsc-winners.json"
INDEX_FILE  = REPO_ROOT / "index.html"

# Markers in index.html that wrap the auto-generated cards block
OPEN_MARKER  = "<!-- GSC_TRENDING_START -->"
CLOSE_MARKER = "<!-- GSC_TRENDING_END -->"


# ── Card renderer ────────────────────────────────────────────────────────────

def render_card(winner: dict) -> str:
    query       = escape(winner["query"])
    description = escape(winner["description"])
    page        = winner.get("page", "#")
    impressions = winner.get("impressions", 0)
    impr_label  = f"{impressions:,} impr" if impressions else "live now"

    return f'''    <a class="sg-tcard" href="{page}">
      <span class="sg-tcard-pulse"></span>
      <div class="sg-tcard-query">{impr_label}</div>
      <div class="sg-tcard-title">{query}</div>
      <div class="sg-tcard-desc">{description}</div>
      <div class="sg-tcard-cta">See how SideGuy solves this &rarr;</div>
    </a>'''


def render_section(winners: list) -> str:
    today     = date.today().strftime("%B %-d, %Y")
    pulled    = winners[0].get("pulled_date", str(date.today())) if winners else str(date.today())
    window    = winners[0].get("window_start", "") if winners else ""

    cards_html = "\n\n".join(render_card(w) for w in winners)

    return f"""{OPEN_MARKER}
<section class="sg-trending" aria-label="Trending problems SideGuy is solving">
  <div class="sg-trending-head">
    <div class="sg-trending-eye"><span class="sg-live-dot"></span> Live GSC Signals &middot; Updated {today}</div>
    <h2 class="sg-trending-title">Trending Real Problems SideGuy Is Solving</h2>
    <p class="sg-trending-sub">These are real problems Google is already routing into SideGuy right now. Live search demand from real people in the last 7 days.</p>
  </div>
  <div class="sg-trending-grid">

{cards_html}

  </div>
</section>
{CLOSE_MARKER}"""


# ── Inject into index.html ───────────────────────────────────────────────────

def inject(winners: list):
    html = INDEX_FILE.read_text()

    new_section = render_section(winners)

    if OPEN_MARKER in html and CLOSE_MARKER in html:
        # Replace existing block
        pattern = re.escape(OPEN_MARKER) + r".*?" + re.escape(CLOSE_MARKER)
        html = re.sub(pattern, new_section, html, flags=re.S)
        print("Replaced existing GSC trending section.")
    else:
        # First run — insert after the hero section closing tag
        insert_after = "</section>\n\n<!-- MEME FACTORY STRIP -->"
        replacement  = f"</section>\n\n{new_section}\n\n<!-- MEME FACTORY STRIP -->"
        if insert_after in html:
            html = html.replace(insert_after, replacement, 1)
            print("Inserted GSC trending section after hero.")
        else:
            print("WARNING: Could not find hero section end marker. Appending to main.")
            # Fallback — insert before meme strip
            html = html.replace(
                "<!-- MEME FACTORY STRIP -->",
                f"{new_section}\n\n<!-- MEME FACTORY STRIP -->",
                1
            )

    INDEX_FILE.write_text(html)
    print(f"index.html updated with {len(winners)} cards.")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not DATA_FILE.exists():
        print(f"ERROR: {DATA_FILE} not found. Run gsc_query_puller.py first.")
        raise SystemExit(1)

    winners = json.loads(DATA_FILE.read_text())
    if not winners:
        print("No winners in data file. Skipping update.")
        return

    print(f"Building cards for {len(winners)} queries...")
    inject(winners)
    print("Done.")


if __name__ == "__main__":
    main()
