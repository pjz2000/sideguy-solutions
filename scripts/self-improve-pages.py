#!/usr/bin/env python3
"""
SIDEGUY SELF-IMPROVING PAGES ENGINE
- NON-DESTRUCTIVE, marker-based, idempotent upgrades
- Prioritizes pages using:
    1) gsc-priority.txt (if exists)
    2) data/problem-map.json top_nodes (if exists)
    3) fallback: scan buckets safely
- Adds/repairs (only if missing or inside marker-block):
    ✅ <title> (safe upgrade)
    ✅ meta description (safe upgrade)
    ✅ canonical (safe upgrade)
    ✅ H1 (if missing)
    ✅ "Clarity before cost" intro block
    ✅ FAQ (5 items) + JSON-LD FAQ schema
    ✅ Breadcrumbs + internal links (bucket-aware)
    ✅ Text PJ CTA (sms:+17735441231) inside upgraded block
- Writes backups to reports/self-improve-backups/
"""

import os, re, json, shutil, html as html_module
from datetime import datetime
from collections import defaultdict

PHONE_SMS = "sms:+17735441231"
SITE      = "https://sideguysolutions.com"

LIMIT = int(os.environ.get("IMPROVE_LIMIT", "120"))

GSC_LISTS    = ["gsc-priority.txt", "reports/gsc-priority.txt", "data/gsc-priority.txt"]
PROBLEM_MAPS = ["data/problem-map.json", "reports/problem-map.json"]

SCAN_BUCKETS = [
    "problems","concepts","clusters","pillars","generated","auto",
    "decisions","prediction-markets","authority","knowledge","fresh",
    "gravity","future-build",
]

START     = "<!-- SG_SELF_IMPROVE_START -->"
END       = "<!-- SG_SELF_IMPROVE_END -->"
FAQ_START = "<!-- SG_FAQ_START -->"
FAQ_END   = "<!-- SG_FAQ_END -->"


def now_stamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def read(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def write(path, s):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)


def safe(s):
    return html_module.escape(str(s or ""))


def rel_from_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return ""
    if u.startswith(SITE):
        u = u[len(SITE):]
    if u.startswith("http://") or u.startswith("https://"):
        return ""
    if u == "/":
        return "index.html"
    if u.startswith("/"):
        u = u[1:]
    return u or "index.html"


def url_from_rel(rel: str) -> str:
    rel = rel.replace("\\", "/").lstrip("./")
    if rel == "index.html":
        return SITE + "/"
    return SITE + "/" + rel


def bucket_of(rel: str) -> str:
    rel = rel.replace("\\", "/").lstrip("./")
    parts = rel.split("/")
    return parts[0] if len(parts) > 1 else "root"


def file_exists(rel: str) -> bool:
    return os.path.isfile(rel)


def backup_file(path: str):
    bdir = os.path.join("reports", "self-improve-backups", now_stamp())
    os.makedirs(bdir, exist_ok=True)
    dst = os.path.join(bdir, path.replace("/", "__"))
    shutil.copy2(path, dst)


def extract_title(doc: str) -> str:
    m = re.search(r"<title>(.*?)</title>", doc, re.I | re.S)
    if m:
        return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", m.group(1))).strip()
    return ""


def extract_h1(doc: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", doc, re.I | re.S)
    if m:
        return re.sub(r"\s+", " ", re.sub(r"<.*?>", "", m.group(1))).strip()
    return ""


def derive_topic(rel: str, title: str, h1: str) -> str:
    base = h1 or title
    if base:
        base = re.sub(r"\s*\|\s*SideGuy.*$", "", base, flags=re.I).strip()
        base = re.sub(r"\s+", " ", base).strip()
        return base[:80]
    fn = os.path.basename(rel).replace(".html", "").replace("_", "-")
    fn = re.sub(r"-+", "-", fn).strip("-")
    words = [w for w in fn.split("-") if w]
    return " ".join([w.capitalize() for w in words])[:80] or "SideGuy Guide"


def ensure_meta_tag(doc: str, name: str, content: str) -> str:
    pat = re.compile(rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\'].*?["\']\s*/?>', re.I)
    tag = f'<meta name="{name}" content="{safe(content)}"/>'
    if pat.search(doc):
        return pat.sub(tag, doc, count=1)
    if re.search(r"</head>", doc, re.I):
        return re.sub(r"</head>", tag + "\n</head>", doc, flags=re.I, count=1)
    return doc


def ensure_canonical(doc: str, canon_url: str) -> str:
    pat = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'].*?["\']\s*/?>', re.I)
    tag = f'<link rel="canonical" href="{safe(canon_url)}"/>'
    if pat.search(doc):
        return pat.sub(tag, doc, count=1)
    if re.search(r"</head>", doc, re.I):
        return re.sub(r"</head>", tag + "\n</head>", doc, flags=re.I, count=1)
    return doc


