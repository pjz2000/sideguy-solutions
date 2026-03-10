#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
OUTPUT="$ROOT/docs/index/page-metadata.tsv"

echo "Building page metadata index..."

python3 - "$ROOT" "$OUTPUT" << 'PYEOF'
import sys, os, re
from datetime import datetime

root = sys.argv[1]
output = sys.argv[2]

link_re = re.compile(r'<a ', re.IGNORECASE)
h2_re   = re.compile(r'<h2', re.IGNORECASE)

count = 0
with open(output, 'w') as out:
    out.write("slug\twords\tlinks\th2\tlastmod\n")
    for fname in os.listdir(root):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d')
            with open(fpath, 'r', errors='replace') as f:
                text = f.read()
            words   = len(text.split())
            links   = len(link_re.findall(text))
            h2s     = len(h2_re.findall(text))
            out.write(f"{fname}\t{words}\t{links}\t{h2s}\t{mtime}\n")
            count += 1
        except Exception:
            pass

print(f"Indexed {count} pages")
PYEOF

echo "Index written to: $OUTPUT"
wc -l "$OUTPUT"

