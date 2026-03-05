#!/usr/bin/env python3
"""
SideGuy Authority Injection
------------------------------
Injects deterministic cross-cluster "See Also" links FROM strong cluster hub
pages INTO them — pointing to the most thematically relevant weak-topic leaf
pages.

Scope: ONLY auto-hubs/clusters/*.html and hubs/*.html (hub files).
       Does NOT touch the 12k+ leaf pages.

Strong hub criteria: ai-cost, ai-tools, ai-overview, ai-scheduling, ai-city
Weak leaf criteria : payment, chargeback, stripe, contractor, processing,
                     merchant, troubleshooting

For each strong hub:
  1. Find weak leaf pages whose slug shares at least one keyword with the hub.
  2. Pick the top MAX_LINKS by keyword overlap (deterministic — sorted).
  3. Inject a "Related topics" block before </body> if not already present.

Outputs:
  docs/authority-reports/authority-injection-audit.md  — dry-run preview
  (then patches files in place if DRY_RUN=False)
"""

import glob, os, re
from pathlib import Path
from collections import defaultdict

ROOT    = Path(__file__).parent.parent.parent.resolve()
DRY_RUN = False          # set True to only write audit, no file changes
MAX_LINKS = 3
PHONE  = "773-544-1231"
SMS    = "sms:+17735441231"
SITE   = "https://sideguysolutions.com"

STRONG_KEYS = ["ai-cost", "ai-tools", "ai-overview", "ai-scheduling", "ai-city"]
WEAK_KEYS   = ["payment", "chargeback", "stripe", "contractor",
               "processing", "merchant", "troubleshooting"]

INJECT_MARKER = "<!-- sideguy-authority-links -->"

# ── Collect pages ─────────────────────────────────────────────────────────────
all_html = [
    Path(f) for f in glob.glob(str(ROOT / "**" / "*.html"), recursive=True)
    if "_quarantine" not in f and ".git" not in f
]

hub_files  = [p for p in all_html if "auto-hubs" in str(p) or str(p).startswith(str(ROOT / "hubs"))]
leaf_files = [p for p in all_html if p not in hub_files]

strong_hubs = [p for p in hub_files  if any(k in p.name.lower() for k in STRONG_KEYS)]
weak_leaves = [p for p in leaf_files if any(k in p.name.lower() for k in WEAK_KEYS)]

# ── Keyword overlap scorer ────────────────────────────────────────────────────
def slug_tokens(path: Path) -> set[str]:
    """Extract meaningful tokens from a filename slug."""
    name = path.stem.lower()
    tokens = set(re.split(r"[-_]", name)) - {"san", "diego", "html", "the", "a", "for", "and", "to", "of", "in"}
    return tokens

def relevance(hub: Path, leaf: Path) -> int:
    return len(slug_tokens(hub) & slug_tokens(leaf))

# ── For each strong hub, pick top-N most relevant weak leaves ─────────────────
injection_plan: dict[Path, list[Path]] = {}
for hub in sorted(strong_hubs):
    scored = sorted(weak_leaves, key=lambda l: (-relevance(hub, l), l.name))
    top = [l for l in scored if relevance(hub, l) > 0][:MAX_LINKS]
    if not top:
        top = sorted(weak_leaves, key=lambda l: l.name)[:MAX_LINKS]
    injection_plan[hub] = top

# ── Build HTML injection block ────────────────────────────────────────────────
def make_block(targets: list[Path]) -> str:
    items = ""
    for t in targets:
        href = "/" + t.relative_to(ROOT).as_posix()
        label = t.stem.replace("-", " ").title()
        items += f'  <li><a href="{href}" style="color:#073044;text-decoration:underline;">{label}</a></li>\n'
    return (
        f'\n{INJECT_MARKER}\n'
        f'<section style="margin-top:28px;padding:18px 20px;background:#fff;'
        f'border:1px solid rgba(7,48,68,.12);border-radius:12px;">\n'
        f'  <div style="font-size:.72rem;font-weight:700;letter-spacing:.08em;'
        f'text-transform:uppercase;color:#3f6173;margin-bottom:10px;">Related Topics</div>\n'
        f'  <ul style="margin:0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:6px 20px;">\n'
        f'{items}'
        f'  </ul>\n'
        f'</section>\n'
    )

# ── Write audit report ────────────────────────────────────────────────────────
audit_dir = ROOT / "docs" / "authority-reports"
audit_dir.mkdir(parents=True, exist_ok=True)
audit_path = audit_dir / "authority-injection-audit.md"

audit_lines = [
    "# SideGuy Authority Injection — Audit Report",
    "",
    f"Dry-run: {DRY_RUN}  |  Strong hubs: {len(strong_hubs)}  |  Weak leaves in scope: {len(weak_leaves)}",
    "",
    "---",
    "",
]
for hub, targets in sorted(injection_plan.items()):
    html = hub.read_text(encoding="utf-8", errors="replace")
    already = INJECT_MARKER in html
    audit_lines += [
        f"### {hub.relative_to(ROOT)}",
        f"- Already injected: {'yes (skip)' if already else 'no'}",
        "- Links to inject:",
    ]
    for t in targets:
        audit_lines.append(f"  - `/{t.relative_to(ROOT).as_posix()}`")
    audit_lines.append("")

audit_path.write_text("\n".join(audit_lines), encoding="utf-8")
print(f"✓ Audit written: {audit_path.relative_to(ROOT)}")

# ── Inject (if not DRY_RUN) ───────────────────────────────────────────────────
patched = 0
skipped = 0

for hub, targets in injection_plan.items():
    html = hub.read_text(encoding="utf-8", errors="replace")
    if INJECT_MARKER in html:
        skipped += 1
        continue
    block = make_block(targets)
    new_html = html.replace("</body>", block + "</body>", 1)
    if new_html == html:
        skipped += 1
        continue
    if not DRY_RUN:
        hub.write_text(new_html, encoding="utf-8")
    patched += 1

action = "Would patch" if DRY_RUN else "Patched"
print(f"Authority injection complete")
print(f"  Strong hubs  : {len(strong_hubs)}")
print(f"  Weak leaves  : {len(weak_leaves)}")
print(f"  {action}      : {patched}")
print(f"  Skipped      : {skipped}")
print(f"  Audit report : docs/authority-reports/authority-injection-audit.md")
