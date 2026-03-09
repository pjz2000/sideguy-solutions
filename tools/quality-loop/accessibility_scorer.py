#!/usr/bin/env python3
"""
Accessibility/Schema Quality Scorer — SideGuy Solutions
=======================================================
Extends the quality scorer to check for FAQ schema, alt text, and ARIA labels.
Writes a TSV report and flags pages missing accessibility/schema for upgrade.
"""
from pathlib import Path
import re, datetime, html

ROOT     = Path("/workspaces/sideguy-solutions")
OUT_DIR  = ROOT / "docs" / "quality-loop"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY    = datetime.date.today().isoformat()
SCORES_FILE  = OUT_DIR / f"accessibility-scores-{TODAY}.tsv"
UPGRADE_FILE = OUT_DIR / "needs_accessibility_upgrade.txt"

# Skip these to keep the audit fast and avoid backup noise
SKIP_DIRS = {
    ".git", "node_modules", "_quarantine_backups",
    "backups_20251230_191613", "backup_pages", "backup_old_pages",
    "crawl-sitemaps",
}

TAG_RE    = re.compile(r"<[^>]+>")
SPACE_RE  = re.compile(r"\s+")

SCHEMA_MARKER = "FAQPage JSON-LD"


def _skip(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & SKIP_DIRS)


def _visible_words(raw: str) -> int:
    text = TAG_RE.sub(" ", raw)
    text = html.unescape(text)
    return len(SPACE_RE.split(text.strip()))


def score_page(path: Path) -> dict:
    try:
        raw = path.read_text(errors="ignore")
    except Exception:
        return None

    raw_lower = raw.lower()

    schema     = 1 if SCHEMA_MARKER.lower() in raw_lower else 0
    alt_text   = 1 if re.search(r'alt="[^"]+"', raw_lower) else 0
    aria_label = 1 if re.search(r'aria-label="[^"]+"', raw_lower) else 0

    total = schema + alt_text + aria_label

    return {
        "path":      str(path.relative_to(ROOT)),
        "score":     total,
        "schema":    schema,
        "alt_text":  alt_text,
        "aria_label": aria_label,
    }


def run_scorer():
    pages = [
        p for p in (ROOT / "public").rglob("*.html")
        if not _skip(p)
    ]

    print(f"Accessibility scorer: scanning {len(pages)} pages…")

    results   = []
    low_pages = []

    for p in pages:
        r = score_page(p)
        if r is None:
            continue
        results.append(r)
        if r["score"] < 2:
            low_pages.append(r["path"])

    # Sort: lowest score first
    results.sort(key=lambda x: x["score"])

    # Write TSV
    header = "path\tscore\tschema\talt_text\taria_label\n"
    rows   = "\n".join(
        f"{r['path']}\t{r['score']}\t{r['schema']}\t{r['alt_text']}\t{r['aria_label']}"
        for r in results
    )
    SCORES_FILE.write_text(header + rows + "\n")

    # Write upgrade queue
    UPGRADE_FILE.write_text("\n".join(low_pages) + "\n")

    print(f"Accessibility audit {TODAY}: {len(low_pages)} pages flagged for upgrade.")


if __name__ == "__main__":
    run_scorer()
