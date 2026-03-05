#!/usr/bin/env python3
"""
SideGuy Radar Page Builder
----------------------------
Reads docs/problem-radar/RADAR_QUEUE.md and builds a properly styled SideGuy
HTML page for each seed topic that doesn't already have a matching file.

Output: public/auto-pages/<slug>.html

Skips seeds that:
  - Are raw URLs (http/https)
  - Are cluster headers (## lines)
  - Already have a matching HTML file anywhere in the repo

Styling matches the SideGuy inline-CSS pattern: mint gradient, --ink #073044.
"""

import glob
import os
import re
from pathlib import Path

ROOT      = Path(__file__).parent.parent.parent.resolve()
QUEUE_MD  = ROOT / "docs" / "problem-radar" / "RADAR_QUEUE.md"
OUT_DIR   = ROOT / "public" / "auto-pages"
PHONE     = "773-544-1231"
SMS       = "sms:+17735441231"

SKIP_DIRS = {".git", "_quarantine_backups", "node_modules"}

def skip_path(p: str) -> bool:
    return any(f"/{d}/" in f"/{p.replace(os.sep, '/')}/" for d in SKIP_DIRS)

# ── Parse seeds from RADAR_QUEUE.md ──────────────────────────────────────────
def parse_seeds(md_path: Path) -> list[tuple[str, str]]:
    """Returns list of (topic, pillar) tuples parsed from seed bullet lines."""
    if not md_path.exists():
        return []

    seeds = []
    current_pillar = "general"
    pillar_re  = re.compile(r"\*\*Pillar:\*\*\s*`([^`]+)`")
    seed_re    = re.compile(r"^[-*]\s+`(.+?)`")     # - `topic` — note
    url_re     = re.compile(r"^https?")

    for line in md_path.read_text(encoding="utf-8").splitlines():
        pm = pillar_re.search(line)
        if pm:
            current_pillar = pm.group(1)
            continue
        sm = seed_re.match(line.strip())
        if sm:
            raw = sm.group(1).strip()
            # Skip raw URLs and very short strings
            if url_re.match(raw) or len(raw) < 6:
                continue
            # Strip trailing " — note" annotations
            topic = re.sub(r"\s+[—–-].*$", "", raw).strip()
            if topic:
                seeds.append((topic, current_pillar))
    return seeds

# ── Build URL slug ────────────────────────────────────────────────────────────
def slugify(topic: str) -> str:
    slug = topic.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-{2,}", "-", slug)
    return slug[:120]

# ── Check if a similar page already exists repo-wide ─────────────────────────
def build_existing_slugs() -> set[str]:
    slugs = set()
    for p in glob.glob(str(ROOT / "**" / "*.html"), recursive=True):
        if skip_path(p):
            continue
        name = os.path.basename(p).replace(".html", "").lower()
        slugs.add(name)
    return slugs

# ── Page template ─────────────────────────────────────────────────────────────
def make_page(topic: str, pillar: str, slug: str) -> str:
    title_case = topic.title()
    canonical  = f"https://sideguysolutions.com/auto/{slug}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title_case} — San Diego Guide · SideGuy Solutions</title>
