import json

hubs=json.load(open("data/authority/hubs.json"))

for hub in hubs:

    print(f"HUB: {hub}")

    for i in range(1,6):

        print(f"{hub} -> related-page-{i}")
