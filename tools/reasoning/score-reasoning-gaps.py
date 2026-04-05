#!/usr/bin/env python3
"""
SideGuy Reasoning Gap Scorer
Cross-references GSC winners with reasoning nodes.
Flags: monetization gaps, missing calculators, escalation holes, high-impr/no-cta pages.
"""
import csv
from pathlib import Path
from collections import defaultdict

SEEDS = Path("data/reasoning/reasoning-seeds.csv")
OUTPUT = Path("docs/reasoning/reasoning-gap-report.md")

def load_seeds():
    with open(SEEDS) as f:
        return list(csv.DictReader(f))

def score(seeds):
    # Group by source node
    by_source = defaultdict(list)
    for s in seeds:
        by_source[s["source"]].append(s)

    escalation_nodes  = [s for s in seeds if s["relationship"] == "escalates_to"]
    calculator_nodes  = [s for s in seeds if s["node_type"] == "calculator"]
    monetize_nodes    = [s for s in seeds if s["relationship"] == "monetizes_with"]
    high_impr_no_cta  = [s for s in seeds if int(s.get("gsc_impr", 0)) >= 20 and s["target"] != "text-pj-orb"]
    pos_crack         = [s for s in seeds if 0 < float(s.get("gsc_pos", 0)) <= 15 and int(s.get("gsc_impr", 0)) >= 10]

    lines = []
    lines.append("# SideGuy Reasoning Gap Report\n")
    lines.append(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    lines.append(f"Total seeds: {len(seeds)}  |  Unique source nodes: {len(by_source)}\n")

    lines.append("\n## 🔴 High-Impression Pages Without Direct Escalation\n")
    lines.append("These pages have GSC volume but no text-pj-orb edge — conversion gap.\n")
    for s in high_impr_no_cta:
        impr = s.get("gsc_impr", "0")
        pos  = s.get("gsc_pos", "?")
        lines.append(f"- **{s['source']}** → `{s['target']}` ({s['relationship']}) | {impr} impr, pos {pos} | {s['page_url']}")

    lines.append("\n\n## 🟡 Page-1 Crack Zone (pos ≤15, ≥10 impr)\n")
    lines.append("Closest to earning clicks — prioritize CTR surgery here.\n")
    seen = set()
    for s in sorted(pos_crack, key=lambda x: float(x.get("gsc_pos", 99))):
        if s["source"] not in seen:
            seen.add(s["source"])
            lines.append(f"- **{s['source']}** | pos {s['gsc_pos']}, {s['gsc_impr']} impr | {s['page_url']}")

    lines.append("\n\n## 🟢 Active Escalation Paths (source → text-pj-orb)\n")
    for s in sorted(escalation_nodes, key=lambda x: -int(x.get("gsc_impr", 0))):
        flag = " 🔥" if int(s.get("gsc_impr", 0)) >= 30 else ""
        lines.append(f"- {s['source']}{flag} | {s['gsc_impr']} impr, pos {s['gsc_pos']} | {s['page_url']}")

    lines.append("\n\n## 🔵 Calculator Opportunities\n")
    lines.append("Every `compares` or `fee-calculator` edge is a tool opportunity.\n")
    for s in calculator_nodes:
        lines.append(f"- **{s['source']}** → `{s['target']}` | pos {s['gsc_pos']}, {s['gsc_impr']} impr | {s['page_url']}")

    lines.append("\n\n## 💰 Monetization Edges\n")
    for s in monetize_nodes:
        lines.append(f"- {s['source']} → {s['target']} ({s['relationship']}) | priority {s['priority']} | {s['page_url']}")

    lines.append("\n\n## ⚡ Recommended Next Builds\n")
    lines.append("Based on gap analysis:\n")
    lines.append("1. **Stripe fee calculator** — `stripe-fees` at pos 4, 33 impr, no interactive tool")
    lines.append("2. **HVAC repair vs replace calculator** — priority 10, no page yet")
    lines.append("3. **Twilio escalation hook** — 188 impr, needs stronger Text PJ CTA above fold")
    lines.append("4. **Compliance SOC2 comparison tool** — 44 impr, pos 11, calculator would convert")
    lines.append("5. **Stripe vs Square fee calculator** — 92 impr at pos 75, tool would earn links")

    return "\n".join(lines) + "\n"

if __name__ == "__main__":
    seeds = load_seeds()
    report = score(seeds)
    OUTPUT.write_text(report)
    print(f"Gap report written → {OUTPUT}")
    print(f"Seeds: {len(seeds)} | Top recommendation: Stripe fee calculator")
