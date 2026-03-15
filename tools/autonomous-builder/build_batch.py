from pathlib import Path
import sys
from datetime import datetime

ROOT = Path("/workspaces/sideguy-solutions")
PUBLIC = ROOT / "public" / "auto"
LOG_DIR = ROOT / "docs" / "autonomous-builder" / "logs"
STATE = ROOT / "docs" / "autonomous-builder" / "state" / "built-pages.txt"

if len(sys.argv) < 2:
    print("Usage: python3 tools/autonomous-builder/build_batch.py docs/autonomous-builder/queues/batch-0001.tsv")
    raise SystemExit(1)

batch_file = Path(sys.argv[1])
if not batch_file.exists():
    print(f"Missing batch file: {batch_file}")
    raise SystemExit(1)

PUBLIC.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
STATE.parent.mkdir(parents=True, exist_ok=True)
if not STATE.exists():
    STATE.write_text("", encoding="utf-8")

built = set(x.strip() for x in STATE.read_text(encoding="utf-8").splitlines() if x.strip())

ts = datetime.utcnow().isoformat() + "Z"
created = 0
skipped = 0
log_path = LOG_DIR / f"{batch_file.stem}-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.log"

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{h1}. Human-first clarity from SideGuy Solutions.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/auto/{slug}">
</head>
<body>
  <main style="max-width:980px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.7;">
    <p><a href="/index.html">&larr; Back to Home</a></p>

    <h1>{h1}</h1>

    <p>
      SideGuy explains {topic_text} for {industry_text} teams in {location_text}
      so people can evaluate tools, costs, risks, and implementation without wasting time or money.
    </p>

    <h2>What this page covers</h2>
    <p>
      This page focuses on the <strong>{modifier_text}</strong> angle, which usually means clearer buying intent,
      stronger operational questions, and more practical decision-making.
    </p>

    <h2>How businesses usually think about this</h2>
    <ul>
      <li>What does it actually do?</li>
      <li>How hard is it to implement?</li>
      <li>What does it cost?</li>
      <li>What are the risks and tradeoffs?</li>
    </ul>

    <h2>Why this matters</h2>
    <p>
      Most teams are not looking for hype. They are looking for clarity, fit, timing, and whether the system solves
      a real operational problem.
    </p>

    <h2>Related SideGuy topics</h2>
    <ul>
      <li><a href="/machine-to-machine-payments.html">Machine-to-Machine Payments</a></li>
      <li><a href="/ai-agent-for-small-business.html">AI Agent for Small Business</a></li>
      <li><a href="/what-is-an-ai-operator.html">What Is an AI Operator?</a></li>
      <li><a href="/why-credit-card-processing-fees-are-so-high.html">Why Credit Card Processing Fees Are So High</a></li>
    </ul>

    <div style="margin-top:48px;padding:22px;border:1px solid #ddd;border-radius:20px;">
      <strong>Text PJ</strong>
      <p>Want a real human to help sort through it?</p>
      <p><a href="sms:+17735441231">Text PJ: 773-544-1231</a></p>
    </div>

    <p style="margin-top:28px;color:#666;font-size:14px;">Build timestamp: {ts}</p>
  </main>
</body>
</html>
"""

with open(batch_file, "r", encoding="utf-8") as f:
    header = next(f)
    rows = [line.rstrip("\n").split("\t") for line in f if line.strip()]

with open(log_path, "w", encoding="utf-8") as log:
    for topic, modifier, location, industry, slug, title, h1 in rows:
        out = PUBLIC / slug

        if slug in built or out.exists():
            skipped += 1
            log.write(f"SKIP\t{slug}\n")
            continue

        html = template.format(
            title=title,
            h1=h1,
            slug=slug,
            topic_text=topic.replace("-", " "),
            modifier_text=modifier.replace("-", " "),
            location_text=location.replace("-", " ").title(),
            industry_text=industry.replace("-", " "),
            ts=ts
        )

        out.write_text(html, encoding="utf-8")
        created += 1
        built.add(slug)
        log.write(f"CREATE\t{slug}\n")

STATE.write_text("\n".join(sorted(built)) + "\n", encoding="utf-8")

print(f"Batch: {batch_file}")
print(f"Created: {created}")
print(f"Skipped: {skipped}")
print(f"Log: {log_path}")
