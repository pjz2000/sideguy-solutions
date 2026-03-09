from pathlib import Path
from itertools import product

ROOT = Path("/workspaces/sideguy-solutions")
DOCS = ROOT / "docs" / "inventory-intelligence"
OUT = DOCS / "generated"
OUT.mkdir(parents=True, exist_ok=True)

skills     = [x.strip() for x in (DOCS / "skills.txt").read_text().splitlines() if x.strip()]
industries = [x.strip() for x in (DOCS / "industries.txt").read_text().splitlines() if x.strip()]
problems   = [x.strip() for x in (DOCS / "problems.txt").read_text().splitlines() if x.strip()]

def score_signal(skill: str, industry: str, problem: str) -> int:
    score = 0

    high_value_problems = {
        "missed calls": 5,
        "slow lead response": 5,
        "manual scheduling": 4,
        "invoice backlog": 4,
        "after hours inquiries": 4,
        "dispatch coordination": 5,
        "admin workload": 3,
        "customer follow up": 4,
        "review management": 2,
        "faq overload": 2,
    }
    score += high_value_problems.get(problem, 1)

    valuable_industries = {
        "hvac companies": 4,
        "dentists": 4,
        "law firms": 4,
        "property managers": 4,
        "medical clinics": 4,
        "real estate agents": 3,
        "plumbers": 4,
        "electricians": 4,
        "roofers": 4,
        "restaurants": 3,
        "auto repair shops": 3,
        "consultants": 2,
        "salons": 2,
        "landscapers": 2,
        "insurance agencies": 3,
    }
    score += valuable_industries.get(industry, 1)

    valuable_skills = {
        "ai chatbot": 3,
        "ai scheduling automation": 5,
        "ai invoice automation": 4,
        "ai crm automation": 4,
        "ai lead qualification": 5,
        "ai review response automation": 2,
        "ai faq automation": 2,
        "ai email automation": 3,
        "ai intake form automation": 4,
        "ai customer support automation": 4,
    }
    score += valuable_skills.get(skill, 1)

    return score

rows = []

for skill, industry, problem in product(skills, industries, problems):
    title = f"{skill} for {industry} with {problem}"
    score = score_signal(skill, industry, problem)
    rows.append((score, title, skill, industry, problem))

rows.sort(reverse=True, key=lambda x: x[0])

all_signals  = OUT / "all_signals.tsv"
top_signals  = OUT / "top_signals.txt"
gravity_append = OUT / "gravity_append.txt"

with all_signals.open("w") as f:
    f.write("score\ttitle\tskill\tindustry\tproblem\n")
    for score, title, skill, industry, problem in rows:
        f.write(f"{score}\t{title}\t{skill}\t{industry}\t{problem}\n")

top_n = 250

with top_signals.open("w") as f:
    for score, title, skill, industry, problem in rows[:top_n]:
        f.write(f"{title}\n")

with gravity_append.open("w") as f:
    for score, title, skill, industry, problem in rows[:top_n]:
        f.write(f"{title}\n")

print(f"Generated {len(rows)} signals")
print(f"Wrote top {top_n} prioritized signals to {top_signals}")
print(f"Wrote gravity-ready list to {gravity_append}")
