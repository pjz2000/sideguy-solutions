#!/usr/bin/env python3
"""
SideGuy Pillar Engine — Wikipedia-style concept pages
Writes pillars/{slug}.html (separate from the 4 {cat}-master-guide.html
files built by build-authority.py — no filename collision).
"""
import os, re, html as htmllib, argparse
from datetime import datetime, timezone

STOP = set("""
a an and are as at be but by for from has have if in into is it its of on or our
so that the their then there these this to up we with you your san diego sideguy
solutions solve solving service services
""".split())


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "pillar"


def title_case(s: str) -> str:
    UPPER = {"ai", "api", "seo", "faq", "sd", "ux", "ui", "llm"}
    return " ".join(
        w.upper() if w.lower() in UPPER else w.capitalize()
        for w in re.split(r"[\s\-]+", s.strip()) if w
    )


def read_lines(path: str):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            out.append(line)
    return out


def pick_hub_topics(hubs_dir="hubs", limit=50):
    topics = []
    if not os.path.isdir(hubs_dir):
        return topics
    for n in sorted(os.listdir(hubs_dir)):
        if not n.endswith(".html"):
            continue
        base = n[:-5]
        base = re.sub(r"^(hub|category|industry|city|cluster)-", "", base)
        base = base.replace("san-diego", "").strip("-")
        if base:
            topics.append(base)
        if len(topics) >= limit:
            break
    return topics


def pick_leaf_links(keyword: str, limit=30):
    kw = keyword.lower().replace("-", "")
    hits = []
    for fn in os.listdir("."):
        if not fn.endswith(".html"):
            continue
        if fn in {"index.html", "hub.html", "404.html", "-hub.html"}:
            continue
        if fn.startswith("aaa-"):
            continue
        if kw in fn.lower().replace("-", ""):
            hits.append(fn)
    hits.sort()
    return hits[:limit]


def pick_hub_links(keyword: str, limit=24):
    kw = keyword.lower().replace("-", "")
    hits = []
    if not os.path.isdir("hubs"):
        return hits
    for fn in sorted(os.listdir("hubs")):
        if not fn.endswith(".html"):
            continue
        if kw in fn.lower().replace("-", ""):
            hits.append("hubs/" + fn)
    return hits[:limit]


