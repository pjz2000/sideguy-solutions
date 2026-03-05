#!/usr/bin/env python3
"""
SideGuy Self-Improving SEO Engine
------------------------------------
Reads GSC Pages export, identifies winner pages (high impressions), then:
  1. Injects a "Related guides" contextual link block into non-winner pages
     pointing TO the winners (concentrates internal authority).
  2. Writes an expansion queue TSV with intent angles for each winner.
  3. Writes a full report to docs/self-improving-seo/report.md.

Re-run safely: pages already injected are skipped (MARKER guard).

GSC CSV location: docs/gsc/gsc_pages.csv
  Export from: Search Console → Performance → Pages → Export CSV
  Expected columns (case-insensitive): Page | Impressions | Clicks
"""

import csv, glob, os, re, random, datetime
from pathlib import Path

ROOT    = Path(__file__).parent.parent.parent.resolve()

# ── Config ────────────────────────────────────────────────────────────────────
GSC_CSV          = ROOT / "docs" / "gsc" / "gsc_pages.csv"
OUT_DIR          = ROOT / "docs" / "self-improving-seo"
REPORT_MD        = OUT_DIR / "report.md"
WINNERS_TXT      = OUT_DIR / "winners.txt"
EXPANSION_TSV    = OUT_DIR / "expansion-queue.tsv"

PHONE            = "773-544-1231"
MIN_IMPRESSIONS  = 5       # minimum impressions to qualify as winner
TOP_WINNERS      = 80      # cap on winner list
INJECT_PAGES_MAX = 350     # max pages modified per run
CONTEXT_LINKS    = 3       # links injected per page
SEED             = 402     # deterministic random (stable diffs across runs)

SKIP_DIRS = {".git", "node_modules", "_quarantine_backups", "dist", "build", "out", "vendor"}
HTML_GLOB = str(ROOT / "**" / "*.html")
MARKER    = "<!-- SideGuy Context Links (Auto) -->"

INTENTS = ["explained", "cost", "tools", "compare", "checklist",
           "mistakes", "troubleshooting", "next-steps"]
# ─────────────────────────────────────────────────────────────────────────────

def now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def skip_path(p: str) -> bool:
    pnorm = p.replace(os.sep, "/")
    return any(f"/{d}/" in f"/{pnorm}/" for d in SKIP_DIRS)

def normalize_page(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"^https?://[^/]+", "", raw)
    raw = raw.lstrip("/")
    if raw.endswith("/"):
        raw += "index.html"
    return raw

def clean_int(s) -> int:
    return int(str(s).replace(",", "").strip() or "0")

def anchor_title(path: str) -> str:
    base = os.path.basename(path).replace(".html", "")
    base = base.replace("-", " ").replace("_", " ").strip()
    return (base[:1].upper() + base[1:]) if base else "Related guide"

# ── Collect HTML files ────────────────────────────────────────────────────────
def list_html_files() -> list[str]:
    return [
        p.replace(os.sep, "/")
        for p in glob.glob(HTML_GLOB, recursive=True)
        if not skip_path(p) and p.lower().endswith(".html")
    ]

