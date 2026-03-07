import os
import csv
import re
import html
import datetime
from pathlib import Path

RADAR_FILE = "docs/problem-radar/radar-signals.tsv"
PAGES_DIR = Path("auto/problem-pages")
HUBS_DIR = Path("auto/problem-hubs")
DOCS_DIR = Path("docs/traffic-engine")
SITEMAP_FILE = Path("public/sitemaps/problem-pages.xml")
LEADERBOARD_FILE = DOCS_DIR / "problem-leaderboard.md"
MANIFEST_FILE = DOCS_DIR / "problem-cluster-manifest.md"
BASE_URL = "https://www.sideguysolutions.com"

for d in [PAGES_DIR, HUBS_DIR, DOCS_DIR, SITEMAP_FILE.parent]:
    d.mkdir(parents=True, exist_ok=True)

HIGH_VALUE_WORDS = [
    "payment", "payments", "processor", "processing", "fees", "software",
    "saas", "ai", "automation", "compliance", "tax", "bookkeeping", "hvac",
    "plumbing", "electrical", "solar", "energy", "repair", "install",
    "installation", "crm", "pos", "chargeback", "merchant", "website",
    "seo", "ads", "lead", "leads", "contractor", "medical", "device",
]

URGENCY_WORDS = [
    "broken", "down", "not working", "stopped", "failed", "problem",
    "issue", "error", "warning", "expensive", "too high", "delayed",
    "stuck", "confusing", "urgent",
]

MONEY_WORDS = [
    "cost", "price", "fees", "quote", "save", "saving", "cheaper",
    "expensive", "roi", "margin", "profit", "waste", "overpaying",
]

LOCAL_MODIFIERS = [
    "san diego", "encinitas", "carlsbad", "oceanside", "vista",
    "san marcos", "escondido", "del mar", "la jolla", "coronado",
    "chula vista",
]

INTENT_MODIFIERS = [
    "cost", "pricing", "near me", "for small business", "for contractors",
    "for restaurants", "for medical offices", "how it works", "best options",
    "explained", "setup guide", "troubleshooting", "vs stripe", "vs square",
    "checklist",
]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def title_case(text: str) -> str:
    return " ".join(w.capitalize() for w in text.split())


def score_problem(topic: str) -> int:
    t = topic.lower()
    score = 0
    for w in HIGH_VALUE_WORDS:
        if w in t:
            score += 5
    for w in URGENCY_WORDS:
        if w in t:
            score += 4
    for w in MONEY_WORDS:
        if w in t:
            score += 4
    for city in LOCAL_MODIFIERS:
        if city in t:
            score += 6
    score += min(len(t.split()), 12)
    return score


def cluster_root(topic: str) -> str:
    t = topic.lower()
    strip_terms = (
        LOCAL_MODIFIERS
        + ["near me", "cost", "pricing", "explained", "checklist",
           "setup guide", "troubleshooting", "best options"]
    )
    for term in strip_terms:
        t = t.replace(f" {term}", "")
    return re.sub(r"\s+", " ", t).strip()


def expand_topic(topic: str):
    seen = set()
    out = []
    root = cluster_root(topic.strip())
    candidates = [topic.strip()]
    for mod in INTENT_MODIFIERS:
        candidates.append(f"{root} {mod}")
    for city in LOCAL_MODIFIERS[:5]:
        candidates.append(f"{root} {city}")
        candidates.append(f"{root} cost {city}")
        candidates.append(f"{root} for small business {city}")
    for c in candidates:
        clean = re.sub(r"\s+", " ", c).strip()
        if clean and clean not in seen:
            seen.add(clean)
            out.append(clean)
    return out[:18]


def read_existing_urls():
    if not SITEMAP_FILE.exists():
        return set()
    return set(re.findall(r"<loc>(.*?)</loc>", SITEMAP_FILE.read_text()))


def ensure_sitemap_header():
    if not SITEMAP_FILE.exists():
        SITEMAP_FILE.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            "</urlset>\n"
        )


def append_sitemap_urls(new_urls):
    ensure_sitemap_header()
    content = SITEMAP_FILE.read_text()
    content = content.rstrip().rstrip("</urlset>").rstrip()
    today = datetime.date.today().isoformat()
    for url in new_urls:
        content += (
            "\n  <url>\n"
            f"    <loc>{html.escape(url)}</loc>\n"
            f"    <lastmod>{today}</lastmod>\n"
            "  </url>"
        )
    SITEMAP_FILE.write_text(content + "\n</urlset>\n")


