#!/usr/bin/env python3
"""
SIDEGUY REPUTATION GRAVITY ENGINE
Turns strong pages into authority flywheels.

Walks all HTML pages, builds an inbound-link count for every page using
a suffix-index O(pages + links) lookup — safe on 14k+ page sites.

Skips: hubs/, problems/multiplied/, sitemaps/, .git/, reports/, map/
Output: data/reputation-gravity.json
"""

import os
import re
import json
import datetime
from collections import defaultdict, Counter

ROOT = "."
OUT  = "data/reputation-gravity.json"
SITE = "https://sideguysolutions.com"

SKIP_DIRS = {
    "hubs", "sitemaps", ".git", "node_modules", ".next",
    "dist", "build", "__pycache__", "reports", "map", "scripts", "data",
}
SKIP_FRAGMENTS = ["/multiplied/", "/hubs/", "/map/", "/sitemaps/"]


def should_skip(path: str) -> bool:
    p = path.replace("\\", "/")
    for frag in SKIP_FRAGMENTS:
        if frag in p:
            return True
    return False


def read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def extract_hrefs(text: str):
    hrefs = re.findall(r'href="([^"]+)"', text, re.I)
    out = []
    for h in hrefs:
        if h.startswith("http"):
            if SITE in h:
                out.append(h.replace(SITE, ""))
        elif h.startswith("/"):
            out.append(h)
        elif h.endswith(".html"):
            out.append("/" + h)
    return out


def normalize_slug(path: str) -> str:
    p = path.replace("\\", "/")
    if p.startswith("./"):
        p = p[2:]
    return p


def main():
    print("[reputation-gravity] Scanning pages…")

    pages   = []
    titles  = {}
    outbound = defaultdict(list)  # path -> list of href strings

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(root, fname).replace("\\", "/")
            if should_skip(fpath):
                continue
            slug = normalize_slug(fpath)
            text = read(fpath)
            # title
            m = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else slug
            pages.append(slug)
            titles[slug] = title
            outbound[slug] = extract_hrefs(text)

    print(f"[reputation-gravity] {len(pages)} pages collected")

    # Build suffix index: "/foo/bar.html" -> [slug, …]
    suffix_index = defaultdict(list)
    for slug in pages:
        # key: absolute-style path
        key = "/" + slug if not slug.startswith("/") else slug
        suffix_index[key].append(slug)

    # also handle "index.html" root alias
    if "index.html" in [os.path.basename(s) for s in pages]:
        suffix_index["/"].extend([s for s in pages if s.endswith("/index.html") or s == "index.html"])

    # Count inbound using suffix index — O(total_links)
    inbound: Counter = Counter()
    for src, hrefs in outbound.items():
        for href in hrefs:
            href = href.split("#")[0].split("?")[0]
            if not href:
                continue
            # normalise to absolute style
            key = href if href.startswith("/") else "/" + href
            targets = suffix_index.get(key, [])
            for t in targets:
                if t != src:       # don't count self-links
                    inbound[t] += 1

    ranked = sorted(inbound.items(), key=lambda x: x[1], reverse=True)

    top100 = [
        {
            "path": "/" + p.lstrip("./"),
            "title": titles.get(p, p),
            "inbound": cnt,
            "bucket": p.split("/")[0] if "/" in p.lstrip("./") else "root",
        }
        for p, cnt in ranked[:100]
    ]

    os.makedirs("data", exist_ok=True)
    report = {
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pages": len(pages),
        "top_pages": top100,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"[reputation-gravity] Pages analyzed : {len(pages)}")
    print(f"[reputation-gravity] Top authority nodes: {len(top100)}")
    print(f"[reputation-gravity] Report → {OUT}")
    print("")
    print("Top 20:")
    for n in top100[:20]:
        print(f"  {n['inbound']:5}  {n['path']}")


if __name__ == "__main__":
    main()