def ensure_title_tag(doc: str, title: str) -> str:
    if re.search(r"<title>.*?</title>", doc, re.I | re.S):
        return re.sub(r"<title>.*?</title>", f"<title>{safe(title)}</title>",
                      doc, flags=re.I | re.S, count=1)
    if re.search(r"</head>", doc, re.I):
        return re.sub(r"</head>", f"<title>{safe(title)}</title>\n</head>",
                      doc, flags=re.I, count=1)
    return doc


def ensure_h1(doc: str, h1: str) -> str:
    if re.search(r"<h1[^>]*>.*?</h1>", doc, re.I | re.S):
        return doc
    if re.search(r"<body[^>]*>", doc, re.I):
        return re.sub(r"(<body[^>]*>)", r"\1\n" + f"<h1>{safe(h1)}</h1>\n",
                      doc, flags=re.I, count=1)
    return doc


def inject_block(doc: str, start: str, end: str, block_html: str) -> str:
    block = start + "\n" + block_html.strip() + "\n" + end
    if start in doc and end in doc:
        return re.sub(re.escape(start) + r".*?" + re.escape(end),
                      lambda m: block, doc, flags=re.S, count=1)
    if re.search(r"</body>", doc, re.I):
        return re.sub(r"</body>", lambda m: block + "\n</body>", doc, flags=re.I, count=1)
    return doc + "\n" + block


STYLE_SNIP = """<style>
  .sg-improve{border:1px solid rgba(255,255,255,.12);background:rgba(0,0,0,.18);border-radius:16px;padding:14px;margin:18px 0}
  .sg-improve h2{margin:0 0 8px;font-size:18px}
  .sg-improve p{margin:0 0 10px;opacity:.85;line-height:1.45}
  .sg-improve .row{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
  .sg-improve a.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 12px;border-radius:14px;border:1px solid rgba(127,255,212,.30);background:rgba(0,0,0,.22);text-decoration:none;font-weight:700}
  .sg-improve .crumbs{font-size:13px;opacity:.75;margin-bottom:10px}
  .sg-improve ul{margin:8px 0 0 18px;opacity:.9}
  .sg-improve li{margin:6px 0}
  .sg-pill{display:inline-block;padding:4px 8px;border-radius:999px;border:1px solid rgba(255,255,255,.12);background:rgba(0,0,0,.15);font-size:12px;opacity:.85}
</style>"""


def faq_for_topic(topic: str, bucket: str):
    return [
        (f"What is {topic}?",
         f"{topic} is a common operator problem area. SideGuy pages explain what it is, "
         f"what breaks, and what a practical fix path looks like."),
        (f"Why does {topic} usually fail?",
         f"Most failures come from configuration mismatches, permissions/keys, environment "
         f"differences, or upstream service changes. Start by isolating the first failing step."),
        (f"What's the fastest way to troubleshoot {topic}?",
         f"Reproduce the issue, check recent changes, verify credentials/config, and confirm "
         f"the expected request/response or system state. Then test the smallest fix first."),
        (f"How do I prevent {topic} issues from happening again?",
         f"Add basic monitoring/logging, pin versions where possible, document the working "
         f"config, and set a quick rollback path."),
        (f"When should I get a human involved?",
         f"If the issue affects revenue, customer access, or you're stuck after the first "
         f"pass of checks, text PJ and we'll get to the shortest path to resolution."),
    ]


def faq_schema(topic: str, faqs):
    main = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main,
    }, indent=2)


def related_links(problem_map, bucket: str, rel: str):
    if not problem_map:
        return []
    out = []
    self_path = "/" + rel.replace("\\", "/").lstrip("./")
    for n in (problem_map.get("top_nodes") or []):
        try:
            if n.get("bucket") == bucket and n.get("path") and n["path"] != self_path and len(out) < 8:
                out.append((n["path"], n.get("title", "") or n["path"]))
        except Exception:
            continue
    return out


def load_problem_map():
    for p in PROBLEM_MAPS:
        if os.path.exists(p):
            try:
                return json.loads(read(p)), p
            except Exception:
                pass
    return None, None


def load_gsc_list():
    for p in GSC_LISTS:
        if os.path.exists(p):
            lines = [x.strip() for x in read(p).splitlines() if x.strip()]
            rels = [r for r in (rel_from_url(x) for x in lines) if r]
            return rels, p
    return [], None


def fallback_candidates():
    rels = []
    seen = set()
    for b in SCAN_BUCKETS:
        if not os.path.isdir(b):
            continue
        for root, _, files in os.walk(b):
            for f in files:
                if f.endswith(".html"):
                    p = os.path.join(root, f).replace("\\", "/")
                    if p not in seen:
                        seen.add(p)
                        rels.append(p)
    if os.path.exists("index.html") and "index.html" not in seen:
        rels.insert(0, "index.html")
    return rels


