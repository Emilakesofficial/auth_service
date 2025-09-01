import uuid
from django.conf import settings

redis_client = settings.redis_client

def generate_reset_token(email: str) -> str:
    token = str(uuid.uuid4())
    key = f"reset_token:{token}"
    redis_client.setex(key, 600, email.lower().strip())  # expire in 10 minutes
    return token

def verify_reset_token(token: str) -> str | None:
    key = f"reset_token:{token}"
    email = redis_client.get(key)
    return email

def delete_reset_token(token: str) -> None:
    """Delete token from Redis once it's used."""
    key = f"reset_token:{token}"
    redis_client.delete(key)
