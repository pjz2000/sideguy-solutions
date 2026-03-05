#!/usr/bin/env python3
"""
SideGuy Problem Discovery
--------------------------
Fetches RSS feeds, extracts problem-shaped titles, deduplicates against
existing radar seeds, and appends new seeds to:
  docs/problem-radar/trends_notes.txt     (feeds your existing radar pipeline)
  docs/problem-radar/discovery_seeds.txt  (this run only)
  docs/problem-radar/discovery_raw.tsv    (full audit trail)

Then kicks off tools/problem-radar/problem_radar.py if present.

Feeds config: tools/problem-discovery/feeds.txt (one URL per line)
"""

import csv, hashlib, os, re, time, datetime, xml.etree.ElementTree as ET
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests")
    exit(1)

ROOT   = Path(__file__).parent.parent.parent.resolve()
OUT_DIR = ROOT / "docs" / "problem-radar"
FEEDS_FILE = ROOT / "tools" / "problem-discovery" / "feeds.txt"

OUT_RAW   = OUT_DIR / "discovery_raw.tsv"
OUT_SEEDS = OUT_DIR / "discovery_seeds.txt"
OUT_NOTES = OUT_DIR / "trends_notes.txt"

PHONE              = "773-544-1231"
MAX_ITEMS_PER_FEED = 20
REQUEST_TIMEOUT    = 12
SLEEP_SECS         = 0.8

SKIP_WORDS = {"help", "question", "advice", "update", "weekly", "thread",
              "megathread", "discussion", "ama", "ask", "meta"}

def now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()

def norm(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"&amp;|&lt;|&gt;|&quot;|&#39;", " ", s)
    s = re.sub(r"[^a-z0-9\s\-+/]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def seedify(title: str) -> str:
    t = norm(title)
    for prefix in ("how do i ", "how to ", "anyone else ", "psa ", "eli5 "):
        if t.startswith(prefix):
            t = t[len(prefix):]
    t = re.sub(r"\b(help|question|advice)\b", "", t)
    return re.sub(r"\s+", " ", t).strip()

def uid(feed: str, title: str) -> str:
    return hashlib.sha1((feed + "::" + title).encode()).hexdigest()[:12]

def parse_titles(xml_text: str) -> list[str]:
    titles = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return titles
    # RSS 2.0
    for item in root.findall(".//item"):
        t = (item.findtext("title") or "").strip()
        if t:
            titles.append(t)
    # Atom
    if not titles:
        for ns in ("http://www.w3.org/2005/Atom", ""):
            prefix = f"{{{ns}}}" if ns else ""
            for entry in root.findall(f".//{prefix}entry"):
                t = (entry.findtext(f"{prefix}title") or "").strip()
                if t:
                    titles.append(t)
    return titles

def load_existing() -> set[str]:
    existing = set()
    for path in [OUT_NOTES, OUT_SEEDS,
                 OUT_DIR / "manual_seeds.txt",
                 OUT_DIR / "trends_notes.txt"]:
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    existing.add(norm(line))
    return existing

OUT_DIR.mkdir(parents=True, exist_ok=True)

feeds = [
    ln.strip() for ln in FEEDS_FILE.read_text().splitlines()
    if ln.strip() and not ln.strip().startswith("#")
] if FEEDS_FILE.exists() else []

if not feeds:
    print("No feeds configured. Add URLs to tools/problem-discovery/feeds.txt")
    exit(0)

existing  = load_existing()
new_seeds : list[str] = []
raw_rows  : list[list] = []

for feed_url in feeds:
    try:
        resp = requests.get(
            feed_url, timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "SideGuyProblemDiscovery/1.0"},
        )
        if resp.status_code != 200:
            print(f"  skip {feed_url} (HTTP {resp.status_code})")
            continue
        titles = parse_titles(resp.text)[:MAX_ITEMS_PER_FEED]
        added = 0
        for title in titles:
            seed = seedify(title)
            if not seed or len(seed) < 8:
                continue
            # Filter pure noise titles
            if norm(seed) in SKIP_WORDS or all(w in SKIP_WORDS for w in seed.split()):
                continue
            sid = uid(feed_url, title)
            raw_rows.append([now_utc(), feed_url, sid, title, seed])
            n = norm(seed)
            if n not in existing:
                existing.add(n)
                new_seeds.append(seed)
                added += 1
        print(f"  {feed_url.split('/')[-2] or feed_url} → {len(titles)} titles, {added} new")
    except Exception as e:
        print(f"  error fetching {feed_url}: {e}")
    time.sleep(SLEEP_SECS)

# Write raw audit TSV
with open(OUT_RAW, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["timestamp_utc", "feed", "id", "title", "seed"])
    for row in raw_rows:
        w.writerow(row)

# Write seeds file (this run)
with open(OUT_SEEDS, "w", encoding="utf-8") as f:
    f.write(f"# SideGuy Problem Discovery seeds\n")
    f.write(f"# generated: {now_utc()}\n")
    f.write(f"# Text PJ: {PHONE}\n\n")
    for s in new_seeds:
        f.write(s + "\n")

# Append into trends_notes.txt for radar pipeline
if new_seeds:
    with open(OUT_NOTES, "a", encoding="utf-8") as f:
        f.write(f"\n# --- discovery {now_utc()} ---\n")
        for s in new_seeds:
            f.write(s + "\n")

print(f"\nDiscovery complete")
print(f"  Feeds fetched  : {len(feeds)}")
print(f"  Raw titles     : {len(raw_rows)}")
print(f"  New seeds      : {len(new_seeds)}")
print(f"  Seeds file     : {OUT_SEEDS.relative_to(ROOT)}")
print(f"  Raw audit      : {OUT_RAW.relative_to(ROOT)}")

# Kick radar engine if present
for candidate in [
    ROOT / "tools" / "problem-radar" / "problem_radar.py",
    ROOT / "scripts" / "problem-radar-engine.py",
]:
    if candidate.exists():
        print(f"\nRunning radar engine: {candidate.relative_to(ROOT)}")
        os.system(f"python3 {candidate}")
        break
