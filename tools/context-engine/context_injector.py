from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions/public")

cities = [
    "Austin", "Chicago", "San Diego", "Dallas", "Phoenix", "Denver", "Atlanta", "Seattle",
    "Miami", "Boston", "Nashville", "Las Vegas"
]

industry_pain = {
    "plumbers":    "emergency call coordination and technician dispatch",
    "dentists":    "appointment scheduling and patient reminders",
    "hvac":        "seasonal service demand and dispatch logistics",
    "restaurants": "reservation handling and customer inquiries",
    "law firms":   "lead intake and consultation scheduling",
    "contractors": "job scheduling and quote follow-ups"
}

tips = [
    "automated reminders reduce no-shows by 30-40%",
    "AI intake forms capture leads instantly after hours",
    "automated scheduling prevents double bookings",
    "AI chatbots handle 24/7 inquiries from website visitors",
    "automation reduces manual admin workload significantly"
]

pages = list(ROOT.rglob("*.html"))

for page in pages:

    text = page.read_text()

    if "Local Context for" not in text:

        slug = page.name.replace(".html", "")

        industry = "business"

        for key in industry_pain:
            if key in slug:
                industry = key

        city = random.choice(cities)
        pain = industry_pain.get(industry, "manual coordination tasks")
        tip  = random.choice(tips)

        block = f"""
<section class="local-context">
<h2>{city} – Local Context for {industry}</h2>
<p>Businesses in {city} often face challenges around {pain}.
AI automation tools can streamline these operations while improving customer response times.</p>
<p><strong>Practical tip:</strong> {tip}</p>
</section>
"""

        text = text.replace("</body>", block + "\n</body>")

        page.write_text(text)

print("Context sections injected")
