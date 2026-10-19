import requests
from app import app
from extensions import db
from models.user import User

print("=========================================")
api_key = input("👉 Paste your ACTIVE (Green) API Key here: ").strip()
print("=========================================")

url = "http://127.0.0.1:5000/api/v1/generate"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
data = {"prompt": "Hello Agha AI!"}

with app.app_context():
    user = User.query.first()
    print(f"💰 Credits BEFORE: {user.credits}")

print("\n⏳ Making API Call...")
response = requests.post(url, json=data, headers=headers)
res_json = response.json()

if response.status_code == 200:
    print("✅ API Call Successful! AI Reply:", res_json.get("text"))
else:
    print("❌ API Call Failed! Reason:", res_json.get("error"))

with app.app_context():
    user = User.query.first()
    print(f"💰 Credits AFTER: {user.credits}")