<meta name="description" content="SideGuy guide: {topic} — plain-language breakdown for San Diego small businesses. What it means, what it costs, and what to do next.">
<link rel="canonical" href="{canonical}">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_case}",
  "description": "Plain-language guide to {topic} for San Diego small businesses.",
  "url": "{canonical}",
  "author": {{"@type": "Organization", "name": "SideGuy Solutions"}}
}}
</script>
<style>
:root{{--bg0:#eefcff;--ink:#073044;--mint:#21d3a1;--dim:#3f6173;--border:rgba(7,48,68,.1)}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,system-ui,"Segoe UI",Roboto,Inter,sans-serif;background:radial-gradient(ellipse 100% 60% at 50% 0%,#d0f7f0 0%,var(--bg0) 60%);color:var(--ink);min-height:100vh;padding-bottom:60px}}
header{{padding:20px 24px 0;max-width:800px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}}
.brand{{font-size:1.05rem;font-weight:700;color:var(--ink);text-decoration:none}}.brand span{{color:var(--mint)}}
.cta{{background:var(--mint);color:var(--ink);font-weight:700;font-size:.85rem;padding:9px 20px;border-radius:999px;text-decoration:none;white-space:nowrap}}
main{{max-width:800px;margin:0 auto;padding:36px 24px 0}}
.breadcrumb{{font-size:.78rem;color:var(--dim);margin-bottom:24px}}.breadcrumb a{{color:var(--dim);text-decoration:underline}}
h1{{font-size:clamp(1.5rem,4vw,2.1rem);font-weight:800;line-height:1.2;letter-spacing:-.02em;margin-bottom:12px}}
.pillar-tag{{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;background:rgba(33,211,161,.15);color:#0a6450;border-radius:999px;padding:3px 10px;margin-bottom:18px}}
section{{margin-top:28px}}
h2{{font-size:1.15rem;font-weight:800;margin-bottom:10px}}
p,li{{font-size:.97rem;line-height:1.7;color:var(--ink)}}
ul{{margin:8px 0 0 20px}}
.card-cta{{background:var(--ink);color:#fff;border-radius:16px;padding:28px 24px;margin-top:40px;text-align:center}}
.card-cta h2{{color:#fff;font-size:1.25rem;margin-bottom:8px}}
.card-cta p{{color:rgba(255,255,255,.75);margin-bottom:18px}}
.card-cta a{{color:var(--mint);font-weight:700;text-decoration:none}}
footer{{text-align:center;font-size:.78rem;color:var(--dim);padding:40px 24px 0}}
footer a{{color:var(--dim)}}
</style>
</head>
<body>
<header>
  <a class="brand" href="/">Side<span>Guy</span> Solutions</a>
  <a class="cta" href="{SMS}">Text PJ · {PHONE}</a>
</header>
<main>
  <nav class="breadcrumb"><a href="/">Home</a> › <a href="/auto/">Guides</a> › {title_case}</nav>
  <span class="pillar-tag">{pillar.replace("-", " ")}</span>
  <h1>{title_case} — San Diego Guide</h1>

  <section>
    <h2>Overview</h2>
    <p>This guide explains <strong>{topic}</strong> in plain language — what it means,
    why it matters to San Diego small businesses, and what to do about it.</p>
  </section>

  <section>
    <h2>Typical Cost</h2>
    <p>Costs vary based on scope, provider, and your current setup.
    This page outlines typical ranges and the factors that drive prices
    up or down — so you're not guessing going into a conversation.</p>
  </section>

  <section>
    <h2>Common Mistakes</h2>
    <ul>
      <li>Moving too fast before understanding the full picture</li>
      <li>Choosing based on price alone instead of fit</li>
      <li>Not asking the right questions before committing</li>
      <li>Underestimating setup time and ongoing costs</li>
    </ul>
  </section>

  <section>
    <h2>Quick Checklist</h2>
    <ul>
      <li>Clarify your actual goal — what outcome do you need?</li>
      <li>List your current tools and constraints</li>
      <li>Compare at least two options before deciding</li>
      <li>Estimate total cost including setup and recurring fees</li>
      <li>Plan a small test before full rollout</li>
    </ul>
  </section>

  <div class="card-cta">
    <h2>Want a human to look at your situation?</h2>
    <p>No forms. No sales pitch. Just a real answer from someone who's seen this before.</p>
    <a href="{SMS}">Text PJ → {PHONE}</a>
  </div>
</main>
<footer>
  <p>SideGuy Solutions · San Diego, CA · <a href="/">Home</a> · <a href="/tools/">Tools</a></p>
  <p style="margin-top:6px">Clarity before cost. Always.</p>
</footer>
</body>
</html>
"""

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    seeds = parse_seeds(QUEUE_MD)
    if not seeds:
        print(f"No seeds found in {QUEUE_MD.relative_to(ROOT)}")
        return

    existing = build_existing_slugs()
    built = skipped = 0

    for topic, pillar in seeds:
        slug = slugify(topic)
        if not slug:
            continue
        out_path = OUT_DIR / f"{slug}.html"
        # Skip if an exact slug match already exists anywhere in the repo
        if slug in existing or out_path.exists():
            skipped += 1
            continue
        out_path.write_text(make_page(topic, pillar, slug), encoding="utf-8")
        built += 1

    print(f"Radar page builder complete")
    print(f"  Seeds parsed : {len(seeds)}")
    print(f"  Pages built  : {built}")
    print(f"  Skipped      : {skipped} (already exist)")
    print(f"  Output dir   : {OUT_DIR.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
