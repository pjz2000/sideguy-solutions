#!/usr/bin/env python3
"""
SIDEGUY CONVERSION UPGRADE — Ship 027
Inject conversion elements into the 20 highest-intent pages.

Elements injected:
  1. Top banner — calm urgency, "Text PJ" CTA
  2. Mid-page trust block — before the help/CTA section
  3. Sticky floating SMS button — bottom-right

Approach:
  - Uses BeautifulSoup for safe HTML parsing (no fragile sed)
  - Adapts to both page structures (styled + main-wrapped)
  - Skips pages that already have conversion elements (idempotent)
  - No .bak files — git is the backup
"""

import os
import sys
from bs4 import BeautifulSoup, NavigableString

PROJECT_ROOT = "/workspaces/sideguy-solutions"
PUBLIC_DIR = os.path.join(PROJECT_ROOT, "public")

# ── 20 highest-intent pages (hand-picked) ──────────────────────────
TARGET_PAGES = [
    # ── Wave 1 (original 20) ──────────────────────────────────
    # Money pages — people actively deciding to spend
    "money-pages/cost-of-hvac-repair-san-diego.html",
    "money-pages/hvac-repair-or-replace.html",
    "money-pages/is-solar-worth-it-san-diego.html",
    "money-pages/best-solar-option-near-me.html",
    "money-pages/should-i-switch-payment-processor.html",
    "money-pages/tesla-vs-gas-cost-california.html",
    # Authority hubs — trust anchors
    "authority/hvac.html",
    "authority/solar.html",
    "authority/payments.html",
    "authority/tesla.html",
    "authority/ai.html",
    # Auto-pages — high-intent problem/solution
    "auto-pages/ac-repair-cost-san-diego.html",
    "auto-pages/hvac-repair-vs-replace-calculator.html",
    "auto-pages/hvac-not-cooling-san-diego-summer.html",
    "auto-pages/stripe-fee-increase-small-business.html",
    "auto-pages/stripe-vs-square-comparison.html",
    "auto-pages/water-heater-replacement-cost-san-diego.html",
    "auto-pages/electrical-panel-upgrade-cost-san-diego.html",
    "auto-pages/who-do-i-call-for-ac-not-cooling.html",
    "auto-pages/payment-processing-savings-calculator.html",
    "auto-pages/lower-credit-card-fees-small-business.html",

    # ── Wave 2: remaining auto-pages (high-intent) ────────────
    # Chargebacks & payment pain — urgent, costly problems
    "auto-pages/chargeback-prevention-software.html",
    "auto-pages/chargeback-win-rate-guide-for-merchants.html",
    "auto-pages/merchant-account-alternatives-to-stripe.html",
    "auto-pages/merchant-processing-hidden-fees.html",
    "auto-pages/stripe-chargeback-increase-2025.html",
    "auto-pages/sideguy-payments-consulting.html",
    # HVAC/home — people with broken stuff right now
    "auto-pages/heat-pump-freezing-up-at-night-san-diego.html",
    "auto-pages/hvac-heat-pump-incentives.html",
    "auto-pages/hvac-troubleshooting-decision-tree.html",
    "auto-pages/who-do-i-call-for-water-heater-leak.html",
    "auto-pages/who-do-i-call-checklist-san-diego.html",
    # EV/solar — high-ticket decisions
    "auto-pages/best-ev-home-charger-san-diego.html",
    "auto-pages/ev-charger-rebates-california.html",
    "auto-pages/ev-charging-installation-cost-san-diego.html",
    "auto-pages/sdge-ev-rate-plan-savings.html",
    "auto-pages/tesla-charging-slow-after-software-update.html",
    # AI automation — business owners evaluating spend
    "auto-pages/ai-receptionist-cost-comparison.html",
    "auto-pages/ai-receptionist-for-small-business.html",
    "auto-pages/ai-phone-answering-for-contractors.html",
    "auto-pages/ai-scheduling-for-hvac-companies.html",
    "auto-pages/ai-scheduling-for-plumbers.html",
    "auto-pages/ai-scheduling-for-dental-offices.html",
    "auto-pages/chatbot-for-local-business-cost.html",
    "auto-pages/ai-automation-for-dental-offices.html",
    "auto-pages/ai-automation-for-real-estate-agents.html",
    "auto-pages/quickbooks-vs-xero-san-diego.html",
    # Crypto/Solana payments — alternative payment seekers
    "auto-pages/crypto-payments-without-volatility.html",
    "auto-pages/solana-pay-for-merchants.html",
    "auto-pages/usdc-payments-for-service-businesses.html",

    # ── Wave 3: who-do-i-call pages (decision-mode visitors) ──
    "who-do-i-call.html",
    "who-do-i-call-about-ai-tools.html",
    "who-do-i-call-about-tech.html",
    "who-do-i-call-when-ai-breaks-my-workflow.html",
    "who-do-i-call-when-ai-confuses-me.html",
    "assist/dmv/who-do-i-call-no-dmv-appointment.html",
    "assist/hospital/who-do-i-call-er-wait-too-long.html",
    "assist/airport/who-do-i-call-missed-flight-san-diego.html",
    "assist/court/who-do-i-call-missed-court.html",
    "auto/who-do-i-call-for-payment-issues.html",
    "auto/who-do-i-call-for-website-help.html",
    "auto/who-do-i-call-for-ai-confusion.html",

    # ── Wave 4: root-level high-intent pages ───────────────────
    # HVAC/plumbing emergencies
    "hvac-repair-san-diego-san-diego.html",
    "hvac-troubleshooting-tips-san-diego.html",
    "plumbing-emergency-san-diego-san-diego.html",
    "plumbing-emergency-response-san-diego.html",
    "plumbing-advice-for-emergencies-san-diego.html",
    "electric-bill-keeps-climbing-and-im-losing-my-mind-san-diego.html",
    # Payments confusion
    "payment-processing-solutions-san-diego.html",
    "payments-confusion-help.html",
    # Industry-specific AI automation
    "ai-automation-hvac.html",
    "ai-automation-plumber.html",
    "ai-automation-contractor.html",
    "ai-automation-dentist.html",
    "ai-automation-restaurant.html",
    "ai-automation-real-estate.html",
    "ai-automation-for-contractors-san-diego.html",

    # ── Wave 5: auto/ San Diego verticals (1 per industry) ─────
    "auto/payment-processing-fees-too-high-hvac-san-diego.html",
    "auto/payment-processing-fees-too-high-contractors-san-diego.html",
    "auto/payment-processing-fees-too-high-dental-san-diego.html",
    "auto/payment-processing-fees-too-high-restaurants-san-diego.html",
    "auto/payment-processing-fees-too-high-plumbing-san-diego.html",
    "auto/payment-processing-fees-too-high-electricians-san-diego.html",
    "auto/payment-processing-fees-too-high-real-estate-san-diego.html",
    "auto/payment-processing-fees-too-high-salons-san-diego.html",
    "auto/ai-automation-replacing-staff-hvac-san-diego.html",
    "auto/ai-automation-replacing-staff-dental-san-diego.html",
    "auto/ai-automation-replacing-staff-restaurants-san-diego.html",
    "auto/ai-automation-replacing-staff-contractors-san-diego.html",
    "auto/ai-automation-for-restaurants.html",
]

