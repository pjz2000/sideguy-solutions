import os

input_file="docs/problem-radar/radar-signals.tsv"
output_file="docs/build-queue/gravity-ranked.txt"

if not os.path.exists(input_file):
    print("Radar signals not found")
    exit()

lines=open(input_file).read().splitlines()

scored=[]

for line in lines[1:]:

    parts=line.split("\t")

    if len(parts) < 3:
        continue

    slug=parts[2]  # col 2 = slug

    score=0

    if "payment" in slug:
        score+=10
    if "software" in slug:
        score+=8
    if "automation" in slug:
        score+=7
    if "crm" in slug:
        score+=7
    if "processing" in slug:
        score+=6
    if "san-diego" in slug:
        score+=5
    if "repair" in slug:
        score+=4

    scored.append((score,slug))

scored.sort(reverse=True)

with open(output_file,"w") as f:
    for score,slug in scored:
        f.write(str(score)+" | "+slug+"\n")

print("Gravity ranking complete:",len(scored),"signals")
