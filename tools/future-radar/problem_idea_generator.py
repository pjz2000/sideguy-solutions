import csv

INPUT = "docs/future-radar/future-problems.tsv"
OUTPUT = "docs/future-radar/page-ideas.txt"

ideas = []

with open(INPUT) as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        title = row["title"].lower()
        idea = "how " + title + " affects small businesses"
        ideas.append(idea)

with open(OUTPUT, "w") as f:
    for i in ideas:
        f.write(i + "\n")

print("Page ideas generated:", len(ideas))
