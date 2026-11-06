import requests
import os
from flask import Blueprint, request

whatsapp_bp = Blueprint('whatsapp', __name__)
VERIFY_TOKEN = "agha_ai_secret_123"

# یہ لائنز Render کے Environment Variables سے چابیاں پڑھیں گی
ACCESS_TOKEN = os.environ.get("WHATSAPP_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_ID", "YOUR_PHONE_NUMBER_ID_HERE")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

@whatsapp_bp.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        return 'Error', 403
        
    elif request.method == 'POST':
        data = request.get_json()
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            if 'messages' in value:
                message = value['messages'][0]
                from_number = message['from']
                
                if 'text' in message:
                    text = message['text']['body']
                    ai_reply = get_ai_response(text)
                    send_whatsapp_message(from_number, ai_reply)
        except Exception as e:
            print(f"Webhook Error: {e}")
        return 'OK', 200

def get_ai_response(user_message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": user_message}]}]}
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "Sorry, main is waqt jawab nahi de sakta. Please try again."

def send_whatsapp_message(to_number, message_text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    requests.post(url, headers=headers, json=data)
