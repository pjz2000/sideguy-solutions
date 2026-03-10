#!/usr/bin/env python3
"""
SideGuy Navigation Injector
Appends a hub-nav before </body> on pages missing command-center links.
Idempotent — safe to re-run.

Usage:
  python3 tools/upgrades/inject-nav-links.py          # dry run (report only)
  python3 tools/upgrades/inject-nav-links.py --run     # apply changes
"""

import os
import sys
import glob

DRY_RUN = '--run' not in sys.argv

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NAV_SNIPPET = '''\n<nav aria-label="SideGuy navigation" style="max-width:900px;margin:0 auto;padding:10px 24px 24px;display:flex;flex-wrap:wrap;gap:12px;font-size:.8rem;color:#3f6173">
  <a href="command-center-v2.html" style="color:#3f6173;text-decoration:none">Command Center</a>
  <a href="payments-knowledge-hub.html" style="color:#3f6173;text-decoration:none">Payments Hub</a>
  <a href="ai-automation-knowledge-hub.html" style="color:#3f6173;text-decoration:none">AI Automation Hub</a>
  <a href="software-development-knowledge-hub.html" style="color:#3f6173;text-decoration:none">Software Hub</a>
  <a href="future-infrastructure-knowledge-hub.html" style="color:#3f6173;text-decoration:none">Future Infrastructure Hub</a>
</nav>'''

pages = glob.glob(os.path.join(ROOT, '*.html'))

updated = 0
skipped_has_link = 0
skipped_no_body = 0
errors = 0

for path in sorted(pages):
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Skip if already has a command-center link
        if 'command-center' in content:
            skipped_has_link += 1
            continue

        # Skip if no </body> to inject before
        if '</body>' not in content.lower():
            skipped_no_body += 1
            continue

        # Inject before the first </body>
        idx = content.lower().index('</body>')
        new_content = content[:idx] + NAV_SNIPPET + '\n' + content[idx:]

        if DRY_RUN:
            print(f'  would update: {os.path.basename(path)}')
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

        updated += 1

    except Exception as e:
        print(f'  error: {path} — {e}')
        errors += 1

mode = 'DRY RUN' if DRY_RUN else 'APPLIED'
print(f'\n[{mode}] {updated} pages would be updated' if DRY_RUN else f'\n[{mode}] {updated} pages updated')
print(f'  {skipped_has_link} already had command-center links (skipped)')
print(f'  {skipped_no_body} had no </body> tag (skipped)')
if errors:
    print(f'  {errors} errors')

if DRY_RUN:
    print(f'\nTo apply: python3 tools/upgrades/inject-nav-links.py --run')
