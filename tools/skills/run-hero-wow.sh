#!/bin/bash
# ============================================================
# SideGuy Skill Launcher: Hero WOW Upgrade
# Pre-flight safety checks + guided upgrade prompts.
# See docs/skills/hero-wow-upgrade.md for full doctrine.
# ============================================================

echo ""
echo "========================================"
echo "  HERO WOW UPGRADE — SKILL LAUNCHER"
echo "  $(date '+%Y-%m-%d %I:%M%p %Z')"
echo "========================================"
echo ""

# ── SAFETY CHECK 1: backdrop-filter collision scan ───────────
echo "--- Safety Check 1: backdrop-filter + overflow:hidden collision ---"
echo ""

python3 - <<'PYEOF'
import re
from pathlib import Path

html = Path("index.html").read_text()
lines = html.splitlines()

# Find elements with backdrop-filter
bf_lines = [(i+1, l) for i, l in enumerate(lines) if 'backdrop-filter' in l]
oh_lines = [(i+1, l) for i, l in enumerate(lines) if 'overflow:hidden' in l or 'overflow: hidden' in l]

print(f"backdrop-filter found on {len(bf_lines)} lines:")
for ln, l in bf_lines[:10]:
    print(f"  line {ln}: {l.strip()[:80]}")

print()
print(f"overflow:hidden found on {len(oh_lines)} lines:")
for ln, l in oh_lines[:10]:
    print(f"  line {ln}: {l.strip()[:80]}")

print()
if bf_lines and oh_lines:
    print("⚠️  Both exist in file. Verify they are NOT on the same element or parent/child relationship.")
    print("   See docs/skills/hero-wow-upgrade.md — THE CARDINAL RULE")
else:
    print("✅ No collision risk detected.")
PYEOF

echo ""

# ── SAFETY CHECK 2: sgHeroLeft background ────────────────────
echo "--- Safety Check 2: sgHeroLeft background (must be transparent) ---"
echo ""
python3 - <<'PYEOF'
from pathlib import Path
html = Path("index.html").read_text()

# Check for any non-transparent sgHeroLeft background
import re
# Look for sgHeroLeft style rules
matches = re.findall(r'\.sgHeroLeft\s*\{[^}]*\}', html, re.S)
for m in matches:
    if 'background' in m and 'transparent' not in m:
        print(f"⚠️  sgHeroLeft has non-transparent background:")
        print(f"   {m[:120]}")
    else:
        print(f"✅ sgHeroLeft background: safe")
        break
else:
    print("✅ No sgHeroLeft CSS block found with background issue.")
PYEOF

echo ""

# ── SAFETY CHECK 3: h1 gradient-background ───────────────────
echo "--- Safety Check 3: h1 gradient background-clip:text (must not exist in hero) ---"
echo ""
python3 - <<'PYEOF'
from pathlib import Path
html = Path("index.html").read_text()
import re

# Check for background-clip:text on h1
if 'background-clip' in html and 'h1' in html:
    lines = html.splitlines()
    for i, l in enumerate(lines):
        if 'background-clip' in l and 'text' in l:
            print(f"⚠️  line {i+1}: {l.strip()[:100]}")
    print("   Verify this is NOT applied to an h1 inside .sgHeroLeft")
else:
    print("✅ No background-clip:text detected.")
PYEOF

echo ""

# ── CURRENT HERO STATE SNAPSHOT ──────────────────────────────
echo "--- Current hero structure snapshot ---"
echo ""
python3 - <<'PYEOF'
from pathlib import Path
import re

html = Path("index.html").read_text()

# Find the hero section
m = re.search(r'(<!-- PREMIUM 2026 SPLIT HERO.*?</section>)', html, re.S)
if m:
    hero = m.group(1)
    # Print first 60 lines of hero
    lines = hero.splitlines()[:40]
    for l in lines:
        print(l[:120])
    if len(hero.splitlines()) > 40:
        print(f"  ... ({len(hero.splitlines())-40} more lines)")
else:
    print("Hero section not found. Search for 'sgHero' manually.")
PYEOF

echo ""

# ── STYLE BLOCK INVENTORY ────────────────────────────────────
echo "--- Existing style blocks (append-only — do not edit these) ---"
echo ""
grep -n 'style id=' index.html | head -20
echo ""

# ── CURRENT VERSION ──────────────────────────────────────────
echo "--- Current version ---"
grep -o '.*GSC layer v[0-9]*.*' index.html | grep "<time" | head -1 | sed 's/.*<time[^>]*>//;s/<.*//'
echo ""

echo "========================================"
echo "  HERO WOW UPGRADE — PRE-FLIGHT COMPLETE"
echo ""
echo "  All clear to proceed. Remember:"
echo "  1. Add CSS in a NEW <style id='sg-hero-pass-vN'> block"
echo "  2. Never edit existing style blocks"
echo "  3. No overflow:hidden + backdrop-filter on same element"
echo "  4. Bump version after changes"
echo "  See: docs/skills/hero-wow-upgrade.md"
echo "========================================"
echo ""
