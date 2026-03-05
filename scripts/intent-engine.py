#!/usr/bin/env python3
"""
SIDEGUY INTENT ENGINE (Final Boss)
------------------------------------
For each cluster, generate an "intent pack" — stub pages covering
the full intent surface area of the topic:
  explained / why / signs / fix / checklist / cost / tools / compare /
  mistakes / timeline / risk / faq / decision-tree / templates /
  troubleshooting / next-steps

1. Reads docs/auto-cluster/generated/page-index.tsv
2. Ranks clusters by leaf count
3. Generates docs/intent-engine/generated/INTENT_PACKS.md
4. Writes stub HTML pages in auto-intent-pages/{pillar}/{cluster}/
5. Produces CLAUDE_INTENT_PROMPT.md
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).parent.parent.resolve()
INDEX_TSV   = ROOT / "docs" / "auto-cluster" / "generated" / "page-index.tsv"
OUT_DOC_DIR = ROOT / "docs" / "intent-engine" / "generated"
OUT_PAGES   = ROOT / "auto-intent-pages"
INTENT_LIB  = ROOT / "docs" / "intent-engine" / "intent_library.tsv"

SITE_BASE       = os.environ.get("SITE_BASE", "https://sideguysolutions.com")
TEXT_PJ_NUMBER  = os.environ.get("TEXT_PJ_NUMBER", "773-544-1231")
TEXT_PJ_LABEL   = os.environ.get("TEXT_PJ_LABEL", "Text PJ")
CLUSTERS_MAX    = int(os.environ.get("CLUSTERS_MAX", "80"))
INTENTS_PER     = int(os.environ.get("INTENTS_PER_CLUSTER", "16"))
WRITE_PAGES     = os.environ.get("WRITE_PAGES", "1") == "1"
OVERWRITE       = os.environ.get("OVERWRITE", "0") == "1"

TIMESTAMP = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

OUT_DOC_DIR.mkdir(parents=True, exist_ok=True)
OUT_PAGES.mkdir(parents=True, exist_ok=True)
(ROOT / "docs" / "intent-engine").mkdir(parents=True, exist_ok=True)

print("🧠 SIDEGUY INTENT ENGINE (Final Boss)")
print(f"Timestamp: {TIMESTAMP}")
print()


# ─── Guard ────────────────────────────────────────────────────────────────────
if not INDEX_TSV.exists():
    print(f"⚠️  Missing {INDEX_TSV}")
    print("Run the Auto-Cluster Engine first.")
    sys.exit(1)


# ─── 1. Load page index ───────────────────────────────────────────────────────
print("📂 Loading page index...")
cluster_pages   = defaultdict(list)
cluster_title_m = {}

with open(INDEX_TSV, encoding="utf-8") as fh:
    header = None
    for line in fh:
        cols = line.rstrip("\n").split("\t")
        if header is None:
            header = cols
            continue
        if len(cols) < 5:
            continue
        pillar, cluster, ctitle = cols[1], cols[2], cols[3]
        key = (pillar, cluster)
        cluster_pages[key].append(cols)
        cluster_title_m[key] = ctitle

clusters_ranked = sorted(cluster_pages.items(), key=lambda x: -len(x[1]))
top_clusters    = clusters_ranked[:CLUSTERS_MAX]
print(f"   Total clusters: {len(clusters_ranked)}")
print(f"   Processing top: {len(top_clusters)}")


# ─── 2. Intent library ────────────────────────────────────────────────────────
DEFAULT_INTENTS = [
    ("explained",      "Explained",              "explained"),
    ("why",            "Why This Happens",        "why"),
    ("signs",          "Signs & Symptoms",        "signs"),
    ("fix",            "Step-by-Step Fix",        "fix"),
    ("checklist",      "Quick Checklist",         "checklist"),
    ("cost",           "Cost & Pricing",          "cost"),
    ("tools",          "Best Tools & Software",   "tools"),
    ("compare",        "Compare Options",         "compare"),
    ("mistakes",       "Common Mistakes",         "mistakes"),
    ("timeline",       "How Long It Takes",       "timeline"),
    ("risk",           "Safety & Risk",           "risk"),
    ("faq",            "FAQ",                     "faq"),
    ("decision_tree",  "Decision Tree",           "decision-tree"),
    ("templates",      "Templates & Examples",    "templates"),
    ("troubleshoot",   "Troubleshooting Guide",   "troubleshooting"),
    ("next_steps",     "What to Do Next",         "next-steps"),
]

# Write intent library if missing
if not INTENT_LIB.exists():
    with open(INTENT_LIB, "w", encoding="utf-8") as fh:
        fh.write("# intent_key\ttitle_suffix\tslug_suffix\n")
        for row in DEFAULT_INTENTS:
            fh.write("\t".join(row) + "\n")
    print(f"✅ Intent library seeded: docs/intent-engine/intent_library.tsv")

# Load intent library
intents = []
with open(INTENT_LIB, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            intents.append((parts[0], parts[1], parts[2]))

intents = intents[:INTENTS_PER]
print(f"   Intent types: {len(intents)}")


# ─── 3. Slug helper ───────────────────────────────────────────────────────────
def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


# ─── 4. Hub URL helpers ───────────────────────────────────────────────────────
PILLAR_CATEGORY_MAP = {
    "ai-automation":        "/auto-hubs/categories/ai-automation.html",
    "payments":             "/auto-hubs/categories/payments.html",
    "operator-tools":       "/auto-hubs/categories/operator-tools.html",
    "problem-intelligence": "/auto-hubs/categories/problem-intelligence.html",
}

def cluster_hub_url(pillar, cluster):
    return f"/auto-hubs/clusters/{pillar}--{cluster}.html"

def pillar_hub_url(pillar):
    return PILLAR_CATEGORY_MAP.get(pillar, f"/auto-hubs/categories/{pillar}.html")


# ─── 5. Stub HTML template ────────────────────────────────────────────────────
def make_stub(page_title, pillar, cluster, ctitle, canonical_url):
    ch  = cluster_hub_url(pillar, cluster)
    ph  = pillar_hub_url(pillar)
    cat = ph  # category = pillar category page
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>{page_title} | SideGuy</title>
  <meta name="description" content="Friendly, structured guidance: {page_title}. Clarity before cost — AI explains, a real human resolves. San Diego."/>
  <link rel="canonical" href="{SITE_BASE}{canonical_url}"/>
  <style>
    body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;max-width:860px;margin:0 auto;padding:24px 16px;line-height:1.6;color:#073044;background:#eefcff}}
    .bc{{font-size:.85rem;margin-bottom:18px;opacity:.7}}
    .bc a{{color:#073044}}
    h1{{margin-top:0;font-size:1.75rem}}
    .sub{{opacity:.65;font-size:.9rem;margin-top:-8px;margin-bottom:20px}}
    .card{{border:1px solid #d0eaf5;border-radius:14px;padding:18px 20px;margin-top:16px;background:#fff}}
    .card h2{{margin-top:0;font-size:1.1rem}}
    ul,ol{{margin:8px 0 0 20px;padding:0}}
    li{{margin-bottom:6px}}
    .cta{{margin-top:14px;padding:16px;border-radius:14px;background:#f4fff6;border:1px solid #d8f3df}}
    .cta strong{{font-size:1.05rem}}
    a{{color:#073044}}
  </style>
</head>
<body>
  <div class="bc">
    <a href="/">Home</a> /
    <a href="{ph}">{pillar.replace("-"," ").title()}</a> /
    <a href="{ch}">{ctitle}</a> /
    {page_title}
  </div>
  <h1>{page_title}</h1>
  <p class="sub">SideGuy Solutions · San Diego · {TIMESTAMP[:10]}</p>

  <div class="card">
    <h2>Quick answer</h2>
    <p>__WRITE_A_CALM_30_SECOND_EXPLANATION__</p>
  </div>

  <div class="card">
    <h2>Why this happens</h2>
    <ul>
      <li>__CAUSE_1__</li>
      <li>__CAUSE_2__</li>
      <li>__CAUSE_3__</li>
    </ul>
  </div>

  <div class="card">
    <h2>What people misunderstand</h2>
    <ul>
      <li>__MISUNDERSTANDING_1__</li>
      <li>__MISUNDERSTANDING_2__</li>
      <li>__MISUNDERSTANDING_3__</li>
    </ul>
  </div>

  <div class="card">
    <h2>Simple next steps</h2>
    <ol>
      <li>__STEP_1__</li>
      <li>__STEP_2__</li>
      <li>__STEP_3__</li>
      <li>__STEP_4__</li>
      <li>__STEP_5__</li>
    </ol>
  </div>

  <!-- SideGuy Authority Footer (auto) -->
  <section id="sideguy-authority-footer" class="card">
    <div style="font-weight:700;margin-bottom:8px">SideGuy Intelligence</div>
    <div style="opacity:.7;margin-bottom:12px;font-size:.9rem">Clarity before cost · AI explains · Human resolves</div>
    <ul>
      <li><a href="{ch}">← Back to {ctitle}</a></li>
      <li><a href="{ph}">← Back to {pillar.replace("-"," ").title()} hub</a></li>
      <li><a href="/auto-hubs/directory.html">SideGuy Directory</a></li>
      <li><a href="/">SideGuy Home</a></li>
    </ul>

    <div style="margin-top:14px;font-weight:700">Related pages in this cluster</div>
    <ul>
      <li><a href="__RELATED_LEAF_1__">__RELATED_TITLE_1__</a></li>
      <li><a href="__RELATED_LEAF_2__">__RELATED_TITLE_2__</a></li>
      <li><a href="__RELATED_LEAF_3__">__RELATED_TITLE_3__</a></li>
    </ul>

    <div style="margin-top:14px;font-weight:700">See also — related clusters</div>
    <ul>
      <li><a href="__SEE_ALSO_CLUSTER_1__">__SEE_ALSO_TITLE_1__</a></li>
      <li><a href="__SEE_ALSO_CLUSTER_2__">__SEE_ALSO_TITLE_2__</a></li>
      <li><a href="__SEE_ALSO_CLUSTER_3__">__SEE_ALSO_TITLE_3__</a></li>
      <li><a href="__SEE_ALSO_CLUSTER_4__">__SEE_ALSO_TITLE_4__</a></li>
    </ul>

    <div class="cta">
      <strong>{TEXT_PJ_LABEL}</strong>
      <div style="margin-top:6px">Still unsure? Text PJ: <strong><a href="sms:+17735441231">{TEXT_PJ_NUMBER}</a></strong></div>
    </div>
  </section>
</body>
</html>
"""


