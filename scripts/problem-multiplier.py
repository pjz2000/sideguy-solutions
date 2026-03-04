#!/usr/bin/env python3
"""
SideGuy Problem Multiplier Engine
Builds a BIG batch of new "problem" pages from existing discovery CSVs,
with ocean CSS + schema + canonical + sms:+17735441231 CTA.
Idempotent: skips any slug that already exists anywhere on disk.
"""
import os, re, csv, json, glob, hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(".").resolve()

PHONE_SMS   = "sms:+17735441231"
PHONE_HUMAN = "773-544-1231"

OUT_DIR = ROOT / "problems" / "multiplied"
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

MULT_DIR = ROOT / "multiplier"
MULT_DIR.mkdir(parents=True, exist_ok=True)

LIMIT      = int(os.getenv("LIMIT",     "250"))
TOPICS     = int(os.getenv("TOPICS",    "35"))
INDUSTRIES = int(os.getenv("INDUSTRIES","16"))

# Prefer existing discovery outputs (in order)
CANDIDATE_SOURCES = [
  "radar/problem-radar-new.csv",
  "problem-ideas-new.csv",
  "radar/problem-radar.csv",
  "problem-ideas.csv",
  "longtail-keywords.csv",
  "multiplier/problem-seeds.csv",
]

def now_iso():
  return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def slugify(s: str) -> str:
  s = s.strip().lower()
  s = re.sub(r"['']", "", s)
  s = re.sub(r"[^a-z0-9]+", "-", s)
  s = re.sub(r"-{2,}", "-", s).strip("-")
  return s[:90] if len(s) > 90 else s

def file_exists_anywhere(slug: str) -> bool:
  patterns = [
    f"{slug}.html",
    f"problems/{slug}.html",
    f"problems/generated/{slug}.html",
    f"problems/multiplied/{slug}.html",
    f"generated/{slug}.html",
    f"auto/{slug}.html",
    f"longtail/{slug}.html",
    f"clusters/{slug}.html",
    f"concepts/{slug}.html",
    f"hubs/{slug}.html",
  ]
  for p in patterns:
    if (ROOT / p).exists():
      return True
  return False

def read_csv_rows(path: Path):
  rows = []
  try:
    with path.open("r", encoding="utf-8", newline="") as f:
      reader = csv.DictReader(f)
      for r in reader:
        rows.append({k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()})
  except Exception:
    try:
      with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for r in reader:
          if not r:
            continue
          rows.append({"query": r[0].strip()})
    except Exception:
      pass
  return rows

def pick_source():
  for rel in CANDIDATE_SOURCES:
    p = ROOT / rel
    if p.exists():
      return p
  return None

def extract_queries(rows):
  cols = ["query", "q", "keyword", "title", "problem", "slug", "text"]
  out = []
  for r in rows:
    val = None
    for c in cols:
      if c in r and r[c]:
        val = r[c]
        break
    if not val:
      for _, v in r.items():
        if isinstance(v, str) and v.strip():
          val = v.strip()
          break
    if not val:
      continue
    out.append(val.strip())
  return out

BASE_INDUSTRIES = [
  "restaurants", "contractors", "hvac", "plumbers", "electricians", "dentists",
  "law-firms", "realtors", "landscapers", "accountants", "insurance-agents",
  "chiropractors", "pest-control", "roofers", "tutors", "physical-therapy",
  "veterinarians", "medical-offices", "ecommerce", "saas"
]

# High-intent problem patterns (the multiplier)
PATTERNS = [
  "not working",
  "not showing up",
  "keeps failing",
  "setup step by step",
  "cost breakdown",
  "best option for {industry}",
  "how to fix for {industry}",
  "quick checklist for {industry}",
  "pricing explained",
  "refund policy explained",
  "chargebacks explained",
  "webhook not working",
  "payment declined",
  "payout pending",
  "dispute response template",
  "integration guide for {industry}",
]


