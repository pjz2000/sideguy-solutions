#!/usr/bin/env python3
"""
inject-faq-schema.py

Scans root-level HTML pages for question-like H2/H3 headings,
extracts the answer from the following paragraph, and injects
FAQPage JSON-LD structured data before </head>.

Idempotent — skips pages already containing FAQPage schema.

Usage:
  python3 tools/upgrades/inject-faq-schema.py --dry-run
  python3 tools/upgrades/inject-faq-schema.py --run
  python3 tools/upgrades/inject-faq-schema.py --run --limit=1000
"""

import os
import re
import json
import sys
from pathlib import Path

ROOT = Path(
    os.popen("git rev-parse --show-toplevel 2>/dev/null || pwd").read().strip()
)

QUESTION_RE = re.compile(
    r'^(what|how|why|when|is|can|do|are|will|should|which|who|where)\b',
    re.IGNORECASE
)

H_TAG_RE = re.compile(r'<h[23][^>]*>(.*?)</h[23]>', re.IGNORECASE | re.DOTALL)
P_TAG_RE  = re.compile(r'<p[^>]*>(.*?)</p>',        re.IGNORECASE | re.DOTALL)


def strip_tags(html: str) -> str:
    text = re.sub(r'<[^>]+>', '', html)
    text = (text
            .replace('&amp;', '&')
            .replace('&lt;', '<')
            .replace('&gt;', '>')
            .replace('&#39;', "'")
            .replace('&quot;', '"')
            .replace('&nbsp;', ' '))
    return ' '.join(text.split()).strip()


def extract_faqs(content: str) -> list:
    faqs = []
    for m in H_TAG_RE.finditer(content):
        heading = strip_tags(m.group(1))
        if not QUESTION_RE.match(heading):
            continue
        rest = content[m.end():]
        p = P_TAG_RE.search(rest)
        if not p:
            continue
        answer = strip_tags(p.group(1))
        if len(answer) < 30:
            continue
        if len(answer) > 320:
            answer = answer[:317] + '...'
        faqs.append({
            "@type": "Question",
            "name": heading,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": answer
            }
        })
        if len(faqs) >= 5:
            break
    return faqs


def build_schema_block(faqs: list) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs
    }
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(schema, indent=2, ensure_ascii=False)
        + '\n</script>'
    )


def process_file(filepath: Path, dry_run: bool) -> str:
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return 'error'

    if 'FAQPage' in content:
        return 'skip-already-has-schema'

    if '</head>' not in content:
        return 'skip-no-head'

    faqs = extract_faqs(content)
    if not faqs:
        return 'skip-no-questions'

    schema_block = build_schema_block(faqs)
    new_content = content.replace('</head>', f'{schema_block}\n</head>', 1)

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return 'updated'


def main():
    dry_run = '--dry-run' in sys.argv
    live    = '--run' in sys.argv

    if not dry_run and not live:
        print("Usage:")
        print("  python3 tools/upgrades/inject-faq-schema.py --dry-run")
        print("  python3 tools/upgrades/inject-faq-schema.py --run")
        print("  python3 tools/upgrades/inject-faq-schema.py --run --limit=1000")
        sys.exit(1)

    limit = None
    for arg in sys.argv[1:]:
        if arg.startswith('--limit='):
            limit = int(arg.split('=')[1])

    mode = 'DRY RUN' if dry_run else 'LIVE'
    print(f"inject-faq-schema.py — {mode}")
    print(f"Root: {ROOT}")
    if limit:
        print(f"Limit: {limit} updates")
    print()

    pages = sorted(ROOT.glob('*.html'))

    counts = {
        'updated': 0,
        'skip-already-has-schema': 0,
        'skip-no-head': 0,
        'skip-no-questions': 0,
        'error': 0,
    }

    for page in pages:
        if limit and counts['updated'] >= limit:
            break

        result = process_file(page, dry_run=dry_run)
        counts[result] = counts.get(result, 0) + 1

        if result == 'updated':
            print(f"{'[DRY] ' if dry_run else ''}FAQ schema → {page.name}")

    print()
    print("Results:")
    print(f"  Schema injected:     {counts['updated']}")
    print(f"  Already had schema:  {counts['skip-already-has-schema']}")
    print(f"  No question headers: {counts['skip-no-questions']}")
    print(f"  No </head>:          {counts['skip-no-head']}")
    print(f"  Errors:              {counts['error']}")
    print()
    if dry_run and counts['updated'] > 0:
        print("Re-run with --run to apply changes.")


if __name__ == '__main__':
    main()