# ─── 6. Main loop: generate packs + stubs ─────────────────────────────────────
print("🧠 Building intent packs + stub pages...")

packs_lines   = [
    f"# SideGuy Intent Packs\nGenerated: {TIMESTAMP}\n",
    "For each cluster, intent pages cover the full topic surface area.\n",
]

pages_written = 0
pages_skipped = 0

for (pillar, cluster), leaves in top_clusters:
    ctitle     = cluster_title_m.get((pillar, cluster), f"{pillar} {cluster}")
    title_base = ctitle
    leaf_count = len(leaves)

    packs_lines.append(f"\n---\n## {title_base}")
    packs_lines.append(f"- Pillar: `{pillar}`  Cluster: `{cluster}`  Leaves: {leaf_count}\n")

    for intent_key, suffix, slug_suffix in intents:
        page_title    = f"{title_base} — {suffix}"
        title_slug    = slugify(title_base)
        page_slug     = f"{title_slug}-{slug_suffix}"
        canonical_url = f"/auto-intent-pages/{pillar}/{cluster}/{page_slug}.html"

        packs_lines.append(f"- [{intent_key}] {page_title} → `{page_slug}.html`")

        if WRITE_PAGES:
            out_dir  = OUT_PAGES / pillar / cluster
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{page_slug}.html"

            if out_file.exists() and not OVERWRITE:
                pages_skipped += 1
            else:
                out_file.write_text(
                    make_stub(page_title, pillar, cluster, ctitle, canonical_url),
                    encoding="utf-8"
                )
                pages_written += 1

    packs_lines.append("")