def ocean_css():
  return """
  :root{
    --bg:#07131a;--card:#0b2230;--card2:#0a1b26;--text:#eaf6ff;--muted:#9dc3d8;
    --a:#7ae7ff;--b:#7cffc2;--line:rgba(255,255,255,.10);--shadow:rgba(0,0,0,.35);
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0;background:radial-gradient(1200px 800px at 20% 0%, rgba(122,231,255,.14), transparent 55%),
                               radial-gradient(900px 700px at 80% 10%, rgba(124,255,194,.10), transparent 55%),
                               linear-gradient(180deg,var(--bg),#041018 70%, #030b10);
            color:var(--text);font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Inter,Arial}
  a{color:var(--a);text-decoration:none}
  a:hover{text-decoration:underline}
  .wrap{max-width:1100px;margin:0 auto;padding:28px 18px 120px}
  .topbar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:16px}
  .brand{font-weight:800;letter-spacing:.4px}
  .pill{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);padding:8px 12px;border-radius:999px;background:rgba(255,255,255,.04)}
  .hero{padding:18px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.03));
        box-shadow:0 18px 40px var(--shadow);margin:14px 0 16px}
  .h1{font-size:30px;line-height:1.12;margin:0 0 8px}
  .sub{color:var(--muted);margin:0;line-height:1.55}
  .grid{display:grid;grid-template-columns:repeat(12,1fr);gap:14px;margin-top:14px}
  .card{grid-column:span 12;border:1px solid var(--line);border-radius:16px;padding:16px;background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.02))}
  @media(min-width:900px){.half{grid-column:span 6}}
  .k{font-weight:800;margin:0 0 8px}
  .muted{color:var(--muted)}
  .list{margin:10px 0 0;padding-left:18px}
  .list li{margin:6px 0;color:#d6f0ff}
  .steps{counter-reset:s}
  .steps li{counter-increment:s;list-style:none;margin:10px 0;padding:10px 12px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.03)}
  .steps li::before{content:counter(s);display:inline-grid;place-items:center;width:26px;height:26px;border-radius:999px;
                    background:linear-gradient(90deg,rgba(122,231,255,.35),rgba(124,255,194,.25));
                    margin-right:10px;font-weight:900}
  .toc{display:flex;flex-wrap:wrap;gap:10px;margin-top:10px}
  .toc a{border:1px solid var(--line);padding:8px 10px;border-radius:12px;background:rgba(255,255,255,.03)}
  .footer{margin-top:18px;color:var(--muted);font-size:13px}
  .floatBtn{
    position:fixed;right:18px;bottom:18px;z-index:9999;
    display:flex;align-items:center;gap:10px;
    padding:14px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.18);
    background:linear-gradient(90deg,rgba(122,231,255,.22),rgba(124,255,194,.18));
    box-shadow:0 16px 50px rgba(0,0,0,.45);
    color:var(--text);font-weight:900;letter-spacing:.2px
  }
  .dot{width:10px;height:10px;border-radius:999px;background:rgba(124,255,194,.9);box-shadow:0 0 18px rgba(124,255,194,.65)}
  .floatBtn:hover{transform:translateY(-2px)}
  """


