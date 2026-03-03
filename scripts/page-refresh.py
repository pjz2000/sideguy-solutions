"""
Page Refresh Engine — rewrites the "Last updated" timestamp on pages
that haven't been modified in > REFRESH_DAYS days.
Avoids double-stamping by replacing the full dated pattern.
"""
import os, re, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

REFRESH_DAYS = 30
today        = datetime.date.today().isoformat()
now          = datetime.datetime.now()
refreshed    = 0
skipped      = 0

# Matches: "Last updated: 2025-01-01" or "Last updated:" with no date
DATE_RE = re.compile(r"Last updated:(\s*\d{4}-\d{2}-\d{2})?", re.IGNORECASE)

for fname in os.listdir("."):
    if not fname.endswith(".html"):
        continue
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fname))
    if (now - mtime).days <= REFRESH_DAYS:
        skipped += 1
        continue

    with open(fname, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    if "Last updated:" not in html:
        skipped += 1
        continue

    new_html = DATE_RE.sub(f"Last updated: {today}", html)
    if new_html == html:
        skipped += 1
        continue

    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_html)
    refreshed += 1

print(f"Page refresh complete — {refreshed} refreshed, {skipped} skipped")
