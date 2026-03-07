import json

industries = [
"hvac",
"plumbing",
"restaurants",
"roofing",
"construction",
"real-estate",
"contractors",
"auto-repair"
]

locations = [
"san-diego",
"california",
"united-states"
]

with open("data/problem-pillars.json") as f:
    data = json.load(f)

for pillar in data["pillars"]:
    for topic in pillar["topics"]:
        for industry in industries:
            for location in locations:
                slug = f"{topic}-{industry}-{location}".replace(" ","-")
                print(slug)
