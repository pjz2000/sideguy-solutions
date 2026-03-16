#!/usr/bin/env python3
"""
SideGuy Lead Amplifier
Injects a 'second opinion' CTA block into pages whose filenames match
high-intent keywords — but only if the block isn't already present.
Run: python3 tools/lead-engine/lead-amplifier.py [pages_dir]
"""
import os
import sys
from datetime import date

PAGES_DIR = sys.argv[1] if len(sys.argv) > 1 else "pages"
LOG_FILE  = "logs/lead-engine/lead-upgrades.log"

KEYWORDS = [
    "quote-too-high",
    "repair-cost",
    "inspection-cost",
    "fees-too-high",
    "repair-vs-replace",
]

MARKER = "sideguy-second-opinion"

CTA_BLOCK = """
<div id="sideguy-second-opinion" style="border:2px solid #21d3a1;padding:22px 24px;margin:40px 0;background:rgba(33,211,161,.07);border-radius:14px;">
  <h2 style="margin-top:0;font-size:1.15rem;color:#073044;">Need a Second Opinion?</h2>
  <p style="color:#3f6173;margin:.5rem 0;">
    If this situation feels confusing or the quote seems unusually high, you're not alone.
    Many people reach out just to sanity-check a decision before spending thousands.
  </p>
  <p style="color:#3f6173;margin:.5rem 0;">
    Text PJ directly at <strong>773-544-1231</strong> and send the quote screenshot.
  </p>
  <p style="margin:.5rem 0 0;">
    <a href="sms:+17735441231" style="display:inline-block;padding:11px 22px;border-radius:999px;background:linear-gradient(135deg,#21d3a1,#00c7ff);color:#fff;font-weight:800;font-size:.9rem;text-decoration:none;">📱 Text PJ — No pressure. Just clarity.</a>
  </p>
</div>"""


def find_html_files(root):
    for dirpath, _, files in os.walk(root):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f), f


def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    upgraded = []
    skipped_present = []
    skipped_no_match = 0

    for filepath, filename in find_html_files(PAGES_DIR):
        matched = any(kw in filename for kw in KEYWORDS)
        if not matched:
            skipped_no_match += 1
            continue

        content = open(filepath, encoding="utf-8", errors="ignore").read()
        if MARKER in content:
            skipped_present.append(filename)
            continue

        # Inject before </body>; fall back to appending if tag not found
        if "</body>" in content:
            content = content.replace("</body>", CTA_BLOCK + "\n</body>", 1)
        else:
            content += CTA_BLOCK

        open(filepath, "w", encoding="utf-8").write(content)
        upgraded.append(filename)

    with open(LOG_FILE, "a") as log:
        log.write(f"Lead amplifier run {date.today()}\n")
        for f in upgraded:
            log.write(f"  upgraded: {f}\n")
        log.write(f"  total upgraded: {len(upgraded)}, already present: {len(skipped_present)}\n\n")

    print(f"\nUpgraded:        {len(upgraded)} pages")
    print(f"Already had CTA: {len(skipped_present)} pages")
    print(f"No keyword match: {skipped_no_match} pages")
    if upgraded:
        print("\nUpgraded files:")
        for f in upgraded:
            print(f"  {f}")
    print(f"\nLog: {LOG_FILE}")


if __name__ == "__main__":
    main()
