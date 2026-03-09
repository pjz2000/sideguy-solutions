#!/usr/bin/env python3
"""
SideGuy Content Differentiation Engine
Injects a city × industry unique section into longtail pages.
Safe to re-run — skips pages already tagged with <!-- SIDEGUY_DIFF -->.
"""
from pathlib import Path
import re, sys

ROOT = Path("/workspaces/sideguy-solutions")
MARKER = "<!-- SIDEGUY_DIFF -->"
DRY_RUN = "--dry-run" in sys.argv

# ── City data ────────────────────────────────────────────────────────────────
CITY_DATA = {
    "austin": {
        "label": "Austin, TX",
        "market": "fast-growing tech and startup hub with 50,000+ active small businesses",
        "note": "Austin's competitive market means faster response times often win jobs over price.",
        "cost_modifier": "slightly above national average",
    },
    "chicago": {
        "label": "Chicago, IL",
        "market": "second-largest U.S. service market, dense with B2B and trade operators",
        "note": "Chicago's business density means operators face more competition for the same customers.",
        "cost_modifier": "at or above national average",
    },
    "dallas": {
        "label": "Dallas, TX",
        "market": "one of the fastest-growing metro markets for independent operators",
        "note": "Dallas operators benefit from lower overhead costs than coastal cities.",
        "cost_modifier": "near national average",
    },
    "denver": {
        "label": "Denver, CO",
        "market": "high-growth mountain-west market with a strong mix of trades and services",
        "note": "Denver's younger demographic skews toward businesses that respond faster digitally.",
        "cost_modifier": "near national average",
    },
    "los-angeles": {
        "label": "Los Angeles, CA",
        "market": "largest single-metro service market in the U.S.",
        "note": "LA's size means niche operators can build sustainable businesses without competing everywhere.",
        "cost_modifier": "above national average",
    },
    "miami": {
        "label": "Miami, FL",
        "market": "bilingual market with high growth in both hospitality and professional services",
        "note": "Miami operators often need tools that work in English and Spanish.",
        "cost_modifier": "near national average",
    },
    "phoenix": {
        "label": "Phoenix, AZ",
        "market": "rapidly expanding Sun Belt market with strong demand for trades and services",
        "note": "Phoenix's sprawl makes automated follow-up more valuable than in walkable cities.",
        "cost_modifier": "below national average",
    },
    "portland": {
        "label": "Portland, OR",
        "market": "independent, sustainability-focused market with a strong local-first preference",
        "note": "Portland buyers respond better to transparency than to aggressive sales automation.",
        "cost_modifier": "near national average",
    },
    "seattle": {
        "label": "Seattle, WA",
        "market": "tech-adjacent market where buyers expect faster digital responses than most metros",
        "note": "Seattle operators benefit from automation most when it reduces decision friction.",
        "cost_modifier": "above national average",
    },
    "san-diego": {
        "label": "San Diego, CA",
        "market": "mid-size coastal market with a mix of trades, health, and professional services",
        "note": "San Diego's relatively high cost of living makes automating admin tasks ROI-positive faster.",
        "cost_modifier": "above national average",
    },
}

