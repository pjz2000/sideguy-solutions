import json

data = json.load(open("data/topic-map/topics.json"))

for topic in data["topics"]:

    print("TOPIC:", topic["name"])

    for cluster in topic["clusters"]:

        print("  ->", cluster)

    print()
