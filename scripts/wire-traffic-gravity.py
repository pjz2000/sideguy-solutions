#!/usr/bin/env python3
"""
SideGuy Wire Traffic Gravity
Reads site pages, builds a topic-similarity link graph, and injects a
"Top Guides" block into high-value content pages.
Idempotent (marker-based). Skips hubs/ and problems/multiplied bulk dirs.
"""
import os, re, json
from pathlib import Path
from datetime import datetime

ROOT = Path(".").resolve()

PHONE_SMS  = "sms:+17735441231"
PHONE_DISP = "773-544-1231"

# Dirs to WIRE links INTO (high-value, not bulk link-dump pages)
WIRE_DIRS = [
    "pillars", "concepts", "authority", "longtail",
    "decisions", "katie", "generated", "clusters",
]

# Dirs to USE as link sources (pages to link TO)
SOURCE_DIRS = [
    "pillars", "concepts", "authority", "longtail",
    "decisions", "katie", "generated", "clusters",
    "prediction-markets",
]

MAX_LINKS_PER_PAGE = int(os.getenv("PER_PAGE", "8"))
DRY_RUN            = os.getenv("DRY_RUN", "0") == "1"

MARKER_START = "<!-- SG_TOPGUIDES_START -->"
MARKER_END   = "<!-- SG_TOPGUIDES_END -->"

# ── Stop-words for keyword extraction ────────────────────────────────────────
STOP = {
    "the","a","an","and","or","for","in","on","of","to","with","how","what",
    "when","why","is","are","was","were","vs","san","diego","sideguy","html",
    "solutions","guide","page","index","hub","you","your","not","do",
}


def extract_title(html: str) -> str:
    m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    if m:
        return m.group(1).strip()
    m2 = re.search(r"<h1[^>]*>([^<]+)</h1>", html, re.I)
    return m2.group(1).strip() if m2 else ""


def title_tokens(title: str) -> set[str]:
    tl = title.lower()
    tl = re.sub(r"[^a-z0-9\s]", " ", tl)
    return {t for t in tl.split() if t and t not in STOP and len(t) > 2}


def slug_tokens(slug: str) -> set[str]:
    """Extract keywords from a file slug."""
    s = slug.replace(".html", "").replace("-", " ")
    return {t for t in s.split() if t and t not in STOP and len(t) > 2}


def similarity(ta: set, tb: set) -> float:
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta | tb), 1)


def has_marker(html: str) -> bool:
    return MARKER_START in html


def inject_or_replace(html: str, block: str) -> str:
    if has_marker(html):
        # Replace existing block
        pattern = re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END)
        return re.sub(pattern, block, html, flags=re.DOTALL)
    # Inject before </body>
    if "</body>" in html:
        return html.replace("</body>", f"\n{block}\n</body>", 1)
    return html + "\n" + block


def build_block(links: list[tuple[str, str]]) -> str:
    """links: list of (href, label)"""
    items = "\n".join(
        f'    <a class="sgtg-pill" href="{href}">{label}</a>'
        for href, label in links
    )
    updated = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""{MARKER_START}
<section class="sgtg-block" aria-label="Top Guides">
  <style>
  .sgtg-block{{margin:28px 0 12px;padding:18px 20px;border-radius:16px;
    border:1px solid rgba(7,48,68,.10);background:rgba(255,255,255,.55);}}
  .sgtg-block h3{{margin:0 0 10px;font-size:16px;color:#073044;}}
  .sgtg-pills{{display:flex;flex-wrap:wrap;gap:8px;}}
  .sgtg-pill{{display:inline-block;border:1px solid rgba(7,48,68,.12);
    border-radius:999px;padding:7px 14px;font-size:13px;color:#073044;
    text-decoration:none;background:#fff;}}
  .sgtg-pill:hover{{background:#eefcff;text-decoration:none;}}
  .sgtg-cta{{margin-top:12px;font-size:13px;color:#3f6173;}}
  .sgtg-cta a{{color:#1f7cff;}}
  </style>
  <h3>Top Guides</h3>
  <div class="sgtg-pills">
{items}
  </div>
  <p class="sgtg-cta">Not finding what you need? <a href="{PHONE_SMS}">Text PJ · {PHONE_DISP}</a></p>
  <!-- updated:{updated} -->
</section>
{MARKER_END}"""


def collect_sources() -> list[dict]:
    """Collect all linkable source pages with title + tokens."""
    sources = []
    for d in SOURCE_DIRS:
        dirpath = ROOT / d
        if not dirpath.is_dir():
            continue
        for f in dirpath.glob("*.html"):
            if f.name == "index.html":
                continue
            try:
                html = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            title = extract_title(html)
            if not title:
                title = f.stem.replace("-", " ").title()
            tokens = title_tokens(title) | slug_tokens(f.stem)
            rel = str(f.relative_to(ROOT))
            sources.append({
                "path": rel,
                "href": "/" + rel,
                "title": title,
                "tokens": tokens,
            })
    return sources


def main():
    sources = collect_sources()
    print(f"  Sources indexed: {len(sources)}")

    wired   = 0
    skipped = 0

    for d in WIRE_DIRS:
        dirpath = ROOT / d
        if not dirpath.is_dir():
            continue
        pages = list(dirpath.glob("*.html"))
        for fp in pages:
            if fp.name == "index.html":
                continue
            try:
                html = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            title  = extract_title(html)
            my_tok = title_tokens(title) | slug_tokens(fp.stem)
            my_rel = str(fp.relative_to(ROOT))

            # Score all sources by similarity, exclude self
            ranked = []
            for s in sources:
                if s["path"] == my_rel:
                    continue
                score = similarity(my_tok, s["tokens"])
                if score > 0:
                    ranked.append((score, s["href"], s["title"]))

            ranked.sort(reverse=True)
            top    = ranked[:MAX_LINKS_PER_PAGE]

            if not top:
                skipped += 1
                continue

            links = [(href, lbl) for _, href, lbl in top]
            block = build_block(links)

            if DRY_RUN:
                print(f"  DRY: would wire {len(links)} links into {my_rel}")
                wired += 1
                continue

            new_html = inject_or_replace(html, block)
            if new_html == html:
                skipped += 1
                continue

            fp.write_text(new_html, encoding="utf-8")
            wired += 1

    print(f"  Wired  : {wired} pages")
    print(f"  Skipped: {skipped} (no matches or already current)")

    # Write a simple report
    report = {
        "ran_at":    datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dry_run":   DRY_RUN,
        "sources":   len(sources),
        "wired":     wired,
        "skipped":   skipped,
        "wire_dirs": WIRE_DIRS,
    }
    (ROOT / "reports" / "wire-traffic-gravity.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
