from pathlib import Path
import datetime

ROOT = Path("/workspaces/sideguy-solutions")
TOPICS = ROOT / "docs" / "hubs" / "hub_topics.txt"
PUBLIC = ROOT / "public" / "hubs"

PUBLIC.mkdir(parents=True, exist_ok=True)

topics = [x.strip() for x in TOPICS.read_text().splitlines() if x.strip()]

timestamp = datetime.datetime.utcnow().isoformat()

for topic in topics:
    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{topic.replace('-', ' ').title()} | SideGuy Solutions</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="SideGuy guide to {topic.replace('-', ' ')} including tools, pricing, automation ideas, and real-world implementation.">
<link rel="canonical" href="https://sideguysolutions.com/hubs/{topic}.html">
</head>
<body>
<h1>{topic.replace('-', ' ').title()}</h1>
<p>
SideGuy explores {topic.replace('-', ' ')} through real-world operator use cases,
automation strategies, pricing insights, and implementation guides.
</p>
<h2>What you'll learn</h2>
<ul>
<li>How {topic.replace('-', ' ')} works</li>
<li>Common automation opportunities</li>
<li>Typical business savings</li>
<li>Implementation strategies</li>
</ul>
<h2>Related SideGuy Pages</h2>
<ul>
<li><a href="/">SideGuy Home</a></li>
<li><a href="/ai/">AI Automation</a></li>
<li><a href="/payments/">Payments</a></li>
</ul>
<p><em>Generated {timestamp}</em></p>
</body>
</html>
"""
    (PUBLIC / f"{topic}.html").write_text(html)

print(f"Generated {len(topics)} hub pages")
