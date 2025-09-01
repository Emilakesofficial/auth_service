from upstash_redis import Redis
import uuid
from decouple import config

# Lazy initialization of Redis
def get_redis_client():
    return Redis(
        url=config("UPSTASH_URL"),
        token=config("UPSTASH_TOKEN")
    )

def generate_reset_token(email):
    """Generate a unique token and store in Redis for 10min"""
    token = str(uuid.uuid4())
    redis_client = get_redis_client()
    redis_client.set(f"reset_token:{token}", email.lower().strip(), ex=600)  # 600 seconds
    return token

def verify_reset_token(token):
    """Get email linked to token if valid, else None"""
    redis_client = get_redis_client()
    stored_email = redis_client.get(f"reset_token:{token}")
    return stored_email
