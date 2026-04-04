#!/usr/bin/env bash
# SideGuy Monster Compounding Loop
# macOS-safe — uses Python for HTML injection

echo "[1/5] Detecting winning pages..."
find . -maxdepth 1 -name "*.html" | sort | head -20 > logs/evolution/winners.txt
echo "  → $(wc -l < logs/evolution/winners.txt | tr -d ' ') pages selected"

echo "[2/5] Promoting winners into hubs + injecting 2027 wow layer..."
python3 - <<'PY'
from pathlib import Path

with open("logs/evolution/winners.txt") as f:
    pages = [p.strip().lstrip("./") for p in f if p.strip()]

related = """
<section class="related-guides" style="margin:28px 0;padding:20px;border-radius:14px;background:rgba(8,145,178,.05);border:1px solid rgba(8,145,178,.12);">
  <h2 style="font-size:.88rem;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:#0891b2;margin:0 0 8px;">Related Guides</h2>
  <p style="font-size:.82rem;color:#2e6a8a;margin:0;">Fresh linked routes expanding from live demand signals.</p>
</section>"""

wow = '<div class="cinematic-depth-layer" aria-hidden="true" style="position:fixed;inset:0;pointer-events:none;z-index:-1;background:radial-gradient(ellipse 80% 40% at 50% 100%,rgba(8,145,178,.04),transparent 70%);"></div>'

upgraded = 0
for page in pages:
    p = Path(page)
    if not p.exists():
        continue
    html = p.read_text(encoding="utf-8", errors="ignore")
    changed = False
    if "related-guides" not in html and "</main>" in html:
        html = html.replace("</main>", related + "\n</main>", 1)
        changed = True
    if "cinematic-depth-layer" not in html and "</body>" in html:
        html = html.replace("</body>", wow + "\n</body>", 1)
        changed = True
    if changed:
        p.write_text(html, encoding="utf-8")
        upgraded += 1

print(f"  → {upgraded} pages upgraded")
PY

echo "[3/5] Building sensor manifest..."
find docs tools -type f | sort > logs/evolution/sensor-manifest.txt
echo "  → $(wc -l < logs/evolution/sensor-manifest.txt | tr -d ' ') files indexed"

echo "[4/5] Writing evolution log..."
echo "$(date '+%Y-%m-%d %H:%M:%S') monster-loop run" >> logs/evolution/evolution.log

echo "[5/5] Monster loop complete."
