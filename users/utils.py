import requests
import uuid
from decouple import config

UPSTASH_URL = config("UPSTASH_REDIS_REST_URL")
UPSTASH_TOKEN = config("UPSTASH_REDIS_REST_TOKEN")
HEADERS = {"Authorization": f"Bearer {UPSTASH_TOKEN}"}

def generate_reset_token(email: str) -> str:
    token = str(uuid.uuid4())
    key = f"reset_token:{token}"
    data = {"command": "SET", "key": key, "value": email.lower().strip(), "ex": 600}
    response = requests.post(UPSTASH_URL, json=data, headers=HEADERS)
    response.raise_for_status()
    return token

def verify_reset_token(token: str) -> str | None:
    key = f"reset_token:{token}"
    data = {"command": "GET", "key": key}
    response = requests.post(UPSTASH_URL, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("result")
