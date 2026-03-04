#!/usr/bin/env python3
# ==============================================================
# SIDEGUY GAP TOPICS WIRING
# Injects gap topic links into:
#   1. knowledge/sideguy-knowledge-map.html  (new cluster section)
#   2. payments.html                         (gap topics card)
# Uses markers so it's idempotent (safe to re-run).
# ==============================================================

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
TSV  = ROOT / "reports" / "gap-topics-to-build.tsv"

PILLAR_FILE_MAP = {
    "payments":            ROOT / "payments.html",
    "ai-automation":       ROOT / "ai-automation-hub.html",
    "small-business-tech": ROOT / "operator-tools-hub.html",
}

# ── Read TSV ──────────────────────────────────────────────────

def read_tsv(path):
    rows = []
    with path.open() as f:
        headers = f.readline().strip().split("\t")
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split("\t")
            rows.append(dict(zip(headers, parts)))
    return rows

rows   = read_tsv(TSV)
by_pillar: dict = {}
for r in rows:
    by_pillar.setdefault(r["pillar"].strip(), []).append(
        (r["slug"].strip(), r["title"].strip())
    )

# ── 1. Knowledge Map ──────────────────────────────────────────

KM = ROOT / "knowledge" / "sideguy-knowledge-map.html"
START = "<!-- SIDEGUY_GAP_TOPICS_START -->"
END   = "<!-- SIDEGUY_GAP_TOPICS_END -->"

def km_node(slug, title, pillar):
    label = pillar.replace("-", " ").title()
    return (
        f'      <a class="node" href="/generated/{slug}.html">\n'
        f'        <span class="node-type type-guide">Gap</span>\n'
        f'        <div class="node-title">{title}</div>\n'
        f'        <div class="node-desc">{label} · Operator guide</div>\n'
        f'      </a>'
    )

nodes_html = "\n".join(km_node(r["slug"], r["title"], r["pillar"]) for r in rows)

section = f"""
  <!-- SIDEGUY_GAP_TOPICS_SECTION -->
  <div class="cluster-group">
    <div class="cluster-header">
      <div class="cluster-icon">🗂️</div>
      <div>
        <div class="cluster-title">Gap Topics — High-Priority Guides</div>
        <div class="cluster-sub">39 missing operator topics discovered by the Site Intelligence gap report — now built.</div>
      </div>
      <a class="cluster-cta" href="/knowledge-hub.html">Knowledge Hub →</a>
    </div>
    <div class="node-grid">
{START}
{nodes_html}
{END}
    </div>
  </div>
  <!-- END SIDEGUY_GAP_TOPICS_SECTION -->
"""

html = KM.read_text()

if START in html and END in html:
    html = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        f"{START}\n{nodes_html}\n{END}",
        html, flags=re.S
    )
    print(f"  KM: updated existing gap topics section ({len(rows)} nodes)")
elif "<!-- SIDEGUY_CONCEPTS_SECTION -->" in html:
    html = html.replace(
        "<!-- SIDEGUY_CONCEPTS_SECTION -->",
        section + "<!-- SIDEGUY_CONCEPTS_SECTION -->"
    )
    print(f"  KM: inserted gap topics section before concepts ({len(rows)} nodes)")
else:
    html = html.replace('<div class="microFooter"', section + '\n  <div class="microFooter"')
    print(f"  KM: inserted gap topics section near footer ({len(rows)} nodes)")

KM.write_text(html)

# ── 2. Pillar page injection ──────────────────────────────────

def inject_pillar(pillar_key: str, items: list):
    path = PILLAR_FILE_MAP.get(pillar_key)
    if not path or not path.exists():
        print(f"  SKIP pillar: {pillar_key} (file not found)")
        return

    p_start = f"<!-- GAP_{pillar_key.upper()}_START -->"
    p_end   = f"<!-- GAP_{pillar_key.upper()}_END -->"

    links = "\n".join(
        f'            <a class="pill" href="/generated/{slug}.html">{title}</a>'
        for slug, title in items
    )

    section_html = f"""
  <!-- GAP_SECTION_{pillar_key.upper()} -->
  <div style="margin:32px 0;padding:24px;background:rgba(255,255,255,.75);border:1px solid rgba(0,0,0,.08);border-radius:18px;">
    <div style="font-size:.72rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#3f6173;margin-bottom:12px;">📋 Gap Topic Guides — Just Added</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;">
{p_start}
{links}
{p_end}
    </div>
  </div>
  <!-- END GAP_SECTION_{pillar_key.upper()} -->
"""

    content = path.read_text()
    if p_start in content and p_end in content:
        content = re.sub(
            re.escape(p_start) + r".*?" + re.escape(p_end),
            f"{p_start}\n{links}\n{p_end}",
            content, flags=re.S
        )
        print(f"  Pillar updated: {path.name} ({len(items)} links)")
    else:
        anchor = "</main>" if "</main>" in content else "</body>"
        content = content.replace(anchor, section_html + "\n" + anchor, 1)
        print(f"  Pillar injected: {path.name} ({len(items)} links)")

    path.write_text(content)

for pillar_key, items in by_pillar.items():
    inject_pillar(pillar_key, items)

print(f"\n✅  Gap topics wired — {len(rows)} pages linked into knowledge map + pillar pages")
