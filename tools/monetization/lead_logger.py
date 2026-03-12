import datetime

LOG = "data/leads/leads.tsv"

def log_lead(page, category):
    with open(LOG, "a") as f:
        f.write(
            page + "\t" +
            category + "\t" +
            datetime.datetime.utcnow().isoformat() + "\n"
        )

print("Lead logger ready")
