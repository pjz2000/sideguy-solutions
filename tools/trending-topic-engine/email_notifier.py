#!/usr/bin/env python3
"""
Email Notifier — SideGuy Solutions
=================================
Sends an email alert to peter.z@kromeon.com whenever new pages are built and committed.
Requires SMTP credentials for production use.
"""
from pathlib import Path
import smtplib
from email.mime.text import MIMEText

RECIPIENT = 'peter.z@kromeon.com'
SENDER = 'sideguy-alerts@yourdomain.com'
SMTP_SERVER = 'smtp.yourdomain.com'
SMTP_PORT = 587
SMTP_USER = 'sideguy-alerts@yourdomain.com'
SMTP_PASS = 'YOUR_SMTP_PASSWORD'

LOG = Path("/workspaces/sideguy-solutions/docs/trending-topic-engine/realtime_pages.txt")
if LOG.exists():
    pages = LOG.read_text()
else:
    pages = 'No new pages.'

msg = MIMEText(f"New pages built:\n\n{pages}")
msg['Subject'] = 'SideGuy Solutions: New Pages Built'
msg['From'] = SENDER
msg['To'] = RECIPIENT

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
    print("Email alert sent.")
except Exception as e:
    print(f"Email failed: {e}")
