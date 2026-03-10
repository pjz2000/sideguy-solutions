#!/usr/bin/env bash
# SideGuy Semantic Density Booster
# Injects How It Works, Cost Considerations, and Related Guides sections
# Uses Python for single-pass performance at 34k+ pages

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)

echo "Running SideGuy Semantic Booster..."

python3 - "$ROOT" << 'PYEOF'
import sys, os, re

root = sys.argv[1]

HOW_IT_WORKS = """\
<section class="sideguy-how-it-works">
<h2>How It Works</h2>
<p>This guide explains the system, tools, and strategies businesses use to solve this problem.</p>
</section>"""

COST = """\
<section class="sideguy-cost">
<h2>Cost Considerations</h2>
<p>Understanding pricing and operational costs helps businesses make smarter decisions.</p>
</section>"""

RELATED = """\
<section class="sideguy-related">
<h2>Related SideGuy Guides</h2>
<ul>
<li><a href="/ai-automation-knowledge-hub.html">AI Automation Hub</a></li>
<li><a href="/payments-knowledge-hub.html">Payments Hub</a></li>
<li><a href="/future-infrastructure-knowledge-hub.html">Future Infrastructure</a></li>
</ul>
</section>"""

updated = skipped = 0

for fname in os.listdir(root):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(root, fname)
    try:
        with open(fpath, 'r', errors='replace') as f:
            html = f.read()

        if '</body>' not in html:
            continue

        inject = []
        if 'How It Works' not in html:
            inject.append(HOW_IT_WORKS)
        if 'Cost Considerations' not in html:
            inject.append(COST)
        if 'Related SideGuy Guides' not in html:
            inject.append(RELATED)

        if not inject:
            skipped += 1
            continue

        insertion = '\n'.join(inject) + '\n'
        html = html.replace('</body>', insertion + '</body>', 1)

        with open(fpath, 'w') as f:
            f.write(html)
        updated += 1

    except Exception as e:
        pass

print(f"[DONE] {updated} pages updated, {skipped} already complete")
PYEOF
