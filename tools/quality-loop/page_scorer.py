#!/usr/bin/env python3
"""
Page Quality Scorer — SideGuy Quality Loop
==========================================
Scans all public/ HTML pages, scores each on 5 SEO quality signals,
writes a TSV report, and queues low-scoring pages for re-upgrade.

Scoring rubric (each worth 1 point, max 5):
  1. canonical   — has <link rel="canonical">
  2. h1           — has <h1> tag
  3. meta_desc    — has <meta name="description" ...>
  4. word_count   — visible word count ≥ 250 (strips HTML tags)
  5. context_block — has a SideGuy context/uniqueness block

Pages scoring ≤ 2 are written to docs/quality-loop/needs_upgrade.txt.
Re-run the context engine on that list to lift them on the next pipeline run.

Output files:
  docs/quality-loop/scores-<date>.tsv  — full audit
  docs/quality-loop/needs_upgrade.txt  — paths needing work (overwritten each run)
  docs/quality-loop/summary.txt        — one-line stats
"""
from pathlib import Path
import re, datetime, html

ROOT     = Path("/workspaces/sideguy-solutions")
OUT_DIR  = ROOT / "docs" / "quality-loop"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TODAY    = datetime.date.today().isoformat()
SCORES_FILE  = OUT_DIR / f"scores-{TODAY}.tsv"
UPGRADE_FILE = OUT_DIR / "needs_upgrade.txt"
SUMMARY_FILE = OUT_DIR / "summary.txt"

LOW_THRESHOLD = 2   # pages with score ≤ this go into the upgrade queue

# Skip these to keep the audit fast and avoid backup noise
SKIP_DIRS = {
    ".git", "node_modules", "_quarantine_backups",
    "backups_20251230_191613", "backup_pages", "backup_old_pages",
    "crawl-sitemaps",
}

TAG_RE    = re.compile(r"<[^>]+>")
SPACE_RE  = re.compile(r"\s+")

CONTEXT_MARKERS = [
    "SideGuy Unique Context",
    "sideguy-unique",
    "SIDEGUY_DIFF",
    "SideGuy Context",
    "Local Context for",
]


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

    canonical   = 1 if 'rel="canonical"' in raw_lower else 0
    h1          = 1 if re.search(r"<h1[\s>]", raw_lower) else 0
    meta_desc   = 1 if re.search(r'<meta[^>]+name=["\']description["\']', raw_lower) else 0
    words       = _visible_words(raw)
    word_score  = 1 if words >= 250 else 0
    ctx_block   = 1 if any(m.lower() in raw_lower for m in CONTEXT_MARKERS) else 0

    total = canonical + h1 + meta_desc + word_score + ctx_block

    return {
        "path":      str(path.relative_to(ROOT)),
        "score":     total,
        "canonical": canonical,
        "h1":        h1,
        "meta_desc": meta_desc,
        "words":     words,
        "ctx_block": ctx_block,
    }


def run_scorer():
    pages = [
        p for p in (ROOT / "public").rglob("*.html")
        if not _skip(p)
    ]

    print(f"Quality scorer: scanning {len(pages)} pages…")

    results   = []
    low_pages = []

    for p in pages:
        r = score_page(p)
        if r is None:
            continue
        results.append(r)
        if r["score"] <= LOW_THRESHOLD:
            low_pages.append(r["path"])

    # Sort: lowest score first
    results.sort(key=lambda x: x["score"])

    # Write TSV
    header = "path\tscore\tcanonical\th1\tmeta_desc\twords\tctx_block\n"
    rows   = "\n".join(
        f"{r['path']}\t{r['score']}\t{r['canonical']}\t{r['h1']}\t"
        f"{r['meta_desc']}\t{r['words']}\t{r['ctx_block']}"
        for r in results
    )
    SCORES_FILE.write_text(header + rows + "\n")

    # Write upgrade queue
    UPGRADE_FILE.write_text("\n".join(low_pages) + "\n")

    # Stats
    total_pages = len(results)
    avg_score   = sum(r["score"] for r in results) / total_pages if total_pages else 0
    dist        = {i: sum(1 for r in results if r["score"] == i) for i in range(6)}

    summary = (
        f"Quality audit {TODAY}\n"
        f"Pages scanned : {total_pages}\n"
        f"Average score : {avg_score:.2f} / 5\n"
        f"Score dist    : { '  '.join(f'{k}={v}' for k,v in dist.items()) }\n"
        f"Needs upgrade : {len(low_pages)} pages (score ≤ {LOW_THRESHOLD})\n"
        f"Full report   : {SCORES_FILE.name}\n"
    )
    SUMMARY_FILE.write_text(summary)
    print(summary.strip())
    print(f"Upgrade queue → {UPGRADE_FILE}")


if __name__ == "__main__":
    run_scorer()
