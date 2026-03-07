"""
problem_detector.py
-------------------
Filters discussion signals for problem-indicating phrases and writes
docs/problem-scanner/problem-signals.txt.
"""
import os

signals_file = "docs/problem-scanner/discussion-signals.txt"

if not os.path.exists(signals_file):
    print("No discussion signals — run discussion_scanner.py first")
    exit(1)

signals = [l for l in open(signals_file).read().splitlines() if l.strip()]

problem_words = [
    "problem", "issue", "fix", "help", "fail", "error",
    "too expensive", "slow", "not working", "broken",
    "replace", "alternative", "switch", "versus", "vs",
    "bad", "worst", "terrible", "struggle", "frustrat",
    "can't", "won't", "doesn't", "stopped", "down",
    "overpriced", "complicated", "confusing",
]

problems = []
for s in signals:
    for p in problem_words:
        if p in s:
            problems.append(s)
            break  # one match per signal

with open("docs/problem-scanner/problem-signals.txt", "w") as f:
    for p in problems:
        f.write(p + "\n")

print(f"Problem signals detected: {len(problems)} of {len(signals)} total")
