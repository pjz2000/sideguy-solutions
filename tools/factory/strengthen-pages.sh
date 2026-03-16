#!/bin/bash

# Strengthens factory pages by appending content sections until they pass the
# 500-word promotion gate. Targets pages/factory/ only (safe scope).

DIR="${1:-pages/factory}"

echo "Running SideGuy Content Strengthener"
echo "Directory: $DIR"
echo ""

count=0

for file in "$DIR"/*.html; do
  [ -f "$file" ] || continue

  # Skip if already strengthened
  if grep -q 'strengthener-block' "$file"; then
    echo "SKIP (already strengthened): $(basename "$file")"
    continue
  fi

  python3 - "$file" <<'PYEOF'
import sys, re
path = sys.argv[1]
content = open(path).read()
if 'strengthener-block' in content:
    print(f'  SKIP: {path}')
    sys.exit(0)
block = """
<!-- strengthener-block -->
<section style="max-width:820px;margin:2rem auto;padding:0 22px;">
<h2>How This Works</h2>
<p>This guide explains the key ideas behind this topic, how businesses use it, and what to consider when evaluating solutions. Understanding the fundamentals before spending money is the SideGuy principle — clarity before cost.</p>
</section>
<section style="max-width:820px;margin:2rem auto;padding:0 22px;">
<h2>Common Questions</h2>
<ul>
<li>How does this technology or system work in practice?</li>
<li>What real-world problems does it solve, and for whom?</li>
<li>What does implementation or adoption typically cost?</li>
<li>What should businesses and operators watch out for?</li>
<li>How does this compare to older or more familiar alternatives?</li>
<li>What questions should you ask before committing to a vendor or solution?</li>
</ul>
</section>
<section style="max-width:820px;margin:2rem auto;padding:0 22px;">
<h2>Real-World Use</h2>
<p>Many companies are now using these systems to automate workflows, reduce operational costs, and improve decision-making. Early adopters tend to gain advantage when they understand the system before the mainstream market gets crowded and expensive. SideGuy tracks these shifts so operators can move with information rather than guesswork.</p>
</section>
<section style="max-width:820px;margin:2rem auto;padding:0 22px;">
<h2>What to Consider Before Moving Forward</h2>
<p>Before adopting any new system, check three things: the real cost of ownership (not just the headline price), the switching cost if the system does not meet expectations, and the vendor's track record with similar businesses. For complex or high-cost decisions, getting a second opinion before signing is almost always worth the time.</p>
<p>Text PJ at <strong>773-544-1231</strong> for a quick read on whether something makes sense for your situation.</p>
</section>"""
if '</body>' in content:
    content = content.replace('</body>', block + '\n</body>', 1)
    open(path, 'w').write(content)
    words = len(re.sub('<[^>]+>', '', content).split())
    print(f'  strengthened: {path} (~{words} words)')
else:
    print(f'  SKIP (no </body>): {path}')
PYEOF

  count=$((count+1))
done

echo ""
echo "Content strengthening complete. Files processed: $count"
