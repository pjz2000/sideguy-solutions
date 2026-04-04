#!/usr/bin/env bash
# SideGuy Pantera 2027 Domination Loop — macOS-safe

echo "[1/6] Finding heavy winners..."
find . -maxdepth 1 -name "*.html" | sort -R | head -15 > logs/domination/winners.txt
echo "  → $(wc -l < logs/domination/winners.txt | tr -d ' ') pages selected"

echo "[2/6] Tightening weak riffs + stage-light wow..."
python3 - <<'PY'
from pathlib import Path

with open("logs/domination/winners.txt") as f:
    pages = [p.strip().lstrip("./") for p in f if p.strip()]

pressure = """
<section class="operator-pressure-block" style="margin:28px 0;padding:22px;border-radius:14px;background:linear-gradient(135deg,rgba(8,145,178,.07),rgba(6,182,212,.04));border:1px solid rgba(8,145,178,.15);">
  <h2 style="font-size:.85rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:#0891b2;margin:0 0 8px;">Operator Intelligence Upgrade</h2>
  <p style="font-size:.80rem;color:#2e6a8a;margin:0;line-height:1.55;">This route is actively evolving from real search demand and live operator upgrades.</p>
</section>"""

stage = '<div class="stage-light-layer" aria-hidden="true" style="position:fixed;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(8,145,178,.35),transparent);pointer-events:none;z-index:100;"></div>'

upgraded = 0
for page in pages:
    p = Path(page)
    if not p.exists():
        continue
    html = p.read_text(encoding="utf-8", errors="ignore")
    changed = False
    if "operator-pressure-block" not in html and "</main>" in html:
        html = html.replace("</main>", pressure + "\n</main>", 1)
        changed = True
    if "stage-light-layer" not in html and "</body>" in html:
        html = html.replace("</body>", stage + "\n</body>", 1)
        changed = True
    if changed:
        p.write_text(html, encoding="utf-8")
        upgraded += 1

print(f"  → {upgraded} pages upgraded")
PY

echo "[3/6] Deepening local authority index..."
grep -RIl "San Diego\|Encinitas\|Solana Beach" . --include="*.html" 2>/dev/null | sort > logs/domination/local-authority-pages.txt
echo "  → $(wc -l < logs/domination/local-authority-pages.txt | tr -d ' ') local authority pages"

echo "[4/6] Building domination manifest..."
find docs tools -type f | sort > logs/domination/domination-manifest.txt
echo "  → $(wc -l < logs/domination/domination-manifest.txt | tr -d ' ') files indexed"

echo "[5/6] Writing pressure log..."
echo "$(date '+%Y-%m-%d %H:%M:%S') domination-loop run" >> logs/domination/pressure.log 2>/dev/null || true

echo "[6/6] DOMINATION LOOP COMPLETE"
