#!/usr/bin/env python3
# ==============================================================
# SIDEGUY PHONE ENFORCER
# Scans problems/, concepts/, generated/, a few key root files
# Corrects any old phone numbers to TARGET_PHONE display,
# and TARGET_PHONE_DIGIT for sms:/tel: href attributes.
# ==============================================================

import os, re

TARGET_PHONE   = "773-544-1231"          # display format
TARGET_DIGIT   = "+17735441231"           # href format (sms: / tel:)

# Any past phone numbers to auto-correct
BAD_PHONES = [
    "760-454-1860",
    "7604541860",
    "760.454.1860",
    "760 454 1860",
]

SCAN_DIRS  = ["problems", "concepts", "generated"]
SCAN_FILES = [
    "index.html",
    "knowledge/sideguy-knowledge-map.html",
    "payments.html",
    "ai-automation-hub.html",
    "operator-tools-hub.html",
    "payments-infrastructure-hub.html",
    "knowledge-hub.html",
]

def list_targets():
    files = []
    for d in SCAN_DIRS:
        if os.path.isdir(d):
            for root, _, fs in os.walk(d):
                for f in fs:
                    if f.endswith(".html"):
                        files.append(os.path.join(root, f))
    for f in SCAN_FILES:
        if os.path.exists(f):
            files.append(f)
    return sorted(set(files))

def fix_text(txt: str) -> str:
    # Fix display text occurrences
    for b in BAD_PHONES:
        txt = txt.replace(b, TARGET_PHONE)

    # Fix sms: links  →  sms:+17735441231
    txt = re.sub(
        r'sms:\s*\+?1?\s*[\d\-\.\s]{10,}',
        f"sms:{TARGET_DIGIT}",
        txt, flags=re.I
    )
    # Fix tel: links  →  tel:+17735441231
    txt = re.sub(
        r'tel:\s*\+?1?\s*[\d\-\.\s]{10,}',
        f"tel:{TARGET_DIGIT}",
        txt, flags=re.I
    )
    return txt

if __name__ == "__main__":
    print("=== SideGuy Phone Enforcer ===\n")
    changed = 0
    scanned = 0
    for path in list_targets():
        try:
            orig = open(path, "r", encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        new = fix_text(orig)
        if new != orig:
            open(path, "w", encoding="utf-8").write(new)
            print(f"  FIXED  {path}")
            changed += 1
        scanned += 1

    print(f"\n  Scanned: {scanned}   Fixed: {changed}")
    print(f"  Phone enforced: {TARGET_PHONE} / {TARGET_DIGIT}")
