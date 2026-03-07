import random

signals = open("docs/recursive-builder/pages-to-build.txt").read().splitlines()

priorities = []

for s in signals:
    score = random.randint(1, 100)
    priorities.append((score, s))

priorities.sort(reverse=True)

with open("docs/recursive-builder/priority-pages.txt", "w") as f:
    for score, page in priorities:
        f.write(f"{score} {page}\n")

print("Priority list generated:", len(priorities))
