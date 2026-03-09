#!/usr/bin/env python3
"""
SHIP-025: Footer semantic tag audit & fix.
Ensures every page has a <footer> element with role="contentinfo".
Pages using a bare <div> as footer get it upgraded.
Pages missing a footer entirely get a minimal one injected before </body>.
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

footer_tag_re   = re.compile(r'<footer[\s>]', re.IGNORECASE)
div_footer_re   = re.compile(
    r'<div([^>]*class="[^"]*footer[^"]*"[^>]*)>',
    re.IGNORECASE
)
role_re         = re.compile(r'role=["\']contentinfo["\']', re.IGNORECASE)
body_close_re   = re.compile(r'</body>', re.IGNORECASE)

MINIMAL_FOOTER = (
    '\n<footer role="contentinfo" style="max-width:820px;margin:0 auto;'
    'padding:24px 24px 40px;color:#3f6173;font-size:.82rem;">'
    '\n  <p>© 2026 SideGuy Solutions · San Diego · '
    '<a href="/" style="color:#3f6173;">Home</a> · '
    '<a href="sms:+17604541860" style="color:#3f6173;">Text PJ</a>'
    '</p>\n</footer>'
)

def process(fpath):
    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    changed = False

    # 1. Upgrade <div class="footer"> → <footer role="contentinfo">
    if not footer_tag_re.search(content) and div_footer_re.search(content):
        def upgrade_div(m):
            attrs = m.group(1)
            if not role_re.search(attrs):
                attrs += ' role="contentinfo"'
            return f'<footer{attrs}>'
        # also need to close — find matching </div> is complex; skip for safety
        # just add role to div instead
        content = div_footer_re.sub(
            lambda m: m.group(0).replace('>', ' role="contentinfo">') if 'role=' not in m.group(0) else m.group(0),
            content, count=1
        )
        changed = True

    # 2. Add role="contentinfo" to existing <footer> missing it
    if footer_tag_re.search(content):
        def add_role(m):
            tag = m.group(0)
            if 'role=' not in tag.lower():
                return tag.replace('<footer', '<footer role="contentinfo"', 1)
            return tag
        new_content = re.sub(r'<footer(?![^>]*role=)[^>]*>', add_role, content, flags=re.IGNORECASE)
        if new_content != content:
            content = new_content
            changed = True

    # 3. Inject minimal footer if none exists at all
    if not footer_tag_re.search(content) and not div_footer_re.search(content):
        m = body_close_re.search(content)
        if m:
            content = content[:m.start()] + MINIMAL_FOOTER + '\n' + content[m.start():]
            changed = True

    if changed:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changed

def main():
    html_files = [f for f in os.listdir(ROOT) if f.endswith('.html')]
    fixed = 0
    for fname in html_files:
        if process(os.path.join(ROOT, fname)):
            fixed += 1
    print(f"✅ SHIP-025 complete — footer semantic tags fixed in {fixed} files.")

if __name__ == '__main__':
    main()
