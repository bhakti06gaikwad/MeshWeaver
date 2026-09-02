import hashlib
import hmac
import json


SECRET_KEY = b"meshweaver-secret-key"


def sign_message(message):
    """Create a cryptographic signature for a message."""

    data = json.dumps(
        message,
        sort_keys=True
    ).encode("utf-8")

    signature = hmac.new(
        SECRET_KEY,
        data,
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_message(message, signature):
    """Verify that a message has a valid signature."""

    expected_signature = sign_message(message)

    return hmac.compare_digest(
        expected_signature,
        signature
    )