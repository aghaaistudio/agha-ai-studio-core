import os
import requests
from flask import Blueprint, request, jsonify

whatsapp_bp = Blueprint('whatsapp', __name__)
VERIFY_TOKEN = "agha_ai_secret_123"

# ان پلیس ہولڈرز کو ہم اگلے سٹیپ میں اپڈیٹ کریں گے
ACCESS_TOKEN = "EAAUwtBGpxSEBSxbmRLAUZBmvyTqHqd1Jy5MtQ5ZAXjTwqGj1lqfSMmZATBpMHXidHr1IQaoCw7sT6e2XMId4IzD5d9AI2BTvjNZBBsWFRAMtuMkFdYO5eh7GXZAYGkdu6NNjFkggFrXstZClaA1KVgmjgYydqCAEgg59BNPokgz5v83r7yOOyCotlYT2IJg9eMMAFywMvC2xiT8eDeWvxEPZBb9jtKTRy79cyHz"
PHONE_NUMBER_ID = "1460469257157697"

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
                text = message['text']['body']
                
                # یہاں ہم آپ کے AI سسٹم کو کال کریں گے (فلحال ایک ٹیسٹ جواب)
                ai_reply = f"Agha AI Studio received: {text}"
                
                send_whatsapp_message(from_number, ai_reply)
        except Exception as e:
            print(f"Error parsing webhook: {e}")
        return 'OK', 200

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
    response = requests.post(url, headers=headers, json=data)
    print(f"WhatsApp API Response: {response.text}")
