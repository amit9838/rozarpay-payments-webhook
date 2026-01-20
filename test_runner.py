import requests
import hmac
import hashlib
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
SECRET = "test_secret"

payloads = [
    {
        "event": "payment.authorized",
        "payload": {
            "payment": { "entity": { "id": "pay_014", "status": "authorized", "amount": 5000, "currency": "INR" } }
        },
        "created_at": 1751889865,
        "id": "evt_auth_014"
    },
    {
        "event": "payment.captured",
        "payload": {
            "payment": { "entity": { "id": "pay_014", "status": "captured", "amount": 5000, "currency": "INR" } }
        },
        "created_at": 1751889900,
        "id": "evt_cap_014"
    }
]

def generate_signature(secret, body):
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

def send_webhook(data):
    body_str = json.dumps(data)
    signature = generate_signature(SECRET, body_str)
    
    headers = {
        "Content-Type": "application/json",
        "X-Razorpay-Signature": signature
    }
    
    print(f"Sending Event: {data['event']} | ID: {data['id']}")
    response = requests.post(f"{BASE_URL}/webhook/payments", data=body_str, headers=headers)
    print(f"Status: {response.status_code} | Response: {response.json()}")
    print("-" * 30)

def test_get_history(payment_id):
    print(f"Fetching History for: {payment_id}")
    response = requests.get(f"{BASE_URL}/payments/{payment_id}/events")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    # 1. Send Webhooks
    for p in payloads:
        send_webhook(p)
        time.sleep(1) 
    
    # 2. Test Idempotency (Send the first one again)
    print("Testing Idempotency (Sending Duplicate)...")
    send_webhook(payloads[0])

    # 3. Fetch History
    test_get_history("pay_014")