# ── Industry data ─────────────────────────────────────────────────────────────
INDUSTRY_DATA = {
    "accounting-firms": {
        "label": "accounting firms",
        "top_win": "automating client onboarding and document collection requests",
        "time_saved": "3–6 hours per week per client",
        "biggest_pain": "chasing clients for documents and signatures",
        "tool_hint": "A simple intake form + automated reminder sequence handles 80% of the friction.",
    },
    "adu-builders": {
        "label": "ADU builders",
        "top_win": "automating permit status updates and client progress notifications",
        "time_saved": "4–8 hours per project",
        "biggest_pain": "clients calling for project status updates",
        "tool_hint": "A status-update SMS trigger when milestones are hit eliminates most check-in calls.",
    },
    "hvac": {
        "label": "HVAC companies",
        "top_win": "missed call text-back and maintenance reminder sequences",
        "time_saved": "5–10 hours per week",
        "biggest_pain": "missed calls going to competitors",
        "tool_hint": "A missed-call auto-text capturing the lead is the single highest-ROI automation for HVAC.",
    },
    "plumbing": {
        "label": "plumbing companies",
        "top_win": "automated dispatch confirmations and after-job review requests",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "no-shows and late cancellations",
        "tool_hint": "A 2-hour reminder text with a reschedule link reduces no-shows by 30–40%.",
    },
    "roofing": {
        "label": "roofing contractors",
        "top_win": "storm-event lead capture and automated estimate follow-up",
        "time_saved": "5–8 hours per week during peak season",
        "biggest_pain": "following up on estimates before they go cold",
        "tool_hint": "Automated 3-day and 7-day estimate follow-ups close 15–25% more jobs without a sales call.",
    },
    "restaurants": {
        "label": "restaurants",
        "top_win": "review request automation after dining visits",
        "time_saved": "2–4 hours per week",
        "biggest_pain": "inconsistent review volume hurting local search ranking",
        "tool_hint": "A post-visit text requesting a review, sent 2 hours after checkout, is the simplest ROI win.",
    },
    "real-estate": {
        "label": "real estate agents",
        "top_win": "lead nurture sequences and showing reminder automation",
        "time_saved": "5–10 hours per week",
        "biggest_pain": "leads going cold between first contact and first showing",
        "tool_hint": "A 7-step email/text sequence keeping leads warm over 30 days closes more deals with no extra calls.",
    },
    "law-firms": {
        "label": "law firms",
        "top_win": "client intake automation and appointment reminder sequences",
        "time_saved": "4–8 hours per week",
        "biggest_pain": "manual intake forms and scheduling back-and-forth",
        "tool_hint": "Automated intake + calendar booking reduces administrative load per new client by 60–70%.",
    },
    "dentists": {
        "label": "dental practices",
        "top_win": "appointment reminders and reactivation sequences for lapsed patients",
        "time_saved": "3–6 hours per week",
        "biggest_pain": "no-shows and last-minute cancellations",
        "tool_hint": "A 48-hour and 2-hour reminder sequence typically cuts no-shows in half.",
    },
    "contractors": {
        "label": "contractors",
        "top_win": "bid follow-up automation and job completion check-ins",
        "time_saved": "4–7 hours per week",
        "biggest_pain": "bids going unanswered for days",
        "tool_hint": "A 3-day bid follow-up text increases response rates without the awkward sales call.",
    },
    "landscaping": {
        "label": "landscaping companies",
        "top_win": "seasonal outreach sequences and recurring service reminders",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "losing recurring customers between seasons",
        "tool_hint": "A spring outreach sequence to past customers books 20–30% of the season before ads are needed.",
    },
    "salons": {
        "label": "salons",
        "top_win": "appointment reminders and rebooking prompts after visits",
        "time_saved": "2–4 hours per week",
        "biggest_pain": "clients not rebooking until they're already past due",
        "tool_hint": "A rebooking reminder sent 3–4 weeks after a visit increases return visit rate by 15–25%.",
    },
    "gyms": {
        "label": "gyms and fitness studios",
        "top_win": "lead nurture for trial signups and churn-risk reactivation",
        "time_saved": "4–6 hours per week",
        "biggest_pain": "trial members not converting to paid memberships",
        "tool_hint": "A 5-step trial nurture sequence starting day 1 increases conversion rates by 20–35%.",
    },
    "electricians": {
        "label": "electricians",
        "top_win": "missed call text-back and job-completion review requests",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "losing jobs to whoever answers faster",
        "tool_hint": "An instant missed-call text response captures leads before they call the next electrician.",
    },
    "insurance-agencies": {
        "label": "insurance agencies",
        "top_win": "renewal reminders and lead follow-up sequences",
        "time_saved": "5–8 hours per week",
        "biggest_pain": "policy renewals slipping through without outreach",
        "tool_hint": "A 90-day, 30-day, and 7-day renewal sequence eliminates most manual renewal calls.",
    },
    "pest-control": {
        "label": "pest control companies",
        "top_win": "recurring service reminder sequences and seasonal outreach",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "customers canceling recurring service when they forget the value",
        "tool_hint": "A quarterly service reminder with a 1-click reschedule link dramatically reduces churn.",
    },
    "cleaning-services": {
        "label": "cleaning services",
        "top_win": "booking confirmation automation and post-clean review requests",
        "time_saved": "2–4 hours per week",
        "biggest_pain": "inconsistent review volume and no-shows",
        "tool_hint": "A day-before reminder + same-day arrival notice reduces cancellations and builds trust.",
    },
    "physical-therapy": {
        "label": "physical therapy practices",
        "top_win": "appointment reminders and home exercise program follow-ups",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "patients missing appointments and not completing home programs",
        "tool_hint": "Automated session reminders and between-visit check-ins improve both attendance and outcomes.",
    },
    "chiropractors": {
        "label": "chiropractic offices",
        "top_win": "appointment reminders and care plan follow-up sequences",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "patients dropping off care plans before completion",
        "tool_hint": "Automated check-ins between appointments keep patients engaged with their care plan.",
    },
    "tutors": {
        "label": "tutoring services",
        "top_win": "session reminder automation and progress update sequences for parents",
        "time_saved": "2–3 hours per week",
        "biggest_pain": "session cancellations with no notice",
        "tool_hint": "A 24-hour session reminder with a 1-click cancel/reschedule link cuts no-shows significantly.",
    },
    "veterinarians": {
        "label": "veterinary practices",
        "top_win": "vaccination reminder sequences and appointment reminders",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "pets falling behind on care because owners forget",
        "tool_hint": "Automated annual wellness reminders are the highest-ROI automation for most vet practices.",
    },
    "property-management": {
        "label": "property management companies",
        "top_win": "maintenance request automation and lease renewal reminders",
        "time_saved": "5–10 hours per week",
        "biggest_pain": "manual maintenance request tracking and tenant communication",
        "tool_hint": "Automated maintenance status updates reduce inbound tenant calls by 40–60%.",
    },
    "moving-companies": {
        "label": "moving companies",
        "top_win": "booking confirmation automation and pre-move checklist sequences",
        "time_saved": "3–5 hours per week",
        "biggest_pain": "customers canceling last minute or being unprepared on move day",
        "tool_hint": "A 7-day and 1-day pre-move sequence with a packing checklist reduces day-of surprises.",
    },
    "photographers": {
        "label": "photographers",
        "top_win": "booking confirmation automation and gallery delivery notifications",
        "time_saved": "2–4 hours per week",
        "biggest_pain": "clients asking 'when will my photos be ready?' repeatedly",
        "tool_hint": "An automated delivery timeline sequence set at booking eliminates most follow-up calls.",
    },
    "marketing-agencies": {
        "label": "marketing agencies",
        "top_win": "client reporting automation and project milestone notifications",
        "time_saved": "4–8 hours per week",
        "biggest_pain": "manual reporting consuming billable hours",
        "tool_hint": "Automated campaign reports sent directly to clients reduce reporting time by 60–70%.",
    },
}

