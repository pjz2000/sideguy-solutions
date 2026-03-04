#!/usr/bin/env python3
# ==============================================================
# SIDEGUY OPERATOR BRAIN
# Problem → Knowledge Router
# ==============================================================
# Matches a plain-English operator query to the best SideGuy
# pages using keyword scoring (no ML required).
#
# Usage (interactive):  python3 brain/router.py
# Usage (import):
#   from brain.router import route_problem
#   pages = route_problem("stripe payout stuck")
#
# Data file: data/problem-map.json
# ==============================================================

import json, os, re
from pathlib import Path

ROOT      = Path(__file__).parent.parent
MAP_PATH  = ROOT / "data" / "problem-map.json"
DOMAIN    = "https://sideguysolutions.com"

# ── Load routes ───────────────────────────────────────────────

def _load_routes() -> dict:
    with MAP_PATH.open() as f:
        return json.load(f)

_ROUTES = _load_routes()

# ── Routing logic ─────────────────────────────────────────────

def route_problem(query: str) -> dict:
    """
    Match query to the most relevant problem-map entry.

    Returns a dict:
      {
        "matched_key":  str | None,
        "summary":      str | None,
        "pages":        list[str],   # full URLs
      }
    """
    q = query.lower().strip()
    q = re.sub(r"[^a-z0-9\s]", " ", q)

    best_key   = None
    best_score = 0

    for key in _ROUTES:
        # Score = number of key tokens found in query
        key_tokens = key.lower().split()
        score = sum(1 for t in key_tokens if t in q)
        # Exact substring match is a strong bonus
        if key.lower() in q:
            score += len(key_tokens)
        if score > best_score:
            best_score = score
            best_key   = key

    if best_key and best_score > 0:
        entry   = _ROUTES[best_key]
        pages   = entry.get("pages", [])
        summary = entry.get("summary")
        full_urls = [
            p if p.startswith("http") else f"{DOMAIN}{p}"
            for p in pages
        ]
        return {"matched_key": best_key, "summary": summary, "pages": full_urls}

    # Fallback: send to homepage + knowledge hub
    return {
        "matched_key": None,
        "summary": None,
        "pages": [DOMAIN + "/", DOMAIN + "/knowledge-hub.html"],
    }


def reload_routes():
    """Reload the problem-map.json without restarting the process."""
    global _ROUTES
    _ROUTES = _load_routes()
    print(f"  Reloaded {len(_ROUTES)} routes from {MAP_PATH}")


# ── CLI ───────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 54)
    print("  SideGuy Operator Brain — Problem Router")
    print(f"  {len(_ROUTES)} routes loaded")
    print("  Type 'quit' or Ctrl-C to exit")
    print("=" * 54)

    while True:
        try:
            q = input("\nProblem: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nbye")
            break

        if q.lower() in ("quit", "exit", "q", ""):
            break

        result = route_problem(q)

        print()
        if result["matched_key"]:
            print(f"  Matched: \"{result['matched_key']}\"")
        else:
            print("  No direct match — showing general navigation")

        if result["summary"]:
            print(f"\n  Quick answer: {result['summary']}")

        print("\n  Best SideGuy pages:\n")
        for p in result["pages"]:
            print(f"    {p}")
