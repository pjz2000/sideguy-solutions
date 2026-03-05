#!/usr/bin/env python3
"""
SIDEGUY TRAFFIC BLACK HOLE ENGINE
Routes internal traffic toward the strongest authority pages by injecting
a "Featured Guides" block into key content pages.

Injection scope (safe — excludes mega-dirs):
  pillars, concepts, authority, decisions, longtail,
  generated, auto, fresh, gravity, clusters, katie, prediction-markets

Skips: hubs/, problems/multiplied/, map/, sitemaps/, radar/, reports/,
       node_modules/, .git/

Idempotent: re-running updates existing blocks in-place.
"""

import os
import re
import json
import datetime
from collections import defaultdict

MAP       = "data/problem-map.json"
START     = "<!-- SG_BLACKHOLE_START -->"
END       = "<!-- SG_BLACKHOLE_END -->"
TOP_N     = int(os.environ.get("BH_TOP_N", "20"))
DRY_RUN   = os.environ.get("BH_DRY_RUN", "0") == "1"
REPORT    = "reports/traffic-blackhole.json"

# Inject into these directories only — safe, bounded scope
INJECT_DIRS = {
    "pillars", "concepts", "authority", "decisions", "longtail",
    "generated", "auto", "fresh", "gravity", "clusters", "katie",
    "prediction-markets",
}

# Always skip these regardless
SKIP_DIRS = {
    "hubs", "map", "sitemaps", "radar", "reports",
    "node_modules", ".git", ".next", "dist", "build", "__pycache__",
    "scripts", "data",
}

# Paths containing these will be skipped too (path fragment match)
SKIP_FRAGMENTS = ["/multiplied/", "/hubs/", "/map/", "/sitemaps/"]


def read(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_top_nodes():
    if not os.path.exists(MAP):
        print(f"[blackhole] ERROR: {MAP} not found. Run problem-map.sh first.")
        return []
    with open(MAP, "r", encoding="utf-8") as f:
        data = json.load(f)
    nodes = data.get("top_nodes", [])
    # Filter out bare root "/" (not a useful link label) and pages with no title
    filtered = []
    for n in nodes:
        p = n.get("path", "")
        t = n.get("title", "").strip()
        if p in ("/", "") or not t:
            continue
        # Skip known junk slugs
        if re.search(r"(index\.html|hub\.html)$", p) and n.get("bucket") == "root":
            continue
        filtered.append(n)
    return filtered[:TOP_N]


def blackhole_block(top_nodes):
    """Build the featured-guides HTML block with dark ocean styling."""
    links = "\n".join(
        f'        <li><a href="{n["path"]}">{n["title"]}</a>'
        f'<span class="bh-bkt">{n["bucket"]}</span></li>'
        for n in top_nodes
    )
    return f"""{START}
<div class="sg-blackhole">
  <style scoped>
    .sg-blackhole{{margin:28px 0;padding:16px;border:1px solid rgba(255,255,255,.12);border-radius:14px;background:rgba(0,0,0,.18)}}
    .sg-blackhole h3{{margin:0 0 10px;font-size:14px;color:rgba(255,255,255,.75);letter-spacing:.3px}}
    .sg-blackhole ul{{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:6px}}
    .sg-blackhole li a{{display:block;padding:8px 10px;border-radius:10px;border:1px solid rgba(255,255,255,.08);background:rgba(0,0,0,.12);font-size:13px;color:rgba(0,255,200,.85);text-decoration:none}}
    .sg-blackhole li a:hover{{background:rgba(0,255,200,.07);text-decoration:underline}}
    .bh-bkt{{display:inline-block;margin-left:6px;font-size:11px;color:rgba(255,255,255,.38);vertical-align:middle}}
  </style>
  <h3>🔥 Featured Guides</h3>
  <ul>
{links}
  </ul>
</div>
{END}"""


def should_inject(filepath):
    """Return True if the file lives in an INJECT_DIR and not a SKIP path."""
    fp = filepath.replace("\\", "/")
    # Fragment-based skip
    for frag in SKIP_FRAGMENTS:
        if frag in fp:
            return False
    # Must be in an inject dir
    parts = fp.lstrip("./").split("/")
    if len(parts) < 2:
        return False  # root-level files — skip (too broad)
    top_dir = parts[0]
    if top_dir in SKIP_DIRS:
        return False
    if top_dir not in INJECT_DIRS:
        return False
    return True


def inject(path, block, stats):
    try:
        content = read(path)
    except Exception as e:
        stats["errors"].append(f"{path}: {e}")
        return

    if START in content and END in content:
        # Update existing block
        new_content = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            block,
            content,
            flags=re.S,
        )
        if new_content == content:
            stats["unchanged"] += 1
            return
        if not DRY_RUN:
            write_file(path, new_content)
        stats["updated"] += 1
    elif "</body>" in content:
        # First injection — insert before </body>
        new_content = content.replace("</body>", block + "\n</body>", 1)
        if not DRY_RUN:
            write_file(path, new_content)
        stats["injected"] += 1
    else:
        # Append to end
        new_content = content + "\n" + block + "\n"
        if not DRY_RUN:
            write_file(path, new_content)
        stats["injected"] += 1


def main():
    print(f"[blackhole] Loading top {TOP_N} nodes from {MAP}…")
    top_nodes = load_top_nodes()
    if not top_nodes:
        print("[blackhole] No nodes found — aborting.")
        return

    print(f"[blackhole] Top nodes selected: {len(top_nodes)}")
    for n in top_nodes:
        print(f"  {n['bucket']:20}  inbound={n['inbound']:4}  {n['path']}")

    block = blackhole_block(top_nodes)

    stats = {"injected": 0, "updated": 0, "unchanged": 0, "errors": []}

    for root, dirs, files in os.walk("."):
        # Prune walk at skip dirs to avoid descending into them
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith(".html"):
                continue
            fpath = os.path.join(root, fname).replace("\\", "/")
            if not should_inject(fpath):
                continue
            inject(fpath, block, stats)

    total = stats["injected"] + stats["updated"]
    print(f"\n[blackhole] {'DRY RUN — ' if DRY_RUN else ''}Results:")
    print(f"  Injected (new) : {stats['injected']}")
    print(f"  Updated (exist): {stats['updated']}")
    print(f"  Unchanged      : {stats['unchanged']}")
    print(f"  Errors         : {len(stats['errors'])}")
    if stats["errors"]:
        for e in stats["errors"][:10]:
            print(f"    ⚠ {e}")

    os.makedirs("reports", exist_ok=True)
    report = {
        "generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dry_run": DRY_RUN,
        "top_n": TOP_N,
        "injected": stats["injected"],
        "updated": stats["updated"],
        "unchanged": stats["unchanged"],
        "errors": stats["errors"][:20],
        "top_nodes": [{"path": n["path"], "title": n["title"], "bucket": n["bucket"]} for n in top_nodes],
    }
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"[blackhole] Report → {REPORT}")
    print(f"[blackhole] DONE — Black hole routing active ({total} pages wired)")


if __name__ == "__main__":
    main()
