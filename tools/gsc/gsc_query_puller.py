#!/usr/bin/env python3
"""
GSC Query Puller
Pulls top impression-winning queries from Google Search Console
and writes them to data/gsc-winners.json for the homepage card builder.

Usage:
  python3 tools/gsc/gsc_query_puller.py

Auth (pick one):
  1. Set GSC_SERVICE_ACCOUNT_JSON env var (GitHub Actions secret)
  2. Place credentials at credentials/gsc-service-account.json
  3. Set GSC_CREDENTIALS_FILE env var pointing to a JSON key file

Required env:
  GSC_SITE_URL — e.g. "sc-domain:sideguysolutions.com"
                  or "https://www.sideguysolutions.com/"
"""

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
DATA_FILE  = REPO_ROOT / "data" / "gsc-winners.json"
TOP_N      = 15   # how many winners to keep
DAYS_BACK  = 7    # rolling window

# ── Auth ────────────────────────────────────────────────────────────────────

def get_credentials():
    """Return google.oauth2 credentials from whichever source is available."""
    from google.oauth2 import service_account

    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

    # 1. Env var containing the JSON blob
    raw = os.environ.get("GSC_SERVICE_ACCOUNT_JSON")
    if raw:
        info = json.loads(raw)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

    # 2. Explicit file path via env
    path = os.environ.get("GSC_CREDENTIALS_FILE")
    if path and Path(path).exists():
        return service_account.Credentials.from_service_account_file(path, scopes=SCOPES)

    # 3. Default local file
    default = REPO_ROOT / "credentials" / "gsc-service-account.json"
    if default.exists():
        return service_account.Credentials.from_service_account_file(str(default), scopes=SCOPES)

    print("ERROR: No GSC credentials found. See header comment for setup.")
    sys.exit(1)


# ── Pull ────────────────────────────────────────────────────────────────────

def pull_winners():
    from googleapiclient.discovery import build

    site_url = os.environ.get("GSC_SITE_URL", "sc-domain:sideguysolutions.com")
    creds    = get_credentials()
    service  = build("searchconsole", "v1", credentials=creds)

    end   = date.today() - timedelta(days=2)   # GSC lags ~2 days
    start = end - timedelta(days=DAYS_BACK)

    body = {
        "startDate": str(start),
        "endDate":   str(end),
        "dimensions": ["query"],
        "rowLimit":   200,
        "orderBy":    [{"fieldName": "impressions", "sortOrder": "DESCENDING"}],
    }

    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    rows     = response.get("rows", [])

    winners = []
    for row in rows[:TOP_N]:
        query      = row["keys"][0]
        impressions = row.get("impressions", 0)
        clicks      = row.get("clicks", 0)
        ctr         = row.get("ctr", 0)
        position    = row.get("position", 0)

        winners.append({
            "query":       query,
            "impressions": int(impressions),
            "clicks":      int(clicks),
            "ctr":         round(ctr, 4),
            "position":    round(position, 1),
            "pulled_date": str(date.today()),
            "window_start": str(start),
            "window_end":   str(end),
        })

    return winners


# ── Page matching ────────────────────────────────────────────────────────────

def find_best_page(query: str) -> str:
    """Return the best matching page path for a query, or '#' if none found."""
    # Build slug from query
    slug = query.lower().strip()
    for ch in "',!?.()":
        slug = slug.replace(ch, "")
    slug = slug.replace(" ", "-").replace("--", "-")

    # Direct match
    exact = REPO_ROOT / f"{slug}.html"
    if exact.exists():
        return f"/{slug}.html"

    # Partial match — find page whose filename contains the most query words
    words = [w for w in slug.split("-") if len(w) > 3]
    if not words:
        return "#"

    candidates = list(REPO_ROOT.glob("*.html"))
    best_score = 0
    best_path  = "#"
    for p in candidates:
        name  = p.stem
        score = sum(1 for w in words if w in name)
        if score > best_score:
            best_score = score
            best_path  = f"/{p.name}"

    return best_path if best_score >= 2 else "#"


# ── Description templates ────────────────────────────────────────────────────

def make_description(query: str) -> str:
    q = query.lower()
    if " vs " in q:
        parts = q.split(" vs ")
        return f"The real comparison operators use to decide between {parts[0].strip()} and {parts[1].strip()}."
    if q.endswith("cost") or " cost " in q or "how much" in q:
        topic = q.replace("cost", "").replace("how much", "").replace("does", "").strip(" -")
        return f"What {topic} actually costs — before you commit or get a surprise invoice."
    if "ai chatbot" in q or "ai voice" in q or "ai scheduling" in q:
        return f"Which AI tools actually help — without breaking existing workflows or overpaying for features you won't use."
    if "ai consulting" in q or "ai business" in q or "ai solution" in q:
        return f"What a real AI engagement looks like vs. a vendor pitch dressed as one."
    if "inspection" in q:
        return f"What inspectors actually check vs. what ends up on the invoice — decoded before you book."
    if "san diego" in q:
        return f"Local clarity for San Diego operators navigating this exact situation right now."
    return f"Real clarity on {query.lower()} — no vendor spin, no weird portals."


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"Pulling GSC winners (last {DAYS_BACK} days)...")
    winners = pull_winners()
    print(f"Got {len(winners)} queries.")

    # Enrich with page + description
    for w in winners:
        w["page"]        = find_best_page(w["query"])
        w["description"] = make_description(w["query"])

    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(winners, indent=2))
    print(f"Saved to {DATA_FILE}")
    for w in winners:
        print(f"  [{w['impressions']:>5} impr]  {w['query']}  →  {w['page']}")


if __name__ == "__main__":
    main()
