#!/usr/bin/env python3
import os, re, json, time
from collections import defaultdict

PHONE_SMS = "sms:+17735441231"

# knobs
GLOBAL_N = int(os.environ.get("LOOPS_GLOBAL", "20"))
BUCKET_N = int(os.environ.get("LOOPS_BUCKET", "8"))
TIGHT_N  = int(os.environ.get("LOOPS_TIGHT",  "5"))

MAP = "data/problem-map.json"

# marker blocks (must match earlier engines)
BH_START   = "<!-- SG_BLACKHOLE_START -->"
BH_END     = "<!-- SG_BLACKHOLE_END -->"

GL_START   = "<!-- SG_GRAVITY_LINKS_START -->"
GL_END     = "<!-- SG_GRAVITY_LINKS_END -->"

LOOP_START = "<!-- SG_AUTHORITY_LOOP_START -->"
LOOP_END   = "<!-- SG_AUTHORITY_LOOP_END -->"


def read(p):
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def inject(doc, start, end, block_html):
    """Idempotent marker-based injection. Uses lambdas to avoid re.sub backslash escaping."""
    block = start + "\n" + block_html.strip() + "\n" + end
    if start in doc and end in doc:
        return re.sub(
            re.escape(start) + r".*?" + re.escape(end),
            lambda m: block, doc, flags=re.S, count=1
        )
    if re.search(r"</body>", doc, re.I):
        return re.sub(
            r"</body>",
            lambda m: block + "\n</body>", doc, flags=re.I, count=1
        )
    return doc + "\n" + block


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def load_map():
    if not os.path.exists(MAP):
        return None
    try:
        return json.loads(read(MAP))
    except Exception:
        return None


def normalize_bucket(b):
    return (b or "root").strip() or "root"


def build_global(nodes):
    top = nodes[:GLOBAL_N]
    lis = "\n".join([
        f"    <li><a href='{esc(n['path'])}'>{esc(n.get('title') or n['path'])}</a></li>"
        for n in top
    ])
    return f"""<div class="sg-blackhole" style="border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:14px;margin:18px 0;background:rgba(0,0,0,.18)">
  <h3 style="margin:0 0 8px">&#x1F525; Featured Guides</h3>
  <div style="opacity:.75;font-size:13px;margin-bottom:10px">Auto-refreshed from the live Problem Map. Strongest pages pull internal authority.</div>
  <ul style="margin:0;padding-left:18px;line-height:1.45">
{lis}
  </ul>
  <div style="margin-top:12px">
    <a href="{PHONE_SMS}" style="display:inline-block;padding:10px 12px;border-radius:14px;border:1px solid rgba(127,255,212,.30);background:rgba(0,0,0,.20);text-decoration:none;font-weight:700">&#x1F4AC; Text PJ</a>
  </div>
</div>""".strip()


def build_bucket(nodes_by_bucket, bucket):
    arr = nodes_by_bucket.get(bucket, [])
    top = arr[:BUCKET_N]
    if not top:
        return ""
    items = "\n".join([
        f"    <li><a href='{esc(n['path'])}'>{esc(n.get('title') or n['path'])}</a></li>"
        for n in top
    ])
    return f"""<div class="sg-top-links" style="border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:14px;margin:18px 0;background:rgba(0,0,0,.18)">
  <h3 style="margin:0 0 8px">Top Guides</h3>
  <div style="opacity:.75;font-size:13px;margin-bottom:10px">Bucket-aware authority links (auto-refreshed).</div>
  <ul style="margin:0;padding-left:18px;line-height:1.45">
{items}
  </ul>
</div>""".strip()


def build_tight_loop(nodes_by_bucket, bucket, global_nodes):
    """Top TIGHT_N bucket nodes + up to 3 global (deduped)."""
    arr = nodes_by_bucket.get(bucket, [])[:TIGHT_N]
    seen = set(n["path"] for n in arr)
    g = []
    for n in global_nodes:
        if n["path"] not in seen:
            g.append(n)
            seen.add(n["path"])
        if len(g) >= 3:
            break
    mix = arr + g
    if not mix:
        return ""
    links = " ".join([
        f"<a href='{esc(n['path'])}' style='margin-right:10px'>{esc((n.get('title') or n['path'])[:48])}</a>"
        for n in mix
    ])
    return f"""<div class="sg-loop" style="border:1px solid rgba(127,255,212,.18);border-radius:16px;padding:12px;margin:14px 0;background:rgba(0,0,0,.14)">
  <div style="opacity:.8;font-size:12px;margin-bottom:6px">Authority Loop (compounding links)</div>
  <div style="line-height:1.6">{links}</div>
</div>""".strip()


def bucket_from_path(path):
    p = (path or "").strip()
    if p == "/":
        return "root"
    if p.startswith("/"):
        p = p[1:]
    parts = p.split("/")
    return normalize_bucket(parts[0]) if len(parts) > 1 else "root"


SKIP_DIRS = {
    "node_modules", ".git", ".next", "dist", "build",
    "__pycache__", "reports", "data", "future/raw",
    "sitemaps", "hubs", "multiplied", "_quarantine_backups",
}


def scan_html_files():
    files = []
    for root, dirs, fs in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in fs:
            if f.endswith(".html"):
                files.append(os.path.join(root, f).replace("\\", "/"))
    return files


def main():
    m = load_map()
    if not m or "top_nodes" not in m:
        print("[final-boss] Missing data/problem-map.json top_nodes. Build problem map first.")
        print("Run: bash scripts/problem-map.sh")
        return

    nodes = [n for n in m["top_nodes"] if n.get("path")]

    nodes_by_bucket = defaultdict(list)
    for n in nodes:
        b = normalize_bucket(n.get("bucket") or bucket_from_path(n.get("path", "")))
        nodes_by_bucket[b].append(n)

    global_block = build_global(nodes)

    changed = 0
    touched = 0

    for fp in scan_html_files():
        # skip any backup/quarantine paths
        if "_quarantine" in fp or ".backup." in fp or "/reports/" in fp:
            continue
        try:
            doc = read(fp)
        except Exception:
            continue
        orig = doc

        # bucket detection from file path
        rel = fp.replace("\\", "/").lstrip("./")
        b = normalize_bucket(rel.split("/")[0] if "/" in rel else "root")

        # 1) site-wide blackhole (replaces / updates existing SG_BLACKHOLE blocks)
        doc = inject(doc, BH_START, BH_END, global_block)

        # 2) bucket-aware top guides
        bucket_block = build_bucket(nodes_by_bucket, b)
        if bucket_block:
            doc = inject(doc, GL_START, GL_END, bucket_block)

        # 3) tight authority loop
        loop_block = build_tight_loop(nodes_by_bucket, b, nodes[:GLOBAL_N])
        if loop_block:
            doc = inject(doc, LOOP_START, LOOP_END, loop_block)

        if doc != orig:
            write(fp, doc)
            changed += 1
        touched += 1

    report = {
        "generated_at": int(time.time()),
        "global_n": GLOBAL_N,
        "bucket_n": BUCKET_N,
        "tight_n": TIGHT_N,
        "files_scanned": touched,
        "files_changed": changed,
        "phone_sms": PHONE_SMS,
    }
    write("reports/final-boss-loops.json", json.dumps(report, indent=2))
    print(f"[final-boss] scanned={touched}  changed={changed}")
    print("[final-boss] report=reports/final-boss-loops.json")


if __name__ == "__main__":
    main()
