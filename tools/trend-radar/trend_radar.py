import datetime
import os

topics = [
"AI receptionist for small business",
"AI hiring assistants",
"autonomous energy systems",
"virtual power plant payments",
"robotaxis insurance",
"AI compliance tools",
"AI automation for local services",
"crypto payment rails for business",
"AI accounting automation",
"AI call center replacement",
"AI automation for contractors",
"AI automation for real estate",
"machine to machine payments infrastructure",
"Solana merchant payment systems",
"AI SEO automation tools",
"agentic workflow software",
"AI help desk automation",
"AI cybersecurity monitoring",
"autonomous trucking logistics",
"robot warehouse automation"
]

out = "docs/trend-signals/trend-signals.tsv"
os.makedirs("docs/trend-signals", exist_ok=True)

with open(out, "a") as f:
    for t in topics:
        f.write(f"{datetime.datetime.utcnow().isoformat()}\t{t}\n")

print("Trend radar signals written to", out)
