#!/usr/bin/env python3
"""
promote-reserve.py
──────────────────
Promotes pages from seo-reserve/ to the production root.

What it does per page:
  1. Fixes the HTML structure (content after </html> is moved inside <body>)
  2. Updates <title> and <meta description> if they're still template defaults
  3. Injects the sg2026 style block (aurora, glass2.0, shine, scroll-reveal)
  4. Injects a minimal FAQPage JSON-LD schema (if absent)
  5. Adds a <link rel="canonical"> (if absent)
  6. Skips pages that already exist in the production root (no overwrite)
  7. Skips seo-reserve/build-nothing-yet/ (policy)

Usage:
  python3 tools/seo-reserve/promote-reserve.py            # dry-run
  python3 tools/seo-reserve/promote-reserve.py --deploy   # write files
  python3 tools/seo-reserve/promote-reserve.py --deploy --limit 50
"""

import os, re, sys, argparse
from pathlib import Path
from datetime import date

REPO   = Path("/workspaces/sideguy-solutions")
RESERVE = REPO / "seo-reserve"
PROD   = REPO          # production root is the repo root

SKIP_DIRS  = {"build-nothing-yet"}
TEMPLATE_TITLE = "Who Do I Call? · SideGuy Solutions (San Diego)"
TEMPLATE_DESC  = "SideGuy is a human guidance layer for San Diego operators. One text. Clear options. Clarity before cost."
TODAY = date.today().strftime("%Y-%m-%d")

SG2026 = """
  <!-- SIDEGUY 2026 — Aurora · Glass 2.0 · Kinetic · Bento -->
  <style id="sg2026">
    :root{--ease-spring:cubic-bezier(.34,1.56,.64,1);--ease-smooth:cubic-bezier(.25,.46,.45,.94);--dur:.30s}
    @keyframes sg-aurora{0%{transform:translate(0,0) scale(1)}28%{transform:translate(1.8%,-1.2%) scale(1.04)}55%{transform:translate(-1.4%,1.8%) scale(.97)}82%{transform:translate(1.2%,.9%) scale(1.02)}100%{transform:translate(0,0) scale(1)}}
    body:before{animation:sg-aurora 26s ease-in-out infinite;background:radial-gradient(closest-side at 15% 18%,rgba(33,211,161,.30),transparent 56%),radial-gradient(closest-side at 80% 24%,rgba(74,169,255,.26),transparent 52%),radial-gradient(closest-side at 55% 76%,rgba(0,199,255,.24),transparent 56%),radial-gradient(closest-side at 22% 86%,rgba(33,211,161,.16),transparent 58%),radial-gradient(closest-side at 90% 70%,rgba(100,130,255,.12),transparent 50%);filter:blur(24px)}
    body:after{content:"";position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.68' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E");opacity:.028;pointer-events:none;z-index:998;mix-blend-mode:overlay}
    @keyframes sg-grad{0%,100%{background-position:0% 50%}50%{background-position:200% 50%}}
    h1{font-size:clamp(28px,5.6vw,56px) !important;letter-spacing:-.035em;line-height:1.01;background:linear-gradient(135deg,var(--ink,#073044) 0%,#0c5f78 28%,var(--mint,#21d3a1) 58%,var(--mint2,#00c7ff) 82%,var(--blue,#4aa9ff) 100%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;animation:sg-grad 14s ease-in-out infinite}
    @media(max-width:520px){h1{font-size:clamp(24px,8vw,36px) !important}}
    .card{background:linear-gradient(155deg,rgba(255,255,255,.84),rgba(255,255,255,.60));border:1px solid rgba(255,255,255,.74);border-radius:22px;backdrop-filter:blur(22px) saturate(168%);-webkit-backdrop-filter:blur(22px) saturate(168%);box-shadow:0 2px 0 rgba(255,255,255,.84) inset,0 16px 44px rgba(7,48,68,.09),0 0 0 1px rgba(33,211,161,.08);transition:transform var(--dur) var(--ease-spring),box-shadow var(--dur) ease;will-change:transform;min-height:140px}
    .card:hover{transform:translateY(-5px) scale(1.016);box-shadow:0 2px 0 rgba(255,255,255,.94) inset,0 32px 68px rgba(7,48,68,.13),0 0 0 1px rgba(33,211,161,.24)}
    @keyframes sg-shine{from{background-position:-200% center}to{background-position:200% center}}
    .btn{background:linear-gradient(100deg,var(--mint,#21d3a1) 0%,var(--mint2,#00c7ff) 28%,#b8fdef 54%,var(--mint2,#00c7ff) 72%,var(--mint,#21d3a1) 100%);background-size:250% 100%;animation:sg-shine 3.8s linear infinite;box-shadow:0 0 0 1px rgba(255,255,255,.55) inset,0 24px 52px rgba(0,199,255,.28);padding:13px 24px;font-size:13px;font-weight:900;letter-spacing:.01em;transition:transform var(--dur) var(--ease-spring),box-shadow var(--dur) ease}
    .btn:hover{transform:translateY(-2px) scale(1.04);box-shadow:0 0 0 1px rgba(255,255,255,.75) inset,0 32px 68px rgba(0,199,255,.38)}
    .bigCta{background:linear-gradient(135deg,rgba(33,211,161,.13) 0%,rgba(255,255,255,.62) 42%,rgba(0,199,255,.11) 100%);border:1px solid rgba(33,211,161,.22);border-radius:28px;padding:26px 24px;box-shadow:0 2px 0 rgba(255,255,255,.92) inset,0 28px 72px rgba(7,48,68,.10);backdrop-filter:blur(22px) saturate(152%);-webkit-backdrop-filter:blur(22px) saturate(152%)}
    .noteCard{background:linear-gradient(135deg,rgba(33,211,161,.07),rgba(0,199,255,.06));border:1px solid rgba(33,211,161,.22);border-radius:22px;backdrop-filter:blur(20px) saturate(148%);-webkit-backdrop-filter:blur(20px) saturate(148%);padding:16px 20px;font-size:13px;line-height:1.62}
    .floatBtn{width:60px;height:60px;box-shadow:0 0 0 4px rgba(255,255,255,.96),0 30px 76px rgba(0,199,255,.32);transition:transform var(--dur) var(--ease-spring),box-shadow var(--dur) ease}
    .floatBtn:hover{transform:scale(1.1);box-shadow:0 0 0 5px rgba(255,255,255,.98),0 38px 92px rgba(0,199,255,.42)}
    .sg-reveal{opacity:0;transform:translateY(20px);transition:opacity .60s ease,transform .60s var(--ease-smooth)}
    .sg-reveal.sg-in{opacity:1;transform:translateY(0)}
  </style>
  <script>
    (function(){var io=new IntersectionObserver(function(e){e.forEach(function(x){if(x.isIntersecting){x.target.classList.add('sg-in');io.unobserve(x.target)}})},{threshold:.10,rootMargin:'0px 0px -40px 0px'});document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.card,.bigCta,.noteCard').forEach(function(el){el.classList.add('sg-reveal');io.observe(el)})})})();
  </script>
"""

