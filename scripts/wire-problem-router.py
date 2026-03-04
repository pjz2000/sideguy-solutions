#!/usr/bin/env python3
# ==============================================================
# SIDEGUY ROUTER ENGINE v3
# Adds "Best Next Pages" pills to every problems/*.html
# Routes by keyword → Concepts / Pillars / Hubs
# SAFE: only edits problems/ (no 15k bulk)
# Idempotent via <!-- ROUTER_START/END --> markers.
# ==============================================================

import os, re

PROBLEMS_DIR = "problems"
MARKER_S     = "<!-- ROUTER_START -->"
MARKER_E     = "<!-- ROUTER_END -->"

# ── Core hubs (always included) ──────────────────────────────
HUBS = [
    ("Knowledge Hub",    "/knowledge-hub.html"),
    ("Problem Library",  "/problems/"),
    ("Concept Library",  "/concepts/index.html"),
]

# ── Pillar pages — checked for existence ─────────────────────
PILLAR_CANDIDATES = [
    ("Payments Hub",           "payments-infrastructure-hub.html",  "/payments-infrastructure-hub.html"),
    ("AI Automation Hub",      "ai-automation-hub.html",             "/ai-automation-hub.html"),
    ("Operator Tools Hub",     "operator-tools-hub.html",            "/operator-tools-hub.html"),
    ("Payments",               "payments.html",                      "/payments.html"),
]

# ── Concepts — only include if file exists ────────────────────
CONCEPT_CANDIDATES = [
    ("AI Automation",      "concepts/ai-automation.html",         "/concepts/ai-automation.html"),
    ("Prediction Markets", "concepts/prediction-markets.html",    "/concepts/prediction-markets.html"),
    ("Crypto Payments",    "concepts/crypto-payments.html",       "/concepts/crypto-payments.html"),
    ("Payment Processing", "concepts/payment-processing.html",    "/concepts/payment-processing.html"),
    ("AI Agents",          "concepts/ai-agents.html",             "/concepts/ai-agents.html"),
    ("Chargebacks",        "concepts/chargebacks.html",           "/concepts/chargebacks.html"),
    ("Interchange Fees",   "concepts/interchange-fees.html",      "/concepts/interchange-fees.html"),
    ("Merchant Fees",      "concepts/merchant-fees.html",         "/concepts/merchant-fees.html"),
    ("CRM Automation",     "concepts/crm-automation.html",        "/concepts/crm-automation.html"),
    ("Invoice Automation", "concepts/invoice-automation.html",    "/concepts/invoice-automation.html"),
    ("Stablecoin Payments","concepts/stablecoin-payments.html",   "/concepts/stablecoin-payments.html"),
    ("Solana Payments",    "concepts/solana-payments.html",       "/concepts/solana-payments.html"),
    ("Polymarket Trading", "concepts/polymarket-trading.html",    "/concepts/polymarket-trading.html"),
    ("Kalshi Trading",     "concepts/kalshi-trading.html",        "/concepts/kalshi-trading.html"),
]

