import os, re, json, hashlib, datetime
from pathlib import Path

ROOT = Path(".").resolve()
PILLARS_DIR = ROOT / "pillars"
HUBS_DIR = ROOT / "hubs"

# Adjust if your root leaf pages are in repo root with "-san-diego.html"
LEAF_GLOB = "*-san-diego.html"

BAD_TOKENS = set([
  "sideguy","sideguy solutions","solutions","solve","services","service","san","diego",
  "near","me","best","top","guide","how","what","why","today","now","your"
])

def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s

def stable_int(s: str) -> int:
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()
    return int(h[:12], 16)

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def write_text(p: Path, txt: str):
    p.write_text(txt, encoding="utf-8")

def find_first(pattern: str, txt: str):
    m = re.search(pattern, txt, flags=re.I|re.S)
    return m.group(1) if m else None

def extract_title(txt: str) -> str:
    h1 = find_first(r'<h1[^>]*>(.*?)</h1>', txt)
    if h1:
        return re.sub(r'<[^>]+>', '', h1).strip()
    t = find_first(r'<title[^>]*>(.*?)</title>', txt)
    if t:
        return re.sub(r'\s+', ' ', t).strip()
    return ""

def extract_meta_desc(txt: str) -> str:
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', txt, flags=re.I)
    return m.group(1).strip() if m else ""

def get_body_insert_point(txt: str) -> int:
    # prefer right after opening <body ...>
    m = re.search(r'<body[^>]*>', txt, flags=re.I)
    if not m: return -1
    return m.end()

def get_head_end(txt: str) -> int:
    m = re.search(r'</head\s*>', txt, flags=re.I)
    return m.start() if m else -1

def has_marker(txt: str, marker: str) -> bool:
    return marker in txt

def ensure_css(txt: str) -> str:
    # inject CSS once per page (head)
    css_marker = "/* SG_PILLAR_WIRING_V1 */"
    if css_marker in txt: return txt

    css = f"""
<style>
{css_marker}
.sg-concept-box {{
  margin: 18px auto 14px auto;
  padding: 14px 14px 12px 14px;
  border: 1px solid rgba(0,0,0,0.12);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(0,180,255,0.10), rgba(0,0,0,0.02));
  max-width: 980px;
}}
.sg-concept-top {{
  display:flex; gap:12px; align-items:flex-start; justify-content:space-between; flex-wrap:wrap;
}}
.sg-concept-title {{
  font-size: 16px; font-weight: 800; letter-spacing: .2px;
}}
.sg-concept-sub {{
  font-size: 13px; opacity:.9; margin-top:6px; line-height:1.35;
}}
.sg-pill-link a {{
  display:inline-block;
  padding: 8px 10px;
  border-radius: 999px;
  border: 1px solid rgba(0,0,0,0.14);
  text-decoration:none;
  font-weight:700;
  font-size: 13px;
}}
.sg-pill-link a:hover {{ transform: translateY(-1px); }}
.sg-mini {{
  margin-top: 10px;
  display:flex; gap:10px; flex-wrap:wrap;
}}
.sg-mini a {{
  font-size: 12px; text-decoration:none;
  padding: 6px 8px;
  border-radius: 10px;
  border: 1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.55);
}}
.sg-mini a:hover {{ background: rgba(255,255,255,0.85); }}
.sg-glossary {{
  margin: 14px auto 0 auto;
  max-width: 980px;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px dashed rgba(0,0,0,0.14);
  background: rgba(0,0,0,0.02);
}}
.sg-glossary h3 {{ margin:0 0 8px 0; font-size: 14px; }}
.sg-glossary dl {{ margin:0; display:grid; grid-template-columns: 1fr; gap:8px; }}
.sg-glossary dt {{ font-weight:800; font-size: 13px; }}
.sg-glossary dd {{ margin:2px 0 0 0; font-size: 13px; opacity:.95; line-height:1.35; }}
.sg-toc {{
  margin: 10px auto 0 auto;
  max-width: 980px;
  padding: 10px 14px;
  border-radius: 14px;
  border: 1px solid rgba(0,0,0,0.10);
  background: rgba(255,255,255,0.55);
}}
.sg-toc b {{ display:block; margin-bottom:6px; }}
.sg-toc a {{ margin-right:10px; font-size: 12px; text-decoration:none; }}
</style>
"""
    head_end = get_head_end(txt)
    if head_end == -1:
        return txt
    return txt[:head_end] + css + "\n" + txt[head_end:]

def list_pillars():
    if not PILLARS_DIR.exists(): return []
    pills = []
    for p in sorted(PILLARS_DIR.glob("*.html")):
        txt = read_text(p)
        title = extract_title(txt) or p.stem
        pills.append({"path": str(p), "file": p.name, "title": title, "slug": p.stem})
    return pills

