#!/usr/bin/env python3
"""
Signal Scanner — SideGuy Solutions
====================================
Stores curated external search signals (keywords / queries worth tracking)
and converts NEW ones to gravity page slugs for the builder.

Idempotent: signals already recorded in external_signals.txt are never
duplicated. Only first-seen signals get appended to the gravity queue.

To add more signals: extend the SIGNALS list and re-run.
"""
import datetime, re
from pathlib import Path

ROOT    = Path("/workspaces/sideguy-solutions")
OUT_DIR = ROOT / "docs" / "signal-scanner"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SIGNALS_FILE = OUT_DIR / "external_signals.txt"
GRAVITY      = ROOT / "docs" / "problem-gravity" / "gravity_pages.txt"

# ── Signal library ────────────────────────────────────────────────────────────
SIGNALS = [
    "why stripe fees are high",
    "how businesses lower payment processing fees",
    "ai automation for hvac dispatch",
    "best ai tools for contractors",
    "restaurant reservation automation tools",
    "ai chatbot for dentists",
    "how to automate appointment reminders",
    "ai lead followup system",
    "how to reduce no shows with sms reminders",
    "automation for small service businesses",
    "how to automate invoice reminders",
    "ai scheduling for salons",
    "ai followup for medical clinics",
    "how to automate review requests",
    "ai chatbot for law firms",
    "best ai tools for real estate",
    "how to automate client intake",
    "ai for missed call recovery",
    "how to automate bid followup",
    "ai for after-hours lead capture",
    "how to automate seasonal outreach",
    "ai for emergency dispatch",
    "how to automate payment reconciliation",
    "ai for appointment confirmation",
    "how to automate loyalty outreach",
    "ai for technician dispatch",
    "how to automate offer followup",
    "ai for patient reactivation",
    "how to automate repair status updates",
    "ai for service reminder automation",
    "how to automate client check-ins",
    "funniest ai office memes",
    "best ai meme generators",
    "ai for office productivity",
    "how to automate office tasks",
    "ai for meeting scheduling",
    "ai for email triage",
    "ai for document summarization",
    "how to automate HR onboarding",
    "ai for payroll automation",
    "ai for compliance tracking",
    "how to automate expense reports",
    "ai for team collaboration",
    "ai for project management",
    "how to automate office reminders",
    "ai for office birthday memes",
    "how to automate meme content for business",
    "ai for office watercooler jokes",
    "how to automate office newsletter memes",
    "ai for office holiday memes",
    "how to automate meme distribution in Slack",
]


def _to_slug(signal: str) -> str:
    """Convert a natural-language signal to a URL-safe slug."""
    slug = signal.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = slug.strip("-")
    return slug + "-san-diego"


def run():
    ts = datetime.datetime.now(datetime.UTC).isoformat()

    # Load already-recorded signals (strip timestamps to get plain text)
    existing_signals: set[str] = set()
    if SIGNALS_FILE.exists():
        for line in SIGNALS_FILE.read_text().splitlines():
            parts = line.split("\t", 1)
            if len(parts) == 2:
                existing_signals.add(parts[1].strip().lower())

    # Load gravity queue to avoid duplicate slugs
    existing_slugs: set[str] = set()
    if GRAVITY.exists():
        for line in GRAVITY.read_text().splitlines():
            existing_slugs.add(line.strip().lower())

    new_signals: list[str] = []
    new_slugs:   list[str] = []

    for signal in SIGNALS:
        key  = signal.lower().strip()
        slug = _to_slug(signal)

        if key not in existing_signals:
            new_signals.append(f"{ts}\t{signal}")
            existing_signals.add(key)

        if slug not in existing_slugs:
            new_slugs.append(slug)
            existing_slugs.add(slug)

    # Write new signals to log
    if new_signals:
        with open(SIGNALS_FILE, "a") as f:
            f.write("\n".join(new_signals) + "\n")
        print(f"Signal scanner: {len(new_signals)} new signals logged → {SIGNALS_FILE.name}")
    else:
        print("Signal scanner: all signals already recorded — no new entries")

    # Append new slugs to gravity queue
    if new_slugs:
        with open(GRAVITY, "a") as f:
            f.write("\n".join(new_slugs) + "\n")
        print(f"Signal scanner: {len(new_slugs)} new slugs → gravity queue")
    else:
        print("Signal scanner: all slugs already in gravity queue")


if __name__ == "__main__":
    run()