# ── Keyword routing: (token list, [(title, href), ...]) ──────
RULES = [
    # Payments
    (["payment","fee","fees","interchange","processor","processing",
      "chargeback","fraud","pci","settlement","markup","stripe","square"], [
        ("Payments Hub",              "/payments-infrastructure-hub.html"),
        ("Payment Processing",        "/concepts/payment-processing.html"),
        ("Chargebacks",               "/concepts/chargebacks.html"),
        ("Interchange Fees",          "/concepts/interchange-fees.html"),
        ("Merchant Fees",             "/concepts/merchant-fees.html"),
    ]),
    # Customer ops
    (["missed","call","calls","review","reply","text","sms","follow","lead","support","intake"], [
        ("AI Automation Hub",         "/ai-automation-hub.html"),
        ("Operator Tools Hub",        "/operator-tools-hub.html"),
    ]),
    # Systems / automation
    (["schedule","scheduling","booking","appointment","crm","invoic",
      "workflow","sop","process","automation","system","dashboard"], [
        ("AI Automation Hub",         "/ai-automation-hub.html"),
        ("CRM Automation",            "/concepts/crm-automation.html"),
        ("Invoice Automation",        "/concepts/invoice-automation.html"),
        ("Operator Tools Hub",        "/operator-tools-hub.html"),
    ]),
    # AI / agents
    (["ai","agent","agents","gpt","bot","copilot","machine","learning"], [
        ("AI Automation Hub",         "/ai-automation-hub.html"),
        ("AI Agents",                 "/concepts/ai-agents.html"),
        ("AI Automation",             "/concepts/ai-automation.html"),
    ]),
    # Crypto
    (["crypto","wallet","stablecoin","stablecoins","solana","token","blockchain"], [
        ("Stablecoin Payments",       "/concepts/stablecoin-payments.html"),
        ("Solana Payments",           "/concepts/solana-payments.html"),
        ("Crypto Payments",           "/concepts/crypto-payments.html"),
        ("Payments Hub",              "/payments-infrastructure-hub.html"),
    ]),
    # Prediction markets
    (["prediction","kalshi","polymarket","market","markets","bet","hedge","hedging"], [
        ("Kalshi Trading",            "/concepts/kalshi-trading.html"),
        ("Polymarket Trading",        "/concepts/polymarket-trading.html"),
        ("Prediction Markets",        "/concepts/prediction-markets.html"),
    ]),
]

def build_pills(slug: str) -> str:
    links = list(HUBS)  # always start with hubs

    for _, fs_path, href in PILLAR_CANDIDATES:
        if os.path.exists(fs_path):
            links.append((_, href))

    for title, fs_path, href in CONCEPT_CANDIDATES:
        if os.path.exists(fs_path):
            links.append((title, href))

    s = slug.lower()
    for keys, dests in RULES:
        if any(k in s for k in keys):
            for title, href in dests:
                if href.startswith("/concepts/"):
                    if not os.path.exists(href.lstrip("/")):
                        continue
                links.append((title, href))

    # de-dupe preserving order, limit to 10
    seen, uniq = set(), []
    for t, h in links:
        k = (t, h)
        if k not in seen:
            seen.add(k)
            uniq.append((t, h))

    pills = "\n".join(
        f'    <a href="{h}" style="display:inline-block;border:1px solid #d7f5ff;'
        f'border-radius:999px;padding:8px 14px;text-decoration:none;color:#073044;'
        f'font-size:.84rem;font-weight:500;background:rgba(255,255,255,.8)">{t}</a>'
        for t, h in uniq[:10]
    )
    return pills

def inject_router(html: str, slug: str) -> str:
    block = build_pills(slug)
    section = (
        '\n<section style="margin-top:18px;padding-top:14px;border-top:2px solid #d7f5ff">'
        '\n  <h2 style="font-size:1.1rem;font-weight:800;margin-bottom:10px">Best Next Pages</h2>'
        '\n  <div style="display:flex;flex-wrap:wrap;gap:8px">'
        f'\n{MARKER_S}\n{block}\n{MARKER_E}'
        '\n  </div>'
        '\n</section>'
    )
    if MARKER_S in html and MARKER_E in html:
        return re.sub(
            re.escape(MARKER_S) + r".*?" + re.escape(MARKER_E),
            f"{MARKER_S}\n{block}\n{MARKER_E}",
            html, flags=re.S
        )
    anchor = "</main>" if "</main>" in html else "</body>"
    return html.replace(anchor, section + "\n" + anchor, 1)

if __name__ == "__main__":
    print("=== Problem Router Engine v3 ===\n")

    if not os.path.isdir(PROBLEMS_DIR):
        print("ERROR: problems/ dir not found"); exit(1)

    changed = 0
    for fn in sorted(os.listdir(PROBLEMS_DIR)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        path = os.path.join(PROBLEMS_DIR, fn)
        html = open(path, "r", encoding="utf-8", errors="ignore").read()
        new  = inject_router(html, fn.replace(".html",""))
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1

    print(f"  Router wired on {changed} pages")