# Write INTENT_PACKS.md
packs_md = OUT_DOC_DIR / "INTENT_PACKS.md"
packs_md.write_text("\n".join(packs_lines), encoding="utf-8")
print(f"✅ INTENT_PACKS.md written")
if WRITE_PAGES:
    print(f"   Stub pages written : {pages_written}")
    print(f"   Stub pages skipped : {pages_skipped} (already exist)")


# ─── 7. Claude prompt ─────────────────────────────────────────────────────────
weak_clusters = [
    (p, c, cluster_title_m.get((p, c), c), len(v))
    for (p, c), v in top_clusters
    if len(v) < 10
]
strong_clusters = [
    (p, c, cluster_title_m.get((p, c), c), len(v))
    for (p, c), v in top_clusters
    if len(v) > 50
][:6]

claude_lines = [f"""# Claude Prompt — SideGuy Intent Engine (Final Boss)
Generated: {TIMESTAMP}

## Goal
Turn each cluster into a high-traffic intent surface area that ranks for many
related queries. Each cluster gets 16 intent pages covering every angle a
searcher might use.

## What was generated
- Intent packs doc : `docs/intent-engine/generated/INTENT_PACKS.md`
- Stub pages dir   : `auto-intent-pages/{{pillar}}/{{cluster}}/`
- Total stubs      : {pages_written} new files

## Page structure (non-negotiable)
Every intent page must follow SideGuy format:
1. Quick answer (30 seconds, calm)
2. Why this happens (3 bullets)
3. What people misunderstand (3 bullets)
4. Simple next steps (5 steps max)
5. {TEXT_PJ_LABEL} CTA — Text PJ: {TEXT_PJ_NUMBER}

## Internal links to inject (replace placeholders)
- `__RELATED_LEAF_1/2/3__` → 3 real sibling intent pages in same cluster
- `__SEE_ALSO_CLUSTER_1/2/3/4__` → 4 related cluster hub URLs from See-Also engine
- `__RELATED_TITLE_*__` / `__SEE_ALSO_TITLE_*__` → human-readable link text

## Priority order
Start with high-traffic clusters (most existing leaves = most authority):
"""]