# ── Read GSC CSV ──────────────────────────────────────────────────────────────
def read_gsc(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            page = (r.get("Page") or r.get("page") or r.get("URL") or
                    r.get("Url") or r.get("Landing Page") or r.get("Landing page") or "").strip()
            if not page:
                continue
            imp = clean_int(r.get("Impressions") or r.get("impressions") or "0")
            clk = clean_int(r.get("Clicks") or r.get("clicks") or "0")
            rows.append({"page": normalize_page(page), "impressions": imp, "clicks": clk})
    return rows

# ── Pick winners ──────────────────────────────────────────────────────────────
def pick_winners(gsc_rows: list[dict], html_set: set[str]) -> list[dict]:
    winners = [
        r for r in gsc_rows
        if r["impressions"] >= MIN_IMPRESSIONS and r["page"] in html_set
    ]
    winners.sort(key=lambda x: (x["impressions"], x["clicks"]), reverse=True)
    return winners[:TOP_WINNERS]

# ── Inject contextual links ───────────────────────────────────────────────────
def inject_links(winners: list[dict], html_files: list[str]) -> dict:
    random.seed(SEED)
    winner_paths = {w["page"] for w in winners}
    winner_list  = [w["page"] for w in winners]

    # Only inject into non-winner pages
    targets = [p for p in html_files if p not in winner_paths]
    random.shuffle(targets)
    targets = targets[:INJECT_PAGES_MAX]

    modified = skipped_marker = skipped_body = 0

    for page in targets:
        try:
            html = Path(page).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        if MARKER in html:
            skipped_marker += 1
            continue

        idx = html.lower().rfind("</body>")
        if idx == -1:
            skipped_body += 1
            continue

        picks = random.sample(winner_list, min(CONTEXT_LINKS, len(winner_list)))

        li_items = "".join(
            f'\n<li><a href="/{t}">{anchor_title(t)}</a></li>'
            for t in picks
        )

        block = (
            f"\n{MARKER}\n"
            f'<section class="sideguy-context-links" style="margin:28px 0;padding:16px 14px;'
            f'border:1px solid rgba(255,255,255,.14);border-radius:14px;background:rgba(0,0,0,.18)">\n'
            f'<div style="font-weight:700;margin-bottom:8px">Related guides:</div>\n'
            f'<ul style="margin:0;padding-left:18px;line-height:1.6">{li_items}\n</ul>\n'
            f'<div style="margin-top:10px;opacity:.9">Need help fast? '
            f'<strong>Text PJ</strong>: '
            f'<a href="sms:+1{PHONE.replace("-", "")}">{PHONE}</a></div>\n'
            f'</section>\n'
        )

        new_html = html[:idx] + block + html[idx:]
        try:
            Path(page).write_text(new_html, encoding="utf-8")
            modified += 1
        except OSError:
            continue

    return {"modified": modified, "skipped_marker": skipped_marker, "skipped_body": skipped_body}

# ── Expansion queue ───────────────────────────────────────────────────────────
def build_expansion_queue(winners: list[dict]) -> int:
    rows = []
    ts = now_utc()
    for w in winners:
        slug = w["page"].replace(".html", "")
        base = os.path.basename(w["page"]).replace(".html", "").replace("-", " ").strip()
        for intent in INTENTS:
            rows.append({
                "timestamp": ts,
                "source": "gsc-winner",
                "winner_page": w["page"],
                "impressions": w["impressions"],
                "clicks": w["clicks"],
                "intent": intent,
                "topic": f"{base} {intent}",
                "slug_hint": slug + "-" + intent,
            })
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(EXPANSION_TSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["timestamp","source","winner_page","impressions","clicks","intent","topic","slug_hint"])
        for r in rows:
            w.writerow([r[k] for k in ["timestamp","source","winner_page","impressions","clicks","intent","topic","slug_hint"]])
    return len(rows)

# ── Report ────────────────────────────────────────────────────────────────────
def write_report(winners, inject_stats, expansion_count, total_html):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(WINNERS_TXT, "w", encoding="utf-8") as f:
        for w in winners:
            f.write(f"{w['impressions']}\t{w['clicks']}\t{w['page']}\n")

    gsc_status = "FOUND" if GSC_CSV.exists() else "MISSING — export from GSC → Performance → Pages → Export CSV"
    lines = [
        "# SideGuy Self-Improving SEO Report",
        "",
        f"- Run: **{now_utc()}**",
        f"- Phone: **{PHONE}**",
        "",
        "## Inputs",
        f"- GSC CSV: `{GSC_CSV.relative_to(ROOT)}` ({gsc_status})",
        f"- MIN_IMPRESSIONS: `{MIN_IMPRESSIONS}`",
        "",
        "## Inventory",
        f"- HTML files scanned: **{total_html:,}**",
        "",
        "## Winners",
        f"- Winners detected: **{len(winners)}** (cap {TOP_WINNERS})",
        "",
    ]
    if winners:
        lines += [
            "| Impr | Clicks | Page |",
            "|---:|---:|---|",
        ]
        for w in winners[:20]:
            lines.append(f"| {w['impressions']} | {w['clicks']} | `{w['page']}` |")
        if len(winners) > 20:
            lines.append(f"| … | … | ({len(winners) - 20} more in `{WINNERS_TXT.relative_to(ROOT)}`) |")
    else:
        lines.append("> No GSC winners yet. Export docs/gsc/gsc_pages.csv and re-run.")
    lines += [
        "",
        "## Auto Internal Link Boost",
        f"- Pages modified: **{inject_stats['modified']}** (cap {INJECT_PAGES_MAX})",
        f"- Skipped (already injected): **{inject_stats['skipped_marker']}**",
        f"- Skipped (no </body>): **{inject_stats['skipped_body']}**",
        "",
        "## Expansion Queue",
        f"- Queue rows: **{expansion_count}**",
        f"- File: `{EXPANSION_TSV.relative_to(ROOT)}`",
        "",
        "## Next steps",
        "1. Export GSC **Pages** CSV → `docs/gsc/gsc_pages.csv` (if not done).",
        "2. Re-run after fresh GSC data.",
        "3. Feed `expansion-queue.tsv` into auto-page builder for intent pages.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    html_files = list_html_files()
    html_set   = set(html_files)
    gsc_rows   = read_gsc(GSC_CSV)
    winners    = pick_winners(gsc_rows, html_set)

    inject_stats    = inject_links(winners, html_files) if winners else {"modified": 0, "skipped_marker": 0, "skipped_body": 0}
    expansion_count = build_expansion_queue(winners) if winners else 0
    write_report(winners, inject_stats, expansion_count, len(html_files))

    print(f"Self-Improving SEO Engine complete")
    print(f"  HTML scanned     : {len(html_files):,}")
    print(f"  GSC winners      : {len(winners)}")
    print(f"  Pages modified   : {inject_stats['modified']}")
    print(f"  Expansion rows   : {expansion_count}")
    print(f"  Report           : {REPORT_MD.relative_to(ROOT)}")
    if not GSC_CSV.exists():
        print(f"\n  ⚠  GSC CSV missing. Export to: {GSC_CSV.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
