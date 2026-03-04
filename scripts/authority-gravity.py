#!/usr/bin/env python3
import os, re, json, math
from pathlib import Path
from html import escape

ROOT      = Path(".")
PHONE_SMS = "sms:+17735441231"
PHONE_TEL = "tel:+17735441231"

# Directories to wire (problems & hubs are excluded — problems already have pills;
# hubs are link-dump pages; both would cause O(n²) slowdown with no SEO benefit)
INCLUDE_DIRS = [
    "pillars", "clusters", "concepts", "generated", "auto",
    "longtail", "prediction-markets", "knowledge", "authority", "fresh",
    "operator-guides", "operator-tools", "gravity",
]
EXCLUDE_DIRS       = {"node_modules", ".git", ".next", "dist", "build", "out", "public", "assets", "images", "img", "static", "sitemaps"}
EXCLUDE_PATH_HINTS = ["/node_modules/", "/.git/", "/.next/", "/dist/", "/out/", "/sitemaps/"]

# Set True only if you want to also wire the 2,000+ problems pages (slow)
INCLUDE_PROBLEMS = False

MARK_START = "<!-- SG:RELATED_GUIDES_START -->"
MARK_END   = "<!-- SG:RELATED_GUIDES_END -->"

STOPWORDS = set(
    "a an and are as at be but by can could did do does doing for from had has "
    "have how i if in into is it its just may might more most much must my no "
    "not of on or our out over same should so some than that the their them then "
    "there these they this to too up us was we were what when where which who "
    "why will with you your".split()
)


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def write_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def tokenize(s: str):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s\-]+", " ", s)
    toks = []
    for t in re.split(r"[\s\-]+", s):
        if t and t not in STOPWORDS and len(t) > 2:
            toks.append(t)
    return toks


def extract_title_h1(html: str):
    title = ""
    h1    = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        title = re.sub(r"\s*[·|]\s*SideGuy.*$", "", title).strip()
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if m:
        h1 = re.sub(r"<[^>]+>", "", m.group(1))
        h1 = re.sub(r"\s+", " ", h1).strip()
    return title, h1


def bucket_for(path: str) -> str:
    p = path.lstrip("./")
    if p.startswith("problems/"):       return "problems"
    if p.startswith("pillars/"):        return "pillars"
    if p.startswith("hubs/"):           return "hubs"
    if p.startswith("clusters/"):       return "clusters"
    if p.startswith("concepts/"):       return "concepts"
    if p.startswith("generated/"):      return "generated"
    if p.startswith("auto/"):           return "auto"
    if p.startswith("longtail/"):       return "longtail"
    if p.startswith("prediction-markets/"): return "prediction-markets"
    if p.startswith("knowledge/"):      return "knowledge"
    if p.startswith("authority/"):      return "authority"
    if p.startswith("fresh/"):          return "fresh"
    if p.startswith("gravity/"):        return "gravity"
    return "root"


def rel_url(path: str) -> str:
    return "/" + path.lstrip("./")


def exists_marker(html: str) -> bool:
    return MARK_START in html and MARK_END in html


def inject_or_replace(html: str, block: str) -> str:
    insert = MARK_START + "\n" + block.strip() + "\n" + MARK_END + "\n"
    if exists_marker(html):
        pre, rest = html.split(MARK_START, 1)
        _, post   = rest.split(MARK_END, 1)
        return pre + insert[:-1] + post  # -1 removes trailing \n before post
    if re.search(r"</main>", html, re.I):
        return re.sub(r"</main>", insert + "</main>", html, flags=re.I, count=1)
    if re.search(r"</body>", html, re.I):
        return re.sub(r"</body>", insert + "</body>", html, flags=re.I, count=1)
    return html + "\n" + insert


def enforce_phone(html: str) -> str:
    html = re.sub(r'href="sms:[^"]*773\-?544\-?1231[^"]*"', f'href="{PHONE_SMS}"', html)
    html = re.sub(r'href="sms:[^"]*17735441231[^"]*"',       f'href="{PHONE_SMS}"', html)
    html = re.sub(r'href="tel:[^"]*773\-?544\-?1231[^"]*"',  f'href="{PHONE_TEL}"', html)
    html = re.sub(r'href="tel:[^"]*17735441231[^"]*"',        f'href="{PHONE_TEL}"', html)
    return html


def build_inventory():
    pages = []
    for d in INCLUDE_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*.html"):
            sp  = str(p).replace("\\", "/")
            top = sp.split("/")[0]
            if top in EXCLUDE_DIRS:
                continue
            if any(h in sp for h in EXCLUDE_PATH_HINTS):
                continue
            if not INCLUDE_PROBLEMS and sp.startswith("problems/"):
                continue
            html = read_text(p)
            if not html.strip():
                continue
            title, h1 = extract_title_h1(html)
            if len(title) < 3 and len(h1) < 3:
                continue
            slug   = Path(sp).stem
            bucket = bucket_for(sp)
            toks   = tokenize(" ".join([title, h1, slug, sp]))
            pages.append({
                "path":   sp,
                "url":    rel_url(sp),
                "title":  (title or h1 or slug).strip(),
                "bucket": bucket,
                "tokens": sorted(set(toks)),
            })
    # dedupe by url
    best = {}
    for pg in pages:
        u = pg["url"]
        if u not in best:
            best[u] = pg
    return list(best.values())


