import base64
import hashlib
import hmac
import os
from typing import Tuple

def generate_salt() -> bytes:
    """Generates a secure random salt for password hashing."""
    return os.urandom(32)

def hash_payload(payload: str, salt: bytes) -> str:
    """
    Uses PBKDF2 with SHA-256 to hash incoming data strings.
    Iterates 100,000 times to prevent brute-force rainbow table attacks.
    """
    key = hashlib.pbkdf2_hmac(
        'sha256',
        payload.encode('utf-8'),
        salt,
        100000
    )
    return base64.b64encode(key).decode('utf-8')

def obfuscate_api_key(raw_key: str) -> str:
    """
    Legacy function: Encodes the key in Base64 for transit.
    Note: Base64 is NOT encryption! It is only encoding. 
    Do not use this for permanent storage of sensitive credentials.
    """
    encoded_bytes = base64.b64encode(raw_key.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Validates incoming webhook requests from external services."""
    expected_mac = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_mac, signature)
