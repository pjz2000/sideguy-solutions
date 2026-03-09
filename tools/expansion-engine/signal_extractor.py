#!/usr/bin/env python3
"""
Signal Extractor — SideGuy Expansion Engine
============================================
Closes the feedback loop: mines page titles from public/auto/ to generate
new slug variations, then appends them to gravity_pages.txt.

Each pipeline run:
  1. Builds pages from gravity_pages.txt  (existing step)
  2. THIS SCRIPT mines those new pages for keyword patterns
  3. Generates CITIES × PROBLEMS cross-product slugs (new combinations only)
  4. Appends up to MAX_NEW_SIGNALS per run to keep growth controlled

Result: every run expands the available pages for the NEXT run automatically.
"""
from pathlib import Path
import re, datetime

ROOT    = Path("/workspaces/sideguy-solutions")
AUTO    = ROOT / "public" / "auto"
GRAVITY = ROOT / "docs" / "problem-gravity" / "gravity_pages.txt"
LOG_DIR = ROOT / "docs" / "expansion-engine"
LOG_DIR.mkdir(parents=True, exist_ok=True)

MAX_NEW_SIGNALS = 500   # maximum expansion per run — Arnold mode

# ── Geography tiers ───────────────────────────────────────────────────────────
CITIES = [
    "san-diego", "north-county", "chula-vista", "el-cajon", "escondido",
    "la-mesa", "oceanside", "carlsbad", "encinitas", "vista",
    "national-city", "spring-valley", "santee", "poway", "lemon-grove",
    "los-angeles", "orange-county", "riverside", "inland-empire", "bay-area",
]

# ── Industry expansions tiers ─────────────────────────────────────────────────
INDUSTRIES = [
    "hvac", "plumber", "dentist", "contractor", "restaurant",
    "law-firm", "real-estate", "salon", "auto-repair", "medical",
    "landscaping", "electrician", "roofing", "pest-control", "cleaning",
    "accounting", "insurance", "mortgage", "gym", "childcare",
]

# Noise words to strip from slugs when extracting the core problem phrase
_NOISE = {
    "san", "diego", "north", "county", "chula", "vista", "el", "cajon",
    "escondido", "la", "mesa", "oceanside", "carlsbad", "encinitas",
    "national", "city", "spring", "valley", "santee", "poway", "lemon",
    "grove", "los", "angeles", "orange", "riverside", "inland", "empire",
    "bay", "area", "for", "a", "in", "the", "and", "with", "to",
    "how", "what", "why", "who", "is", "are", "do", "does", "can",
    "hvac", "plumber", "dentist", "contractor", "restaurant", "law", "firm",
    "real", "estate", "salon", "auto", "repair", "medical", "landscaping",
    "electrician", "roofing", "pest", "control", "cleaning", "accounting",
    "insurance", "mortgage", "gym", "childcare",
}


def _extract_problem(slug: str) -> str | None:
    """Strip city/industry noise words leaving the core problem phrase."""
    parts = [p for p in slug.split("-") if p and p not in _NOISE]
    if len(parts) < 2:
        return None
    return "-".join(parts)


def _mine_auto_pages() -> set[str]:
    """Return problem-phrase slugs extracted from public/auto/ page stems."""
    problems: set[str] = set()
    for html in AUTO.glob("*.html"):
        p = _extract_problem(html.stem)
        if p:
            problems.add(p)
    return problems


def extract_and_expand() -> int:
    # Load existing gravity slugs to avoid duplicates
    existing = set()
    if GRAVITY.exists():
        for line in GRAVITY.read_text().splitlines():
            existing.add(line.strip().lower())

    problems = _mine_auto_pages()
    if not problems:
        print("Signal extractor: no problems mined from public/auto/ — skipping")
        return 0

    # Generate city × problem × industry combinations
    candidates: list[str] = []
    for problem in sorted(problems):
        for city in CITIES:
            slug = f"{problem}-{city}"
            if slug not in existing:
                candidates.append(slug)
        for industry in INDUSTRIES:
            slug = f"{problem}-{industry}-san-diego"
            if slug not in existing:
                candidates.append(slug)

    # Deduplicate candidates list preserving order, cap at MAX_NEW_SIGNALS
    seen: set[str] = set()
    fresh: list[str] = []
    for c in candidates:
        if c not in seen and c not in existing:
            seen.add(c)
            fresh.append(c)
        if len(fresh) >= MAX_NEW_SIGNALS:
            break

    if not fresh:
        print("Signal extractor: all candidates already in queue — nothing to add")
        return 0

    # Append to gravity queue
    with open(GRAVITY, "a") as f:
        f.write("\n".join(fresh) + "\n")

    # Write log
    today = datetime.date.today().isoformat()
    log   = LOG_DIR / f"expansion-{today}.txt"
    log.write_text("\n".join(fresh) + "\n")

    print(f"Signal extractor: {len(fresh)} new slugs appended to gravity queue "
          f"({len(existing)+len(fresh)} total). Mined from {len(problems)} problem patterns.")
    return len(fresh)


if __name__ == "__main__":
    extract_and_expand()