def build_page(title: str, slug: str, topic: str, industry: str | None):
  canonical = f"https://sideguysolutions.com/problems/multiplied/{slug}.html"
  desc = f"Operator-grade quick fix guide: {title}. Steps, checks, causes, and the human layer. Text PJ for help."
  updated = now_iso()

  # Topic-aware "Best Next Pages"
  hub_candidates = [
    ("AI Automation Hub",       "/ai-automation-hub.html"),
    ("Payments Hub",            "/payments-infrastructure-hub.html"),
    ("Prediction Markets Hub",  "/prediction-markets-hub.html"),
    ("Operator Tools Hub",      "/operator-tools-hub.html"),
    ("Knowledge Hub",           "/knowledge-hub.html"),
    ("Decisions",               "/decisions/index.html"),
    ("Problems Index",          "/problems/index.html"),
  ]
  hub_links = []
  for label, href in hub_candidates:
    if (ROOT / href.lstrip("/")).exists():
      hub_links.append((label, href))

  # Simple FAQ
  faq = [
    (f"Why is \"{topic}\" failing?",
     "Usually it's one of: permissions, a missing configuration step, a stale token, or a hidden dependency. Use the checklist below to isolate the exact failure."),
    ("What's the fastest way to confirm the root cause?",
     "Reproduce once, capture the exact error text, then test the smallest single change (one variable at a time). This prevents chasing ghosts."),
    ("Can I fix this without switching tools?",
     "Often yes. Most \"not working\" cases are configuration + routing, not the vendor. If the same failure repeats after clean setup, then evaluate switching."),
    ("When should I text PJ?",
     "When you want a human to confirm the fastest fix path, sanity-check your setup, or help you decide whether to stay or switch—before you waste hours."),
  ]

  # JSON-LD: BreadcrumbList + FAQPage
  breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "SideGuy Solutions",   "item": "https://sideguysolutions.com/"},
      {"@type": "ListItem", "position": 2, "name": "Problems",            "item": "https://sideguysolutions.com/problems/index.html"},
      {"@type": "ListItem", "position": 3, "name": "Multiplied",          "item": "https://sideguysolutions.com/problems/multiplied/"},
      {"@type": "ListItem", "position": 4, "name": title,                 "item": canonical},
    ]
  }
  faq_ld = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {"@type": "Question", "name": q,
       "acceptedAnswer": {"@type": "Answer", "text": a}}
      for q, a in faq
    ]
  }

  industry_line = f"<strong>Industry lens:</strong> {industry.replace('-', ' ')}" if industry else "<strong>Industry lens:</strong> operator-general"

  checks = [
    "Confirm the exact error text (copy/paste it into notes).",
    "Verify credentials / permissions / API keys (the #1 silent failure).",
    "Check one-step-at-a-time config: endpoint → auth → payload → response.",
    "Test with a minimal example (remove extras until it works).",
    "If webhooks: verify URL, method, signature/secret, and retries.",
    "If payments: confirm test/live mode, payout status, and risk flags.",
    "If it repeats after clean setup: consider switching (decision page linked below).",
  ]
  if industry:
    checks.insert(2, f"Validate your {industry.replace('-', ' ')} workflow assumptions (who triggers what, when).")

  steps = [
    "Reproduce once and capture the exact message / status code.",
    "Identify the layer: browser/app → server → vendor → downstream system.",
    "Run the smallest controlled test (one variable changed).",
    "Fix the failing layer, then re-run the full flow.",
    "Add a guardrail so it can't silently break again (alerts/logging/checklist).",
  ]

  decision_links = []
  decision_map = [
    ("Stripe vs Square",     "/decisions/stripe-vs-square.html"),
    ("Kalshi vs Polymarket", "/decisions/kalshi-vs-polymarket.html"),
    ("Zapier vs Make",       "/decisions/zapier-vs-make-automation.html"),
    ("Claude vs OpenAI GPT", "/decisions/claude-vs-openai-gpt.html"),
  ]
  for label, href in decision_map:
    if (ROOT / href.lstrip("/")).exists():
      decision_links.append((label, href))

  toc = [
    ("Quick checks",    "#quick-checks"),
    ("Step-by-step fix","#steps"),
    ("Common causes",   "#causes"),
    ("FAQ",             "#faq"),
  ]

  causes = [
    "Missing permission/scope or wrong account (test vs live).",
    "Bad endpoint URL, wrong method, or blocked network/DNS.",
    "Payload mismatch (field name, type, encoding, signature).",
    "Rate limits/timeouts or vendor retry behavior.",
    "Downstream dependency changed (webhook receiver, CRM mapping, workflow step).",
  ]
  if "payment" in topic.lower() or "stripe" in topic.lower():
    causes.insert(0, "Risk controls triggered (verification, disputes, payout holds).")

  html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{title} | SideGuy Problem Guide</title>
  <meta name="description" content="{desc}"/>
  <link rel="canonical" href="{canonical}"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:type" content="article"/>
  <meta property="og:url" content="{canonical}"/>
  <style>{ocean_css()}</style>
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
  <a class="floatBtn" href="{PHONE_SMS}">
    <span class="dot"></span> Text PJ <span class="muted">({PHONE_HUMAN})</span>
  </a>

  <div class="wrap">
    <div class="topbar">
      <div class="brand"><a href="/">SideGuy Solutions</a></div>
      <div class="pill">
        <span class="muted">Updated:</span> <strong>{updated}</strong>
      </div>
    </div>

    <div class="hero">
      <h1 class="h1">{title}</h1>
      <p class="sub">
        {industry_line}<br/>
        Built for speed: isolate the failing layer, fix the root cause, then add a guardrail so it can&#39;t silently break again.
      </p>
      <div class="toc">
        {"".join([f'<a href="{href}">{label}</a>' for label, href in toc])}
      </div>
    </div>

    <div class="grid">
      <section class="card half" id="quick-checks">
        <h2 class="k">Quick checks (60 seconds)</h2>
        <ul class="list">
          {"".join([f"<li>{c}</li>" for c in checks])}
        </ul>
      </section>

      <section class="card half" id="steps">
        <h2 class="k">Step-by-step fix (operator mode)</h2>
        <ol class="steps">
          {"".join([f"<li>{s}</li>" for s in steps])}
        </ol>
      </section>

      <section class="card" id="causes">
        <h2 class="k">Common causes</h2>
        <p class="muted">Fix the <em>first</em> failing layer, not the last visible symptom.</p>
        <ul class="list">
          {"".join([f"<li>{c}</li>" for c in causes])}
        </ul>
        <div class="footer">
          <strong>Topic:</strong> {topic} &nbsp;&middot;&nbsp; <strong>Slug:</strong> {slug}
        </div>
      </section>

      <section class="card half" id="faq">
        <h2 class="k">FAQ</h2>
        {"".join([f'<p><strong>{q}</strong><br/><span class="muted">{a}</span></p>' for q, a in faq])}
      </section>

      <section class="card half">
        <h2 class="k">Best next pages</h2>
        <p class="muted">Jump to the right hub or decision guide.</p>
        <div class="toc">
          {"".join([f'<a href="{href}">{label}</a>' for label, href in (hub_links + decision_links)]) if (hub_links or decision_links) else '<span class="muted">No hubs detected on disk yet.</span>'}
        </div>
      </section>
    </div>

    <div class="footer">
      <a href="/problems/index.html">← Back to Problems</a> &nbsp;&middot;&nbsp;
      <a href="/knowledge-hub.html">Knowledge Hub</a> &nbsp;&middot;&nbsp;
      <span class="muted">Clarity before cost.</span>
    </div>
  </div>
