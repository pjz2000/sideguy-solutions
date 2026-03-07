import json

with open("data/authority/hubs.json") as f:
    hubs=json.load(f)

for hub in hubs:

    filename=f"{hub}.html"

    html=f"""<!DOCTYPE html>
<html>
<head>
<title>{hub.replace('-',' ').title()} | SideGuy Solutions</title>
<meta name="description" content="SideGuy guide to {hub.replace('-',' ')} for small businesses.">
<link rel="canonical" href="https://www.sideguysolutions.com/{filename}">
</head>

<body>

<h1>{hub.replace('-',' ').title()}</h1>

<p>This hub explains common problems related to {hub.replace('-',' ')} and how operators can solve them.</p>

<h2>Common Problems</h2>

<ul>
<li>Understanding tools</li>
<li>Reducing costs</li>
<li>Automation options</li>
<li>Implementation challenges</li>
</ul>

<p>Need help? Text PJ.</p>

</body>
</html>
"""

    with open(filename,"w") as f:
        f.write(html)

    print("Created hub page:",filename)
