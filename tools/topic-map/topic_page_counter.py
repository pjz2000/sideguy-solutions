import os, json

topics = json.load(open("data/topic-map/topics.json"))

html_pages = []

for root, dirs, files in os.walk("."):

    for f in files:

        if f.endswith(".html"):

            html_pages.append(f.lower())

for topic in topics["topics"]:

    count = 0

    for page in html_pages:

        for cluster in topic["clusters"]:

            slug = cluster.replace(" ", "-")

            if slug in page:

                count += 1

    print(topic["name"], ":", count, "pages")
