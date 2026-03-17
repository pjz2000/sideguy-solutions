# SideGuy Real Texting

Recommended stack:

Twilio phone number or Messaging Service
→ incoming webhook
→ SideGuy responder
→ optional PJ escalation

What Twilio needs:

1. Twilio account
2. SMS-capable sender
3. Webhook URL for incoming messages
4. Environment variables:
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - TWILIO_PHONE_NUMBER
   - PJ_PHONE_NUMBER

Compliance note:
If you use a US 10DLC number to message US recipients from an application, register for A2P 10DLC.
Toll-free numbers are a separate sender path.

Run locally:

python3 -m venv .venv
source .venv/bin/activate
pip install flask twilio python-dotenv
python3 sideguy_sms/app.py

Then expose locally with your preferred tunnel and paste the public URL into the Twilio inbound webhook.

Webhook path:
/sms/incoming
