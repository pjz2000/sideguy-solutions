#!/usr/bin/env python3
"""
SideGuy GSC Coverage Fixer
-----------------------------
Fixes two GSC coverage issues identified from the March 2026 report:

  1. "Duplicate without user-selected canonical" (90 pages)
     → Adds self-referencing <link rel="canonical"> to full HTML pages
       that are missing one. Only touches full HTML docs (have <html> tag).

  2. Backup copies sharing a live page's canonical
     → Adds <meta name="robots" content="noindex,follow"> to pages inside
       reports/self-improve-backups/ so Google stops counting them as dupes.

Skipped dirs: .git, _quarantine_backups, backup_pages, backup_old_pages,
              backups_20251230_191613, backups/pre-blanket, _BACKUPS,
              .sideguy-backups, node_modules

Canonical URL pattern:
  ./ac-not-cooling-san-diego.html
    → https://sideguysolutions.com/ac-not-cooling-san-diego.html
  ./auto-hubs/payments--overview.html
    → https://sideguysolutions.com/auto-hubs/payments--overview.html

Outputs:
  docs/authority-reports/coverage-fix-report.md  — full audit of changes
"""

import glob
import os
import re
from pathlib import Path

ROOT   = Path(__file__).parent.parent.parent.resolve()
SITE   = "https://sideguysolutions.com"
OUT_MD = ROOT / "docs" / "authority-reports" / "coverage-fix-report.md"

SKIP_DIRS = {
    ".git", "_quarantine_backups", "backup_pages", "backup_old_pages",
    "backups_20251230_191613", "backups", "_BACKUPS", ".sideguy-backups",
    "node_modules", "dist", "build",
}

BACKUP_DIR_MARKER = "reports/self-improve-backups"  # noindex these

CANONICAL_RE = re.compile(r'<link\s[^>]*rel=["\']canonical["\'][^>]*>', re.IGNORECASE)
NOINDEX_RE   = re.compile(r'<meta\s[^>]*name=["\']robots["\'][^>]*>', re.IGNORECASE)
HEAD_END_RE  = re.compile(r'</head>', re.IGNORECASE)
HEAD_START_RE = re.compile(r'<head[^>]*>', re.IGNORECASE)

def skip(path: str) -> bool:
    p = path.replace(os.sep, "/")
    return any(f"/{d}/" in f"/{p}/" or p.startswith(f"{d}/") for d in SKIP_DIRS)

def is_backup_copy(rel: str) -> bool:
    return BACKUP_DIR_MARKER in rel.replace(os.sep, "/")

def rel_canonical(rel_path: str) -> str:
    """Build the canonical URL from a repo-relative path."""
    url_path = rel_path.replace(os.sep, "/").lstrip("./")
    return f"{SITE}/{url_path}"

def insert_into_head(html: str, tag: str) -> str:
    """Insert tag just before </head>. Falls back to after <head>."""
    m = HEAD_END_RE.search(html)
    if m:
        return html[:m.start()] + tag + "\n" + html[m.start():]
    m = HEAD_START_RE.search(html)
    if m:
        return html[:m.end()] + "\n" + tag + html[m.end():]
    return html  # can't find head — leave unchanged

# ── Scan all HTML files ───────────────────────────────────────────────────────
all_html = [
    Path(p) for p in glob.glob(str(ROOT / "**" / "*.html"), recursive=True)
    if not skip(os.path.relpath(p, ROOT))
]

added_canonical = []
added_noindex   = []
skipped_fragment = []
skipped_already  = []

for page in sorted(all_html):
    rel = os.path.relpath(page, ROOT)
    try:
        html = page.read_text(encoding="utf-8", errors="replace")
    except OSError:
        continue

    # Only process full HTML documents (not partials/fragments)
    if "<html" not in html.lower():
        skipped_fragment.append(rel)
        continue

    # ── Case 1: backup copy → add noindex if missing
    if is_backup_copy(rel):
        if not NOINDEX_RE.search(html):
            tag = '<meta name="robots" content="noindex,follow">'
            new_html = insert_into_head(html, tag)
            if new_html != html:
                page.write_text(new_html, encoding="utf-8")
                added_noindex.append(rel)
        else:
            skipped_already.append(rel)
        continue

    # ── Case 2: missing canonical → add self-referencing canonical
    if CANONICAL_RE.search(html):
        skipped_already.append(rel)
        continue

    canonical_url = rel_canonical(rel)
    tag = f'<link rel="canonical" href="{canonical_url}">'
    new_html = insert_into_head(html, tag)
    if new_html != html:
        page.write_text(new_html, encoding="utf-8")
        added_canonical.append((rel, canonical_url))
    else:
        skipped_already.append(rel)

# ── Write report ──────────────────────────────────────────────────────────────
OUT_MD.parent.mkdir(parents=True, exist_ok=True)

lines = [
    "# GSC Coverage Fix Report",
    "",
    f"Run: March 5, 2026  |  Repo: sideguysolutions.com",
    "",
    "## Summary",
    "",
    f"| Fix | Count |",
    f"|---|---|",
    f"| Canonical tags added | {len(added_canonical)} |",
    f"| Noindex added to backup copies | {len(added_noindex)} |",
    f"| Already had canonical (skipped) | {len(skipped_already)} |",
    f"| HTML fragments (skipped) | {len(skipped_fragment)} |",
    "",
    "---",
    "",
    f"## Canonical tags added ({len(added_canonical)} pages)",
    "",
]
for rel, url in added_canonical[:100]:
    lines.append(f"- `{rel}` → `{url}`")
if len(added_canonical) > 100:
    lines.append(f"- … and {len(added_canonical) - 100} more")

lines += [
    "",
    f"## Noindex added to backup copies ({len(added_noindex)} pages)",
    "",
]
for rel in added_noindex[:50]:
    lines.append(f"- `{rel}`")
if len(added_noindex) > 50:
    lines.append(f"- … and {len(added_noindex) - 50} more")

lines += [
    "",
    "## What this fixes in GSC",
    "",
    "- **Duplicate without user-selected canonical**: resolved by adding self-referencing",
    "  canonical to pages that had none. Google now knows which URL is authoritative.",
    "- **Backup copy duplication**: resolved by adding noindex to",
    f"  `{BACKUP_DIR_MARKER}/` copies so Google stops treating them as competing pages.",
    "",
    "## Next steps",
    "1. Request re-indexing in GSC → URL Inspection → Request Indexing",
    "2. Re-submit sitemap.xml in GSC → Sitemaps",
    "3. Monitor Coverage report — 'Duplicate without user-selected canonical'",
    "   should drop toward 0 within 2–4 weeks.",
    "",
]

OUT_MD.write_text("\n".join(lines), encoding="utf-8")

print(f"GSC Coverage Fixer complete")
print(f"  Canonical tags added      : {len(added_canonical)}")
print(f"  Noindex added (backups)   : {len(added_noindex)}")
print(f"  Already had canonical     : {len(skipped_already)}")
print(f"  Fragments skipped         : {len(skipped_fragment)}")
print(f"  Report                    : {OUT_MD.relative_to(ROOT)}")
