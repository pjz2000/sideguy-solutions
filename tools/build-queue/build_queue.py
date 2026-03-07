import os

rank_file="docs/build-queue/gravity-ranked.txt"
queue_file="docs/build-queue/build-queue.txt"

lines=open(rank_file).read().splitlines()

top=lines[:50]

with open(queue_file,"w") as f:
    for line in top:
        slug=line.split("|")[1].strip()
        f.write(slug+"\n")

print("Build queue created:",len(top),"pages queued")
