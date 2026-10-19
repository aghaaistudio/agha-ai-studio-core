import requests
from app import app
from extensions import db
from models.usage import UsageRecord

print("=========================================")
api_key = input("👉 Please paste your API Key here: ").strip()
print("=========================================")

url = "http://127.0.0.1:5000/api/v1/generate"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
data = {"prompt": "DB Test"}

print("\n1. Making API call...")
response = requests.post(url, json=data, headers=headers)
print("Response:", response.json())

print("\n2. Checking Database...")
with app.app_context():
    print("Total Usage Records:", UsageRecord.query.count())
