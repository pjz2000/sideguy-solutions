#!/usr/bin/env python3
"""
SideGuy Knowledge Graph Engine
- Builds an inverted index of tokens -> pages
- Computes candidate neighbors via shared tokens
- Scores with weighted Jaccard (rarer tokens count more)
- Writes per-page neighbor links + cluster hubs
"""
import os, re, math, json, time
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(".")
HUB_DIR = Path("kg/hubs")
HUB_DIR.mkdir(parents=True, exist_ok=True)

# Safety knobs
KG_LIMIT          = int(os.environ.get("KG_LIMIT",      "6000"))
MAX_TOKENS_PER_PAGE = int(os.environ.get("KG_TOKENS",   "60"))
NEIGHBORS         = int(os.environ.get("KG_NEIGHBORS",  "7"))
MAX_CANDIDATES    = int(os.environ.get("KG_CANDIDATES", "120"))
MIN_TOKEN_LEN     = 4

IGNORE_DIRS = {
    ".git", "node_modules", "signals", "_quarantine_backups",
    "seo-reserve", ".github", "kg", "sitemaps",
}

STOP = set("""
a an and are as at be by for from has have how i in is it its of on or our
that the their this to vs was we what when where who why will with you your
""".split())


def is_ignored(path: Path) -> bool:
    return any(d in set(path.parts) for d in IGNORE_DIRS)


