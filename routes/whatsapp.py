import os
import requests
from flask import Blueprint, request, jsonify
from services.gemini import generate_text

whatsapp_bp = Blueprint("whatsapp", __name__)

@whatsapp_bp.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == os.getenv("WHATSAPP_VERIFY_TOKEN"):
            return challenge, 200
        return "Forbidden", 403

    data = request.get_json()
    if data and data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    message = value["messages"][0]
                    sender = message["from"]
                    text = message["text"]["body"]

                    ai_result = generate_text(text, "gemini-3.5-flash-lite")

                    if ai_result.get("ok"):
                        access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
                        phone_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
                        url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
                        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
                        payload = {
                            "messaging_product": "whatsapp",
                            "to": sender,
                            "type": "text",
                            "text": {"body": ai_result["text"]}
                        }
                        requests.post(url, json=payload, headers=headers)
        return "OK", 200
    return "Not Found", 404