def build_page(topic_title: str, topic_slug: str,
               related_hubs, related_pages, updated_iso: str) -> str:
    esc   = htmllib.escape
    t     = esc(topic_title)
    u     = esc(updated_iso)
    sl    = esc(topic_slug)
    canon = f"https://sideguysolutions.com/pillars/{sl}.html"

    hub_items = "\n".join(
        f'<li><a href="/{esc(p)}">{esc(os.path.basename(p).replace(".html","").replace("-"," "))}</a></li>'
        for p in related_hubs
    ) or "<li><em>More hub links will appear as the graph expands.</em></li>"

    leaf_items = "\n".join(
        f'<li><a href="/{esc(p)}">{esc(p.replace(".html","").replace("-"," "))}</a></li>'
        for p in related_pages
    ) or "<li><em>More related pages will appear on next build.</em></li>"

    jsonld = (
        '<script type="application/ld+json">\n'
        '{\n'
        f'  "@context":"https://schema.org",\n'
        f'  "@type":"Article",\n'
        f'  "headline":"{t}",\n'
        f'  "description":"Wikipedia-style operator guide to {t}.",\n'
        f'  "url":"{esc(canon)}",\n'
        f'  "dateModified":"{u}",\n'
        '  "author":{"@type":"Organization","name":"SideGuy Solutions"},\n'
        '  "publisher":{"@type":"Organization","name":"SideGuy Solutions","url":"https://sideguysolutions.com"}\n'
        '}\n'
        '</script>'
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{t} — SideGuy Concept Guide</title>
  <meta name="description" content="Wikipedia-style operator guide to {t}: what it is, how it works, common pitfalls, and real San Diego context. Clarity before cost."/>
  <link rel="canonical" href="{esc(canon)}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="{t} — SideGuy Concept Guide"/>
  <meta property="og:url" content="{esc(canon)}"/>
  <meta property="og:site_name" content="SideGuy Solutions"/>
  {jsonld}
  <style>
    :root {{
      --bg:#07121a;--card:#0b1b25;--text:#e9f2ff;--muted:#a9c0d6;
      --line:#123041;--accent:#68f0c6;--accent2:#7ab6ff;
      --mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Courier New",monospace;
      --sans:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
    }}
    *{{box-sizing:border-box}}
    body{{margin:0;font-family:var(--sans);
      background:radial-gradient(1200px 700px at 20% 0%,#0b2331 0%,var(--bg) 55%),var(--bg);
      color:var(--text);line-height:1.6}}
    a{{color:var(--accent2);text-decoration:none}} a:hover{{text-decoration:underline}}
    .wrap{{max-width:1040px;margin:0 auto;padding:28px 18px 80px}}
    .topbar{{display:flex;gap:12px;align-items:center;justify-content:space-between;
      margin-bottom:18px;flex-wrap:wrap}}
    .badge{{font-family:var(--mono);font-size:12px;color:var(--muted);
      border:1px solid var(--line);padding:6px 10px;border-radius:999px;
      background:rgba(255,255,255,0.03)}}
    h1{{font-size:clamp(1.6rem,4vw,2.1rem);line-height:1.15;margin:10px 0 8px;font-weight:900}}
    .sub{{color:var(--muted);margin:0 0 22px}}
    .k{{color:var(--accent);font-family:var(--mono);font-size:12px}}
    .layout{{display:grid;grid-template-columns:1.25fr .75fr;gap:16px}}
    @media(max-width:820px){{.layout{{grid-template-columns:1fr}}}}
    .card{{background:rgba(255,255,255,0.03);border:1px solid var(--line);
      border-radius:14px;padding:20px}}
    .card h2{{margin:22px 0 10px;font-size:1.1rem;font-weight:800;color:var(--text)}}
    .card h2:first-child{{margin-top:0}}
    .card h3{{margin:14px 0 8px;font-size:.95rem;color:var(--accent);font-weight:700}}
    .card ul{{margin:8px 0 0 20px;padding:0}}
    .card li{{margin-bottom:5px;font-size:.95rem;color:var(--muted)}}
    .card li a{{color:var(--accent2)}}
    .card p{{color:var(--muted);font-size:.95rem;margin:8px 0}}
    .toc-links a{{display:block;padding:5px 0;border-bottom:1px solid var(--line);
      font-size:.9rem;color:var(--muted)}}
    .toc-links a:last-child{{border-bottom:none}}
    .toc-links a:hover{{color:var(--text)}}
    .pill{{display:inline-block;border:1px solid var(--line);
      background:rgba(255,255,255,0.025);padding:4px 10px;border-radius:999px;
      margin:4px 6px 0 0;font-size:.8rem;color:var(--muted)}}
    .note{{color:var(--muted);font-size:.8rem;margin-top:6px}}
    .footer{{margin-top:30px;color:var(--muted);font-size:.8rem;
      border-top:1px solid var(--line);padding-top:16px}}
    .orb{{position:fixed;right:18px;bottom:18px;width:72px;height:72px;
      border-radius:999px;
      background:radial-gradient(circle at 30% 30%,rgba(104,240,198,.95),rgba(122,182,255,.25) 60%,rgba(0,0,0,.25) 100%);
      box-shadow:0 0 0 1px rgba(104,240,198,.25),0 10px 40px rgba(0,0,0,.4);
      display:flex;align-items:center;justify-content:center;text-align:center;
      animation:pulse 2.2s ease-in-out infinite}}
    .orb a{{color:#001018;font-weight:800;font-size:12px;text-decoration:none}}
    @keyframes pulse{{0%,100%{{transform:translateY(0) scale(1)}}50%{{transform:translateY(-2px) scale(1.03)}}}}
  </style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <div class="badge">SideGuy Pillar Engine · <span class="k">Updated</span> {u}</div>
    <div class="badge"><a href="/hub.html">Operator Hub</a> · <a href="/">Home</a> · <a href="/pillars/index.html">All Pillars</a></div>
  </div>

  <h1>{t}</h1>
  <p class="sub">Wikipedia-style concept guide. Operator-first. <span class="k">Clarity before cost.</span></p>

  <div class="layout">

    <div class="card">
      <h2 id="overview">Overview</h2>
      <p>
        <strong>{t}</strong> is a real-world operator problem-space that touches
        scheduling, cash flow, customer trust, and operational efficiency.
        This page explains what it is, how it works, where operators get stuck,
        and what a minimum-viable resolution looks like — with San Diego context.
      </p>

      <h2 id="definition">Definition</h2>
      <p>
        At its core, <strong>{t}</strong> means having the right system at the
        right cost, with a human escalation path when things go wrong.
        Not a product. Not a vendor. A clear outcome with a measurable definition
        of &ldquo;done.&rdquo;
      </p>

      <h2 id="when">When you need this</h2>
      <ul>
        <li>You&rsquo;re losing time, money, or customer trust and can&rsquo;t identify the leverage point.</li>
        <li>You have tools but they&rsquo;re disconnected or underused.</li>
        <li>You need one clean workflow, a checklist, and a human backstop.</li>
        <li>A competitor is moving faster and you don&rsquo;t know why.</li>
      </ul>

      <h2 id="how">How it works (plain English)</h2>
      <ul>
        <li><strong>Define the outcome</strong> — what &ldquo;done&rdquo; looks like in a single testable sentence.</li>
        <li><strong>Pick the minimum viable system</strong> — one end-to-end workflow before adding complexity.</li>
        <li><strong>Instrument it</strong> — logs, confirmations, metrics that surface problems before customers do.</li>
        <li><strong>Scale after signal</strong> — expand only once the first layer is stable and measurable.</li>
      </ul>

      <h2 id="components">Key components</h2>
      <div class="pill">Clear intake process</div>
      <div class="pill">Authority structure</div>
      <div class="pill">Internal linking</div>
      <div class="pill">Schema + FAQ coverage</div>
      <div class="pill">Refresh / decay cycle</div>
      <div class="pill">Human escalation path</div>
      <div class="pill">Settlement / delivery speed</div>
      <div class="pill">Error + edge-case handling</div>

      <h2 id="mistakes">Common mistakes</h2>
      <ul>
        <li><strong>Random tooling</strong> — disconnected products with no integration plan.</li>
        <li><strong>Over-automation before feedback</strong> — no loop, no human fallback.</li>
        <li><strong>Thin execution</strong> — presence without depth (no structure, no intent match).</li>
        <li><strong>No hub path</strong> — users and crawlers can&rsquo;t navigate to related context.</li>
        <li><strong>Long contracts before pilots</strong> — signing 12 months before running 30 days.</li>
      </ul>

      <h2 id="sd">San Diego considerations</h2>
      <ul>
        <li>Local intent matters: neighborhoods, service-area clarity, and &ldquo;near me&rdquo; signals carry real weight.</li>
        <li>Operators want fast, honest decisions: price ranges, timelines, and explicit risk flags.</li>
        <li>Trust is the currency: human contact info, clear process, and transparency convert better than polish.</li>
        <li>Seasonal + tourism patterns affect timing for many SD service categories.</li>
      </ul>

      <h2 id="evaluation">Evaluation checklist</h2>
      <ul>
        <li>&#9744; What&rsquo;s the setup fee and monthly cost?</li>
        <li>&#9744; What does success look like at 30 / 90 days?</li>
        <li>&#9744; Can I cancel month-to-month?</li>
        <li>&#9744; Who owns the data?</li>
        <li>&#9744; What happens when something goes wrong?</li>
        <li>&#9744; Do you have case studies from similar operators?</li>
      </ul>

      <h2 id="faq">FAQ</h2>
      <ul>
        <li><strong>Is this a service marketplace?</strong> No — SideGuy is a clarity layer that routes you to the right next step, not the highest bidder.</li>
        <li><strong>Do I need to buy anything to start?</strong> No. Build the smallest working system first. Spend only after signal.</li>
        <li><strong>What&rsquo;s the fastest win?</strong> Fix internal structure, publish the right concept pages, and make sure every page has a clear human escalation path.</li>
        <li><strong>How do I know if this applies to my business?</strong> If a customer asked you about {t} this week and you didn&rsquo;t have a clean answer, it applies.</li>
      </ul>
      <p class="note">This pillar is structured so the pipeline stamps schema / OG / FAQ and keeps it fresh on every weekly rebuild.</p>
    </div>

    <div>
      <div class="card" style="margin-bottom:16px">
        <h2 style="margin-top:0">Contents</h2>
        <div class="toc-links">
          <a href="#overview">Overview</a>
          <a href="#definition">Definition</a>
          <a href="#when">When you need this</a>
          <a href="#how">How it works</a>
          <a href="#components">Key components</a>
          <a href="#mistakes">Common mistakes</a>
          <a href="#sd">San Diego considerations</a>
          <a href="#evaluation">Evaluation checklist</a>
          <a href="#faq">FAQ</a>
          <a href="#hubs">Related hubs</a>
          <a href="#pages">Related pages</a>
        </div>
      </div>

      <div class="card" style="margin-bottom:16px">
        <h2 id="hubs" style="margin-top:0">Related hubs</h2>
        <ul>{hub_items}</ul>
      </div>

      <div class="card">
        <h2 id="pages" style="margin-top:0">Related pages</h2>
        <ul>{leaf_items}</ul>
      </div>
    </div>

  </div>

  <div class="footer">
    <strong>Next step:</strong> If this matches what you&rsquo;re working on,
    text PJ and we&rsquo;ll route you to the cleanest move.
    <br/><span class="note">Generated by Pillar Engine · Updated {u}</span>
  </div>
</div>
<div class="orb"><a href="sms:+17604541860">Text<br/>PJ</a></div>
</body>
</html>
"""


def build_index(built: list, updated_iso: str) -> str:
    esc   = htmllib.escape
    links = "\n".join(
        f'<li><a href="/{esc(p)}">{esc(title_case(os.path.basename(p).replace(".html", "")))}</a></li>'
        for p in built
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>SideGuy Pillars — Concept Index</title>
  <meta name="description" content="Wikipedia-style concept guides for operators. SideGuy Solutions — clarity before cost."/>
  <link rel="canonical" href="https://sideguysolutions.com/pillars/index.html"/>
  <style>
    body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;background:#07121a;color:#e9f2ff;line-height:1.6}}
    a{{color:#7ab6ff;text-decoration:none}} a:hover{{text-decoration:underline}}
    .wrap{{max-width:920px;margin:0 auto;padding:26px 16px 80px}}
    .card{{border:1px solid #123041;background:rgba(255,255,255,0.03);border-radius:14px;padding:20px}}
    .muted{{color:#a9c0d6;font-size:.9rem}} ul{{margin:12px 0 0 20px}} li{{margin-bottom:6px}}
    .top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;flex-wrap:wrap;gap:10px}}
    .badge{{font-family:ui-monospace,monospace;font-size:12px;color:#a9c0d6;border:1px solid #123041;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.03)}}
  </style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="badge">Pillars · Updated {esc(updated_iso)}</div>
    <div class="badge"><a href="/hub.html">Operator Hub</a> · <a href="/">Home</a></div>
  </div>
  <div class="card">
    <h1 style="margin:0 0 8px">SideGuy Pillar Concept Pages</h1>
    <p class="muted">Wikipedia-style guides built for authority, navigation, and knowledge-graph connection.</p>
    <ul>{links}</ul>
  </div>
</div>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit",      type=int, default=35)
    ap.add_argument("--industries", default="signals/industries.txt")
    ap.add_argument("--pj_topics",  default="signals/pj-topics.txt")
    args = ap.parse_args()

    base = [
        "ai-automation", "payments", "crypto-solana", "san-diego",
        "seo", "operations", "small-business-systems",
    ]
    hub_topics = pick_hub_topics(limit=50)
    industries = [slugify(x) for x in read_lines(args.industries)][:50]
    pj_topics  = [slugify(x) for x in read_lines(args.pj_topics)][:25]

    raw  = base + hub_topics + industries + pj_topics
    seen = set()
    topics = []
    for t in raw:
        if not t or t in seen:
            continue
        seen.add(t)
        topics.append(t)
    topics = topics[: max(5, args.limit)]

    updated = now_iso()
    built   = []
    os.makedirs("pillars", exist_ok=True)

    for t in topics:
        title = title_case(
            t.replace("san-diego",    "San Diego")
             .replace("crypto-solana","Crypto Solana")
             .replace("ai-automation","AI Automation")
        )
        hubs  = pick_hub_links(t, limit=24)
        pages = pick_leaf_links(t, limit=30)
        out   = build_page(title, t, hubs, pages, updated)

        # Use plain slug — no collision with existing {cat}-master-guide.html files
        dest = os.path.join("pillars", f"{t}.html")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(out)
        built.append(dest)

    idx_path = os.path.join("pillars", "index.html")
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(build_index(built, updated))

    print(f"[pillar-engine] {len(built)} concept pillars + pillars/index.html @ {updated}")
    for p in built[:12]:
        print(" -", p)
    if len(built) > 12:
        print(f" - ... (+{len(built) - 12} more)")


if __name__ == "__main__":
    main()
