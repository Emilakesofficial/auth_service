import redis
import uuid
from decouple import config

# Redis client
REDIS_URL = config("REDIS_URL")  # e.g. redis://:password@host:port/0
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def generate_reset_token(email):
    """Generate a unique token and store in Redis for 10min"""
    token = str(uuid.uuid4())
    redis_client.setex(f"reset_token:{token}", 600, email.lower().strip())
    return token

def verify_reset_token( token):
    """Get email linked to token if valid, else None"""
    stored_email = redis_client.get(f"reset_token:{token}")
    return stored_email