#!/usr/bin/env python3
"""
SideGuy Page Builder
Generates SEO pages from seo-reserve/manifest.json.
Pages follow the site's inline-CSS, self-contained style.
Features:
  - Slug dedup: strips trailing -san-diego before appending it
  - Internal linking: each page links to 3-5 related pages
  - Up-links: each page links to its hub(s) and pillar(s)
  - Sitemap regeneration after every build run
"""

import json, os, re, datetime, subprocess, sys

sys.path.insert(0, os.path.dirname(__file__))
from sideguy_classify import (
    slugify, topic_to_filename, classify_topic,
    CATEGORY_HUB_PATH, CATEGORY_HUB_LABELS,
    PILLAR_MAP, PILLAR_LABELS,
    industry_hub_path, industry_hub_label,
)

MANIFEST   = "seo-reserve/manifest.json"
OUTPUT_DIR = "."


def score_relatedness(a, b):
    """Count shared meaningful words between two topic strings."""
    stopwords = {'for', 'to', 'a', 'an', 'the', 'of', 'and', 'in', 'with',
                 'how', 'best', 'what', 'is', 'are', 'do', 'san', 'diego'}
    words_a = set(re.findall(r'[a-z]+', a.lower())) - stopwords
    words_b = set(re.findall(r'[a-z]+', b.lower())) - stopwords
    return len(words_a & words_b)


def pick_related(topic, all_topics, n=5):
    """Return up to n most-related topics (excluding self)."""
    scored = [
        (score_relatedness(topic, t), t)
        for t in all_topics if t != topic
    ]
    scored.sort(key=lambda x: -x[0])
    top = [t for score, t in scored[:n] if score > 0]
    if len(top) < 3:
        top = [t for _, t in scored[:n]]
    return top[:n]


def build_related_links_html(related_topics):
    if not related_topics:
        return ""
    items = "".join(
        f'    <li><a href="{topic_to_filename(t)}">{t.title()}</a></li>\n'
        for t in related_topics
    )
    return f"""
  <div class="card">
    <h2>Related guides</h2>
    <ul style="margin:0;padding-left:1.4rem;color:var(--muted);line-height:1.9;">
{items}    </ul>
  </div>
"""


def build_uplinks_html(topic):
    """
    Returns an uplinks breadcrumb-style nav bar linking to:
    hub.html, category hub(s), industry hub (if any), pillar(s).
    """
    info  = classify_topic(topic)
    links = [('<a href="/hub.html">Operator Hub</a>', None)]

    for cat in info['categories']:
        hub_path  = CATEGORY_HUB_PATH.get(cat, '')
        hub_label = CATEGORY_HUB_LABELS.get(cat, '')
        if hub_path:
            links.append((f'<a href="/{hub_path}">{hub_label}</a>', None))

    ind = info['industry']
    if ind:
        links.append((f'<a href="/{industry_hub_path(ind)}">{industry_hub_label(ind)}</a>', None))

    for cat in info['categories']:
        pillar = PILLAR_MAP.get(cat, '')
        plabel = PILLAR_LABELS.get(cat, '')
        if pillar:
            links.append((f'<a href="/{pillar}">{plabel}</a>', None))

    if len(links) <= 1:
        return ""

    sep = '<span style="opacity:.4;margin:0 4px;">/</span>'
    chain = sep.join(a for a, _ in links)
    return f"""
<nav style="max-width:820px;margin:12px auto 0;padding:0 24px;
     font-size:.82rem;color:#3f6173;display:flex;flex-wrap:wrap;
     align-items:center;gap:4px;">
  {chain}
</nav>"""


def build_page(topic, all_topics):
    title_case = topic.title()
    slug = slugify(topic)
    filename = topic_to_filename(topic)
    path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(path):
        print(f"Skip (exists): {filename}")
        return None

    today    = datetime.date.today().isoformat()
    canonical = f"https://sideguysolutions.com/{filename}"
    related   = pick_related(topic, all_topics, n=5)
    related_html = build_related_links_html(related)
    uplinks_html = build_uplinks_html(topic)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{title_case} San Diego · SideGuy</title>