def classify_to_pillar(title: str, pillars):
    # deterministic: best overlap score; fallback hash
    t = re.sub(r'[^a-z0-9\s]', ' ', title.lower())
    tokens = [x for x in t.split() if x and x not in BAD_TOKENS and len(x) > 2]
    if not tokens:
        i = stable_int(title) % max(1, len(pillars))
        return pillars[i] if pillars else None

    best = None
    best_score = -1
    for pill in pillars:
        pt = re.sub(r'[^a-z0-9\s]', ' ', pill["title"].lower())
        ptoks = set([x for x in pt.split() if x and x not in BAD_TOKENS and len(x) > 2])
        score = sum(1 for x in tokens if x in ptoks)
        if score > best_score:
            best_score = score
            best = pill

    if best_score <= 0 and pillars:
        best = pillars[stable_int(title) % len(pillars)]
    return best

def infer_hub_for_leaf(filename: str):
    # crude but stable: take slug before "-san-diego"
    base = filename.replace("-san-diego.html","")
    # if you have hubs by category/industry already, this still gives a stable "topic token"
    return base

def build_concept_box(pill, page_type: str, title: str):
    # page_type: leaf|hub|pillar
    pill_url = f"/pillars/{pill['file']}"
    pill_title = pill["title"]
    if page_type == "pillar":
        # On pillar pages, show "this is a pillar" + jump links
        return f"""
<!-- SG_CONCEPT_BOX_V1 -->
<div class="sg-concept-box" id="sg-concept">
  <div class="sg-concept-top">
    <div>
      <div class="sg-concept-title">Concept Pillar: {pill_title}</div>
      <div class="sg-concept-sub">Wikipedia-style concept page. This is the authority anchor that hubs + pages link back to.</div>
    </div>
    <div class="sg-pill-link"><a href="{pill_url}">You are here</a></div>
  </div>
</div>
<!-- /SG_CONCEPT_BOX_V1 -->
"""
    else:
        return f"""
<!-- SG_CONCEPT_BOX_V1 -->
<div class="sg-concept-box" id="sg-concept">
  <div class="sg-concept-top">
    <div>
      <div class="sg-concept-title">Concept: {pill_title}</div>
      <div class="sg-concept-sub">Want the "big picture" first? This is the Wikipedia-style explainer for what this page is about — built for clarity before cost.</div>
    </div>
    <div class="sg-pill-link"><a href="{pill_url}">Read the Concept →</a></div>
  </div>
  <div class="sg-mini">
    <a href="#sg-toc">Jump links</a>
    <a href="#sg-glossary">Mini glossary</a>
    <a href="#faq">FAQ</a>
  </div>
</div>
<!-- /SG_CONCEPT_BOX_V1 -->
"""

def build_toc():
    return """
<!-- SG_TOC_V1 -->
<div class="sg-toc" id="sg-toc">
  <b>Quick navigation</b>
  <a href="#sg-concept">Concept</a>
  <a href="#what">What this is</a>
  <a href="#steps">Fast steps</a>
  <a href="#cost">Cost + time</a>
  <a href="#mistakes">Common mistakes</a>
  <a href="#faq">FAQ</a>
</div>
<!-- /SG_TOC_V1 -->
"""

def build_glossary(pill_title: str):
    # small, safe glossary. You can expand later.
    return f"""
<!-- SG_GLOSSARY_V1 -->
<div class="sg-glossary" id="sg-glossary">
  <h3>Mini glossary (operator-friendly)</h3>
  <dl>
    <div>
      <dt>Concept Pillar</dt>
      <dd>A Wikipedia-style explainer page that defines the topic and links out to related hubs and pages. You're reading: <b>{pill_title}</b>.</dd>
    </div>
    <div>
      <dt>Hub</dt>
      <dd>A directory page that groups many related pages (and points back up to the concept).</dd>
    </div>
    <div>
      <dt>Leaf Page</dt>
      <dd>A specific "problem + solution" page built to match a real query. It should always link back to the concept for trust.</dd>
    </div>
  </dl>
</div>
<!-- /SG_GLOSSARY_V1 -->
"""

def insert_after_h1(txt: str, block: str) -> str:
    # If concept box already exists, do nothing
    if "SG_CONCEPT_BOX_V1" in txt: return txt
    m = re.search(r'(<h1[^>]*>.*?</h1>)', txt, flags=re.I|re.S)
    if not m:
        # fallback: after <body>
        bi = get_body_insert_point(txt)
        if bi == -1: return txt
        return txt[:bi] + "\n" + block + "\n" + txt[bi:]
    end = m.end()
    return txt[:end] + "\n" + block + "\n" + txt[end:]