</body>
</html>
"""
  return html


def main():
  source = pick_source()
  if not source:
    seed_path = ROOT / "multiplier" / "problem-seeds.csv"
    if not seed_path.exists():
      seed_path.write_text("query\nstripe webhook not working\npayment declined\nai agents not working\nzapier not triggering\n", encoding="utf-8")
    source = seed_path

  rows = read_csv_rows(source)
  queries = extract_queries(rows)

  # Normalize to topics (first 2-5 words)
  topics = []
  for q in queries:
    q2 = re.sub(r"\s+", " ", q.replace("-", " ")).strip()
    toks = q2.split(" ")
    base = " ".join(toks[:5]).strip()
    if base:
      topics.append(base)

  # Deduplicate while preserving order
  seen  = set()
  topics2 = []
  for t in topics:
    key = t.lower()
    if key in seen:
      continue
    seen.add(key)
    topics2.append(t)

  topics2   = topics2[:TOPICS]
  industries = BASE_INDUSTRIES[:max(3, min(INDUSTRIES, len(BASE_INDUSTRIES)))]

  # Build candidate titles/slugs
  candidates = []
  for t in topics2:
    for pat in PATTERNS:
      if "{industry}" in pat:
        for ind in industries:
          title = f"{t} {pat.format(industry=ind.replace('-', ' '))}".strip()
          candidates.append((title, t, ind))
      else:
        title = f"{t} {pat}".strip()
        candidates.append((title, t, None))

  # Score candidates (shorter + high-intent words)
  def score(title: str) -> float:
    tl = title.lower()
    s  = 0.0
    for w in ["not working","payment declined","webhook","chargeback","setup",
              "step by step","best option","how to fix","pricing"]:
      if w in tl:
        s += 3.0
    s += max(0.0, 8.0 - (len(title) / 18.0))
    return s

  candidates.sort(key=lambda x: score(x[0]), reverse=True)

  built   = 0
  written = []
  for title, topic, industry in candidates:
    slug = slugify(title)
    if not slug or len(slug) < 6:
      continue
    if file_exists_anywhere(slug):
      continue
    out_path = OUT_DIR / f"{slug}.html"
    out_path.write_text(build_page(title=title, slug=slug, topic=topic, industry=industry), encoding="utf-8")
    written.append((title, slug, topic, industry or "operator-general"))
    built += 1
    if built >= LIMIT:
      break

  # Write manifest CSV
  manifest_csv = MULT_DIR / "problem-multiplier-built.csv"
  with manifest_csv.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["title", "slug", "topic", "industry", "path"])
    for title, slug, topic, industry in written:
      w.writerow([title, slug, topic, industry, f"problems/multiplied/{slug}.html"])

  # Write JSON report
  report = {
    "ran_at":         now_iso(),
    "source":         str(source),
    "limit":          LIMIT,
    "topics_used":    topics2,
    "industries_used": industries,
    "built_count":    built,
    "out_dir":        str(OUT_DIR),
    "manifest_csv":   str(manifest_csv),
  }
  (REPORT_DIR / "problem-multiplier-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

  print("\n== SideGuy Problem Multiplier ==")
  print(f"Source:   {source}")
  print(f"Built:    {built} new pages -> {OUT_DIR}")
  print(f"Manifest: {manifest_csv}")
  print("Sample slugs:")
  for _, slug, _, _ in written[:10]:
    print(" -", slug)


if __name__ == "__main__":
  main()
