#!/usr/bin/env python3
"""Strip HTML anchor tags from meta description content attributes."""
import os, re, sys

line_re = re.compile(r'<meta\s+name="description"[^\n]*sms:', re.IGNORECASE)
anchor_re = re.compile(r'<a\s+href="sms:[^"]*">[^<]*</a>', re.IGNORECASE)
cleanup_re = re.compile(r'\s*[·•\-]?\s*Text PJ:?\s*$', re.IGNORECASE)

fixed = 0
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
skip_dirs = {'.git', 'node_modules', 'reports', 'tools', 'signals', 'self-improve-backups'}

for root, dirs, files in os.walk(root_dir):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        path = os.path.join(root, fname)
        try:
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
        except:
            continue
        if 'sms:' not in content:
            continue
        lines = content.split('\n')
        changed = False
        new_lines = []
        for line in lines:
            if line_re.search(line):
                new_line = anchor_re.sub('', line)
                new_line = cleanup_re.sub('', new_line)
                new_line = re.sub(r'  +', ' ', new_line)
                if new_line != line:
                    changed = True
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        if changed:
            with open(path, 'w', errors='ignore') as f:
                f.write('\n'.join(new_lines))
            fixed += 1

print(f'Fixed: {fixed} files')
sys.stdout.flush()
