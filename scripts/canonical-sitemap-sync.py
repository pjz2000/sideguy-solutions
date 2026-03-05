#!/usr/bin/env python3
"""
SIDEGUY CANONICAL + SITEMAP SYNC ENGINE
----------------------------------------
1. Inventory all public HTML files (exclude backups, docs, seo-reserve, etc.)
2. Inject/update <link rel="canonical"> on pages missing or wrong canonicals
3. Rebuild sitemap.xml from actual HTML inventory
4. Preserve all existing robots.txt Disallow rules, update Sitemap: line
5. Write diagnostics to docs/crawl-plumbing/generated/

SITE_BASE env var overrides the default domain.
"""

import os
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent.resolve()
SITE_BASE = os.environ.get("SITE_BASE", "https://sideguysolutions.com").rstrip("/")
TODAY = date.today().isoformat()
DIAG_DIR = ROOT / "docs" / "crawl-plumbing" / "generated"
DIAG_DIR.mkdir(parents=True, exist_ok=True)

# ─── Exclusion rules ──────────────────────────────────────────────────────────
# Any path segment (directory name) matching these is excluded from sitemap/canonical injection.
# Mirror robots.txt Disallow entries + known backup / internal dirs.
EXCLUDE_SEGMENTS = {
    ".git", "node_modules",
    # robots.txt disallows
    "backups", "docs", "site", "public", ".github", "signals", "data", "seo-reserve",
    # backup-pattern dirs
    ".sideguy-backups", "_BACKUPS", "_layout_backups", "_quarantine_backups",
    "backup_pages", "backup_old_pages", "reports", "reserve", "autogen",
    "templates", "savings-logs", "tickets",
    # internal dev dirs
    "aaa-global-layout", "aaa-homepage-test", "partials",
}
# Also exclude any segment that contains the word "backup" (case-insensitive)
EXCLUDE_PATTERN = re.compile(r"backup", re.IGNORECASE)


def is_excluded(path: Path) -> bool:
    """Return True if any path segment matches exclusion rules."""
    for part in path.parts:
        if part in EXCLUDE_SEGMENTS:
            return True
        if EXCLUDE_PATTERN.search(part):
            return True
    return False


# ─── Step 1: Inventory HTML files ────────────────────────────────────────────
def inventory_html() -> list[tuple[Path, str]]:
    """Return list of (abs_path, canonical_url) for all includable HTML files."""
    results = []
    for html_file in sorted(ROOT.rglob("*.html")):
        rel = html_file.relative_to(ROOT)
        if is_excluded(rel):
            continue
        # Build canonical URL
        url_path = "/" + str(rel).replace("\\", "/")
        # index.html → directory root
        if url_path.lower().endswith("/index.html"):
            url_path = url_path[: -len("index.html")]
        # Root index.html → /
        if url_path == "/index.html":
            url_path = "/"
        canonical = SITE_BASE + url_path
        results.append((html_file, canonical))
    return results


# ─── Step 2: Canonical injection ─────────────────────────────────────────────
CANON_RE = re.compile(
    r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\'][^>]*/?>|'
    r'<link\s+href=["\']([^"\']*)["\'][^>]*rel=["\']canonical["\'][^>]*/?>'
    , re.IGNORECASE,
)
HEAD_RE = re.compile(r"(<head\b[^>]*>)", re.IGNORECASE)


def fix_canonical(html_file: Path, expected_url: str) -> str:
    """
    Returns 'updated', 'inserted', or 'ok' depending on action taken.
    Mutates the file if needed.
    """
    try:
        text = html_file.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return "error"

    new_tag = f'<link rel="canonical" href="{expected_url}"/>'

    m = CANON_RE.search(text)
    if m:
        existing_href = m.group(1) or m.group(2) or ""
        if existing_href == expected_url:
            return "ok"
        # Replace existing canonical regardless of href
        new_text = CANON_RE.sub(new_tag, text, count=1)
        html_file.write_text(new_text, encoding="utf-8")
        return f"updated ({existing_href} → {expected_url})"
    else:
        # Inject after <head>
        head_m = HEAD_RE.search(text)
        if not head_m:
            return "no-head"
        insert_pos = head_m.end()
        new_text = text[:insert_pos] + "\n" + new_tag + text[insert_pos:]
        html_file.write_text(new_text, encoding="utf-8")
        return "inserted"


# ─── Step 3: Build sitemap.xml ───────────────────────────────────────────────
SITEMAP_HEADER = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
SITEMAP_FOOTER = "</urlset>\n"