SMS_NUMBER = "+17735441231"
SMS_PRETTY = "773-544-1231"
MARKER = "sideguy-conversion-upgrade"  # idempotency marker

# ── Conversion HTML blocks ──────────────────────────────────────────

TOP_BANNER = f"""
<!-- {MARKER}: top-banner -->
<div id="sg-top-banner" style="
  background: linear-gradient(90deg, #073044, #0f4c63);
  color: #eaf6ff;
  padding: 12px 16px;
  text-align: center;
  font-family: -apple-system, system-ui, Inter, sans-serif;
  font-size: 0.95rem;
  letter-spacing: 0.01em;
">
  Not sure what to do? A real human answers in minutes&nbsp;&rarr;&nbsp;
  <a href="sms:{SMS_NUMBER}" style="
    color: #21d3a1;
    font-weight: 600;
    text-decoration: none;
    border-bottom: 1px solid #21d3a180;
  ">Text PJ ({SMS_PRETTY})</a>
</div>
"""

TRUST_BLOCK = f"""
<!-- {MARKER}: trust-block -->
<div id="sg-trust-block" style="
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 12px;
  padding: 24px 20px;
  margin: 32px 0;
  font-family: -apple-system, system-ui, Inter, sans-serif;
  line-height: 1.6;
  color: #073044;
">
  <p style="font-size: 1.1rem; font-weight: 600; margin: 0 0 8px;">
    Not sure if you should fix, replace, or wait?
  </p>
  <p style="margin: 0 0 12px; color: #3f6173;">
    Most sites push you to buy. We don't. Text PJ &mdash; get a straight answer
    in minutes before you spend anything.
  </p>
  <a href="sms:{SMS_NUMBER}" style="
    display: inline-block;
    padding: 10px 18px;
    background: #10b981;
    color: white;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
  ">Text PJ Now</a>
</div>
"""

