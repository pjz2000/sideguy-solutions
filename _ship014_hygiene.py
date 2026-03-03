#!/usr/bin/env python3
"""SHIP-014: Production Hygiene + Crawl Efficiency Pass
Phase 1: robots.txt hard-disallow of non-production dirs
Phase 2: Root HTML validation report
Phase 3: Duplicate title/meta/H1 detection
Phase 4: Sitemap priority tuning

Outputs:
  SHIP-014-report.txt -- validation + duplication report
  (modifies)   robots.txt    -- Phase 1
  (modifies)   sitemap.xml   -- Phase 4
"""
import os, glob, re, json
from collections import defaultdict

ROOT = "/workspaces/sideguy-solutions"
REPORT_PATH = os.path.join(ROOT, "SHIP-014-report.txt")

# ── Phase 1 — robots.txt ──────────────────────────────────────────────────────
ROBOTS_PATH = os.path.join(ROOT, "robots.txt")
NON_PROD_DIRS = ["/backups/", "/docs/", "/site/", "/public/", "/seo-reserve/",
                 "/.github/", "/signals/", "/data/"]

def phase1_robots():
    with open(ROBOTS_PATH, "r") as f:
        content = f.read()

    lines = content.strip().splitlines()
    existing_disallows = {l.split("Disallow:", 1)[1].strip()
                         for l in lines if l.startswith("Disallow:")}

    added = []
    for d in NON_PROD_DIRS:
        if d not in existing_disallows:
            # insert after "Allow: /" line
            added.append(f"Disallow: {d}")

    if added:
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("Allow: /"):
                for a in added:
                    new_lines.append(a)
        with open(ROBOTS_PATH, "w") as f:
            f.write("\n".join(new_lines) + "\n")
        return f"robots.txt updated — added {len(added)} Disallow rules:\n" + \
               "\n".join(f"  {a}" for a in added)
    else:
        return "robots.txt — all required Disallow rules already present."


# ── Phase 2 + 3 — HTML validation ────────────────────────────────────────────
def extract_tag(content, pattern):
    m = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def validate_html_files():
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    print(f"  Scanning {len(files)} HTML files...")

    titles = defaultdict(list)
    descs  = defaultdict(list)
    h1s    = defaultdict(list)

    issues = []
    missing_title   = []
    missing_desc    = []
    missing_h1      = []
    multiple_h1     = []
    missing_canonical = []
    orphan_faq_schema = []

    for fp in files:
        slug = os.path.basename(fp)
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except Exception as e:
            issues.append(f"READ ERROR {slug}: {e}")
            continue

        # title
        title = extract_tag(content, r"<title>(.*?)</title>")
        if not title:
            missing_title.append(slug)
        else:
            titles[title].append(slug)

        # meta description
        desc = extract_tag(content, r'<meta\s+name="description"\s+content="(.*?)"')
        if not desc:
            desc = extract_tag(content, r'<meta\s+content="(.*?)"\s+name="description"')
        if not desc:
            missing_desc.append(slug)
        else:
            descs[desc].append(slug)

        # H1
        h1_matches = re.findall(r"<h1[^>]*>(.*?)</h1>", content,
                                re.IGNORECASE | re.DOTALL)
        h1_clean = [re.sub(r"<[^>]+>", "", h).strip() for h in h1_matches]
        if not h1_clean:
            missing_h1.append(slug)
        elif len(h1_clean) > 1:
            multiple_h1.append((slug, len(h1_clean)))
        if h1_clean:
            h1s[h1_clean[0]].append(slug)

        # canonical
        if 'rel="canonical"' not in content and "rel='canonical'" not in content:
            missing_canonical.append(slug)

        # FAQ schema only if FAQ content present
        has_faq_schema = '"@type":"FAQPage"' in content or '"@type": "FAQPage"' in content
        has_faq_content = bool(re.search(r'<details|<summary|faq|FAQ', content))
        if has_faq_schema and not has_faq_content:
            orphan_faq_schema.append(slug)

    # duplicate detection
    dup_titles = {t: fs for t, fs in titles.items() if len(fs) > 1}
    dup_descs  = {d: fs for d, fs in descs.items() if len(fs) > 1}
    dup_h1s    = {h: fs for h, fs in h1s.items() if len(fs) > 1}

    return {
        "total_files": len(files),
        "missing_title": missing_title,
        "missing_desc": missing_desc,
        "missing_h1": missing_h1,
        "multiple_h1": multiple_h1,
        "missing_canonical": missing_canonical,
        "orphan_faq_schema": orphan_faq_schema,
        "dup_titles": dup_titles,
        "dup_descs": dup_descs,
        "dup_h1s": dup_h1s,
        "issues": issues,
    }


