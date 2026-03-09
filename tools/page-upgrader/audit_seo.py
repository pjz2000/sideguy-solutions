from pathlib import Path

root = Path("/workspaces/sideguy-solutions")
pages = list(root.glob("*.html"))
total = len(pages)

no_canonical = 0
no_meta = 0
no_h1 = 0
no_title = 0
dupe_h1 = 0

for p in pages:
    try:
        t = p.read_text(errors="ignore")
        if 'rel="canonical"' not in t: no_canonical += 1
        if '<meta name="description"' not in t: no_meta += 1
        if '<h1' not in t: no_h1 += 1
        if '<title' not in t: no_title += 1
        if t.count('<h1') > 1: dupe_h1 += 1
    except:
        pass

print(f"Total root HTML pages : {total}")
print(f"Missing canonical     : {no_canonical}  ({no_canonical*100//total if total else 0}%)")
print(f"Missing meta desc     : {no_meta}  ({no_meta*100//total if total else 0}%)")
print(f"Missing H1            : {no_h1}  ({no_h1*100//total if total else 0}%)")
print(f"Missing title tag     : {no_title}  ({no_title*100//total if total else 0}%)")
print(f"Duplicate H1 tags     : {dupe_h1}  ({dupe_h1*100//total if total else 0}%)")
