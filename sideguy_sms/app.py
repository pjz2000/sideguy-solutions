import os
from pathlib import Path
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

app = Flask(__name__)

LOG_DIR = Path("logs/twilio")
LOG_DIR.mkdir(parents=True, exist_ok=True)

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")
PJ_PHONE_NUMBER = os.getenv("PJ_PHONE_NUMBER", "")

client = Client(ACCOUNT_SID, AUTH_TOKEN) if ACCOUNT_SID and AUTH_TOKEN else None

def classify_intent(text: str) -> str:
    t = (text or "").lower()

    if any(x in t for x in ["cost", "price", "quote", "expensive", "fee", "fees"]):
        return "pricing"
    if any(x in t for x in ["best", "vs", "compare", "option", "options"]):
        return "decision"
    if any(x in t for x in ["broken", "not working", "issue", "problem", "help", "urgent", "asap"]):
        return "problem"
    if any(x in t for x in ["hvac", "ac", "air conditioning", "furnace"]):
        return "hvac"
    if any(x in t for x in ["solar", "battery", "ev", "charger", "tesla"]):
        return "energy"
    if any(x in t for x in ["stripe", "payments", "payment", "processor", "merchant"]):
        return "payments"
    if any(x in t for x in ["ai", "automation", "agent", "workflow"]):
        return "ai"

    return "general"

def build_response(intent: str) -> str:
    responses = {
        "pricing": "Got it — pricing can vary a lot depending on scope, equipment, and markup. Send the quote or details and I'll help sanity check it.",
        "decision": "Good question — this usually comes down to your exact setup and goals. I can help you compare the cleanest next step.",
        "problem": "That sounds frustrating — usually there's a root cause that isn't obvious at first. Send a little more detail and I'll help narrow it down.",
        "hvac": "HVAC quotes and repair-vs-replace calls can vary a lot. If you send the quote or symptoms, I can give you a second opinion.",
        "energy": "EV, battery, and solar decisions depend a lot on usage, rates, and install setup. I can help simplify it.",
        "payments": "Payments setups and processor fees can get confusing fast. If you send what you're seeing, I can help break it down.",
        "ai": "AI and automation can be useful, but the right setup depends on the workflow. Tell me what you're trying to solve.",
        "general": "Happy to help — tell me what you're trying to figure out, and I'll point you in the right direction."
    }
    return f"{responses.get(intent, responses['general'])} Text PJ anytime at 773-544-1231."

def should_escalate(text: str) -> bool:
    t = (text or "").lower()
    triggers = ["urgent", "asap", "expensive", "quote", "help", "broken", "not working", "contract", "today"]
    return any(x in t for x in triggers)

def log_line(filename: str, line: str) -> None:
    with open(LOG_DIR / filename, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def alert_pj(from_number: str, body: str, intent: str) -> None:
    if not client or not TWILIO_PHONE_NUMBER or not PJ_PHONE_NUMBER:
        return
    msg = f"SideGuy escalation\nFrom: {from_number}\nIntent: {intent}\nMessage: {body}"
    try:
        client.messages.create(
            from_=TWILIO_PHONE_NUMBER,
            to=PJ_PHONE_NUMBER,
            body=msg
        )
    except Exception as e:
        log_line("errors.log", f"PJ alert failed | {e}")

@app.route("/health", methods=["GET"])
def health():
    return {"ok": True}

@app.route("/sms/incoming", methods=["POST"])
def sms_incoming():
    from_number = request.form.get("From", "")
    body = request.form.get("Body", "").strip()

    intent = classify_intent(body)
    reply = build_response(intent)

    log_line("inbox.log", f"{from_number} | {intent} | {body}")

    if should_escalate(body):
        alert_pj(from_number, body, intent)
        log_line("escalations.log", f"{from_number} | {intent} | {body}")

    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml), 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
