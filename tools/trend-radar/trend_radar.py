import datetime,os

topics=[
"AI receptionist for small business",
"AI hiring assistants",
"AI automation for contractors",
"AI automation for real estate",
"crypto payment rails for business",
"AI accounting automation",
"robot warehouse automation",
"AI SEO automation tools",
"autonomous trucking logistics",
"Solana merchant payment systems"
]

os.makedirs("docs/trend-signals",exist_ok=True)

out="docs/trend-signals/trend-signals.tsv"

with open(out,"a") as f:
    for t in topics:
        f.write(f"{datetime.datetime.utcnow().isoformat()}\t{t}\n")

print("Trend radar signals written")