for p, c, t, cnt in strong_clusters:
    claude_lines.append(f"- **{t}** (`{p}/{c}`) — {cnt} existing pages")

claude_lines.append("""
## Then strengthen weak clusters (need most authority injection):
""")
for p, c, t, cnt in weak_clusters:
    hub = cluster_hub_url(p, c)
    claude_lines.append(f"- **{t}** (`{p}/{c}`) — {cnt} pages — hub: `{hub}`")

claude_lines.append(f"""
## Execution plan
1. Fill the first 6 intent pages for each top cluster with human-quality content
2. Use those as the writing pattern
3. Batch-fill remaining intent pages consistently
4. Replace all `__PLACEHOLDER__` strings with real content + links
5. Set canonical to: `{SITE_BASE}/auto-intent-pages/{{pillar}}/{{cluster}}/{{slug}}.html`

## Files
- Stubs: `auto-intent-pages/`
- Packs: `docs/intent-engine/generated/INTENT_PACKS.md`
- Intent library: `docs/intent-engine/intent_library.tsv`
""")

claude_md = OUT_DOC_DIR / "CLAUDE_INTENT_PROMPT.md"
claude_md.write_text("\n".join(claude_lines), encoding="utf-8")
print(f"✅ CLAUDE_INTENT_PROMPT.md written")


# ─── 8. Summary ───────────────────────────────────────────────────────────────
total_stubs = sum(1 for _ in OUT_PAGES.rglob("*.html"))

print()
print("─" * 52)
print("🧠✅ INTENT ENGINE COMPLETE")
print(f"   Clusters processed : {len(top_clusters)}")
print(f"   Intent types       : {len(intents)}")
print(f"   Stub pages written : {pages_written}")
print(f"   Total in dir       : {total_stubs}")
print(f"   Intent packs       : docs/intent-engine/generated/INTENT_PACKS.md")
print(f"   Claude prompt      : docs/intent-engine/generated/CLAUDE_INTENT_PROMPT.md")
print(f"   Stub pages dir     : auto-intent-pages/")
print("─" * 52)
print()
print("NEXT: Internal Link Contextualizer — add 2–4 in-body")
print("      contextual links per page (not just footer links).")