def build_candidates(problem_map, gsc_rels):
    candidates, seen = [], set()
    for r in gsc_rels:
        if file_exists(r) and r not in seen:
            seen.add(r); candidates.append(r)
    if problem_map and "top_nodes" in problem_map:
        for n in problem_map["top_nodes"]:
            r = rel_from_url(n.get("path", ""))
            if r and file_exists(r) and r not in seen:
                seen.add(r); candidates.append(r)
    for r in fallback_candidates():
        if file_exists(r) and r not in seen:
            seen.add(r); candidates.append(r)
    return candidates[:LIMIT]


def improve_one(rel: str, problem_map):
    doc  = read(rel)
    orig = doc

    title  = extract_title(doc)
    h1     = extract_h1(doc)
    topic  = derive_topic(rel, title, h1)
    bucket = bucket_of(rel)
    canon  = url_from_rel(rel)

    # 1) Meta tags + canonical
    desired_title = (title if (title and len(title) >= 12 and "sideguy" in title.lower())
                     else f"{topic} | SideGuy")
    desired_desc  = (f"Clarity-first guide for {topic}. Fast explanation, common failure points, "
                     f"and the shortest path to a working fix. Text PJ if you want help.")
    doc = ensure_title_tag(doc, desired_title)
    doc = ensure_meta_tag(doc, "description", desired_desc)
    doc = ensure_canonical(doc, canon)

    # 2) H1
    doc = ensure_h1(doc, topic)

    # 3) Self-improve intro block
    crumbs = (f'<div class="crumbs"><span class="sg-pill">SideGuy</span> &nbsp;›&nbsp; '
              f'<a href="/">Home</a> &nbsp;›&nbsp; <span class="sg-pill">{safe(bucket)}</span></div>')

    rel_links = related_links(problem_map, bucket, rel)
    rel_list  = ""
    if rel_links:
        items    = "".join(f'<li><a href="{safe(p)}">{safe(t)}</a></li>' for p, t in rel_links)
        rel_list = f'<h2>Related pages</h2><ul>{items}</ul>'

    improve_block = f"""{STYLE_SNIP}
<section class="sg-improve">
  {crumbs}
  <h2>Clarity before cost</h2>
  <p>
    SideGuy is where Google discovers the problem, AI explains it, and a real human resolves it.
    This page is auto-maintained to stay clean, crawlable, and helpful.
  </p>
  <div class="row">
    <a class="btn" href="{PHONE_SMS}">💬 Text PJ</a>
    <a class="btn" href="/map/index.html">🧭 Problem Map</a>
    <a class="btn" href="/authority/index.html">🌊 Authority Hubs</a>
  </div>
  {rel_list}
  <p style="opacity:.75;margin-top:12px;font-size:13px;">
    Updated: {datetime.now().strftime("%Y-%m-%d")} &bull; Bucket: {safe(bucket)}
  </p>
</section>"""

    doc = inject_block(doc, START, END, improve_block)

    # 4) FAQ block + schema
    faqs     = faq_for_topic(topic, bucket)
    faq_items = "".join(
        f'<li><strong>{safe(q)}</strong><br/><span style="opacity:.85">{safe(a)}</span></li>'
        for q, a in faqs
    )
    faq_block = f"""<section class="sg-improve">
  <h2>FAQ</h2>
  <ul>{faq_items}</ul>
  <script type="application/ld+json">
{faq_schema(topic, faqs)}
  </script>
</section>"""

    doc = inject_block(doc, FAQ_START, FAQ_END, faq_block)

    return doc, (doc != orig), {"rel": rel, "bucket": bucket, "topic": topic}


def main():
    problem_map, pm_path = load_problem_map()
    gsc_rels, gsc_path   = load_gsc_list()
    candidates           = build_candidates(problem_map, gsc_rels)

    changed, skipped, touched = 0, 0, []

    for rel in candidates:
        if not file_exists(rel):
            skipped += 1
            continue
        doc, did_change, meta = improve_one(rel, problem_map)
        if did_change:
            backup_file(rel)
            write(rel, doc)
            changed += 1
            touched.append(meta)
        else:
            skipped += 1

    report = {
        "generated_at":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "limit":         LIMIT,
        "problem_map":   pm_path,
        "gsc_list":      gsc_path,
        "candidates":    len(candidates),
        "changed":       changed,
        "skipped":       skipped,
        "touched":       touched[:500],
    }
    os.makedirs("reports", exist_ok=True)
    write("reports/self-improve-report.json", json.dumps(report, indent=2))

    print(f"[self-improve] candidates={report['candidates']}")
    print(f"[self-improve] changed   ={report['changed']}")
    print(f"[self-improve] skipped   ={report['skipped']}")
    print(f"[self-improve] backups   → reports/self-improve-backups/")
    print(f"[self-improve] report    → reports/self-improve-report.json")


if __name__ == "__main__":
    main()
