INDUSTRIES = [
    "restaurants",
    "food-trucks",
    "salons",
    "contractors",
    "gyms",
    "dentists",
    "retail-stores",
    "property-managers"
]

TOPICS = [
    "best-payment-processor",
    "best-pos-system",
    "best-ai-tools"
]

HTML = """<!doctype html>
<html>
<head>
<title>{title}</title>
<meta name="description" content="{title} with SideGuy operator-first recommendations.">
<link rel="canonical" href="https://sideguysolutions.com/{slug}">
</head>
<body>
<h1>{title}</h1>
<p>Best options ranked by cost, speed, support, and long-term ROI.</p>

<section>
<h2>Top picks</h2>
<ul>
<li>Budget-first</li>
<li>Growth-first</li>
<li>Fastest setup</li>
<li>Best support</li>
</ul>
</section>

<section>
<h2>Run the calculator + compare routes</h2>
<p>Then text PJ for human decision help.</p>
</section>

</body>
</html>
"""

count = 0
for industry in INDUSTRIES:
    for topic in TOPICS:
        slug = f"{topic}-{industry}-san-diego.html"
        title = f"{topic.replace('-', ' ').title()} for {industry.replace('-', ' ').title()} in San Diego"
        with open(slug, "w") as f:
            f.write(HTML.format(slug=slug, title=title))
        count += 1

print(f"Created {count} best-of industry pages")