STICKY_BUTTON = f"""
<!-- {MARKER}: sticky-button -->
<div id="sg-sticky-cta" style="
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
">
  <a href="sms:{SMS_NUMBER}" style="
    display: flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    padding: 14px 20px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.95rem;
    text-decoration: none;
    box-shadow: 0 4px 24px rgba(16, 185, 129, 0.5);
    font-family: -apple-system, system-ui, Inter, sans-serif;
    transition: transform 0.2s, box-shadow 0.2s;
  " onmouseover="this.style.transform='scale(1.05)';this.style.boxShadow='0 6px 32px rgba(16,185,129,0.7)'"
    onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 4px 24px rgba(16,185,129,0.5)'"
  >&#x1F4AC; Text PJ</a>
</div>
"""


def already_upgraded(html_text: str) -> bool:
    return MARKER in html_text


def inject_conversion(filepath: str) -> bool:
    """Inject conversion elements into a single page. Returns True if modified."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    if already_upgraded(raw):
        print(f"  ⏭  Already upgraded: {os.path.basename(filepath)}")
        return False

    soup = BeautifulSoup(raw, "html.parser")

    body = soup.find("body")
    if not body:
        print(f"  ⚠  No <body> found: {os.path.basename(filepath)}")
        return False

    # ── 1. Top banner: insert as first child of <body> ──────────
    banner_soup = BeautifulSoup(TOP_BANNER, "html.parser")
    first_child = body.contents[0] if body.contents else None
    if first_child:
        first_child.insert_before(banner_soup)
    else:
        body.append(banner_soup)

    # ── 2. Trust block: insert before .sideguy-help or last <div>/<section> ──
    trust_soup = BeautifulSoup(TRUST_BLOCK, "html.parser")

    # Strategy: find the "Need Help" or CTA section and put trust block before it
    help_section = soup.find("section", class_="sideguy-help")
    if not help_section:
        # Try finding a div/section containing "Text PJ" or "Fastest Way"
        for tag in soup.find_all(["section", "div"]):
            text = tag.get_text(strip=True)
            if any(phrase in text for phrase in ["Need Help", "Fastest Way", "Text PJ directly"]):
                help_section = tag
                break

    if help_section:
        help_section.insert_before(trust_soup)
    else:
        # Fallback: insert before the interlinks block or last element in body
        interlinks = soup.find(string=lambda t: t and "sideguy-interlinks" in str(t))
        if interlinks:
            # Find the parent comment's next div
            parent = interlinks.find_parent()
            if parent:
                parent.insert_before(trust_soup)
            else:
                body.append(trust_soup)
        else:
            body.append(trust_soup)

    # ── 3. Sticky button: insert before </body> ────────────────
    # Remove any existing sticky CTA first (class="cta" fixed-position buttons)
    existing_sticky = soup.find("a", class_="cta")
    if existing_sticky:
        existing_sticky.decompose()

    sticky_soup = BeautifulSoup(STICKY_BUTTON, "html.parser")
    body.append(sticky_soup)

    # ── Write back ──────────────────────────────────────────────
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(soup))

    return True


def main():
    print("━" * 50)
    print("⚡ SIDEGUY CONVERSION UPGRADE — Ship 027")
    print("━" * 50)
    print()

    upgraded = 0
    skipped = 0
    errors = 0

    for rel_path in TARGET_PAGES:
        filepath = os.path.join(PUBLIC_DIR, rel_path)

        if not os.path.exists(filepath):
            print(f"  ✗  Missing: {rel_path}")
            errors += 1
            continue

        print(f"  → {rel_path}")
        try:
            if inject_conversion(filepath):
                upgraded += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ✗  Error: {e}")
            errors += 1

    print()
    print("━" * 50)
    print(f"  ✅ Upgraded: {upgraded}")
    print(f"  ⏭  Skipped:  {skipped}")
    print(f"  ✗  Errors:   {errors}")
    print("━" * 50)
    print()
    print("Conversion elements added:")
    print("  • Top banner (dark, calm urgency)")
    print("  • Trust block (green, decision support)")
    print("  • Sticky SMS button (floating, bottom-right)")
    print()
    print("Run again safely — idempotent (skips already-upgraded pages).")


if __name__ == "__main__":
    main()
