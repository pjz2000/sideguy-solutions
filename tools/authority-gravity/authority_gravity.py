#!/usr/bin/env python3
"""
Authority Gravity — read-only link equity audit.
Scans root HTML files, scores each page by inbound/outbound
internal links and word count, writes a ranked TSV report.
Does not modify any files.
"""
import os, re
from collections import Counter

ROOT = "/workspaces/sideguy-solutions"
OUT_DIR = os.path.join(ROOT, "docs/authority-gravity")
IGNORE = {"index.html", "404.html"}


def html_files():
    return sorted(
        os.path.join(ROOT, f)
        for f in os.listdir(ROOT)
        if f.endswith(".html") and f not in IGNORE
    )


LINK_RE = re.compile(r'href=["\']([^"\']{1,200})["\']', re.I)


def extract_links(html):
    return LINK_RE.findall(html)


def normalize(link):
    link = link.split("#")[0].split("?")[0]
    return link.lstrip("/")


def is_internal(link):
    if link.startswith("http"):
        return "sideguysolutions.com" in link
    return link.endswith(".html") or link.startswith("/")


def analyze():
    files = html_files()
    data = {}
    outlinks = {}
    incoming = Counter()

    for path in files:
        # Read only – no strip, no word count regex on full file
        try:
            raw = open(path, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            raw = ""
        slug = os.path.basename(path)
        # File size proxy: pages >12KB of HTML likely have >800 real words
        large = len(raw) > 12_000
        ls = [normalize(l) for l in extract_links(raw) if is_internal(l)]
        data[slug] = {"large": large, "out": len(ls)}
        outlinks[slug] = ls

    for src, ls in outlinks.items():
        for l in ls:
            base = os.path.basename(l)
            if base in data:
                incoming[base] += 1

    rows = []
    for slug, info in data.items():
        score = incoming.get(slug, 0) * 4 + info["out"] * 2
        if info["large"]:
            score += 10
        rows.append({
            "page": slug,
            "size": "large" if info["large"] else "small",
            "out": info["out"],
            "in": incoming.get(slug, 0),
            "score": score,
        })

    rows.sort(key=lambda x: (-x["score"], -x["in"]))

    os.makedirs(OUT_DIR, exist_ok=True)
    tsv = os.path.join(OUT_DIR, "authority-gravity.tsv")
    with open(tsv, "w") as f:
        f.write("score\tin\tout\tsize\tpage\n")
        for r in rows:
            f.write(f"{r['score']}\t{r['in']}\t{r['out']}\t{r['size']}\t{r['page']}\n")

    print(f"Authority report written: {tsv}")
    print(f"Pages analyzed: {len(rows)}")


if __name__ == "__main__":
    analyze()
