import requests
from app import app
from extensions import db
from models.user import User

print("=========================================")
api_key = input("agha_sk_km3OdGgiGTiPsCrDuj9t-9oDzsiGFnhsRdE1BmaPUWA").strip()
print("=========================================")

url = "http://127.0.0.1:5000/api/v1/generate"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
data = {"prompt": "Credit test"}

with app.app_context():
    user = User.query.first()
    if not user:
        print("❌ No user found in database!")
        exit()
    print(f"💰 Current Credits BEFORE API call: {user.credits}")

print("\n1. Making API call...")
response = requests.post(url, json=data, headers=headers)
res_json = response.json()
print("Response Status:", response.status_code)
print("Response Text:", res_json.get("text", res_json.get("error")))

with app.app_context():
    user = User.query.first()
    print(f"\n💰 Current Credits AFTER API call: {user.credits}")
    
    # Force credits to 0 to test the block
    user.credits = 0
    db.session.commit()
    print("⚠️ Forced credits to 0 for testing block.")

print("\n2. Making API call with 0 credits...")
response2 = requests.post(url, json=data, headers=headers)
print("Response Status:", response2.status_code)
print("Response Text:", response2.json())
