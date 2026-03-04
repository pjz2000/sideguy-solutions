#!/usr/bin/env python3
# ==============================================================
# SIDEGUY KNOWLEDGE GRAPH BUILDER
# Cross-links related pages across auto/, concepts/, clusters/,
# pillars/, generated/ using slug-token similarity.
# NOTE: Skips problems/ (already has Related Problems + Router).
# Idempotent: won't touch a page that already has Related Guides.
# ==============================================================

import os, re

CONTENT_DIRS = ["auto", "concepts", "clusters", "pillars", "generated"]
MAX_LINKS    = 6
STOPWORDS    = {
    "for","and","the","a","an","to","of","in","on","with","without","my","your",
    "business","san","diego","guide","how","what","why","when","explained","basics",
    "simple","html","index",
}
MARKER_TEXT  = "<!-- KGB_LINKS -->"

def slug_words(path: str) -> set:
    fn = os.path.basename(path).replace(".html", "").replace("_", "-")
    return {p for p in fn.split("-") if p and p not in STOPWORDS}

def collect_pages() -> list:
    pages = []
    for d in CONTENT_DIRS:
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".html") and f not in ("index.html",):
                pages.append(f"{d}/{f}")
    return sorted(pages)

def score(a: str, b: str) -> int:
    return len(slug_words(a) & slug_words(b))

def best_related(page: str, pages: list) -> list:
    candidates = sorted(
        [(score(page, q), q) for q in pages if q != page],
        reverse=True
    )
    return [p for sc, p in candidates if sc > 0][:MAX_LINKS]

def link_block(links: list) -> str:
    items = ""
    for l in links:
        name = os.path.basename(l).replace(".html","").replace("-"," ").title()
        items += (
            f'  <a href="/{l}" style="display:inline-block;border:1px solid #d7f5ff;'
            f'border-radius:999px;padding:7px 14px;text-decoration:none;color:#073044;'
            f'font-size:.84rem;font-weight:500;background:rgba(255,255,255,.8)">{name}</a>\n'
        )
    return items.rstrip()

def inject(html: str, links: list) -> str | None:
    if "Related Guides" in html:
        return None  # already wired
    block = link_block(links)
    section = (
        f'\n<section style="margin-top:26px;padding-top:14px;border-top:2px solid #d7f5ff">'
        f'\n<h2 style="font-size:1.05rem;font-weight:800;margin-bottom:10px">Related Guides</h2>'
        f'\n<div style="display:flex;flex-wrap:wrap;gap:8px">'
        f'\n{MARKER_TEXT}\n{block}\n</div>'
        f'\n</section>'
    )
    anchor = "</main>" if "</main>" in html else "</body>"
    return html.replace(anchor, section + "\n" + anchor, 1)

if __name__ == "__main__":
    print("=== Knowledge Graph Builder ===\n")

    pages = collect_pages()
    print(f"  Pages found: {len(pages)}")

    changed = 0
    for page in pages:
        links = best_related(page, pages)
        if not links:
            continue
        try:
            html = open(page, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        new = inject(html, links)
        if new is None:
            continue  # already has Related Guides
        open(page, "w", encoding="utf-8").write(new)
        changed += 1

    print(f"  Related Guides added to: {changed} pages")
    print(f"  (pages already wired were skipped)")