def insert_after_concept(txt: str, block: str, marker: str) -> str:
    if marker in txt: return txt
    # place after concept box if exists else after h1
    m = re.search(r'<!-- /SG_CONCEPT_BOX_V1 -->', txt, flags=re.I)
    if m:
        end = m.end()
        return txt[:end] + "\n" + block + "\n" + txt[end:]
    return insert_after_h1(txt, block)

def patch_anchor_targets(txt: str) -> str:
    # Ensure basic anchors exist; harmless if duplicate IDs already present
    # We do minimal, only if headers exist without ids.
    replacements = [
        (r'(<h2[^>]*>\s*What[^<]*</h2>)', r'<h2 id="what">What this is</h2>'),
        (r'(<h2[^>]*>\s*Steps[^<]*</h2>)', r'<h2 id="steps">Fast steps</h2>'),
        (r'(<h2[^>]*>\s*Cost[^<]*</h2>)', r'<h2 id="cost">Cost + time</h2>'),
        (r'(<h2[^>]*>\s*Common[^<]*</h2>)', r'<h2 id="mistakes">Common mistakes</h2>'),
        (r'(<h2[^>]*>\s*FAQ[^<]*</h2>)', r'<h2 id="faq">FAQ</h2>'),
    ]
    out = txt
    for pat, rep in replacements:
        if re.search(rep, out, flags=re.I):  # already patched
            continue
        if re.search(pat, out, flags=re.I):
            out = re.sub(pat, rep, out, flags=re.I)
    return out

def should_skip(path: Path) -> bool:
    s = str(path)
    if "/.git/" in s: return True
    if "/seo-reserve/" in s: return True
    if "/_quarantine_backups/" in s: return True
    if path.name.startswith("aaa-"): return True
    if path.name in ["404.html","hub.html","index.html"]: return True
    return False

def main():
    pillars = list_pillars()
    if not pillars:
        print("No pillars found in ./pillars. Run pillar engine first.")
        return

    leaf_paths = [p for p in ROOT.glob(LEAF_GLOB) if p.is_file() and not should_skip(p)]
    hub_paths = [p for p in HUBS_DIR.glob("*.html") if p.is_file() and not should_skip(p)]
    pillar_paths = [Path(x["path"]) for x in pillars if Path(x["path"]).exists()]

    changed = 0
    for p in leaf_paths:
        txt = read_text(p)
        title = extract_title(txt) or p.stem
        pill = classify_to_pillar(title, pillars)
        if not pill:
            continue
        txt = ensure_css(txt)
        txt = insert_after_h1(txt, build_concept_box(pill, "leaf", title))
        txt = insert_after_concept(txt, build_toc(), "SG_TOC_V1")
        txt = insert_after_concept(txt, build_glossary(pill["title"]), "SG_GLOSSARY_V1")
        txt = patch_anchor_targets(txt)
        write_text(p, txt)
        changed += 1

    for p in hub_paths:
        txt = read_text(p)
        title = extract_title(txt) or p.stem
        pill = classify_to_pillar(title, pillars)
        if not pill:
            continue
        txt = ensure_css(txt)
        txt = insert_after_h1(txt, build_concept_box(pill, "hub", title))
        txt = insert_after_concept(txt, build_toc(), "SG_TOC_V1")
        txt = insert_after_concept(txt, build_glossary(pill["title"]), "SG_GLOSSARY_V1")
        txt = patch_anchor_targets(txt)
        write_text(p, txt)
        changed += 1

    # Light touch on pillar pages: add the "this is a pillar" top box (if missing) + toc
    for p in pillar_paths:
        txt = read_text(p)
        title = extract_title(txt) or p.stem
        pill = classify_to_pillar(title, pillars) or {"title": title, "file": p.name}
        txt = ensure_css(txt)
        txt = insert_after_h1(txt, build_concept_box(pill, "pillar", title))
        txt = insert_after_concept(txt, build_toc(), "SG_TOC_V1")
        txt = insert_after_concept(txt, build_glossary(title), "SG_GLOSSARY_V1")
        txt = patch_anchor_targets(txt)
        write_text(p, txt)
        changed += 1

    stamp = datetime.datetime.utcnow().isoformat()
    report = {
        "timestamp": stamp,
        "leaf_pages_touched": len(leaf_paths),
        "hub_pages_touched": len(hub_paths),
        "pillar_pages_touched": len(pillar_paths),
        "files_written": changed
    }
    (ROOT / "signals").mkdir(parents=True, exist_ok=True)
    (ROOT / "signals" / f"pillar-wiring-{stamp[:10]}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"OK: wired concept boxes + toc + glossary on {changed} files")
    print(f"Report: signals/pillar-wiring-{stamp[:10]}.json")

if __name__ == "__main__":
    main()