<link rel="canonical" href="{canonical}"/>
<meta name="description" content="{title_case} in San Diego — plain-language guide and real help from SideGuy. Clarity before cost."/>
<style>
  :root{{
    --bg0:#eefcff;
    --bg1:#d7f5ff;
    --bg2:#bfeeff;
    --ink:#073044;
    --muted:#3f6173;
    --card:#ffffffcc;
    --stroke:rgba(7,48,68,.10);
    --shadow:0 18px 50px rgba(7,48,68,.10);
    --mint:#21d3a1;
    --mint2:#00c7ff;
    --r:22px;
    --pill:999px;
    --phone:"+17604541860";
    --phonePretty:"760-454-1860";
    --city:"San Diego";
  }}
  *{{box-sizing:border-box}}
  html,body{{height:100%}}
  body{{
    margin:0;
    font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,Arial,sans-serif;
    color:var(--ink);
    background:radial-gradient(ellipse 120% 80% at 50% -10%,var(--bg2) 0%,var(--bg1) 40%,var(--bg0) 100%);
    min-height:100vh;
  }}
  header{{
    max-width:820px;margin:0 auto;padding:40px 24px 0;
    display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;
  }}
  .logo{{font-weight:800;font-size:1.25rem;color:var(--ink);text-decoration:none;letter-spacing:-.5px;}}
  .cta-pill{{
    background:linear-gradient(135deg,var(--mint),var(--mint2));
    color:#fff;font-weight:700;font-size:.9rem;
    padding:10px 22px;border-radius:var(--pill);text-decoration:none;
    box-shadow:0 4px 16px rgba(33,211,161,.35);
  }}
  main{{max-width:820px;margin:0 auto;padding:48px 24px 80px;}}
  h1{{font-size:clamp(1.6rem,4vw,2.4rem);font-weight:900;line-height:1.2;margin:0 0 16px;}}
  .subtitle{{font-size:1.05rem;color:var(--muted);margin:0 0 40px;line-height:1.6;}}
  .card{{
    background:var(--card);border:1px solid var(--stroke);
    border-radius:var(--r);padding:28px 32px;margin-bottom:24px;
    box-shadow:var(--shadow);
  }}
  .card h2{{font-size:1.2rem;font-weight:800;margin:0 0 12px;}}
  .card p{{margin:0 0 10px;line-height:1.7;color:var(--muted);}}
  .card p:last-child{{margin-bottom:0;}}
  .card ul a{{color:var(--ink);font-weight:600;}}
  .cta-block{{
    background:linear-gradient(135deg,var(--mint),var(--mint2));
    border-radius:var(--r);padding:36px 32px;text-align:center;margin-top:40px;
    box-shadow:0 12px 40px rgba(33,211,161,.3);
  }}
  .cta-block p{{color:#fff;font-size:1.05rem;margin:0 0 20px;font-weight:500;}}
  .cta-block a{{
    display:inline-block;background:#fff;color:var(--ink);
    font-weight:800;font-size:1rem;padding:14px 32px;
    border-radius:var(--pill);text-decoration:none;
    box-shadow:0 4px 14px rgba(0,0,0,.12);
  }}
  footer{{
    max-width:820px;margin:0 auto;padding:0 24px 48px;
    color:var(--muted);font-size:.85rem;
  }}
  footer a{{color:var(--muted);}}
</style>
</head>
<body>
<header>
  <a class="logo" href="/">SideGuy</a>
  <a class="cta-pill" href="sms:+17604541860">Text PJ</a>
</header>
{uplinks_html}
<main>
  <h1>{title_case} — Plain-Language Guide (San Diego)</h1>
  <p class="subtitle">
    Most people searching for "{topic}" just want a straight answer before spending money.
    Here's what you actually need to know.
  </p>

  <div class="card">
    <h2>What this is</h2>
    <p>
      {title_case} is something a lot of San Diego businesses and operators are figuring out right now.
      The terminology is confusing, the vendors are pushy, and it's hard to know who to trust.
    </p>
    <p>
      SideGuy is a human-first clarity layer. We explain options honestly before any transaction happens.
    </p>
  </div>

  <div class="card">
    <h2>What you should know first</h2>
    <p>
      Before hiring anyone or buying anything related to {topic}, make sure you understand
      what problem you're actually solving. Most pitches oversell complexity.
    </p>
    <p>
      Ask: What does success look like in 90 days? What does it cost if nothing works?
      Can I reverse this decision?
    </p>
  </div>

  <div class="card">
    <h2>Common mistakes</h2>
    <p>Paying for a solution before defining the problem clearly.</p>
    <p>Choosing a vendor because they ranked first on Google.</p>
    <p>Signing long contracts for services you haven't tested yet.</p>
  </div>
{related_html}
  <div class="cta-block">
    <p>Want a real human to look at your situation — no pitch, no pressure?</p>
    <a href="sms:+17604541860">Text PJ · 760-454-1860</a>
  </div>
</main>
<footer>
  <p>
    <a href="/">SideGuy Solutions</a> · San Diego ·
    <a href="sms:+17604541860">760-454-1860</a>
  </p>
  <p>Clarity before cost. Updated {today}.</p>
</footer>
</body>
</html>
"""

    with open(path, "w") as f:
        f.write(html)
    print(f"Created: {filename}")
    return filename


def main():
    with open(MANIFEST) as f:
        data = json.load(f)

    all_topics = data["topics"]
    created = []
    for topic in all_topics:
        result = build_page(topic, all_topics)
        if result:
            created.append(result)

    print(f"Done. {len(all_topics)} topics processed, {len(created)} new pages created.")

    # Always regenerate sitemap after a build run
    scripts_dir = os.path.dirname(__file__)
    sitemap_script = os.path.join(scripts_dir, "generate-sitemap.py")
    if os.path.exists(sitemap_script):
        subprocess.run(["python3", sitemap_script], check=True)

    return created


if __name__ == "__main__":
    main()
