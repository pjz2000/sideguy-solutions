#!/usr/bin/env python3
# ==============================================================
# SIDEGUY RELATED PROBLEMS GRAPH
# Adds a "Related Problems" pill row to each problems/*.html
# using token-overlap similarity on slug keywords.
# SAFE: only edits problems/*.html
# Idempotent via <!-- RELATED_PROBLEMS_START/END --> markers.
# ==============================================================

import os, re

PROBLEMS_DIR = "problems"
MAX_RELATED  = 6
MARKER_S     = "<!-- RELATED_PROBLEMS_START -->"
MARKER_E     = "<!-- RELATED_PROBLEMS_END -->"

STOPWORDS = {
    "for","and","the","a","an","to","of","in","on","with","without",
    "my","your","business","how","what","why","when","san","diego",
    "guide","explained","basics","simple",
}

def tokens(fn):
    slug = fn.replace(".html","").replace("_","-")
    return [p for p in slug.split("-") if p and p not in STOPWORDS]

def score(ta, tb):
    sa, sb = set(ta), set(tb)
    if not sa or not sb:
        return 0
    return len(sa & sb)

def pill_html(fn):
    title = " ".join(w.capitalize() for w in fn.replace(".html","").replace("-"," ").split())
    return (
        f'    <a href="/problems/{fn}" '
        f'style="display:inline-block;border:1px solid #d7f5ff;border-radius:999px;'
        f'padding:8px 14px;text-decoration:none;color:#073044;font-size:.84rem;'
        f'font-weight:500;background:rgba(255,255,255,.8)">{title}</a>'
    )

def inject_related(html, block_lines):
    block = "\n".join(block_lines) if block_lines else (
        '    <span style="color:#3f6173;font-size:.84rem">More guides coming soon.</span>'
    )
    section = (
        '\n<section style="margin-top:28px;padding-top:16px;border-top:2px solid #d7f5ff">'
        '\n  <h2 style="font-size:1.1rem;font-weight:800;margin-bottom:10px">Related Problems</h2>'
        '\n  <div style="display:flex;flex-wrap:wrap;gap:8px">'
        f'\n{MARKER_S}\n{block}\n{MARKER_E}'
        '\n  </div>'
        '\n</section>'
    )
    if MARKER_S in html and MARKER_E in html:
        return re.sub(
            re.escape(MARKER_S) + r".*?" + re.escape(MARKER_E),
            f"{MARKER_S}\n{block}\n{MARKER_E}",
            html, flags=re.S
        )
    anchor = "</main>" if "</main>" in html else "</body>"
    return html.replace(anchor, section + "\n" + anchor, 1)

if __name__ == "__main__":
    print("=== Related Problems Wiring ===\n")

    if not os.path.isdir(PROBLEMS_DIR):
        print("ERROR: problems/ dir not found"); exit(1)

    pages  = sorted(f for f in os.listdir(PROBLEMS_DIR) if f.endswith(".html") and f != "index.html")
    tok    = {p: tokens(p) for p in pages}
    changed = 0

    for p in pages:
        candidates = sorted(
            [(score(tok[p], tok[q]), q) for q in pages if q != p],
            reverse=True
        )
        rel = [q for sc, q in candidates if sc > 0][:MAX_RELATED]
        block_lines = [pill_html(fn) for fn in rel]

        path = os.path.join(PROBLEMS_DIR, p)
        html = open(path, "r", encoding="utf-8", errors="ignore").read()
        new  = inject_related(html, block_lines)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1

    print(f"  Related problems wired on {changed} pages")