# ── Slug parsing ──────────────────────────────────────────────────────────────
def extract_city_industry(stem: str):
    """Return (city_key, industry_key) or (None, None)."""
    city = next((c for c in CITY_DATA if f"-in-{c}" in stem or stem.endswith(f"-{c}")), None)
    industry = next((i for i in INDUSTRY_DATA if i in stem), None)
    return city, industry

# ── Unique section builder ────────────────────────────────────────────────────
def build_section(city_key: str, industry_key: str) -> str:
    c = CITY_DATA[city_key]
    i = INDUSTRY_DATA[industry_key]
    return f"""{MARKER}
<section style="margin:32px 0;padding:24px 28px;background:rgba(255,255,255,.72);border:1px solid rgba(0,100,80,.12);border-radius:16px;">
  <h2 style="font-size:1rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:#3f6173;margin-bottom:14px;">
    📍 {c['label']} — Local Context for {i['label'].title()}
  </h2>
  <p style="font-size:.95rem;line-height:1.65;color:#073044;margin-bottom:10px;">
    {c['label']} is a {c['market']}. For {i['label']}, the highest-ROI starting point is typically
    <strong>{i['top_win']}</strong> — which saves most operators roughly <strong>{i['time_saved']}</strong>
    of manual follow-up per week.
  </p>
  <p style="font-size:.92rem;line-height:1.65;color:#3f6173;margin-bottom:10px;">
    The most common pain point: <em>{i['biggest_pain']}</em>.
    Automation costs in {c['label']} are {c['cost_modifier']} due to local labor rates and tooling availability.
  </p>
  <p style="font-size:.92rem;line-height:1.65;color:#3f6173;margin-bottom:0;">
    <strong>Practical tip:</strong> {i['tool_hint']} {c['note']}
  </p>
</section>
"""

# ── Main loop ─────────────────────────────────────────────────────────────────
pages = list(ROOT.glob("*.html"))
updated = 0
skipped_marker = 0
skipped_no_match = 0
skipped_no_body = 0

for page in pages:
    try:
        text = page.read_text(errors="ignore")
    except Exception:
        continue

    if MARKER in text:
        skipped_marker += 1
        continue

    city, industry = extract_city_industry(page.stem)
    if not city or not industry:
        skipped_no_match += 1
        continue

    # Find the closing </main> or </body> — insert section before it
    insert_before = "</main>" if "</main>" in text else "</body>"
    if insert_before not in text:
        skipped_no_body += 1
        continue

    section = build_section(city, industry)
    new_text = text.replace(insert_before, section + "\n" + insert_before, 1)

    if not DRY_RUN:
        page.write_text(new_text)
    updated += 1

print(f"Pages updated          : {updated}")
print(f"Skipped (already done) : {skipped_marker}")
print(f"Skipped (no city/ind.) : {skipped_no_match}")
print(f"Skipped (no body tag)  : {skipped_no_body}")
if DRY_RUN:
    print("DRY RUN — no files written")
