u from pathlib import Path
import re

ROOT = Path("/workspaces/sideguy-solutions")
RADAR = ROOT / "docs" / "problem-radar" / "radar-signals.tsv"
ALT_RADAR = ROOT / "docs" / "internet-radar" / "internet_signals.tsv"
QUEUE = ROOT / "docs" / "opportunity-engine" / "priority_queue.txt"
REPORT = ROOT / "docs" / "opportunity-engine" / "priority_report.tsv"
GRAVITY = ROOT / "docs" / "auto-builder" / "gravity_pages.txt"

sources = []
if RADAR.exists():
    sources.append(RADAR)
if ALT_RADAR.exists():
    sources.append(ALT_RADAR)

if not sources:
    raise SystemExit("No radar signal files found in docs/problem-radar or docs/internet-radar")

raw = []

for src in sources:
    lines = src.read_text(errors="ignore").splitlines()
    for line in lines:
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            signal = parts[-1].strip()
        elif len(parts) == 2:
            signal = parts[-1].strip()
        else:
            signal = line.strip()
        if signal and "timestamp" not in signal.lower():
            raw.append(signal)

def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s

signals = sorted(set(normalize(x) for x in raw))

high_value_terms = {
    "cost": 5,
    "pricing": 5,
    "roi": 5,
    "savings": 5,
    "fees": 5,
    "implementation": 4,
    "automation": 4,
    "dispatch": 4,
    "scheduling": 4,
    "chatbot": 3,
    "lead": 4,
    "follow up": 4,
    "payment": 5,
    "stripe": 5,
    "square": 4,
    "hvac": 4,
    "contractor": 4,
    "restaurant": 3,
    "dentist": 4,
    "law firm": 4,
    "property manager": 4,
    "small business": 3,
    "comparison": 4,
    "vs": 4,
}

def score_signal(s: str) -> int:
    score = 0
    # base commercial / operator value
    for term, pts in high_value_terms.items():
        if term in s:
            score += pts
    # strong modifiers
    if len(s.split()) >= 4:
        score += 2
    if "how" in s:
        score += 1
    if "best" in s:
        score += 1
    if "for " in s:
        score += 2
    # de-prioritize weak / broad chatter
    weak_terms = ["meme", "joke", "funny", "news", "trend"]
    for term in weak_terms:
        if term in s:
            score -= 2
    return score

ranked = [(score_signal(s), s) for s in signals]
ranked.sort(key=lambda x: (-x[0], x[1]))

top_n = 250
top = ranked[:top_n]

QUEUE.parent.mkdir(parents=True, exist_ok=True)
with QUEUE.open("w") as f:
    for _, s in top:
        f.write(s + "\n")

with REPORT.open("w") as f:
    f.write("score\tsignal\n")
    for score, s in ranked:
        f.write(f"{score}\t{s}\n")

existing = set()
if GRAVITY.exists():
    existing = set(x.strip() for x in GRAVITY.read_text().splitlines() if x.strip())

added = []
with GRAVITY.open("a") as f:
    for _, s in top:
        if s not in existing:
            f.write(s + "\n")
            added.append(s)
            existing.add(s)

print(f"Total normalized signals: {len(signals)}")
print(f"Top queued signals: {len(top)}")
print(f"Appended to gravity queue: {len(added)}")
print(f"Queue file: {QUEUE}")
print(f"Report file: {REPORT}")