def build_sitemap(pages: list[tuple[Path, str]]) -> None:
    url_entries = ""
    for _, canonical in pages:
        safe_url = (
            canonical.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        url_entries += f"  <url>\n    <loc>{safe_url}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
    sitemap_path = ROOT / "sitemap.xml"
    sitemap_path.write_text(SITEMAP_HEADER + url_entries + SITEMAP_FOOTER, encoding="utf-8")
    print(f"✅ sitemap.xml written — {len(pages)} URLs")


# ─── Step 4: Update robots.txt ───────────────────────────────────────────────
def update_robots() -> None:
    robots_path = ROOT / "robots.txt"
    current = robots_path.read_text(encoding="utf-8") if robots_path.exists() else ""
    sitemap_line = f"Sitemap: {SITE_BASE}/sitemap.xml"
    # Remove any existing Sitemap: lines (including sitemap-index.xml refs)
    lines = [l for l in current.splitlines() if not l.startswith("Sitemap:")]
    lines.append(sitemap_line)
    robots_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ robots.txt updated — Sitemap: line → {SITE_BASE}/sitemap.xml")


# ─── Step 5: Diagnostics ─────────────────────────────────────────────────────
def write_diagnostics(pages: list[tuple[Path, str]], canon_log: list[tuple]) -> None:
    # canonical injection log
    canon_log_path = DIAG_DIR / "canonical_injection.log"
    with open(canon_log_path, "w") as f:
        for action, path, url in canon_log:
            f.write(f"{action}\t{path}\t{url}\n")

    # duplicate canonical check
    from collections import Counter
    url_counts = Counter(url for _, url in pages)
    dupes = {url: cnt for url, cnt in url_counts.items() if cnt > 1}
    dupe_path = DIAG_DIR / "duplicate_canonicals.tsv"
    with open(dupe_path, "w") as f:
        for url, cnt in sorted(dupes.items()):
            f.write(f"{url}\t{cnt}\n")

    # url list
    url_list_path = DIAG_DIR / "sitemap_urls.tsv"
    with open(url_list_path, "w") as f:
        for path, url in pages:
            f.write(f"{url}\t{TODAY}\t{path.relative_to(ROOT)}\n")

    # summary
    updated = [r for r in canon_log if not r[0].startswith("ok") and not r[0].startswith("error")]
    summary = DIAG_DIR / "CRAWL_PLUMBING_SUMMARY.md"
    summary.write_text(f"""# Crawl Plumbing Summary
Generated: {TODAY}

## Inventory
- HTML files included in sitemap: {len(pages)}
- Duplicate canonical URLs: {len(dupes)}

## Canonical Actions
- OK (no change): {sum(1 for r in canon_log if r[0] == 'ok')}
- Inserted: {sum(1 for r in canon_log if r[0] == 'inserted')}
- Updated: {sum(1 for r in canon_log if r[0].startswith('updated'))}
- No-head (skipped): {sum(1 for r in canon_log if r[0] == 'no-head')}
- Errors: {sum(1 for r in canon_log if r[0] == 'error')}

## Outputs
- sitemap.xml: {ROOT}/sitemap.xml
- robots.txt: {ROOT}/robots.txt

## Diagnostics
- Canonical log: {canon_log_path}
- Duplicate canonicals: {dupe_path}
- Full URL list: {url_list_path}

## Directory Breakdown
""", encoding="utf-8")

    from collections import defaultdict
    dir_counts: dict = defaultdict(int)
    for path, _ in pages:
        rel = path.relative_to(ROOT)
        top_dir = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        dir_counts[top_dir] += 1
    with open(summary, "a") as f:
        for d, cnt in sorted(dir_counts.items(), key=lambda x: -x[1]):
            f.write(f"- `{d}`: {cnt} pages\n")

    print(f"✅ Diagnostics written to {DIAG_DIR}")
    if dupes:
        print(f"⚠️  {len(dupes)} duplicate canonical URLs found — check {dupe_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("🌊 SIDEGUY CANONICAL + SITEMAP SYNC ENGINE")
    print(f"   SITE_BASE : {SITE_BASE}")
    print(f"   ROOT      : {ROOT}")
    print(f"   Date      : {TODAY}")
    print()

    print("📂 Inventorying HTML files...")
    pages = inventory_html()
    print(f"   Found {len(pages)} includable HTML files")
    print()

    print("🧲 Checking/injecting canonical tags...")
    canon_log = []
    updated_count = 0
    inserted_count = 0
    for html_file, canonical in pages:
        result = fix_canonical(html_file, canonical)
        canon_log.append((result, str(html_file.relative_to(ROOT)), canonical))
        if result.startswith("updated"):
            updated_count += 1
        elif result == "inserted":
            inserted_count += 1
    print(f"   Inserted: {inserted_count}  |  Updated: {updated_count}  |  OK: {len(pages) - inserted_count - updated_count}")
    print()

    print("🗺️  Building sitemap.xml...")
    build_sitemap(pages)

    print("🤖 Updating robots.txt...")
    update_robots()
    print()

    print("🧪 Writing diagnostics...")
    write_diagnostics(pages, canon_log)
    print()

    print("─" * 48)
    print("✅ CANONICAL + SITEMAP SYNC COMPLETE")
    print(f"   sitemap.xml : {len(pages)} URLs")
    print(f"   canonicals  : {inserted_count} inserted, {updated_count} updated")
    print()
    print("NEXT: Link Equity Balancer — ensure pillars/clusters receive")
    print("      enough internal links from Directory + Categories.")
    print("─" * 48)


if __name__ == "__main__":
    main()
