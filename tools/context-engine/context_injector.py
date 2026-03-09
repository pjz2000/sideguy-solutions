from pathlib import Path
import random

ROOT = Path("/workspaces/sideguy-solutions/public")

cities = [
    "Austin", "Chicago", "San Diego", "Dallas", "Phoenix", "Denver", "Atlanta", "Seattle",
    "Miami", "Boston", "Nashville", "Las Vegas"
]

industry_pain = {
    # trades
    "plumber":          "emergency call coordination and technician dispatch",
    "electrician":      "job scheduling and after-hours emergency response",
    "roofer":           "storm-season lead capture and estimate follow-up",
    "hvac":             "seasonal service demand and dispatch logistics",
    "ac-repair":        "seasonal service demand and dispatch logistics",
    "ac-not-cooling":   "seasonal service demand and dispatch logistics",
    "water-heater":     "emergency service dispatch and technician coordination",
    "landscap":         "recurring service scheduling and seasonal outreach",
    "pest-control":     "recurring service reminders and seasonal scheduling",
    "pool-service":     "recurring maintenance scheduling and customer reminders",
    "contractor":       "job scheduling and quote follow-ups",
    "construction":     "subcontractor coordination and project milestone tracking",
    "solar":            "installation scheduling and permit status updates",
    # health & wellness
    "dentist":          "appointment scheduling and patient reminders",
    "dental":           "appointment scheduling and patient reminders",
    "medical":          "patient intake, scheduling, and follow-up coordination",
    "chiropractic":     "care plan follow-ups and appointment reminders",
    "physical-therapy": "session reminders and home program follow-ups",
    "veterinar":        "vaccination reminders and appointment scheduling",
    "salon":            "appointment reminders and rebooking sequences",
    "gym":              "trial member conversion and churn-risk reactivation",
    "fitness":          "trial member conversion and class booking automation",
    "nutrition":        "client check-in sequences and program adherence follow-ups",
    # professional services
    "law-firm":         "lead intake and consultation scheduling",
    "law firm":         "lead intake and consultation scheduling",
    "attorney":         "client intake and deadline reminder automation",
    "legal":            "client intake and deadline reminder automation",
    "accountant":       "client document collection and deadline reminders",
    "accounting":       "client document collection and deadline reminders",
    "insurance":        "policy renewal reminders and lead follow-up sequences",
    "real-estate":      "lead nurture sequences and showing reminders",
    "real estate":      "lead nurture sequences and showing reminders",
    "consultant":       "proposal follow-ups and client onboarding automation",
    "marketing":        "client reporting automation and campaign update sequences",
    "architect":        "project milestone updates and client communication",
    "interior-design":  "project update sequences and vendor coordination",
    # food & hospitality
    "restaurant":       "reservation handling and customer inquiry automation",
    "payment-process":  "fee management, chargebacks, and settlement delays",
    "hotel":            "guest communication and booking confirmation sequences",
    "vacation-rental":  "guest check-in sequences and review request automation",
    # tech & software
    "saas":             "trial onboarding sequences and churn-risk alerting",
    "software":         "client onboarding and support ticket routing",
    "it-service":       "helpdesk ticket triage and SLA breach alerting",
    "managed-service":  "automated monitoring alerts and client status updates",
    "zapier":           "workflow automation failures and API integration gaps",
    "ai-automation":    "workflow setup, tool selection, and implementation clarity",
    "ai-agent":         "workflow setup, tool selection, and implementation clarity",
    "chatgpt":          "prompt engineering, integration, and reliability concerns",
    # payments & compliance
    "payment":          "fee management, chargebacks, and settlement delays",
    "stripe":           "payout delays, account holds, and fee transparency",
    "compliance":       "regulatory requirement tracking and audit preparation",
    "soc-2":            "audit readiness and evidence collection automation",
    # local service
    "cleaning":         "booking confirmation and post-service review requests",
    "moving":           "pre-move checklist automation and booking confirmations",
    "photographer":     "booking confirmation and gallery delivery notifications",
    "wedding":          "vendor coordination sequences and timeline reminders",
    "event":            "booking confirmations and day-of logistics coordination",
    "daycare":          "parent communication sequences and enrollment follow-ups",
    "pet-groom":        "appointment reminders and rebooking sequences",
    "auto-repair":      "repair status updates and service reminder sequences",
    "car-dealership":   "lead follow-up sequences and service appointment reminders",
    # general catch-alls
    "after-hours":      "after-hours lead capture and automated response sequences",
    "missed-call":      "missed call text-back and lead capture automation",
    "who-do-i-call":    "operator guidance, routing, and human-first clarity",
    "when-not-to":      "decision clarity and human judgment in automation",
}

tips = [
    "automated reminders reduce no-shows by 30-40%",
    "AI intake forms capture leads instantly after hours",
    "automated scheduling prevents double bookings",
    "AI chatbots handle 24/7 inquiries from website visitors",
    "automation reduces manual admin workload significantly"
]

pages = list(ROOT.rglob("*.html"))
updated = 0
kept_generic = 0

for page in pages:

    text = page.read_text()
    slug = page.name.replace(".html", "").lower()

    # Remove a previously injected generic "business" block so we can replace with specific
    already_specific = "Local Context for" in text and "Local Context for business" not in text
    if already_specific:
        continue

    # Strip existing generic block before re-injecting specific one
    if "Local Context for business" in text:
        import re
        text = re.sub(
            r'\n<section class="local-context">.*?</section>\n',
            '',
            text,
            flags=re.DOTALL
        )

    industry = None
    for key in industry_pain:
        if key in slug:
            industry = key
            break

    if industry is None:
        kept_generic += 1
        continue  # leave pages that truly have no match alone

    city  = random.choice(cities)
    pain  = industry_pain[industry]
    tip   = random.choice(tips)

    block = f"""
<section class="local-context">
<h2>{city} – Local Context for {industry.replace("-", " ").title()}</h2>
<p>Businesses in {city} often face challenges around {pain}.
AI automation tools can streamline these operations while improving customer response times.</p>
<p><strong>Practical tip:</strong> {tip}</p>
</section>
"""

    text = text.replace("</body>", block + "\n</body>")
    page.write_text(text)
    updated += 1

print(f"Context sections injected/updated : {updated}")
print(f"Pages with no matching industry    : {kept_generic} (left unchanged)")
