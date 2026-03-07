import os
import csv
import datetime

RADAR_FILE = "docs/problem-radar/radar-signals.tsv"
OUTPUT_DIR = "auto/problem-pages"
LEADERBOARD = "docs/problem-engine/problem-leaderboard.md"

problems = []

HIGH_VALUE_WORDS = [
    "payment", "fees", "software", "ai",
    "automation", "compliance", "tax",
    "hvac", "energy", "solar", "install",
    "repair", "cost",
]

URGENCY_WORDS = [
    "broken", "not working", "error",
    "problem", "down", "failed",
]


def score_problem(topic):
    score = 0
    topic = topic.lower()
    for w in HIGH_VALUE_WORDS:
        if w in topic:
            score += 5
    for w in URGENCY_WORDS:
        if w in topic:
            score += 3
    score += len(topic.split())
    return score


def create_page(topic):
    import html as htmlmod
    slug = topic.lower().replace(" ", "-")
    path = f"{OUTPUT_DIR}/{slug}.html"
    if os.path.exists(path):
        return
    esc = htmlmod.escape(topic)
    with open(path, "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc} | SideGuy Solutions</title>
  <meta name="description" content="SideGuy helps explain and solve: {esc}">
</head>
<body>
  <h1>{esc}</h1>
  <p>If you're searching for <strong>{esc}</strong>, you're not alone.</p>
  <p>SideGuy explains the problem clearly before you spend money.</p>
  <p>Text PJ if you want help solving it.</p>
  <a href="sms:+17735441231" style="position:fixed;right:18px;bottom:18px;background:#21d3a1;color:#fff;padding:14px 18px;border-radius:999px;text-decoration:none;font-weight:bold">Text PJ</a>
</body>
</html>
""")


def run():
    if not os.path.exists(RADAR_FILE):
        print(f"[skip] Radar file not found: {RADAR_FILE}")
        return

    with open(RADAR_FILE) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for r in reader:
            topic = (r.get("topic") or "").strip()
            if topic:
                problems.append((topic, score_problem(topic)))

    problems.sort(key=lambda x: x[1], reverse=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LEADERBOARD), exist_ok=True)

    with open(LEADERBOARD, "w") as lb:
        lb.write("# SideGuy Problem Leaderboard\n\n")
        for topic, score in problems[:100]:
            lb.write(f"- {topic} | score {score}\n")
            create_page(topic)

    print(f"Problem Engine: {len(problems)} topics scored")
    print(f"Leaderboard: {LEADERBOARD}")


run()
