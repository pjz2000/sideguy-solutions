"""
problem_extractor.py
--------------------
Reads collected signals and extracts the top 50 keywords by frequency.
Writes docs/problem-engine/problem-keywords.txt.
"""
import os
from collections import Counter

signals_file = "docs/problem-engine/problem-signals.txt"

if not os.path.exists(signals_file):
    print("No signals file found — run problem_collector.py first")
    exit(1)

signals = [l for l in open(signals_file).read().splitlines() if l.strip()]

# stopwords — skip noise tokens
STOP = {"the","a","an","and","or","of","to","for","in","on","at","is","it",
        "with","how","my","your","san","diego","california","north","county",
        "do","i","we","be","not","no","are","was","were","has","have","by",
        "from","this","that","as","if","so","can","our","their","its","us"}

words = []
for s in signals:
    for w in s.replace("-", " ").split():
        w = w.strip(".,?!:;\"'()")
        if w and w not in STOP and len(w) > 2:
            words.append(w)

counts = Counter(words)

with open("docs/problem-engine/problem-keywords.txt", "w") as f:
    f.write(f"{'Keyword':<32} {'Count':>6}\n")
    f.write("-" * 40 + "\n")
    for k, v in counts.most_common(50):
        f.write(f"{k:<32} {v:>6}\n")

print("Keyword map created")
print(f"Top 10: {', '.join(k for k,_ in counts.most_common(10))}")
