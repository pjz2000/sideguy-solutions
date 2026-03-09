from pathlib import Path

ROOT=Path("/workspaces/sideguy-solutions")

PILLARS=(ROOT/"docs/authority-engine/pillars.txt").read_text().splitlines()

OUT=ROOT/"docs/authority-engine/generated"

count=0

for pillar in PILLARS:

 pillar=pillar.strip()
 if not pillar:
  continue

 title=pillar.title()

 slug=pillar.replace(" ","-")

 content=f"# {title}\n\n"

 content+="## Overview\n\n"
 content+=f"{title} helps businesses reduce manual work, improve response times, and automate repetitive tasks using modern AI tools.\n\n"

 content+="## Common AI Automations\n\n"

 content+="- customer support chatbots\n"
 content+="- appointment scheduling automation\n"
 content+="- invoice processing automation\n"
 content+="- lead qualification bots\n"
 content+="- email response automation\n\n"

 content+="## Typical Implementation Cost\n\n"
 content+="$500 – $5000 depending on workflow complexity.\n\n"

 content+="## Typical Monthly Cost\n\n"
 content+="$50 – $300 depending on AI tools used.\n\n"

 content+="## Expected Savings\n\n"
 content+="Businesses often save 5–20 hours per week by automating repetitive tasks.\n\n"

 content+="## SideGuy Perspective\n\n"
 content+="AI automation should be evaluated based on real operational savings and workflow improvements.\n"

 file=OUT/f"{slug}.md"

 file.write_text(content)

 count+=1

print("Authority pages generated:",count)