def page_url(slug: str) -> str:
    return f"{BASE_URL}/auto/problem-pages/{slug}.html"


def hub_url(slug: str) -> str:
    return f"{BASE_URL}/auto/problem-hubs/{slug}.html"


def create_problem_page(topic: str, root: str, score: int):
    slug = slugify(topic)
    path = PAGES_DIR / f"{slug}.html"
    if path.exists():
        return slug, False

    esc_topic = html.escape(topic)
    esc_root = html.escape(root)
    now = datetime.datetime.now().strftime("%B %d, %Y")
    related = [
        f"{root} cost", f"{root} pricing", f"{root} explained",
        f"{root} troubleshooting", f"{root} san diego",
    ]
    related_links = "\n".join(
        f'<li><a href="/auto/problem-pages/{slugify(r)}.html">'
        f'{html.escape(title_case(r))}</a></li>'
        for r in related
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc_topic} | SideGuy Solutions</title>
  <meta name="description" content="Clear help for {esc_topic}. SideGuy explains the problem, options, cost angles, and next steps before you spend money.">
  <link rel="canonical" href="{page_url(slug)}">
  <style>
    :root{{--mint:#21d3a1;--ink:#073044;--bg:#f7fbff}}
    body{{font-family:-apple-system,system-ui,sans-serif;max-width:900px;margin:0 auto;padding:40px 20px;line-height:1.6;background:var(--bg);color:var(--ink)}}
    h1,h2{{line-height:1.25}}
    .card{{background:#fff;border:1px solid #d9e8f2;border-radius:16px;padding:20px;margin:20px 0}}
    .orb{{position:fixed;right:18px;bottom:18px;background:var(--mint);color:#fff;padding:14px 18px;border-radius:999px;text-decoration:none;font-weight:700;box-shadow:0 8px 25px rgba(33,211,161,.4)}}
    a{{color:#0b5cad}}
    ul{{padding-left:20px}}
    .meta{{font-size:.85rem;opacity:.7}}
  </style>
</head>
<body>
  <p><a href="/">← Back to Home</a></p>
  <h1>{esc_topic}</h1>
  <p class="meta">Updated {now} · Problem score: {score}</p>

  <div class="card">
    <p>Searching for <strong>{esc_topic}</strong> usually means something is unclear, expensive, broken, or about to waste time.</p>
    <p>SideGuy is built for this exact moment: clarity before cost.</p>
  </div>

  <div class="card">
    <h2>What this usually means</h2>
    <p>This problem generally sits inside the broader cluster: <strong>{esc_root}</strong>. People usually want a simple answer to one of four things: what it is, what it costs, what to do next, and who to trust.</p>
  </div>

  <div class="card">
    <h2>Fast reality check</h2>
    <ul>
      <li>Is the issue urgent, or just annoying?</li>
      <li>Is there a cost leak happening right now?</li>
      <li>Is this a software/configuration issue or a human/vendor issue?</li>
      <li>Can you avoid paying someone before understanding the root cause?</li>
    </ul>
  </div>

  <div class="card">
    <h2>Related pages</h2>
    <ul>
      {related_links}
    </ul>
  </div>

  <div class="card">
    <h2>Need a human brain on it?</h2>
    <p>Text PJ and get calm, real-world guidance before you overpay, waste time, or get sold the wrong fix.</p>
  </div>

  <a class="orb" href="sms:+17735441231">Text PJ</a>
</body>
</html>
"""
    path.write_text(page)
    return slug, True


def create_hub(root: str, children):
    hub_slug = slugify(root)
    path = HUBS_DIR / f"{hub_slug}.html"
    items = "\n".join(
        f'<li><a href="/auto/problem-pages/{slugify(c["topic"])}.html">'
        f'{html.escape(title_case(c["topic"]))}</a> · score {c["score"]}</li>'
        for c in children[:24]
    )
    now = datetime.datetime.now().strftime("%B %d, %Y")
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title_case(root))} Hub | SideGuy Solutions</title>
  <meta name="description" content="Explore the SideGuy cluster for {html.escape(root)}: costs, troubleshooting, local pages, and operator guidance.">
  <link rel="canonical" href="{hub_url(hub_slug)}">
  <style>
    :root{{--mint:#21d3a1;--ink:#073044;--bg:#f7fbff}}
    body{{font-family:-apple-system,system-ui,sans-serif;max-width:1000px;margin:0 auto;padding:40px 20px;line-height:1.6;background:var(--bg);color:var(--ink)}}
    .card{{background:#fff;border:1px solid #d9e8f2;border-radius:16px;padding:20px;margin:20px 0}}
    .orb{{position:fixed;right:18px;bottom:18px;background:var(--mint);color:#fff;padding:14px 18px;border-radius:999px;text-decoration:none;font-weight:700;box-shadow:0 8px 25px rgba(33,211,161,.4)}}
    a{{color:#0b5cad}}
  </style>
</head>
<body>
  <p><a href="/">← Back to Home</a></p>
  <h1>{html.escape(title_case(root))} Hub</h1>
  <p>Updated {now}. This hub groups problem pages around one real-world issue cluster.</p>

  <div class="card">
    <h2>Cluster pages</h2>
    <ul>
      {items}
    </ul>
  </div>

  <div class="card">
    <h2>Why this exists</h2>
    <p>Most people do not need more noise. They need a clean map of the problem, what it might cost, what to ignore, and what to do next.</p>
  </div>

  <a class="orb" href="sms:+17735441231">Text PJ</a>
</body>
</html>
"""
    path.write_text(page)
    return hub_slug


def load_topics():
    if not os.path.exists(RADAR_FILE):
        return []
    with open(RADAR_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return [
            r.get("topic", "").strip()
            for r in reader
            if r.get("topic", "").strip()
        ]


def main():
    seed_topics = load_topics()
    all_topics = []
    for seed in seed_topics:
        all_topics.extend(expand_topic(seed))

    # Deduplicate by slug
    seen = set()
    deduped = []
    for t in all_topics:
        s = slugify(t)
        if s and s not in seen:
            seen.add(s)
            deduped.append(t)

    scored = sorted(
        [{"topic": t, "root": cluster_root(t), "score": score_problem(t)} for t in deduped],
        key=lambda x: x["score"],
        reverse=True,
    )

    existing_urls = read_existing_urls()
    new_urls = []
    cluster_map = {}
    created_pages = 0

    for item in scored[:250]:
        slug, created = create_problem_page(item["topic"], item["root"], item["score"])
        if created:
            created_pages += 1
        url = page_url(slug)
        if url not in existing_urls:
            new_urls.append(url)
        cluster_map.setdefault(item["root"], []).append(item)

    created_hubs = 0
    top_clusters = sorted(
        cluster_map.items(),
        key=lambda kv: max(x["score"] for x in kv[1]),
        reverse=True,
    )[:40]
    for root, children in top_clusters:
        hub_slug = create_hub(root, children)
        url = hub_url(hub_slug)
        if url not in existing_urls:
            new_urls.append(url)
        created_hubs += 1

    if new_urls:
        append_sitemap_urls(new_urls)

    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        f.write("# SideGuy Problem Leaderboard\n\n")
        f.write(f"Generated: {datetime.datetime.now().isoformat()}\n\n")
        f.write("| Rank | Topic | Score | Cluster |\n")
        f.write("|---|---|---:|---|\n")
        for i, item in enumerate(scored[:100], 1):
            f.write(f"| {i} | {item['topic']} | {item['score']} | {item['root']} |\n")

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        f.write("# SideGuy Problem Cluster Manifest\n\n")
        f.write(f"Generated: {datetime.datetime.now().isoformat()}\n\n")
        for root, children in top_clusters:
            f.write(f"## {title_case(root)}\n\n")
            for child in children[:15]:
                f.write(f"- {child['topic']} | score {child['score']}\n")
            f.write("\n")

    print("Traffic engine complete.")
    print(f"Seed topics loaded:           {len(seed_topics)}")
    print(f"Expanded topics scored:       {len(scored)}")
    print(f"Problem pages created:        {created_pages}")
    print(f"Hubs generated:               {created_hubs}")
    print(f"New sitemap URLs appended:    {len(new_urls)}")
    print(f"Leaderboard:  {LEADERBOARD_FILE}")
    print(f"Manifest:     {MANIFEST_FILE}")
    print(f"Sitemap:      {SITEMAP_FILE}")


if __name__ == "__main__":
    main()
