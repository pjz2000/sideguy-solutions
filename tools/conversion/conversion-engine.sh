#!/bin/bash

echo "Running SideGuy Conversion Engine"

INPUT="docs/opportunity/top-opportunities.txt"
LOG="docs/conversion/conversion-log.txt"

mkdir -p docs/conversion

echo "Conversion Engine Run $(date)" > $LOG
echo "" >> $LOG

if [ ! -f "$INPUT" ]; then
  echo "No opportunity file found. Run opportunity engine first."
  exit 1
fi

python3 << 'PYEOF'
import re, os

INPUT = "docs/opportunity/top-opportunities.txt"
LOG   = "docs/conversion/conversion-log.txt"

BLOCK = '''<div class="conversion-block" style="position:relative;margin:40px auto;padding:24px;max-width:720px;border-radius:16px;background:linear-gradient(135deg,#0ea5e9,#22c55e);color:white;font-family:Inter,sans-serif;text-align:center;">
<h2 style="margin-bottom:12px;">Not sure what to do next?</h2>
<p style="margin-bottom:16px;">Skip the confusion. Get real guidance before you spend money.</p>
<a href="sms:17735441231" style="display:inline-block;padding:12px 20px;background:white;color:black;border-radius:999px;text-decoration:none;font-weight:600;">&#128172; Text PJ</a>
<p style="margin-top:12px;font-size:14px;opacity:0.9;">Clarity before cost.</p>
</div>'''

injected = 0
skipped  = 0

with open(INPUT) as f:
    lines = f.readlines()

with open(LOG, 'a') as log:
    for line in lines:
        parts = line.split('|')
        if len(parts) < 2:
            continue
        filepath = parts[1].strip()
        if not os.path.isfile(filepath):
            continue

        content = open(filepath, encoding='utf-8', errors='ignore').read()

        if 'conversion-block' in content:
            skipped += 1
            log.write(f"SKIP (already has block): {filepath}\n")
            continue

        if '</body>' not in content:
            skipped += 1
            log.write(f"SKIP (no </body> tag): {filepath}\n")
            continue

        new_content = content.replace('</body>', BLOCK + '\n</body>', 1)
        with open(filepath, 'w', encoding='utf-8') as out:
            out.write(new_content)

        injected += 1
        log.write(f"INJECTED: {filepath}\n")

print(f"  Injected: {injected}")
print(f"  Skipped:  {skipped}")
PYEOF

echo ""
echo "Conversion injection complete."
echo "Log saved to: $LOG"