def strip_tags(html: str) -> str:
    html = re.sub(r"(?is)<script.*?>.*?</script>", " ", html)
    html = re.sub(r"(?is)<style.*?>.*?</style>",   " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    toks = re.split(r"[\s\-]+", text)
    return [
        t for t in toks
        if len(t) >= MIN_TOKEN_LEN and t not in STOP and not t.isdigit()
    ]


def read_title(html: str) -> str:
    m = re.search(r"(?is)<title>(.*?)</title>", html)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()[:120]
    return ""


# ── Collect pages ─────────────────────────────────────────────────────────────
pages = sorted(
    [p for p in ROOT.rglob("*.html") if not is_ignored(p)],
    key=lambda x: (len(x.parts), str(x)),
)
if len(pages) > KG_LIMIT:
    pages = pages[:KG_LIMIT]

print(f"KG: scanning {len(pages)} pages...")

# ── Build per-page token set + global document freq ───────────────────────────
page_tokens: dict[str, list] = {}
df = Counter()

for p in pages:
    try:
        html  = p.read_text(encoding="utf-8", errors="ignore")
        plain = strip_tags(html)
        toks  = tokenize(p.stem.replace("-", " ") + " " + plain[:6000])
        c     = Counter(toks)
        top   = [t for t, _ in c.most_common(MAX_TOKENS_PER_PAGE)]
        s     = set(top)
        page_tokens[str(p)] = list(s)
        for t in s:
            df[t] += 1
    except Exception:
        continue

N   = max(1, len(page_tokens))
inv = defaultdict(list)
for path, toks in page_tokens.items():
    for t in toks:
        inv[t].append(path)


def token_weight(t: str) -> float:
    d = df.get(t, 1)
    return min(math.log((N + 1) / (d + 1)) + 1.0, 4.0)


tw = {t: token_weight(t) for t in df}


def score(a_toks, b_toks) -> float:
    a, b = set(a_toks), set(b_toks)
    inter = a & b
    if not inter:
        return 0.0
    union = a | b
    num = sum(tw.get(t, 1.0) for t in inter)
    den = sum(tw.get(t, 1.0) for t in union)
    return num / den if den > 0 else 0.0


# ── Build neighbor graph ──────────────────────────────────────────────────────
neighbors_map: dict[str, list] = {}
titles: dict[str, str] = {}

for i, (path, toks) in enumerate(page_tokens.items(), 1):
    token_list = sorted(toks, key=lambda t: df.get(t, 1))[:25]
    cand_counts: Counter = Counter()
    for t in token_list:
        for other in inv.get(t, []):
            if other != path:
                cand_counts[other] += 1

    candidates = [c for c, _ in cand_counts.most_common(MAX_CANDIDATES)]
    scored = sorted(
        [(score(toks, page_tokens.get(c, [])), c) for c in candidates],
        reverse=True,
    )
    neighbors_map[path] = [c for _, c in scored[:NEIGHBORS]]

    if i % 400 == 0:
        print(f"KG: processed {i}/{len(page_tokens)} pages...")

# Read titles
for path in neighbors_map:
    try:
        html = Path(path).read_text(encoding="utf-8", errors="ignore")
        titles[path] = read_title(html) or Path(path).stem.replace("-", " ").title()
    except Exception:
        titles[path] = Path(path).stem.replace("-", " ").title()

# ── Simple union-find clustering ──────────────────────────────────────────────
parent: dict[str, str] = {}
rank:   dict[str, int] = {}


def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x


def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return
    if rank[ra] < rank[rb]:
        parent[ra] = rb
    elif rank[ra] > rank[rb]:
        parent[rb] = ra
    else:
        parent[rb] = ra
        rank[ra] += 1


for n in neighbors_map:
    parent[n] = n
    rank[n]   = 0

for a, ns in neighbors_map.items():
    for b in ns:
        if b in parent:
            union(a, b)

clusters: dict[str, list] = defaultdict(list)
for n in neighbors_map:
    clusters[find(n)].append(n)

# ── Write cluster hub pages ───────────────────────────────────────────────────
cluster_hubs = []
cluster_id   = 0

for root_node, members in sorted(clusters.items(), key=lambda kv: -len(kv[1])):
    if len(members) < 12:
        continue
    cluster_id += 1

    tok_count: Counter = Counter()
    for m in members[:200]:
        for t in page_tokens.get(m, []):
            tok_count[t] += 1
    for bad in [
        "business", "guide", "solutions", "services", "local", "companies",
        "sideguy", "solve", "whether", "helps", "small", "learn", "about",
        "diego", "finding", "right", "without", "every", "many", "need",
        "help", "work", "best", "good", "make", "take", "find", "keep",
        "look", "know", "call", "also", "more", "same", "most", "just",
        "them", "they", "then", "time", "back", "into", "over", "does",
        "done", "used", "uses", "want", "each", "here", "page", "site",
    ]:
        tok_count.pop(bad, None)

    label    = tok_count.most_common(1)[0][0] if tok_count else f"cluster-{cluster_id}"
    hub_path = HUB_DIR / f"cluster-{cluster_id}-{label}.html"

    items = members[:420]
    lines = [
        "<!doctype html><html lang='en'><head>",
        "<meta charset='utf-8'/>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'/>",
        f"<title>SideGuy Knowledge Cluster: {label} · SideGuy Solutions</title>",
        f"<meta name='description' content='SideGuy knowledge cluster for {label}. Automatically organized for discovery.'/>",
        "<meta name='robots' content='index,follow'/>",
        "</head>",
        "<body style='font-family:-apple-system,system-ui,Segoe UI,Roboto,Arial;max-width:980px;margin:24px auto;padding:0 14px;line-height:1.5;color:#073044;background:#eefcff'>",
        "<p><a href='/'>Home</a> · <a href='/hub.html'>Operator Hub</a></p>",
        f"<h1>Knowledge Cluster: {label}</h1>",
        "<p>Semantically connected pages across the SideGuy network.</p>",
        f"<p><strong>Pages in cluster:</strong> {len(members)}</p>",
        "<ul>",
    ]
    for p in items:
        rel = "/" + Path(p).name
        lines.append(f"<li><a href='{rel}'>{titles.get(p, Path(p).stem)}</a></li>")
    lines += ["</ul>", "</body></html>"]

    hub_path.write_text("\n".join(lines), encoding="utf-8")
    cluster_hubs.append(str(hub_path))

print(f"KG: cluster hubs written: {len(cluster_hubs)}")

# ── Inject neighbor links into pages ─────────────────────────────────────────
inserted = 0

for path, neigh in neighbors_map.items():
    p = Path(path)
    if not neigh:
        continue
    try:
        html = p.read_text(encoding="utf-8", errors="ignore")
        if "SideGuy Knowledge Graph" in html:
            continue

        rows = "\n".join(
            f"<li><a href='/{Path(n).name}'>{titles.get(n, Path(n).stem.replace('-',' ').title())}</a></li>"
            for n in neigh
        )
        block = (
            "\n<section style='border:1px solid rgba(33,211,161,.35);padding:14px 18px;"
            "border-radius:12px;margin:22px 0;background:rgba(0,48,68,.04)'>\n"
            "<h3 style='font-size:1rem;font-weight:700;color:#073044;margin:0 0 6px'>SideGuy Knowledge Graph</h3>\n"
            "<p style='font-size:.85rem;color:#3f6173;margin:0 0 8px'>Related pages connected by topic similarity.</p>\n"
            f"<ul style='margin:0;padding-left:18px;font-size:.9rem'>\n{rows}\n</ul>\n"
            "</section>\n"
        )

        if "</body>" in html:
            html = html.replace("</body>", block + "</body>", 1)
        else:
            html += block

        p.write_text(html, encoding="utf-8")
        inserted += 1
    except Exception:
        continue

# ── Write manifest ────────────────────────────────────────────────────────────
manifest = {
    "generated_at_utc":      time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "pages_scanned":         len(pages),
    "pages_with_neighbors":  inserted,
    "neighbors_per_page":    NEIGHBORS,
    "clusters_written":      len(cluster_hubs),
    "cluster_hubs":          cluster_hubs,
    "neighbors_map_sample":  dict(list(neighbors_map.items())[:20]),
}
Path("kg/knowledge-graph.json").write_text(
    json.dumps(manifest, indent=2), encoding="utf-8"
)

print(f"KG: neighbors injected into {inserted} pages")
print(f"KG: manifest -> kg/knowledge-graph.json")