# ── Phase 4 — sitemap priority tuning ───────────────────────────────────────
SITEMAP_PATH = os.path.join(ROOT, "sitemap.xml")

PRIORITY_RULES = [
    # slug patterns -> priority (checked in order)
    (re.compile(r"^-hub\.html$"),                                          "1.0"),
    (re.compile(r"hub-san-diego\.html$"),                                  "0.9"),
    (re.compile(r"quote-review-san-diego\.html$"),                        "0.8"),
    (re.compile(r"quote-review-(carlsbad|encinitas|oceanside|la-jolla|chula-vista)\.html$"), "0.8"),
    (re.compile(r"html-sitemap\.html$"),                                   "0.6"),
    # generic service pages
    (re.compile(r"-san-diego\.html$"),                                     "0.7"),
]

def get_priority(url):
    # Extract slug from URL
    slug = url.rstrip("/").split("/")[-1]
    for pattern, priority in PRIORITY_RULES:
        if pattern.search(slug):
            return priority
    return None  # don't set if no rule matches


def phase4_sitemap():
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    def replace_url_block(m):
        block = m.group(0)
        loc_match = re.search(r"<loc>(.*?)</loc>", block)
        if not loc_match:
            return block
        url = loc_match.group(1)
        new_prio = get_priority(url)
        if new_prio is None:
            return block

        # Remove existing priority if present
        block = re.sub(r"<priority>[^<]*</priority>", "", block)
        # Insert priority after lastmod (if present) or after changefreq or after loc
        if "<changefreq>" in block:
            block = block.replace("</changefreq>",
                                  f"</changefreq><priority>{new_prio}</priority>", 1)
        elif "<lastmod>" in block:
            block = re.sub(r"(</lastmod>)",
                           rf"\1<priority>{new_prio}</priority>", block, count=1)
        else:
            block = block.replace("</loc>",
                                  f"</loc><priority>{new_prio}</priority>", 1)
        return block

    # Process each <url>...</url> block
    updated_content = re.sub(
        r"<url>.*?</url>",
        replace_url_block,
        content,
        flags=re.DOTALL
    )

    changed = content != updated_content
    if changed:
        with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
    return changed


