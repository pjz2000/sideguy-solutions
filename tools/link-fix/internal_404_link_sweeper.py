import os
import re
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REDIRECT_FILE = ROOT / "public" / "_redirects"
REPORT = ROOT / "docs" / "link-reports" / "internal_link_fixes.md"

# Also scan root-level HTML (web root = repo root)
SCAN_DIRS = [ROOT]
SKIP_DIRS = {
    ".git", "node_modules", "public", "docs", "seo-reserve",
    "signals", "data", "tools", "scripts", "backups",
    "_BACKUPS", ".sideguy-backups", "reports",
}

redirects = {}
if REDIRECT_FILE.exists():
    with open(REDIRECT_FILE) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                redirects[parts[0]] = parts[1]

fixes = []

for scan_root in SCAN_DIRS:
    for dirpath, dirs, files in os.walk(scan_root):
        # prune skipped dirs in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for file in files:
            if not file.endswith(".html"):
                continue
            path = Path(dirpath) / file
            content = path.read_text(encoding="utf-8", errors="ignore")
            original = content
            for bad, good in redirects.items():
                content = content.replace(f'href="{bad}"', f'href="{good}"')
            if content != original:
                path.write_text(content, encoding="utf-8")
                fixes.append(str(path.relative_to(ROOT)))

REPORT.parent.mkdir(parents=True, exist_ok=True)
with open(REPORT, "w") as f:
    f.write("# Internal Link Fix Report\n\n")
    f.write(f"Redirects loaded: {len(redirects)}\n\n")
    if fixes:
        for p in fixes:
            f.write(f"- fixed links in {p}\n")
    else:
        f.write("No broken links found (or no _redirects file present).\n")

print("Internal link sweep complete")
print(f"Redirects loaded : {len(redirects)}")
print(f"Files updated    : {len(fixes)}")
