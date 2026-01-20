import hmac
import hashlib

SECRET_KEY = "test_secret"

def verify_signature(raw_body: bytes, signature: str) -> bool:
    """
    Simulates signature verification.
    expected_signature = hmac_sha256(secret="test_secret", body=raw_payload)
    """
    if not signature:
        return False
    
    # Calculate HMAC SHA256
    expected_signature = hmac.new(
        SECRET_KEY.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()
    
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(expected_signature, signature)