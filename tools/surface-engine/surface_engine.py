import re
import html
import datetime
from pathlib import Path

NETWORK_DIR = Path("public/network")
SITEMAP_DIR = Path("public/sitemaps")
INCLUDES_DIR = Path("public/includes")
DOCS_DIR = Path("docs/surface-engine")

NETWORK_SITEMAP = SITEMAP_DIR / "network.xml"
SITEMAP_INDEX = SITEMAP_DIR / "sitemap-index.xml"
HOME_FEATURES_INCLUDE = INCLUDES_DIR / "network-featured.html"
DISCOVERY_FEATURES_INCLUDE = INCLUDES_DIR / "network-discovery-featured.html"
SURFACE_REPORT = DOCS_DIR / "surface-report.md"

BASE_URL = "https://www.sideguysolutions.com"

for d in [SITEMAP_DIR, INCLUDES_DIR, DOCS_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def nice(text: str) -> str:
    return " ".join(w.capitalize() for w in text.replace("-", " ").split())


def slug_to_url(slug: str) -> str:
    return f"{BASE_URL}/network/{slug}.html"


def find_network_pages():
    if not NETWORK_DIR.exists():
        return []
    pages = []
    for path in sorted(NETWORK_DIR.glob("*.html")):
        if path.stem == "index":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        title_m = re.search(r"<h1>(.*?)</h1>", text, re.I | re.S)
        title = re.sub(r"<.*?>", "", title_m.group(1)).strip() if title_m else nice(path.stem)
        desc_m = re.search(r'<meta name="description" content="(.*?)">', text, re.I | re.S)
        desc = desc_m.group(1).strip() if desc_m else f"Explore the {nice(path.stem)} network."
        topic_count = len(set(re.findall(r'href="(/auto/problem-pages/[^"]+)"', text)))
        pages.append({
            "slug": path.stem, "title": title, "description": desc,
            "topic_count": topic_count, "url": slug_to_url(path.stem),
        })
    pages.sort(key=lambda x: (-x["topic_count"], x["slug"]))
    return pages


def write_network_sitemap(pages):
    today = datetime.date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"  <url><loc>{BASE_URL}/network/index.html</loc><lastmod>{today}</lastmod></url>",
    ]
    for p in pages:
        lines.append(f"  <url><loc>{html.escape(p['url'])}</loc><lastmod>{today}</lastmod></url>")
    lines.append("</urlset>")
    NETWORK_SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def existing_sitemaps():
    priority = ["problem-pages.xml", "network.xml", "pages.xml", "main.xml", "services.xml"]
    found = []
    for name in priority:
        if (SITEMAP_DIR / name).exists():
            found.append(name)
    for p in sorted(SITEMAP_DIR.glob("*.xml")):
        if p.name not in found and p.name != "sitemap-index.xml":
            found.append(p.name)
    return found


def write_sitemap_index():
    today = datetime.date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for name in existing_sitemaps():
        lines.append(f"  <sitemap><loc>{BASE_URL}/sitemaps/{name}</loc><lastmod>{today}</lastmod></sitemap>")
    lines.append("</sitemapindex>")
    SITEMAP_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_home_feature_include(pages):
    cards = []
    for p in pages[:6]:
        cards.append(f"""      <a class="sg-network-card" href="/network/{p['slug']}.html">
        <div class="sg-network-card-kicker">SideGuy Network</div>
        <h3>{html.escape(p['title'])}</h3>
        <p>{html.escape(p['description'])}</p>
        <div class="sg-network-card-meta">{p['topic_count']} mapped topics</div>
      </a>""")

    block = f"""<!-- SideGuy Network Featured Include -->
<section class="sg-network-featured">
  <div class="sg-network-featured-inner">
    <div class="sg-network-featured-copy">
      <p class="sg-kicker">Living Problem Map</p>
      <h2>Explore what SideGuy is seeing across payments, AI, local services, and operator problems.</h2>
      <p>The network layer turns real-world problem clusters into visible authority pages.</p>
    </div>
    <div class="sg-network-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>
<style>
.sg-network-featured{{padding:48px 20px}}
.sg-network-featured-inner{{max-width:1200px;margin:0 auto}}
.sg-kicker{{font-size:12px;letter-spacing:.16em;text-transform:uppercase;opacity:.7;margin:0 0 10px}}
.sg-network-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:24px}}
.sg-network-card{{display:block;text-decoration:none;color:inherit;background:rgba(255,255,255,.82);border:1px solid rgba(120,160,200,.25);border-radius:18px;padding:18px;box-shadow:0 10px 30px rgba(0,0,0,.05)}}
.sg-network-card-kicker{{font-size:11px;text-transform:uppercase;letter-spacing:.14em;opacity:.65;margin-bottom:8px}}
.sg-network-card h3{{margin:0 0 10px;font-size:20px;line-height:1.15}}
.sg-network-card p{{margin:0 0 14px;opacity:.82}}
.sg-network-card-meta{{font-size:13px;opacity:.7}}
</style>
"""
    HOME_FEATURES_INCLUDE.write_text(block, encoding="utf-8")


def write_discovery_feature_include(pages):
    items = "".join(
        f'<li><a href="/network/{p["slug"]}.html">{html.escape(p["title"])}</a> · {p["topic_count"]} mapped topics</li>'
        for p in pages[:10]
    )
    block = f"""<!-- SideGuy Discovery Network Include -->
<section class="sg-discovery-network">
  <h2>Featured Network Clusters</h2>
  <p>Main SideGuy knowledge-map clusters generated from radar signals, problem scoring, and network grouping.</p>
  <ul>{items}</ul>
</section>
"""
    DISCOVERY_FEATURES_INCLUDE.write_text(block, encoding="utf-8")


def write_report(pages):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    lines = [
        "# Surface Engine Report", "",
        f"Generated: {now}", "",
        f"Total network pages found: **{len(pages)}**", "",
        "## Featured Network Pages", "",
    ]
    for i, p in enumerate(pages[:12], 1):
        lines.append(f"{i}. **{p['title']}** — `{p['slug']}` — {p['topic_count']} mapped topics")

    lines += [
        "", "## Files Written", "",
        f"- `{NETWORK_SITEMAP}`",
        f"- `{SITEMAP_INDEX}`",
        f"- `{HOME_FEATURES_INCLUDE}`",
        f"- `{DISCOVERY_FEATURES_INCLUDE}`",
        f"- `{SURFACE_REPORT}`",
        "", "## Suggested Wiring", "",
        "- Add `public/includes/network-featured.html` to homepage below hero or service pillars.",
        "- Add `public/includes/network-discovery-featured.html` to the problem discovery page.",
        "- Submit `/sitemaps/sitemap-index.xml` in Search Console.",
        "- Link `/network/index.html` from homepage nav, footer, or operator index area.",
    ]
    SURFACE_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    pages = find_network_pages()
    write_network_sitemap(pages)
    write_sitemap_index()
    write_home_feature_include(pages)
    write_discovery_feature_include(pages)
    write_report(pages)

    print("Surface engine complete.")
    print(f"Network pages found:    {len(pages)}")
    print(f"Network sitemap:        {NETWORK_SITEMAP}")
    print(f"Sitemap index:          {SITEMAP_INDEX}")
    print(f"Homepage include:       {HOME_FEATURES_INCLUDE}")
    print(f"Discovery include:      {DISCOVERY_FEATURES_INCLUDE}")
    print(f"Report:                 {SURFACE_REPORT}")


if __name__ == "__main__":
    main()
