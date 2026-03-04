#!/usr/bin/env python3
# ==============================================================
# SIDEGUY BETTING LAB — Hedge Analysis
# Reads betting-lab/bet-log.csv and prints win rates by trigger.
# Usage: python3 betting-lab/hedge-summary.py
# ==============================================================

import csv, sys
from pathlib import Path
from collections import defaultdict

LOG_FILE = Path(__file__).parent / "bet-log.csv"

def summarize():
    if not LOG_FILE.exists():
        print("ERROR: bet-log.csv not found"); sys.exit(1)

    rows = []
    with open(LOG_FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("result","").strip():
                rows.append(row)

    if not rows:
        print("No completed bets logged yet.")
        print(f"Add bets to {LOG_FILE}")
        return

    total  = len(rows)
    wins   = sum(1 for r in rows if r["result"].lower() == "win")
    losses = sum(1 for r in rows if r["result"].lower() == "loss")
    pushes = total - wins - losses

    gross_pnl = 0.0
    for r in rows:
        try:
            size  = float(r.get("size", 0) or 0)
            price = float(r.get("price", 0) or 0)
            if r["result"].lower() == "win":
                gross_pnl += size * (1/price - 1) if price else size
            elif r["result"].lower() == "loss":
                gross_pnl -= size
        except (ValueError, ZeroDivisionError):
            pass

    # Per-trigger stats
    triggers = defaultdict(lambda: {"count": 0, "wins": 0, "pnl": 0.0})
    for r in rows:
        t = r.get("trigger","unknown") or "unknown"
        triggers[t]["count"] += 1
        if r["result"].lower() == "win":
            triggers[t]["wins"] += 1

    print()
    print("╔══════════════════════════════╗")
    print("║   SIDEGUY BETTING LAB        ║")
    print("╚══════════════════════════════╝")
    print(f"  Total bets : {total}")
    print(f"  Wins       : {wins}")
    print(f"  Losses     : {losses}")
    if pushes:
        print(f"  Pushes     : {pushes}")
    if total:
        print(f"  Win rate   : {wins/total*100:.1f}%")
    print(f"  Gross P&L  : {'+'if gross_pnl>=0 else ''}{gross_pnl:.2f} units")

    if triggers:
        print()
        print("  By trigger:")
        for t, v in sorted(triggers.items(), key=lambda x: -x[1]["wins"]):
            wr = v["wins"] / v["count"] * 100 if v["count"] else 0
            print(f"    {t:<28} {v['count']:>3} bets  {wr:5.1f}% win")

    print()

if __name__ == "__main__":
    summarize()