def score_pair(a, b):
    ta, tb = set(a["tokens"]), set(b["tokens"])
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    if inter == 0:
        return 0.0
    s = inter / math.sqrt(len(ta) * len(tb))
    if a["bucket"] == b["bucket"]:
        s *= 1.25
    if b["bucket"] in ("pillars", "hubs", "knowledge", "authority"):
        s *= 1.15
    return s


def build_related(pages, k=10):
    rel = {}
    for i, a in enumerate(pages):
        scored = []
        for j, b in enumerate(pages):
            if i == j:
                continue
            s = score_pair(a, b)
            if s > 0:
                scored.append((s, b))
        scored.sort(key=lambda x: -x[0])
        rel[a["path"]] = [b for _, b in scored[:k]]
    return rel


def make_block(page, related):
    pills = []
    for b in related:
        pills.append(
            f'<a class="sgpill" href="{escape(b["url"])}" title="{escape(b["title"])}">'
            f'<span class="sgpill__k">{escape(b["bucket"])}</span>'
            f'<span class="sgpill__t">{escape(b["title"])}</span>'
            f"</a>"
        )
    grid = "\n    ".join(pills) if pills else '<div class="sgmuted">No related guides yet.</div>'

    return f"""
<section class="sgRelatedGuides" aria-label="Related Guides">
  <div class="sgRelatedGuides__head">
    <h2>Related Guides</h2>
    <div class="sgRelatedGuides__sub">Internal links to help operators go deeper (AI explains it, humans resolve it).</div>
  </div>
  <div class="sgRelatedGuides__grid">
    {grid}
  </div>
  <div class="sgRelatedGuides__cta">
    <a class="sgCtaBtn" href="{PHONE_SMS}">Text PJ</a>
    <span class="sgmuted">Fast clarity · No pressure · 773-544-1231</span>
  </div>
</section>
<style>
  .sgRelatedGuides{{margin:28px 0 8px;padding:18px;border-radius:16px;
    background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.02));
    border:1px solid rgba(255,255,255,.10);}}
  .sgRelatedGuides__head h2{{margin:0;font-size:18px;}}
  .sgRelatedGuides__sub{{margin-top:6px;opacity:.85;font-size:13px;}}
  .sgRelatedGuides__grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-top:12px;}}
  .sgpill{{display:flex;gap:10px;align-items:flex-start;text-decoration:none;padding:12px;border-radius:14px;
    border:1px solid rgba(0,0,0,.10);background:rgba(0,0,0,.05);transition:border-color .15s,transform .15s;}}
  .sgpill:hover{{transform:translateY(-1px);border-color:rgba(0,180,140,.35);}}
  .sgpill__k{{font-size:11px;opacity:.65;min-width:72px;text-transform:uppercase;letter-spacing:.6px;}}
  .sgpill__t{{font-size:13px;line-height:1.25;opacity:.95;}}
  .sgRelatedGuides__cta{{display:flex;gap:12px;align-items:center;margin-top:12px;}}
  .sgCtaBtn{{display:inline-flex;align-items:center;justify-content:center;padding:10px 14px;border-radius:12px;
    background:#073044;color:#fff;text-decoration:none;font-weight:700;font-size:14px;}}
  .sgmuted{{opacity:.7;font-size:12px;}}
</style>
""".strip()


def main():
    pages = build_inventory()
    pages.sort(key=lambda x: x["path"])

    buckets = {}
    for p in pages:
        buckets[p["bucket"]] = buckets.get(p["bucket"], 0) + 1

    inv = {
        "count":   len(pages),
        "buckets": buckets,
        "pages":   [{"path": p["path"], "url": p["url"], "title": p["title"], "bucket": p["bucket"]} for p in pages],
    }
    os.makedirs("reports", exist_ok=True)
    Path("reports/authority-inventory.json").write_text(json.dumps(inv, indent=2), encoding="utf-8")

    rel     = build_related(pages, k=10)
    changes = 0
    fixed_phone = 0

    for pg in pages:
        path = Path(pg["path"])
        html = read_text(path)
        if not html:
            continue

        new_html = enforce_phone(html)
        if new_html != html:
            fixed_phone += 1
            html = new_html

        related  = rel.get(pg["path"], [])[:10]
        block    = make_block(pg, related)
        new_html = inject_or_replace(html, block)

        if new_html != html:
            write_text(path, new_html)
            changes += 1

    report = [
        "# Authority Gravity Engine Report\n\n",
        f"- Pages scanned: **{len(pages)}**\n",
        f"- Pages updated (Related Guides block): **{changes}**\n",
        f"- Pages with phone href fixes: **{fixed_phone}**\n\n",
        "## Buckets\n",
    ]
    for k in sorted(buckets):
        report.append(f"- {k}: {buckets[k]}\n")
    Path("reports/authority-gravity-report.md").write_text("".join(report), encoding="utf-8")

    print("=== Authority Gravity Engine Done ===")
    print(f"  Pages scanned  : {len(pages)}")
    print(f"  Pages updated  : {changes}")
    print(f"  Phone fixes    : {fixed_phone}")
    print("  reports/authority-inventory.json")
    print("  reports/authority-gravity-report.md")


if __name__ == "__main__":
    main()