# ── Report generation ────────────────────────────────────────────────────────
def write_report(robots_result, v):
    lines = []
    lines.append("=" * 70)
    lines.append("SHIP-014: Production Hygiene + Crawl Efficiency Report")
    lines.append(f"Generated: 2026-03-03  Root: {ROOT}")
    lines.append("=" * 70)

    lines.append("\n--- PHASE 1: robots.txt ---")
    lines.append(robots_result)

    lines.append("\n--- PHASE 2: HTML Validation Summary ---")
    lines.append(f"Total HTML files scanned: {v['total_files']}")
    lines.append(f"Missing <title>:       {len(v['missing_title'])}")
    lines.append(f"Missing meta desc:     {len(v['missing_desc'])}")
    lines.append(f"Missing H1:            {len(v['missing_h1'])}")
    lines.append(f"Multiple H1s:          {len(v['multiple_h1'])}")
    lines.append(f"Missing canonical:     {len(v['missing_canonical'])}")
    lines.append(f"Orphan FAQ schema:     {len(v['orphan_faq_schema'])}")

    if v['missing_title']:
        lines.append("\nMissing <title> (first 20):")
        for s in v['missing_title'][:20]:
            lines.append(f"  {s}")

    if v['missing_desc']:
        lines.append(f"\nMissing meta description (first 20 of {len(v['missing_desc'])}):")
        for s in v['missing_desc'][:20]:
            lines.append(f"  {s}")

    if v['missing_h1']:
        lines.append(f"\nMissing H1 (first 20 of {len(v['missing_h1'])}):")
        for s in v['missing_h1'][:20]:
            lines.append(f"  {s}")

    if v['multiple_h1']:
        lines.append(f"\nMultiple H1s (first 20 of {len(v['multiple_h1'])}):")
        for s, n in v['multiple_h1'][:20]:
            lines.append(f"  {s}  ({n} H1s)")

    if v['orphan_faq_schema']:
        lines.append(f"\nFAQ schema without FAQ content (first 10):")
        for s in v['orphan_faq_schema'][:10]:
            lines.append(f"  {s}")

    lines.append("\n--- PHASE 3: Duplicate Detection ---")
    lines.append(f"Duplicate <title> groups:    {len(v['dup_titles'])}")
    lines.append(f"Duplicate meta desc groups:  {len(v['dup_descs'])}")
    lines.append(f"Duplicate H1 groups:         {len(v['dup_h1s'])}")

    if v['dup_titles']:
        lines.append(f"\nDuplicate titles (top 30 groups, sorted by frequency):")
        for title, files in sorted(v['dup_titles'].items(),
                                    key=lambda x: -len(x[1]))[:30]:
            lines.append(f"  [{len(files)} pages] \"{title[:80]}\"")
            for f in sorted(files)[:5]:
                lines.append(f"    - {f}")
            if len(files) > 5:
                lines.append(f"    ... and {len(files)-5} more")

    if v['dup_h1s']:
        lines.append(f"\nDuplicate H1s (top 20 groups):")
        for h1, files in sorted(v['dup_h1s'].items(),
                                  key=lambda x: -len(x[1]))[:20]:
            lines.append(f"  [{len(files)} pages] \"{h1[:80]}\"")
            for f in sorted(files)[:4]:
                lines.append(f"    - {f}")
            if len(files) > 4:
                lines.append(f"    ... and {len(files)-4} more")

    lines.append("\n--- PHASE 4: Sitemap Priority Tuning ---")
    lines.append("Priority rules applied:")
    lines.append("  -hub.html (homepage):              1.0")
    lines.append("  *hub-san-diego.html:                0.9")
    lines.append("  *quote-review-san-diego.html:       0.8")
    lines.append("  *quote-review-[city].html:          0.8")
    lines.append("  html-sitemap.html:                  0.6")
    lines.append("  *-san-diego.html (general):         0.7")
    lines.append("sitemap.xml updated.")

    lines.append("\n--- END OF REPORT ---")
    report = "\n".join(lines)
    with open(REPORT_PATH, "w") as f:
        f.write(report)
    return report


def main():
    print("SHIP-014 Phase 1: robots.txt...")
    robots_result = phase1_robots()
    print(f"  {robots_result.splitlines()[0]}")

    print("SHIP-014 Phase 2+3: HTML validation...")
    v = validate_html_files()

    print("SHIP-014 Phase 4: Sitemap priority tuning...")
    sitemap_changed = phase4_sitemap()
    print(f"  sitemap.xml {'updated' if sitemap_changed else 'unchanged'}")

    print("Writing SHIP-014-report.txt...")
    report = write_report(robots_result, v)
    print("Done.")

    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total files: {v['total_files']}")
    print(f"Missing title: {len(v['missing_title'])}")
    print(f"Missing meta desc: {len(v['missing_desc'])}")
    print(f"Missing H1: {len(v['missing_h1'])}")
    print(f"Multiple H1s: {len(v['multiple_h1'])}")
    print(f"Dup title groups: {len(v['dup_titles'])}")
    print(f"Dup H1 groups: {len(v['dup_h1s'])}")


if __name__ == "__main__":
    main()