FAQ_SCHEMA_TPL = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "What is {topic}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "SideGuy explains {topic} in plain language for San Diego business owners and homeowners. Clarity before cost — text PJ at 773-544-1231 for direct human guidance."
      }}
    }},
    {{
      "@type": "Question",
      "name": "How does {topic} affect San Diego businesses?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Local businesses in San Diego may encounter {topic} when making decisions about services, technology, or home systems. SideGuy helps you understand your options before spending money."
      }}
    }}
  ]
}}
</script>'''


def slug_to_title(slug: str) -> str:
    """Convert filename slug to a readable title."""
    name = slug.replace(".html", "").replace("-", " ").replace("_", " ")
    return name.title() + " · SideGuy Solutions (San Diego)"


def slug_to_topic(slug: str) -> str:
    return slug.replace(".html", "").replace("-", " ").replace("_", " ")


def fix_structure(html: str) -> str:
    """Move any content that was appended after </html> back inside <body>."""
    html_close = html.rfind("</html>")
    if html_close == -1:
        return html
    after = html[html_close + 7:].strip()
    if not after:
        return html
    body_close = html.rfind("</body>", 0, html_close)
    if body_close == -1:
        return html
    # Insert orphaned content before </body>
    return html[:body_close] + "\n" + after + "\n</body>\n</html>"


def inject_sg2026(html: str) -> str:
    """Add sg2026 block before </head> if not already present."""
    if 'id="sg2026"' in html:
        return html
    return html.replace("</head>", SG2026 + "\n</head>", 1)


def fix_title(html: str, slug: str) -> str:
    """Replace template title/description with topic-specific ones."""
    title = slug_to_title(slug)
    topic = slug_to_topic(slug)
    desc = f"SideGuy explains {topic} for San Diego business owners and homeowners. Clarity before cost. Real human help at 773-544-1231."[:155]

    # Title
    if TEMPLATE_TITLE in html:
        html = html.replace(TEMPLATE_TITLE, title, 1)
    # Meta description
    if TEMPLATE_DESC in html:
        html = html.replace(TEMPLATE_DESC, desc, 1)
    return html


def inject_schema(html: str, slug: str) -> str:
    """Add FAQPage JSON-LD if absent."""
    if "FAQPage" in html:
        return html
    topic = slug_to_topic(slug)
    schema = FAQ_SCHEMA_TPL.format(topic=topic)
    return html.replace("</head>", schema + "\n</head>", 1)


def inject_canonical(html: str, slug: str) -> str:
    """Add canonical link if absent."""
    if 'rel="canonical"' in html:
        return html
    canonical = f'<link rel="canonical" href="https://sideguysolutions.com/{slug}"/>'
    return html.replace("</head>", canonical + "\n</head>", 1)


def inject_robots(html: str) -> str:
    """Ensure index/follow (remove noindex if present)."""
    if 'noindex' in html:
        html = html.replace(
            '<meta name="robots" content="noindex, nofollow">',
            '<meta name="robots" content="index, follow, max-image-preview:large"/>'
        )
        html = html.replace(
            'content="noindex, nofollow"',
            'content="index, follow, max-image-preview:large"'
        )
    if 'name="robots"' not in html:
        html = html.replace(
            "<head>",
            '<head>\n<meta name="robots" content="index, follow, max-image-preview:large"/>',
            1
        )
    return html


def promote_page(src: Path, dry_run: bool = True) -> dict:
    slug = src.name
    dest = PROD / slug
    result = {"src": str(src), "dest": str(dest), "slug": slug, "action": None, "reason": None}

    if dest.exists():
        result["action"] = "skip"
        result["reason"] = "already exists in production"
        return result

    try:
        html = src.read_text(errors="ignore")
    except Exception as e:
        result["action"] = "error"
        result["reason"] = str(e)
        return result

    # Apply all upgrades
    html = fix_structure(html)
    html = fix_title(html, slug)
    html = inject_robots(html)
    html = inject_canonical(html, slug)
    html = inject_schema(html, slug)
    html = inject_sg2026(html)

    if not dry_run:
        dest.write_text(html, encoding="utf-8")

    result["action"] = "deploy" if not dry_run else "would_deploy"
    return result


def main():
    parser = argparse.ArgumentParser(description="Promote SEO reserve pages to production")
    parser.add_argument("--deploy", action="store_true", help="Actually write files (default: dry-run)")
    parser.add_argument("--limit", type=int, default=0, help="Max pages to process (0 = all)")
    parser.add_argument("--dir", default="", help="Only process a specific subdirectory (e.g. prediction-markets)")
    args = parser.parse_args()

    dry_run = not args.deploy

    print("")
    print("=" * 50)
    print("SideGuy Promote Reserve")
    print(f"Mode: {'DRY RUN' if dry_run else 'DEPLOYING'}")
    print("=" * 50)
    print("")

    pages = []
    search_root = RESERVE / args.dir if args.dir else RESERVE
    for root, dirs, files in os.walk(search_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                pages.append(Path(root) / f)

    if args.limit:
        pages = pages[:args.limit]

    deployed = skipped = errors = 0

    for page in pages:
        r = promote_page(page, dry_run=dry_run)
        if r["action"] == "skip":
            skipped += 1
        elif r["action"] == "error":
            errors += 1
            print(f"  ERROR  {r['slug']}: {r['reason']}")
        else:
            deployed += 1
            verb = "DEPLOY" if not dry_run else "WOULD"
            print(f"  {verb}  {r['slug']}")

    print("")
    print(f"  {'Deployed' if not dry_run else 'Would deploy'}: {deployed}")
    print(f"  Skipped (exists): {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total reserve pages: {len(pages)}")
    print("")
    if dry_run and deployed > 0:
        print("  Run with --deploy to actually write files.")
    print("")


if __name__ == "__main__":
    main()
