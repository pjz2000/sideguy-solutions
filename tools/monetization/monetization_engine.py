import os
import re

ROOT = "."
HTML_EXT = ".html"

SKIP_FILES = {
    "sitemap.xml",
    "recent-pages.html",
    "all-pages-index.html"
}

# Directories to never touch
SKIP_DIRS = {
    "seo-reserve",
    "tools",
    "docs",
    "signals",
    "data",
    ".git",
    "_quarantine_backups"
}

text_pj_block = """
<section class="sideguy-help">
<h2>Need Help Solving This?</h2>

<p>SideGuy exists to provide <strong>clarity before cost</strong>.
If you're stuck or unsure what to do next, text PJ and get a real human answer.</p>

<a href="sms:+17735441231" class="pj-button">📱 Text PJ</a>

<p>No pressure. Just clarity.</p>
</section>
"""

affiliate_block = """
<section class="sideguy-tools">
<h2>Helpful Tools</h2>

<ul>
<li>Energy savings calculator</li>
<li>Payment processing comparison</li>
<li>AI automation starter tools</li>
<li>Home upgrade ROI calculators</li>
</ul>

<p>SideGuy research tools help operators make smarter decisions.</p>
</section>
"""

referral_block = """
<section class="sideguy-operators">
<h2>Verified Operators</h2>

<p>SideGuy connects people to trusted local operators.</p>

<ul>
<li>HVAC installers</li>
<li>Electricians</li>
<li>Solar installers</li>
<li>Payment system installers</li>
</ul>

<p>Need a recommendation? <a href="sms:+17735441231">Text PJ</a></p>
</section>
"""

guide_block = """
<section class="sideguy-guides">
<h2>SideGuy Guides</h2>

<p>Some problems require deeper explanation.</p>

<ul>
<li>How to lower payment processing fees</li>
<li>How to choose the right HVAC system</li>
<li>AI automation for small businesses</li>
</ul>

<p>Premium SideGuy guides coming soon.</p>
</section>
"""

monetization_block = (
    text_pj_block +
    affiliate_block +
    referral_block +
    guide_block
)

def inject(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if "sideguy-help" in content:
        return False

    if "</body>" not in content:
        return False

    new_content = content.replace(
        "</body>",
        monetization_block + "\n</body>"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True

modified = 0
scanned = 0

for root, dirs, files in os.walk(ROOT):
    # Prune skipped directories in-place so os.walk won't descend into them
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]

    for file in files:
        if not file.endswith(HTML_EXT):
            continue
        if file in SKIP_FILES:
            continue

        path = os.path.join(root, file)
        scanned += 1

        if inject(path):
            modified += 1

print("Pages scanned:", scanned)
print("Pages modified:", modified)
